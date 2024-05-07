# plot_restarts.py: code to support the "xt plot restarts" command
import time
import arrow
import datetime
import numpy as np
from collections import defaultdict

from xtlib import time_utils, utils, xt_cmds
from xtlib import job_helper, run_helper, node_helper
from xtlib import plot_helper

class PlotRestarts:
    def __init__(self, store, node_list, workspace, plot_end_runs, plot_checkpoints, plot_catchup):
        self.store = store
        self.ws_name = workspace

        # for now, just support a single job or node name
        job_id = node_list[0]

        if not job_helper.is_job_id(job_id):
            node_index = node_helper.get_node_index(job_id)
            job_id = node_helper.get_job_id(job_id)
        else:
            node_index = -1

        self.job_id = job_id
        self.node_index = node_index
        self.secs_first_time = None
        self.time_states = []
        self.events = []

        self.plot_end_runs = plot_end_runs
        self.plot_checkpoints = plot_checkpoints
        self.plot_catchup = plot_catchup

    def add_ts(self, at, state):
        secs = at.datetime.timestamp()
        rel_secs = (secs - self.secs_first_time) / 3600

        if self.time_states:
            assert rel_secs >= self.time_states[-1][0]

        # also add at, for debugging
        self.time_states.append( (rel_secs, state, at) )

    def add_event(self, name, at):
        secs = at.datetime.timestamp()
        rel_secs = (secs - self.secs_first_time) / 3600

        if self.time_states:
            assert rel_secs >= self.time_states[-1][0]

        # also add at, for debugging
        self.events.append( (name, rel_secs, at) )

    def get_node_queued_running_data(self, last_times_dict, node_index, catch_up = False):
        times = []
        states = []

        CATCH_UP = 2
        RUNNING = 1
        QUEUED = 0

        # 1. read CREATE_TIME from NODE_STATS
        fields_dict = {"create_time": 1, "post_end_time": 1}
        filter_dict = {"ws_name": self.ws_name, "job_id": self.job_id, "node_index": node_index}
        node_records = self.store.database.get_info_for_nodes(self.ws_name, filter_dict, fields_dict)
        text_create_time = node_records[0]["create_time"]
        at_created = time_utils.get_arrow_from_arrow_str(text_create_time)

        # completed_time = node_records[0]["post_end_time"]
        #dt_completed = time_utils.get_time_from_arrow_str(completed_time) if completed_time else None

        # read NODE.LOG for exact start and restart times
        fn = "nodes/node{}/node.log".format(node_index)

        if not self.store.does_job_file_exist(self.ws_name, self.job_id, fn):
            return None, None, None

        text = self.store.read_job_file(self.ws_name, self.job_id, fn)
        node_log_records = utils.load_json_records(text)
        restart_count = 0
        current_run_name = None
        active_programs = {}    # key=run_name, value=last step number logged

        # build time_states list
        self.time_states = []
        self.events = []
        end_run_count = 0

        # add first queued record
        self.secs_first_time = at_created.datetime.timestamp()
        self.add_ts(at_created, QUEUED)

        def is_program_active(name):
            base_name = name.split(".r")[0]
            return base_name in active_programs
        
        def add_to_active(name):
            base_name = name.split(".r")[0]
            active_programs[base_name] = 0

        def remove_from_active(name):
            base_name = name.split(".r")[0]
            del active_programs[base_name]

        at_last_activity = None
        found_node_end = False

        for r, record in enumerate(node_log_records):
            event = record["event"]
            data = record["data"]
            at = time_utils.get_arrow_from_arrow_str(record["time"])

            # # debug
            # if r == 0:
            #     print("------------------------------------------------")
            # print("event: ", event, "  data: ", data, "  time: ", record["time"])

            if event == "started":
                self.add_ts(at, RUNNING)
                at_last_activity = at
                
            elif event == "start_run" and not "_" in data["run"]:
                current_run_name = data["run"]
                at_last_activity = at

                if catch_up and is_program_active(current_run_name):
                    self.add_ts(at, CATCH_UP)
                else:
                    # new program being run
                    add_to_active(current_run_name)
                    #self.add_ts(at, RUNNING)
                
            elif event == "end_run"and not "_" in data["run"]:
                # program completed
                if data["run"] != current_run_name:
                    print("WARNING: plot nodes command doesn't currently support simultaneous runs on same node (end_run doesn't match most recent start_run): {}, {}".format(data["run"], current_run_name))
                    #raise Exception("plot nodes command doesn't currently support simultaneous runs on same node: {}, {}".format(data["run"], current_run_name))
                
                if current_run_name:
                    remove_from_active(current_run_name)
                    current_run_name = None

                at_last_activity = at

                if self.plot_end_runs:
                    self.add_event("end_run", at)
                end_run_count += 1

            elif event == "checkpoint_upload":
                if self.plot_checkpoints:
                    self.add_event("checkpoint", at)

            elif event == "get_index":
                at_last_activity = at
                
            elif event == "node_restart":
                at_last_activity = at
                
            elif event == "node_end":
                # the node has completed
                current_run_name = data["run"]
                self.add_ts(at, QUEUED)
                found_node_end = True
                break

            elif event == "restarted":
                queued_time = None

                if current_run_name and current_run_name in last_times_dict:

                    # limit last_time, in case it was updated after run ended (how??)
                    last_time = last_times_dict[current_run_name]

                    if last_time < at:
                        queued_time = last_time

                if not queued_time:
                    # preemption happened somewhere between last activity and the restart; use their average
                    queued_time = self.avg_arrow_times(at_last_activity, at)

                self.add_ts(queued_time, QUEUED)

                if catch_up:
                    self.add_ts(at, CATCH_UP)
                else:
                    self.add_ts(at, RUNNING)

                current_run_name = None
                restart_count += 1

        if not found_node_end:
            # add an ending transition based on now()
            pair = self.time_states[-1]
            self.add_ts(arrow.now(), (1-pair[1]))

        # convert time_states to times and states
        times = [pair[0] for pair in self.time_states]
        states = [pair[1] for pair in self.time_states]
        events = [ev for ev in self.events]

        return times, states, events, restart_count, end_run_count

    def avg_arrow_times(self, at1, at2):
        secs1 = at1.datetime.timestamp()
        secs2 = at2.datetime.timestamp()
        avg_secs = (secs1 + secs2) / 2
        return arrow.get(avg_secs)

    def build_last_times(self):

        # using run_stats is faster, but the LAST_TIME field is sometimes updated after the run ends
        use_run_stats = False

        if use_run_stats:
            '''
            read LAST_TIME from all run records for this job or node.
            group the results by node_index
            '''
            fields_dict = {"run_name": 1, "node_index": 1, "last_time": 1}
            filter_dict = {"ws_name": self.ws_name, "job_id": self.job_id}

            if self.node_index > -1:
                filter_dict["node_index"] = self.node_index

            run_records = self.store.database.get_info_for_runs(self.ws_name, filter_dict, fields_dict)

            last_times_by_node = defaultdict(dict)

            for rr in run_records:
                last_time = rr["last_time"]
                node_index = rr["node_index"]
                run_name = rr["run_name"]

                ltd = last_times_by_node[node_index]    # create dict on demand, when needed
                ltd[run_name] = time_utils.get_arrow_from_arrow_str(last_time)

        else:
            '''
            read all logged records for this job or node to determine the time of last activity.
            group the results by node_index
            '''
            started = time.time()
            fields_dict = {"run_name":1, "node_index": 1}
            filter_dict = {"ws_name": self.ws_name, "job_id": self.job_id}

            if self.node_index > -1:
                filter_dict["node_index"] = self.node_index
            
            run_records = run_helper.get_run_records(job_id=self.job_id, workspace_name=self.ws_name, fields_dict=fields_dict, 
                filter_dict=filter_dict, include_log_records=True)

            last_times_by_node = defaultdict(dict)

            for rr in run_records:
                run_name = rr["run_name"]
                node_index = rr["node_index"]

                log_records = rr["log_records"]
                last_time = log_records[-1]["time"]

                ltd = last_times_by_node[node_index]    # create dict on demand, when needed
                ltd[run_name] = time_utils.get_arrow_from_arrow_str(last_time)


        # sort last_times_by_node by node_index (ascending)
        last_times_by_node = dict(sorted(last_times_by_node.items(), key=lambda item: item[0]))

        return last_times_by_node

    def plot_core(self):
        # restart_report.py: sketch out code needed to show queued/running states of a run over time
        import matplotlib.pyplot as plt

        # build last_times of runs, grouped node_index        
        last_times = self.build_last_times()

        node_data = {}
        max_time = None

        for node_index, ltd in last_times.items():
            times, states, events, restart_count, end_run_count = self.get_node_queued_running_data(ltd, node_index)
            if times is not None:

                mt = times[-1]
                if max_time is None or mt > max_time:
                    max_time = mt    

                node_data[node_index] = (times, states, events, restart_count, end_run_count)

        plt_count = len(node_data)
        if plt_count == 0:
            print("no nodes found to plot: {}".format(self.job_id))
            return      

        fig_height = 1.3*plt_count
        figsize = (10, min(10, fig_height))
        fig, axes = plt.subplots(plt_count, 1, squeeze=False, figsize=figsize)  # plt_count rows, 1 column

        running_percents = []
        for node_index, (times, states, events, restart_count, end_run_count) in node_data.items():
            # set axis_index to the key index of node_index in last_times
            axis_index = list(node_data.keys()).index(node_index)
            axis = axes[axis_index][0]

            running_percent = self.create_node_subplot(axis, times, states, events, restart_count, node_index, plt_count, 
                end_run_count, max_time)

            running_percents.append(running_percent)

        # Show the plot
        total_restarts = sum([data[3] for data in node_data.values()])
        total_end_runs = sum([data[4] for data in node_data.values()])
        avg_running_percent = sum(running_percents) / len(running_percents)

        if self.plot_end_runs:
            fig.suptitle("Restart Report: {} (restarts: {:}, running: {:.0f}%, ends={})".format(self.job_id, total_restarts, 
                100*avg_running_percent, total_end_runs))
        else:
            fig.suptitle("Restart Report: {} (restarts: {:}, running: {:.0f}%)".format(self.job_id, total_restarts, 100*avg_running_percent))

        our_cmd = "xt " + xt_cmds.orig_xt_cmd
        fig.canvas.manager.set_window_title(our_cmd)
        plt.tight_layout()

        plot_helper.show_plot(True)

    def create_node_subplot(self, axis, times, states, events, restart_count, node_index, plt_count, end_run_count, max_time):

        linewidth = 1
        plot_alpha = .6
        alpha = .4
        colors = ["r-", "g-", "b-"]    # QUEUED, RUNNING, CATCH_UP

        def y_val(state):
            return 0 if state == 0 else 1
        
        # Draw each segment separately
        for i in range(1, len(times)):
            # Horizontal line from the previous time to the current time
            last_state = states[i-1]
            curr_state = states[i]

            color = colors[last_state]
            axis.plot([times[i-1], times[i]], [y_val(last_state), y_val(last_state)], color, linewidth=linewidth, alpha=plot_alpha)  # Default blue

            # Vertical line with opacity=.2
            if i < len(times)-1:    
                if y_val(curr_state) != y_val(last_state):
                    axis.plot([times[i], times[i]], [y_val(last_state), y_val(curr_state)], 'r-', linewidth=linewidth, alpha=plot_alpha)

        # plot markers for events 
        for name, rel_secs, _ in events:
            if name == "end_run" and self.plot_end_runs:
                axis.scatter(rel_secs, 1.0, marker='o', color="blue", s=10, alpha=.8, edgecolors='b', facecolors='none', linewidths=1)

            if name == "checkpoint" and self.plot_end_runs:
                import matplotlib
                axis.scatter(rel_secs, 1.0, marker=matplotlib.markers.TICKDOWN, color="red", s=10, alpha=1)

        axis.set_yticks([0, 1], ['Queued', 'Running'], alpha=alpha, fontsize=8)
        axis.set_xlabel("Hours", alpha=alpha, fontsize=8)
        axis.set_xlim(0, max_time)

        # Set fontsize and alpha for x-axis tick labels
        for label in axis.get_xticklabels():
            label.set_fontsize(8)        # set font size
            label.set_alpha(alpha)          # set transparency

        axis.margins(x=.01, y=.2)   # adds 5% padding to the x-axis and 5% padding to the y-axis

        # Calculate ticks for exactly 10 even divisions
        start_time = times[0]
        end_time = times[-1]

        # calculate the run_percentages (time in run state / total time)
        run_times = []
        for i in range(0, len(times)-1):
            if states[i] == 1:
                run_times.append(times[i+1] - times[i])

        total_run_time = sum(run_times)
        run_percent = total_run_time / (times[-1] - times[0])

        # # debug
        # rt_text = ["{:.1f}".format(rt) for rt in run_times]
        # print("\nrun_times: {}".format(", ".join(rt_text)))
        # print("node: {}, elapsed: {}, total_run_time: {}, run_percent: {:.0f}%".format(node_index, times[-1] - times[0], total_run_time, run_percent*100))

        # text lines to the right of the 
        if plt_count == 1:
            y_spacing = .5 
        elif plt_count == 2:
            y_spacing = .3
        elif plt_count > 10:
            y_spacing = .5
        else:
            y_spacing = .25

        text_x = 1.01*max_time

        axis.text(text_x, 1, "node {}".format(node_index), fontsize=8)
        axis.text(text_x, 1-y_spacing, "restarts: {}".format(restart_count), fontsize=8)
        axis.text(text_x, 1-2*y_spacing, "running: {:.0f}%".format(run_percent*100), fontsize=8)

        if self.plot_end_runs:
            axis.text(text_x, 1-3*y_spacing, "ends: {}".format(end_run_count), fontsize=8)

        # Make spines less prominent
        for position in ["left", "right", "top", "bottom"]:
            # axis.spines[position].set_visible(False)
            axis.spines[position].set_color('lightgray')
            axis.spines[position].set_linewidth(0.5)        

        return run_percent
