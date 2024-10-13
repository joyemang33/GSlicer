import datetime
import random
import config
import networkx.algorithms
import graphs.networkx.oracles as oracles
from graphs.basic_graph.gen import BasicGenerator
from graphs.networkx.loader import networkx_load_graph
from graphs.basic_graph.generators import *
from graphs.basic_graph.partitioners import *



max_nodes=200
max_edges=1000


def execute():
    """
    A single iteration of the testing process.
    """
    # Randomly generate the parameters for the graph generator
    generator = BasicGenerator()
    num_nodes = random.randint(1, max_nodes)
    num_edges = random.randint(0, max_edges)
    allow_loops = bool(random.getrandbits(1))
    allow_parallel_edge = bool(random.getrandbits(1))
    is_directed = bool(random.getrandbits(1))

    # Retrieve valid algorithms according to the parameters
    algorithm_list = config.Config("graphs/networkx/config.json")
    directed = "TRUE" if is_directed else "FALSE"
    paralleledge = "TRUE" if allow_parallel_edge else "FALSE"
    algorithm_nodedict = algorithm_list.get_algorithms(oracle="node_dict", directed=directed, paralleledge=paralleledge)

    # Execute the algorithms and compare the results with the oracles
    for i in range(0, 100):
        try:
            basic_G, partition_arr = generator.gen(num_nodes, num_edges, allow_loops, allow_parallel_edge, is_directed,
                        generator=gen_normal_disconnected.generate, partitioner=par_disconnected_uniform.partition)
        except Exception as e:
            print("Failed to generator with exception: ", e)
            continue

        G, G0, G1, _, _, _, _, _, _ = networkx_load_graph(networkx, basic_G, partition_arr, is_directed=is_directed, allow_parallel_edge=allow_parallel_edge)
        for algorithm in algorithm_nodedict:
            # if algorithm["Function"] != "laplacian_centrality": continue
            algorithm_fun = getattr(networkx.algorithms, algorithm['Function'])
            try:
                d_G0 = algorithm_fun(G0)
                d_G1 = algorithm_fun(G1)
                d_G = algorithm_fun(G)
            except Exception as e:
                print("Failed to execue algoritm " + algorithm['Function'], e)
                continue
            
            try:
                passed, error_msg = oracles.node_dict(d_G, d_G0, d_G1)
            except Exception as e:
                print("Failed to execute validator in " + algorithm['Function'], e)
                continue

            if not passed:
                print("--------------------------------------------------------------------------------------------------------------------------")
                print("Error: " + error_msg)
                print("bug found in " + algorithm['Function'])
                # print("G0 edges: ", G0.edges.data())
                # print("G1 edges: ", G1.edges.data())
                # print("G edges: ", G.edges.data())
                # print("G0 nodes: ", G0.nodes.data())
                # print("G1 nodes: ", G1.nodes.data())
                # print("G nodes: ", G.nodes.data())
                print("--------------------------------------------------------------------------------------------------------------------------")
            


if __name__ =="__main__":
    """
    The main loop for the testing process.
    """
    i = 0
    while True:
        execute()
        i += 1
        if i % 100 == 0:
            print(datetime.datetime.now() + " " + str(i) + " iterations")