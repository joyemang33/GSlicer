import random
from graphs.basic_graph.schema import *
from graphs.basic_graph.partitioners.dsu import DSU

def partition(G : BasicGraph):
    dsu = DSU(G.n)
    for edge in G.edges:
        dsu.merge(edge.node_x, edge.node_y)
    CCs = dsu.listing_conected_components()
    # print(CCs)
    if len(CCs) == 1:
        raise Exception("G is connected. Please re-generate the graph.")
    res = [0 for _ in range(0, G.n)]
    while(1):
        #Ensuring SubGraph is non-empty
        for cc in CCs:
            val = random.randint(0, 1)
            for x in cc: 
                res[x] = val
        
        exit_flag = False
        for i in range(0, G.n):
            if res[i] != res[0]:
                exit_flag = True
        if exit_flag: break        

    return res

if __name__ == "__main__":
    G = BasicGraph(5, 5)
    from graphs.basic_graph.generators import *
    gen_uniform.generate(G)
    print(G.n, G.m)





