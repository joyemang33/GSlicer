import random
import numpy as np
from copy import copy
# import sys
# sys.path.append(".")
from graphs.kuzu.graph_generator import *

def partition(G : GraphData):
    '''
    Partition the nodes of graph G into two sub-graphs (G1, G2).
    Return the G1, G2, cuts (the cut edges between G1 and G2).
    Cuts : List<Edge>
    '''
    if G.no_nodes < 2:
        raise Exception("The number of nodes in the original graph must >= 2.")
    
    #Determine the number of nodes in each sub-graphs
    no_nodes_G1 = random.randint(1, G.no_nodes - 1)
    no_nodes_G2 = G.no_nodes - no_nodes_G1
    
    #Determine the id of nodes in each sub-graphs
    nodes_id_G1 = np.random.choice(range(0, G.no_nodes), no_nodes_G1)
    nodes_id_G2 = []
    for i in range(0, G.no_nodes):
        if i not in nodes_id_G1:
            nodes_id_G2.append(i)
    
    #Copy the basic information from the original graph    
    G1 = copy(G)
    G2 = copy(G)
    cuts = []
    
    #Modify the graph information
    for i, subG in enumerate([G1, G2]):
        #Modfiy the nodes information
        subG.no_nodes = no_nodes_G1 if i == 0 else no_nodes_G2
        nodes = nodes_id_G1 if i == 0 else nodes_id_G2
        new_nodes = []
        for node in subG.nodes:
            if node.id in nodes:
                new_nodes.append(node)
        subG.nodes = new_nodes
        
        #Modfiy the edges information
        new_edges = []
        for edge in subG.edges:
            s, t = edge.source, edge.target
            if (s in nodes) and (t in nodes):
                new_edges.append(edge)
            elif (s in nodes):
                #Update the cuts information
                cuts.append(edge)
        subG.no_edges = len(new_edges)
        subG.edges = new_edges
        
    return G1, G2, cuts

def partition_2CC(G : GraphData):
    G1, G2 = copy(G), copy(G)
    G1.init_from_table(_no_nodes = random.randint(G.no_node_labels, G.no_nodes), _no_edges = random.randint(1, G.no_edges))
    G2.init_from_table(_no_nodes = random.randint(G.no_node_labels, G.no_nodes), _no_edges = random.randint(1, G.no_edges), offset = G1.no_nodes)
    G.nodes = []
    G.edges = []
    for i, subG in enumerate([G1, G2]):
        for node in subG.nodes:
            G.nodes.append(node)
        for edge in subG.edges:
            G.edges.append(edge)
    G.no_nodes = G1.no_nodes + G2.no_edges
    G.no_edges = G2.no_edges + G2.no_edges
    return G, G1, G2
    
if __name__ == "__main__":
    #unit test
    G = GraphData(_no_properties = 10, _no_node_labels = 5, _no_edge_labels = 5, _no_nodes = 5, _no_edges = 10)
    # G1, G2, cuts = partition(G)
    G, G1, G2 = partition_2CC(G)
    client_G = KuzuClient("./graphs/kuzu/data/G")
    client_G1 = KuzuClient("./graphs/kuzu/data/G1")
    client_G2 = KuzuClient("./graphs/kuzu/data/G2")
    G.export(client_G)
    G1.export(client_G1)
    G2.export(client_G2)

