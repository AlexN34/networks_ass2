#!/usr/bin/python3
import sys
from pathing_algorithms import shortest_path
from graph_rep import Graph
# NOTE: empty classes atm
from routing_timer import RoutingTimer
from virtual_connection import VirtualConnection
from statistics_manager import StatisticsManager
from workload_queue import WorkloadQueue, WorkloadTuple


class RoutingPerformance:
    """
    Routing Performance Program
    """

    # NOTE: moved init_topology/ show_graph to graph_rep
    def __init__(self, g, NETWORK_SCHEME, ROUTING_SCHEME, TOPOLOGY_FILE,
                 WORKLOAD_FILE, PACKET_RATE):
        self.graph = g
        # init graph topology: routers, delay, capacity
        self.graph.parse_topology(TOPOLOGY_FILE)
        self.workload = WorkloadQueue(WORKLOAD_FILE)
        self.network_scheme = NETWORK_SCHEME
        self.routing_scheme = ROUTING_SCHEME
        self.packet_rate = PACKET_RATE
        self.statistics_manager = StatisticsManager(self.network_scheme,
                                                    self.packet_rate)
        self.debug = False

    # init VC requests

    def start_requests(self):
        while not self.workload.is_empty():
            cur_time, cur_connection = self.workload.pop()

            if not cur_connection.is_processed:
                # increment total_requests
                self.statistics_manager.update_stats("request", 1)
                # increment total_pkts
                num_pkts = int(cur_connection.duration) * int(PACKET_RATE)
                self.statistics_manager.update_stats("packets", num_pkts)

                status = cur_connection.fill_path(self.graph, shortest_path,
                                                  self.routing_scheme)
                if status:  # found a suitable path!
                    # increment successful pkt
                    self.statistics_manager.update_stats(
                        "pkt_success", num_pkts)
                    # increment circuit_success
                    self.statistics_manager.update_stats("circuit_success", 1)
                    # increment total_hops
                    self.statistics_manager.update_stats(
                        "hops", len(cur_connection.path))
                    # increment total_delay
                    self.statistics_manager.update_stats(
                        "delays", cur_connection.path_delay)
                    # connection worked! add another connection at the end of duration to queue
                    end_time = cur_connection.start + cur_connection.duration
                    end_tuple = WorkloadTuple(
                        time=end_time, connection=cur_connection)
                    self.workload.add(end_tuple)
                else:  # connection was blocked
                    # increment blocked pkt
                    self.statistics_manager.update_stats(
                        "pkt_blocked", num_pkts)
                    if self.debug:
                        print('work loop: connection blocked!')
                cur_connection.is_processed = True
            else:
                # we've seen this before - must be time to pop it back off
                self.graph.remove_connection(cur_connection)

        # TODO report durations here?
        # main loop of program
        # pop off item from queue
        # if flag not set, attempt make connection
        # calculate path
        # attempt to put connection on graph
        # if ok, add connection onto queue at duration (to remove)
        # if not, request is blocked. discard and handle next one
        # if flag set, we just need to remove this connection to free capacity
        # repeat until empty graph

    def close_program(self):
        # print final statistics to terminal here
        self.statistics_manager.print_statistics()


"""
Main Function
"""
# NOTE: test packet rate = 1
if __name__ == '__main__':
    num_args = 6
    if len(sys.argv) != num_args:
        print(
            "Usage: ./networks.py NETWORK_SCHEME ROUTING_SCHEME TOPOLOGY_FILE WORKLOAD_FILE PACKET_RATE"
        )
    else:
        # empty graph
        graph = Graph()

        # grab argument objects
        NETWORK_SCHEME, ROUTING_SCHEME, TOPOLOGY_FILE, WORKLOAD_FILE, PACKET_RATE = sys.argv[
            1:]
        r = RoutingPerformance(graph, NETWORK_SCHEME, ROUTING_SCHEME,
                               TOPOLOGY_FILE, WORKLOAD_FILE, PACKET_RATE)

        # init nodes, links, delay and capacity values is done on creation
        # it should also parseworkload and create queue above

        # start virtual connection requests
        r.start_requests()
        r.close_program()
