class BasicNode:
    def __init__(self, id : int): 
        self.id = id


class BasicEdge:
    def __init__(self, id : int, node_x : int, node_y : int):
        self.id = id
        self.node_x = node_x
        self.node_y = node_y 

class BasicGraph:
    def __init__(self, n : int, m : int, allow_loops = True, 
                 allow_parallel_edge = True, 
                 is_directed = True):
        self.n = n
        self.m = m
        self.nodes = []
        self.edges = []
        self.is_directed = is_directed
        self.allow_loops = allow_loops
        self.allow_parallel_edge = allow_parallel_edge
 
 

