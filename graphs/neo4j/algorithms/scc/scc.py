import pandas as pd
import random
from graphs.neo4j.neo4j_tester import Neo4jTester
from graphs.basic_graph.generators import *
from graphs.basic_graph.partitioners import *

class TestNeo4jSCC(Neo4jTester):
    def __init__(self):
        Neo4jTester.__init__(self)
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0
        self.max_nodes = 100
        self.max_edges = 500

    def create_test_case(self, n, m, my_generator, my_partitioner):
        self.basic_G, self.partition_arr = self.basic_generator.gen(
            n, m,
            allow_loops=True, 
            allow_parallel_edge=True, 
            is_directed=True,
            generator=my_generator,
            partitioner=my_partitioner
        )
        self.G, self.G0, self.G1, self.nodes, self.edges, \
        self.nodes_0, self.edges_0, self.nodes_1, self.edges_1 = self.load(
            self.basic_G, self.partition_arr,
            is_directed=True
        )
    
    def validate(self):
        self.test_cases_counter += 1
        
        # node_labels = random.sample(["L" + str(i) for i in range(0, 5)], random.randint(0, 5))
        # edge_labels = random.sample(["T" + str(i) for i in range(0, 5)], random.randint(0, 5))

        
        res_G = self.gds.alpha.scc.stream(self.G).to_dict('records')
        res_G0 = self.gds.alpha.scc.stream(self.G0, concurrency=12).to_dict('records')
        res_G1 = self.gds.alpha.scc.stream(self.G1).to_dict('records')
        
        d_G, d_G0, d_G1 = dict(), dict(), dict()
        c_G, c_G0, c_G1 = dict(), dict(), dict()

        for x in res_G: c_G[x["nodeId"]] = x["componentId"]
        for x in res_G0: c_G0[x["nodeId"]] = x["componentId"]
        for x in res_G1: c_G1[x["nodeId"]] = x["componentId"]
        
        for x in res_G: 
            if x["componentId"] in d_G.keys():
                d_G[x["componentId"]].append(x["nodeId"])
            else:
                d_G[x["componentId"]] = [x["nodeId"]]
        for x in res_G0: 
            if x["componentId"] in d_G0.keys():
                d_G0[x["componentId"]].append(x["nodeId"])
            else:
                d_G0[x["componentId"]] = [x["nodeId"]]

        for x in res_G1: 
            if x["componentId"] in d_G1.keys():
                d_G1[x["componentId"]].append(x["nodeId"])
            else:
                d_G1[x["componentId"]] = [x["nodeId"]]
        
        for cc in d_G0.keys():
            for x in d_G0[cc]:
                for y in d_G0[cc]:
                    if c_G[x] != c_G[y]:
                        return False
        
        for cc in d_G1.keys():
            for x in d_G1[cc]:
                for y in d_G1[cc]:
                    if c_G[x] != c_G[y]:
                        return False

        for x in c_G0.keys():
            for y in c_G1.keys():
                if c_G[x] == c_G[y]:
                    return False

        
            
    def test(self):
        try:
            self.create_test_case(
                n = random.randint(2, self.max_nodes), m = random.randint(0, self.max_edges),
                my_generator = gen_normal_disconnected_scc.generate,
                my_partitioner = par_scc.partition
            )
        except: 
            return
        if self.validate() == False:
            self.bugs_cases_counter += 1

if __name__ =="__main__":
    
    T = TestNeo4jSCC()
    for i in range(0, 1000): 
        print(i)
        if i % 100 == 0: print(str(i/10)+"%") 
        T.test()
    print("bug-triggering tests/all tests = ", 
        T.bugs_cases_counter, "/", T.test_cases_counter)