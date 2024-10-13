import random
from graphs.basic_graph.schema import *

def partition(G : BasicGraph):
    res = [0 for _ in range(0, G.n)]
    while(1):
        #Ensuring SubGraph is non-empty
        for i in range(0, G.n):
            res[i] = random.randint(0, 1)
        exit_flag = False
        for i in range(0, G.n):
            if res[i] != res[0]:
                exit_flag = True
        if exit_flag: break        

    return res



