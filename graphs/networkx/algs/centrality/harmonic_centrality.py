import random
import networkx as nx

class HarmonicCentralityOracle:
    def __init__(self):
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0
        self.max_nodes = 500
        self.max_edges = 2000
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
        hc_G = nx.harmonic_centrality(self.G)
        
        hc_G1 = nx.harmonic_centrality(self.G1) if len(self.G1) > 0 else {}
        hc_G2 = nx.harmonic_centrality(self.G2) if len(self.G2) > 0 else {}
        
        violations = []
        
        for node in self.partition_V1:
            if node in hc_G1:
                if hc_G[node] < hc_G1[node] - self.eps:
                    violations.append({
                        'node': node,
                        'graph': 'G1',
                        'G_value': hc_G[node],
                        'subgraph_value': hc_G1[node],
                        'difference': hc_G[node] - hc_G1[node]
                    })
        
        for node in self.partition_V2:
            if node in hc_G2:
                if hc_G[node] < hc_G2[node] - self.eps:
                    violations.append({
                        'node': node,
                        'graph': 'G2',
                        'G_value': hc_G[node],
                        'subgraph_value': hc_G2[node],
                        'difference': hc_G[node] - hc_G2[node]
                    })
        
        if violations:
            return False, {
                'violations': violations,
                'hc_G': hc_G,
                'hc_G1': hc_G1,
                'hc_G2': hc_G2
            }
        
        return True, {
            'hc_G': hc_G,
            'hc_G1': hc_G1,
            'hc_G2': hc_G2
        }
    
    def test(self):
        self.test_cases_counter += 1
        
        try:
            _n = random.randint(1, self.max_nodes)
            _m = random.randint(0, min(self.max_edges, _n*(_n-1)//2))
            self.create_test_case(n=_n, m=_m)
        except Exception as e:
            print(f"Error creating test case: {e}")
            return
        
        result, details = self.validate_oracle()
        
        if not result:
            self.bugs_cases_counter += 1
            print(f"\nTest case {self.test_cases_counter} failed:")
            print(f"Graph G: {len(self.G.nodes())} nodes, {len(self.G.edges())} edges")
            print(f"Graph G1: {len(self.G1.nodes())} nodes, {len(self.G1.edges())} edges")
            print(f"Graph G2: {len(self.G2.nodes())} nodes, {len(self.G2.edges())} edges")
            
            print("\nViolations found:")
            for violation in details['violations']:
                print(f"  Node {violation['node']} in {violation['graph']}:")
                print(f"    HC in G: {violation['G_value']:.6f}")
                print(f"    HC in subgraph: {violation['subgraph_value']:.6f}")
                print(f"    Difference: {violation['difference']:.6f}")
            
            nx.write_adjlist(self.G, f"failed_case_{self.test_cases_counter}_G.adjlist")
            nx.write_adjlist(self.G1, f"failed_case_{self.test_cases_counter}_G1.adjlist")
            nx.write_adjlist(self.G2, f"failed_case_{self.test_cases_counter}_G2.adjlist")
            
            print("\nDetailed harmonic centrality values:")
            print(f"G: {details['hc_G']}")
            print(f"G1: {details['hc_G1']}")
            print(f"G2: {details['hc_G2']}")
    
    def run_tests(self, num_tests=100):
        for i in range(num_tests):
            if i % 100 == 0:
                print(f"Running test {i}/{num_tests}")
            self.test()
        
        print(f"\nBug-triggering tests/all tests = {self.bugs_cases_counter} / {self.test_cases_counter}")
        if self.bugs_cases_counter == 0:
            print("All tests passed successfully!")
        else:
            print(f"Found {self.bugs_cases_counter} test failures.")

if __name__ == "__main__":
    random.seed(42)
    oracle_tester = HarmonicCentralityOracle()
    oracle_tester.run_tests(1000)