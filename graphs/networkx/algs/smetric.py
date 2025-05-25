import random
import networkx as nx

class SMetricOracle:
    def __init__(self):
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0
        self.max_nodes = 50
        self.max_edges = 200
        self.eps = 1e-10
    
    def create_test_case(self, n, m):
        self.G = nx.gnm_random_graph(n, m)
        
        all_nodes = list(self.G.nodes())
        random.shuffle(all_nodes)
        split_point = random.randint(1, len(all_nodes)-1) if len(all_nodes) > 1 else 1
        
        self.partition_V1 = set(all_nodes[:split_point])
        self.partition_V2 = set(all_nodes[split_point:])
        
        self.G1 = self.G.subgraph(self.partition_V1).copy()
        self.G2 = self.G.subgraph(self.partition_V2).copy()
    
    def validate_oracle(self):
        s_G = nx.s_metric(self.G, normalized = False)
        s_G1 = nx.s_metric(self.G1, normalized = False)
        s_G2 = nx.s_metric(self.G2, normalized = False)
        
        sum_s = s_G1 + s_G2
        
        if sum_s > s_G + self.eps:
            return False, {
                "G_s_metric": s_G,
                "G1_s_metric": s_G1,
                "G2_s_metric": s_G2,
                "sum_s_metrics": sum_s,
                "difference": sum_s - s_G
            }
        
        return True, {
            "G_s_metric": s_G,
            "G1_s_metric": s_G1,
            "G2_s_metric": s_G2,
            "sum_s_metrics": sum_s
        }
    
    def test(self):
        self.test_cases_counter += 1
        
        try:
            _n = random.randint(5, self.max_nodes)
            _m = random.randint(_n, min(self.max_edges, _n*(_n-1)//2))
            self.create_test_case(n=_n, m=_m)
        except Exception as e:
            print(f"Error creating test case: {e}")
            return
        
        result, details = self.validate_oracle()
        
        if not result:
            self.bugs_cases_counter += 1
            print(f"Test case {self.test_cases_counter} failed:")
            print(f"Graph G: {len(self.G.nodes())} nodes, {len(self.G.edges())} edges")
            print(f"Graph G1: {len(self.G1.nodes())} nodes, {len(self.G1.edges())} edges")
            print(f"Graph G2: {len(self.G2.nodes())} nodes, {len(self.G2.edges())} edges")
            print(f"Details: {details}")
            
            print("Edge details in G:")
            for u, v in self.G.edges():
                print(f"Edge ({u},{v}): {self.G.degree(u)} * {self.G.degree(v)} = {self.G.degree(u) * self.G.degree(v)}")
            
            nx.write_adjlist(self.G, f"failed_case_{self.test_cases_counter}_G.adjlist")
            nx.write_adjlist(self.G1, f"failed_case_{self.test_cases_counter}_G1.adjlist")
            nx.write_adjlist(self.G2, f"failed_case_{self.test_cases_counter}_G2.adjlist")
    
    def run_tests(self, num_tests=100):
        for i in range(num_tests):
            if i % 10 == 0:
                print(f"Running test {i}/{num_tests}")
            self.test()
        
        print(f"Bug-triggering tests/all tests = {self.bugs_cases_counter} / {self.test_cases_counter}")
        if self.bugs_cases_counter == 0:
            print("All tests passed successfully!")
        else:
            print(f"Found {self.bugs_cases_counter} test failures.")

if __name__ == "__main__":
    random.seed(42)
    oracle_tester = SMetricOracle()
    oracle_tester.run_tests(1000)