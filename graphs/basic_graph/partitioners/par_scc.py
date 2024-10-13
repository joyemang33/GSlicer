import random
from graphs.basic_graph.schema import *

#Specical design for SCC algorithm


def partition(G : BasicGraph):
    res = [0 for _ in range(0, G.n)]
    for i in range(G.n // 2, G.n):
        res[i] = 1
    return res



