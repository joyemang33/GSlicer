import random
import numpy as np
from graphs.basic_graph.schema import *
from graphs.basic_graph.gen import BasicGenerator
        
def networkx_load_graph(session, G : BasicGraph, partition_arr,
    is_directed = False,
    allow_parallel_edge = False,
    num_of_properties = 5):
    """Adapter for networkx. 
    Loading an abstract graph into networkx.
    """

    # Define property names
    properties = [["p" + str(i), gen_type()] for i in range(0, num_of_properties)]
    edge_properties = [["q" + str(i), gen_type()] for i in range(0, num_of_properties)]


    G_nodes = dict()
    G_nodes["nodeId"] = list(range(0, G.n))

    # Define graph types according to the requirements of algorithms
    if is_directed:
        if allow_parallel_edge:
            network_G = session.MultiDiGraph()
        else:
            network_G = session.DiGraph()
    else:
        if allow_parallel_edge:
            network_G = session.MultiGraph()
        else:
            network_G = session.Graph()
    network_G.add_nodes_from(G_nodes["nodeId"])

    # Randomly generate property values for nodes and fill them into the graph
    for prop in properties:
        G_nodes[prop[0]] = [np.nan for _ in range(0, G.n)]
        for node in range(0, G.n):
            G_nodes[prop[0]][node] = np.nan if random.randint(1, 4) == 4 else gen_constant(prop[1])
            network_G.nodes[node][prop[0]] = G_nodes[prop[0]][node]

    # Add edges
    # keys are used to identify multiple edges for Multi(Di)Grape. The keys are incremented from 0 for repeated edges.
    keys = network_G.add_edges_from([(i.node_x, i.node_y) for i in G.edges])

    # Create the global structure for maintaining edge properties
    G_edges = dict()
    G_edges["sourceNodeId"] = [G.edges[i].node_x for i in range(0, G.m)]
    G_edges["targetNodeId"] = [G.edges[i].node_y for i in range(0, G.m)]
    if keys is not None:
        G_edges["keys"] = keys

    # Randomly generate property values for edges and fill them into the graph
    for prop in edge_properties:
        G_edges[prop[0]] = [np.nan for _ in range(0, G.m)]
        for edge_i in range(0, G.m):
            G_edges[prop[0]][edge_i] = np.nan if random.randint(1, 4) == 4 else gen_constant(prop[1])
            if "keys" not in G_edges:
                network_G.edges[G_edges["sourceNodeId"][edge_i], G_edges["targetNodeId"][edge_i]][prop[0]] = G_edges[prop[0]][edge_i]
            else:
                network_G.edges[G_edges["sourceNodeId"][edge_i], G_edges["targetNodeId"][edge_i], G_edges["keys"][edge_i]][prop[0]] = G_edges[prop[0]][edge_i]

    # Create subgraphs
    subG_nodes = [dict(), dict()]
    subG_edges = [dict(), dict()]

    network_subG = []
    if is_directed:
        if allow_parallel_edge:
            network_subG.append(session.MultiDiGraph())
            network_subG.append(session.MultiDiGraph())
        else:
            network_subG.append(session.DiGraph())
            network_subG.append(session.DiGraph())
    else:
        if allow_parallel_edge:
            network_subG.append(session.MultiGraph())
            network_subG.append(session.MultiGraph())
        else:
            network_subG.append(session.Graph())
            network_subG.append(session.Graph())
            
    for id in range(0, 2):
        # Create nodes for subgraphs
        subG_nodes[id]["nodeId"] = []
        for prop in properties:
            subG_nodes[id][prop[0]] = []
        for i in range(0, G.n):
            if partition_arr[i] == id:
                subG_nodes[id]["nodeId"].append(i)
                network_subG[id].add_node(i)
                for prop in properties:
                    subG_nodes[id][prop[0]].append(G_nodes[prop[0]][i])
                    network_subG[id].nodes[i][prop[0]] = G_nodes[prop[0]][i]

        # Create edges for subgraphs
        subG_edges[id]["sourceNodeId"] = []
        subG_edges[id]["targetNodeId"] = []
        if "keys" in G_edges:
            subG_edges[id]["keys"] = []
        for prop in edge_properties:
            subG_edges[id][prop[0]] = []
        for i in range(0, G.m):
            if partition_arr[G.edges[i].node_x] == id and partition_arr[G.edges[i].node_y] == id:
                subG_edges[id]["sourceNodeId"].append(G.edges[i].node_x)
                subG_edges[id]["targetNodeId"].append(G.edges[i].node_y)
                key = network_subG[id].add_edge(G.edges[i].node_x, G.edges[i].node_y) # keys are regenerated in subgraphs
                if key is not None:
                    subG_edges[id]["keys"].append(key)
                for prop in edge_properties:
                    subG_edges[id][prop[0]].append(G_edges[prop[0]][i])
                    if "keys" not in G_edges:
                        network_subG[id].edges[G_edges["sourceNodeId"][i], G_edges["targetNodeId"][i]][prop[0]] = G_edges[prop[0]][i]
                    else:
                        network_subG[id].edges[G_edges["sourceNodeId"][i], G_edges["targetNodeId"][i], G_edges["keys"][i]][prop[0]] = G_edges[prop[0]][i]

    return network_G, network_subG[0], network_subG[1], G_nodes, G_edges, \
        subG_nodes[0], subG_edges[0], subG_nodes[1], subG_edges[1]

def gen_type():
        return random.choice(["int", "float"])

def gen_constant(type : str):
    assert type in ["int", "float"]
    if type == "int":
        return random.randint(-(2 ** 63), (2 ** 63) - 1)
    if type == "float":
        return random.random() * random.randint(-(2 ** 63), (2 ** 63) - 1)


if __name__ == "__main__":
    basic_generator = BasicGenerator()
    basic_G, partition_arr = basic_generator.gen(6, 10)
    G, G0, G1, _, _, _, _, _, _ = networkx_load_graph(basic_G, partition_arr)
    print("Original graph:")
    print(G.nodes.data())
    print(G.edges.data())
    print("Subgraph 0:")
    print(G0.nodes.data())
    print(G0.edges.data())
    print("Subgraph 1:")
    print(G1.nodes.data())
    print(G1.edges.data())
    print(G0.number_of_nodes() + G1.number_of_nodes() == G.number_of_nodes())

