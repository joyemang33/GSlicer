import pandas as pd
from graphs.neo4j.neo4j_tester import Neo4jTester
from graphs.basic_graph.generators import *
from graphs.basic_graph.partitioners import *

class TestNeo4jKcore(Neo4jTester):
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
        self.nodes_0, self.edges_0, self.nodes_1, self.edges_1 = self.load(
            self.basic_G, self.partition_arr,
            is_directed=False
        )
    
    def validate(self):
        self.test_cases_counter += 1
        res_G = self.gds.kcore.stream(self.G).to_dict('records')
        res_G0 = self.gds.kcore.stream(self.G0).to_dict('records')
        res_G1 = self.gds.kcore.stream(self.G1).to_dict('records')
        d_G, d_G0, d_G1 = dict(), dict(), dict()
        for x in res_G: d_G[x["nodeId"]] = x["coreValue"]
        for x in res_G0: d_G0[x["nodeId"]] = x["coreValue"]
        for x in res_G1: d_G1[x["nodeId"]] = x["coreValue"]
        
        for v in d_G0.keys():
            if d_G0[v] != d_G[v]: 
                return False

        for v in d_G1.keys():
            if d_G1[v] != d_G[v]: 
                return False
            
    def test(self):
        try:
            self.create_test_case(
                n = 100, m = 200,
                my_generator = gen_normal_disconnected.generate,
                my_partitioner = par_disconnected_uniform.partition
            )
        except: 
            return
        if self.validate() == False:
            self.bugs_cases_counter += 1

if __name__ =="__main__":
    
    T = TestNeo4jKcore()
    for i in range(0, 1000): 
        if i % 100 == 0: print(str(i/10)+"%") 
        T.test()
    
    print("bug-triggering tests/all tests = ", 
        T.bugs_cases_counter, "/", T.test_cases_counter)