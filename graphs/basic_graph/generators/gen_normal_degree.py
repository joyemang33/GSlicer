import numpy as np
import random
from graphs.basic_graph.schema import *

def generate(G : BasicGraph):
    G.nodes, G.edges = [BasicNode(i) for i in range(0, G.n)], []   
    if G.n == 1 and not G.allow_loops and G.m > 0:  
        raise Exception("Given n = 1, m > 0, but no loop is allowed!")

    num_weights = G.n
    mean = 0.5
    std_dev = 0.2
    random_weights = np.random.normal(mean, std_dev, num_weights)
    positive_weights = [abs(w) for w in random_weights]
    total_weight = sum(positive_weights)
    weights = [w / total_weight for w in positive_weights]
    ids = list(range(0, G.n))

    if G.allow_parallel_edge:
        for i in range(0, G.m):
            if G.allow_loops:
                x, y = np.random.choice(ids, size=1, p=weights)[0], np.random.choice(ids, size=1, p=weights)[0]
            else:
                x, y = np.random.choice(ids, size=2, p=weights, replace=False)
            if not G.is_directed: x, y = min(x, y), max(x, y)
            G.edges.append(BasicEdge(i, x, y))
    else:
        count_availiable_edges = 0
        count_availiable_edges = G.n * (G.n - 1) / 2
        if G.allow_loops: 
            count_availiable_edges += G.n
        if G.is_directed:
            count_availiable_edges += G.n * (G.n - 1) / 2
        if G.m > count_availiable_edges:
            raise Exception("no enough edges to produce!")

        created_edges = set()
        for i in range(0, G.m):
            while(1):
                if G.allow_loops:
                    x, y = np.random.choice(ids, size=1, p=weights)[0], np.random.choice(ids, size=1, p=weights)[0]
                else:
                    x, y = np.random.choice(ids, size=2, p=weights, replace=False)
                if G.is_directed == False: x, y = min(x, y), max(x, y)
                if (x, y) not in created_edges: break
                
            created_edges.add((x, y))
            G.edges.append(BasicEdge(i, x, y))
            
        
    assert G.n == len(G.nodes) and G.m == len(G.edges)

    