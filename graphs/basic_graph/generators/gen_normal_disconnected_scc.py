import random
from graphs.basic_graph.schema import *
from graphs.basic_graph.generators.gen_normal_disconnected import generate as basic_gen

#Specical design for SCC algorithm

def generate(G : BasicGraph):
    basic_gen(G)
    assert G.n % 2 == 0
    num_additional_edges = random.randint(1, G.m)
    for _ in range(0, num_additional_edges):
        G.m += 1
        x, y = random.randint(0, G.n // 2 - 1),  random.randint(G.n // 2, G.n - 1)
        G.edges.append(BasicEdge(G.m, x, y))
    
    assert G.n == len(G.nodes) and G.m == len(G.edges)
