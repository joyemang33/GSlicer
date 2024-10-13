from graphs.basic_graph.schema import *
from graphs.basic_graph.generators.gen_normal_degree import generate as basic_gen
def generate(G : BasicGraph):
    G1 = BasicGraph(G.n, G.m, allow_loops=G.allow_loops, 
        allow_parallel_edge=G.allow_parallel_edge,
        is_directed=G.is_directed
    )
    G2 = BasicGraph(G.n, G.m, allow_loops=G.allow_loops, 
        allow_parallel_edge=G.allow_parallel_edge,
        is_directed=G.is_directed
    )
    basic_gen(G1)
    basic_gen(G2)
    for item in G1.nodes:
        G.nodes.append(BasicNode(item.id))
    for item in G2.nodes:
        G.nodes.append(BasicNode(item.id + G.n))
    for item in G1.edges:
        G.edges.append(BasicEdge(item.id, item.node_x, item.node_y))
    for item in G2.edges:
        G.edges.append(BasicEdge(item.id + G.m, item.node_x + G.n, item.node_y + G.n))
    G.n *= 2
    G.m *= 2
    assert G.n == len(G.nodes) and G.m == len(G.edges)


