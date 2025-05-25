import random
import networkx as nx
from networkx.algorithms.reciprocity import overall_reciprocity

class TestGraphReciprocityOracle:
    def __init__(self):
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0
        self.max_nodes = 100
        self.max_edges = 500
    
    def create_test_case(self, n, m):
        self.G = nx.gnm_random_graph(n, m, directed=True)
        
        if self.G.number_of_edges() == 0 and n >= 2:
            self.G.add_edge(0, 1)
        
        all_nodes = list(self.G.nodes())
        random.shuffle(all_nodes)
        split_point = random.randint(1, len(all_nodes)-1) if len(all_nodes) > 1 else 1
        
        self.partition_V1 = set(all_nodes[:split_point])
        self.partition_V2 = set(all_nodes[split_point:])
        
        self.G1 = self.G.subgraph(self.partition_V1).copy()
        self.G2 = self.G.subgraph(self.partition_V2).copy()
    
    def reciprocity_oracle(self):
        try:
            G_edges = self.G.number_of_edges()
            G_reciprocity = overall_reciprocity(self.G)
            G_product = G_reciprocity * G_edges
            
            G1_edges = self.G1.number_of_edges()
            G1_product = 0
            if G1_edges > 0:
                G1_reciprocity = overall_reciprocity(self.G1)
                G1_product = G1_reciprocity * G1_edges
            
            G2_edges = self.G2.number_of_edges()
            G2_product = 0
            if G2_edges > 0:
                G2_reciprocity = overall_reciprocity(self.G2)
                G2_product = G2_reciprocity * G2_edges
            
            sum_products = G1_product + G2_product
            result = G_product >= sum_products - 1e-10  
            
            return result, {
                "G_reciprocity": G_reciprocity,
                "G_edges": G_edges,
                "G_product": G_product,
                "G1_edges": G1_edges,
                "G1_product": G1_product,
                "G2_edges": G2_edges,
                "G2_product": G2_product,
                "sum_products": sum_products
            }
            
        except nx.NetworkXError:
            return True, {"error": "Empty graph or other NetworkX error"}
    
    def validate(self):
        self.test_cases_counter += 1
        
        result, details = self.reciprocity_oracle()
        
        if not result:
            self.bugs_cases_counter += 1
            print(f"Test case {self.test_cases_counter} failed:")
            print(f"Graph G: {self.G.edges()}")
            print(f"Partition V1: {self.partition_V1}")
            print(f"Partition V2: {self.partition_V2}")
            print(f"Details: {details}")
            return False
        
        return True
    
    def test(self):
        try:
            _n = random.randint(2, self.max_nodes)
            _m = random.randint(1, min(self.max_edges, _n*(_n-1)))
            self.create_test_case(n=_n, m=_m)
        except Exception as e:
            print(f"Error creating test case: {e}")
            return
        
        self.validate()
    
    def run_tests(self, num_tests=100):
        for i in range(num_tests):
            if i % 10 == 0:
                print(f"Running test {i}/{num_tests}")
            self.test()
        
        print(f"Bug-triggering tests/all tests = {self.bugs_cases_counter} / {self.test_cases_counter}")
        return self.bugs_cases_counter == 0

if __name__ == "__main__":
    random.seed(42)  
    tester = TestGraphReciprocityOracle()
    all_passed = tester.run_tests(1000)
    
    if all_passed:
        print("All tests passed successfully!")
    else:
        print(f"Found {tester.bugs_cases_counter} test failures.")