import pandas as pd
from graphs.neo4j.neo4j_tester import Neo4jTester
from graphs.basic_graph.generators import *
from graphs.basic_graph.partitioners import *

class TestNeo4jTriangleListing(Neo4jTester):
    def __init__(self):
        Neo4jTester.__init__(self)
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0

    def create_test_case(self, n, m, my_generator, my_partitioner):
        self.basic_G, self.partition_arr = self.basic_generator.gen(
            n, m,
            allow_loops=True, 
            allow_parallel_edge=True, 
            is_directed=False,
            generator=my_generator,
            partitioner=my_partitioner
        )
        self.G, self.G0, self.G1, self.nodes, self.edges, \
        self.nodes_0, self.edges_0, self.node_1, self.edges_1 = self.load(
            self.basic_G, self.partition_arr,
            is_directed=False
        )
    
    def validate(self):
        self.test_cases_counter += 1
        res_G = self.gds.alpha.triangles(self.G).to_dict('records')
        res_G0 = self.gds.alpha.triangles(self.G0).to_dict('records')
        res_G1 = self.gds.alpha.triangles(self.G1).to_dict('records')
        
        d_G, d_G0, d_G1 = [], [], []
        for d in res_G:
            d_G.append((d['nodeA'], d['nodeB'], d['nodeC']))
        for d in res_G0:
            d_G0.append((d['nodeA'], d['nodeB'], d['nodeC']))
        for d in res_G1:
            d_G1.append((d['nodeA'], d['nodeB'], d['nodeC']))

        for triangle in d_G0:
            if triangle not in d_G:
                print("Missing triangle in the result of G:", triangle)
                return False
        
        for triangle in d_G1:
            if triangle not in d_G:
                print("Missing triangle in the result of G:", triangle)
                return False
        

        for triangle in d_G:
            if triangle in d_G0 or triangle in d_G1: continue
            cnt0, cnt1 = 0, 0
            for id in triangle:
                if self.partition_arr[id] == 0: cnt0 += 1
                if self.partition_arr[id] == 1: cnt1 += 1 
            if cnt0 == 0 or cnt1 == 0:
                print("Redundant row in the result of G:", triangle)
                return False
                 
        # return True
    
    def test(self):
        try:
            self.create_test_case(
                n = 10, m = 30,
                my_generator = gen_uniform.generate,
                my_partitioner = par_connected_uniform.partition
            )
        except: 
            return
        if self.validate() == False:
            self.bugs_cases_counter += 1

if __name__ =="__main__":
    
    T = TestNeo4jTriangleListing()
    for _ in range(0, 1000): T.test()
    print("bug-triggering tests/all tests = ", T.bugs_cases_counter, "/", T.test_cases_counter)