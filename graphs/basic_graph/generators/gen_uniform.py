import random
from graphs.basic_graph.schema import *

def generate(G : BasicGraph):
    G.nodes, G.edges = [BasicNode(i) for i in range(0, G.n)], []   
    if G.n == 1 and not G.allow_loops and G.m > 0:  
        raise Exception("Given n = 1, m > 0, but no loop is allowed!")

    if G.allow_parallel_edge:
        for i in range(0, G.m):
            if G.allow_loops:
                x, y = random.randint(0, G.n - 1), random.randint(0, G.n - 1)
            else:
                x, y = random.sample(range(0, G.n), 2)
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

        if G.m < count_availiable_edges ** 0.75:
            created_edges = set()
            for i in range(0, G.m):
                while(1):
                    if G.allow_loops:
                        x, y = random.randint(0, G.n - 1), random.randint(0, G.n - 1)
                    else:
                        x, y = random.sample(range(0, G.n), 2)
                    if G.is_directed == False: x, y = min(x, y), max(x, y)
                    if (x, y) not in created_edges: break
                
                created_edges.add((x, y))
                G.edges.append(BasicEdge(i, x, y))
            
        else:
            candidate_edges = []
            for i in range(0, G.n):
                for j in range(i + 1, G.n):
                    candidate_edges.append((i, j))
            if G.allow_loops:
                for i in range(0, G.n):
                    candidate_edges.append((i, i))
            if G.is_directed:
                for i in range(0, G.n):
                    for j in range(0, i):
                        candidate_edges.append((i, j))

            assert G.m <= len(candidate_edges)
            candidate_edges = random.sample(candidate_edges, G.m)
            for i in range(0, G.m):
                G.edges.append(BasicEdge(i, candidate_edges[i][0], candidate_edges[i][1]))
            
    assert G.n == len(G.nodes) and G.m == len(G.edges)

    