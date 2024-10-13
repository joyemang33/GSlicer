from graphs.basic_graph.schema import *
from graphs.basic_graph.generators import *
from graphs.basic_graph.partitioners import *


class BasicGenerator:
    def gen(self, n, m, allow_loops = True, allow_parallel_edge = True, is_directed = True,
                 generator = gen_uniform.generate,
                 partitioner = par_connected_uniform.partition):
        
        G = BasicGraph(n, m, allow_loops=allow_loops, 
                       allow_parallel_edge=allow_parallel_edge,
                       is_directed=is_directed)
        
        generator(G)

        try:
            partition_arr = partitioner(G)
            return G, partition_arr
        except:
            raise Exception("Failed to partition data.")
        
if __name__ == "__main__":
    BG = BasicGenerator()
    print("OK")
        
        