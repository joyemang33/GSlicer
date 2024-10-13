import json
import random
import networkx.algorithms
from graphs.networkx.oracles import *
from graphs.basic_graph.gen import BasicGenerator
from graphs.networkx.loader import networkx_load_graph
from graphs.basic_graph.generators import *
from graphs.basic_graph.partitioners import *


import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

class Tester():
    def __init__(self):
        self.rules = {
            "node_dict_smaller" : node_dict_smaller, 
            "node_dict_equal" : node_dict_equal, 
            "node_dict_greater" : node_dict_greater, 
            "value_smaller" : value_smaller, 
            "value_equal" : value_equal, 
            "value_greater" : value_greater,
        }

    def gen_testcase(self, num_nodes, num_edges, allow_loops, allow_parallel_edge, is_directed, connected = True):
        generator = BasicGenerator()
        if connected:
            basic_G, partition_arr =  generator.gen(num_nodes, num_edges, allow_loops, allow_parallel_edge, is_directed,
            generator=gen_uniform.generate, partitioner=par_connected_uniform.partition)
        else: 
            basic_G, partition_arr = generator.gen(num_nodes, num_edges, allow_loops, allow_parallel_edge, is_directed,
            generator=gen_normal_disconnected.generate, partitioner=par_disconnected_uniform.partition)

        G, G0, G1, _, _, _, _, _, _ = networkx_load_graph(networkx, 
            basic_G, partition_arr, is_directed=is_directed, allow_parallel_edge=allow_parallel_edge)
        
        return G, G0, G1    

    def run_testcase(self, algorithm, G, G0, G1, validate_rule):
        algorithm_fun = getattr(networkx.algorithms, algorithm)
        try:
            with time_limit(10): res = algorithm_fun(G)
            with time_limit(10): res0 = algorithm_fun(G0)
            with time_limit(10): res1 = algorithm_fun(G1)
        except Exception as e:
            if not any([isinstance(e, E) for E in [
                networkx.NetworkXError, networkx.NetworkXUnfeasible, networkx.NetworkXAlgorithmError,
                networkx.NetworkXPointlessConcept, networkx.NetworkXException, TimeoutException
            ]]): return False, str(e)
            return True, ""
        
        passed, error_msg  = validate_rule(res, res0, res1)
        return passed, error_msg
    
    def execute(self, max_nodes=200, max_edges=1000, max_iter = 20):

        with open("./graphs/networkx/dp.json", "r", encoding="utf-8") as f:
            algorithm_list = json.load(f)

        print("OK")
        for allow_loops in [True, False]:
            for allow_parallel_edge in [True, False]:
                for is_directed in [True, False]:
                    for connected in [True, False]:
                        Graphs = []
                        while len(Graphs) < max_iter:
                            try:
                                num_nodes = random.randint(2, max_nodes)
                                m = max_edges
                                if not allow_parallel_edge:
                                    m = num_nodes * (num_nodes - 1) // 2
                                    if allow_loops: m += num_nodes

                                num_edges = random.randint(0, m)
                                G, G0, G1 = self.gen_testcase(
                                    num_nodes, num_edges, allow_loops, 
                                    allow_parallel_edge, is_directed, connected
                                )
                            except Exception as e:
                                continue
                            Graphs.append((G, G0, G1))
                        
                        for target in algorithm_list:
                            if target["allow_loops"] != allow_loops: continue
                            if target["allow_parallel_edge"] != allow_parallel_edge: continue
                            if target["is_directed"] != is_directed: continue
                            if target["connected"] != connected: continue
                            print("Running: " + target["algorithm"])
                            for G, G0, G1 in Graphs:
                                try:
                                    passed, error_message = self.run_testcase(
                                        target["algorithm"], G, G0, G1, target["rules"])
                                except:
                                    continue
                                if not passed:
                                    print(error_message)
                                    print("!") 

if __name__ == "__main__":
    T = Tester()
    T.execute()
