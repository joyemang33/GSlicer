import json
import random
import networkx.algorithms
from graphs.networkx.oracles import *
from graphs.basic_graph.gen import BasicGenerator
from graphs.networkx.loader import networkx_load_graph
from graphs.basic_graph.generators import *
from graphs.basic_graph.partitioners import *

class Explorer:
    def __init__(self, i):
        self.rules = [sum_equal, sum_smaller, sum_greater, node_dict_smaller, node_dict_equal, node_dict_greater, value_smaller, value_equal, value_greater][i-1:i]
    
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
            res = algorithm_fun(G)
            res0 = algorithm_fun(G0)
            res1 = algorithm_fun(G1)
        except Exception as e:
            if not isinstance(e, networkx.NetworkXError) and not isinstance(e, networkx.NetworkXUnfeasible) \
            and not isinstance(e, networkx.NetworkXAlgorithmError) and not isinstance(e, networkx.NetworkXPointlessConcept) \
            and not isinstance(e, networkx.NetworkXException):
                if "attribute" in str(e): raise e
                if "argument" in str(e): raise e
                if "not implemented" in str(e): raise e
                if "trophic" in algorithm: raise e
                if "No cycle found" in str(e): raise e
                if algorithm in [
                    "degree_pearson_correlation_coefficient",
                    "mixing_dict",
                    "eigenvector_centrality_numpy",
                    "percolation_centrality",
                    "global_reaching_centrality",
                    "flow_hierarchy",
                    "hits",
                    "directed_edge_swap",
                    "random_triad",
                    "from_nested_tuple",
                    "from_prufer_sequence",
                    "random_spanning_tree",
                    "join",
                    "current_flow_betweenness_centrality",
                    "approximate_current_flow_betweenness_centrality",
                    "edge_current_flow_betweenness_centrality",
                    "current_flow_closeness_centrality",
                    "information_centrality",
                    "laplacian_centrality",
                    "max_weight_clique",
                    "effective_size",
                    "k_components",
                    "is_distance_regular",
                    "intersection_array",
                    "is_strongly_regular",
                    "non_randomness",
                    "rich_club_coefficient",
                    "to_prufer_sequence"
                ]: raise e
                # print("Crash!")
            raise e
        passed, error_msg  = validate_rule(res, res0, res1)
        return passed

    def run_explore(self, max_node = 5, max_edges = 20, max_iter = 20, 
        input_file = "./graphs/networkx/algorithm_names.json"):
        
        with open(input_file, "r", encoding="utf-8") as f:
            algorithm_list = json.load(f)
        
        # print(len(algorithm_list) - len([
        #             "degree_pearson_correlation_coefficient",
        #             "mixing_dict",
        #             "eigenvector_centrality_numpy",
        #             "percolation_centrality",
        #             "global_reaching_centrality",
        #             "flow_hierarchy",
        #             "hits",
        #             "directed_edge_swap",
        #             "random_triad",
        #             "from_nested_tuple",
        #             "from_prufer_sequence",
        #             "random_spanning_tree",
        #             "join",
        #             "current_flow_betweenness_centrality",
        #             "approximate_current_flow_betweenness_centrality",
        #             "edge_current_flow_betweenness_centrality",
        #             "current_flow_closeness_centrality",
        #             "information_centrality",
        #             "laplacian_centrality",
        #             "max_weight_clique",
        #             "effective_size",
        #             "k_components",
        #             "is_distance_regular",
        #             "intersection_array",
        #             "is_strongly_regular",
        #             "non_randomness",
        #             "rich_club_coefficient",
        #             "to_prufer_sequence"
        #         ]) - len(["sigma", "omega", "combinatorial_embedding_to_pos", "chromatic_polynomial", "tutte_polynomial", "random_reference", "lattice_reference"]))
        # exit(0)

        result = []
        for allow_loops in [True, False]:
            for allow_parallel_edge in [True, False]:
                for is_directed in [True, False]:
                    for connected in [True, False]:
                        Graphs = []
                        while len(Graphs) < max_iter:
                            try:
                                num_nodes = random.randint(2, max_node)
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
                            

                        for algorithm_name in algorithm_list:
                            print("Now Running : ", algorithm_name)
                            for validate_rule in self.rules:
                                if algorithm_name in ["sigma", "omega", "combinatorial_embedding_to_pos", "chromatic_polynomial", "tutte_polynomial", "random_reference", "lattice_reference"]:
                                    continue
                                count_ok, count_correct = 0, 0
                                for G, G0, G1 in Graphs:
                                    # print(G.edges)
                                    # print(G0.edges)
                                    # print(G1.edges)
                                    try:
                                        passed = self.run_testcase(
                                            algorithm_name, G, G0, G1, validate_rule)
                                    except:
                                        continue
                                    count_ok += 1
                                    if passed: count_correct += 1
                                if count_ok > 3 and count_correct == count_ok:
                                    D = {
                                        "algorithm" : algorithm_name,
                                        "allow_loops" : allow_loops,
                                        "allow_parallel_edge" : allow_parallel_edge,
                                        "is_directed" : is_directed,
                                        "connected" : connected,
                                        "rules" : validate_rule.__name__
                                        
                                    }
                                    result.append(D)
        return result
    
    def analyze(self):
        with open("./graphs/networkx/output.json", "r", encoding="utf-8") as f:
            L = json.load(f)
        s = set()
        for d in L: s.add(d["algorithm"])
        # print(len(s))
        # print(len(L))
        return len(s)

if __name__ == "__main__":
    ans = dict()
    result = []
    for i in range(1, 10):
        sum = 0
        for j in range(0, 5):
            my_explorer = Explorer(i)
            result += my_explorer.run_explore()
            with open("./graphs/networkx/output.json", "w", encoding="utf-8") as file:
                json.dump(result, file)
            sum += my_explorer.analyze()
        ans[i] = sum / 5
        with open("./task_coverage.json", "w", encoding="utf-8") as file:
                json.dump(ans, file)
        print(ans)
    
    print(ans)
    

