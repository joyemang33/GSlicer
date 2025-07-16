import random
import networkx as nx

class LocalReachingCentralityOracle:
    def __init__(self):
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0
        self.max_nodes = 50
        self.max_edges = 200
        self.eps = 1e-10
    
    def create_test_case(self, n, m):
        self.G = nx.gnm_random_graph(n, m, directed=True)
        
        all_nodes = list(self.G.nodes())
        random.shuffle(all_nodes)
        split_point = random.randint(1, len(all_nodes)-1) if len(all_nodes) > 1 else 1
        
        self.partition_V1 = set(all_nodes[:split_point])
        self.partition_V2 = set(all_nodes[split_point:])
        
        self.G1 = self.G.subgraph(self.partition_V1).copy()
        self.G2 = self.G.subgraph(self.partition_V2).copy()
    
    def compute_lnew(self, graph):
        lnew = {}
        
        n = len(graph)
        if n <= 1:
            return {node: 0 for node in graph.nodes()}
        
        for node in graph.nodes():
            try:
                lrc = nx.local_reaching_centrality(graph, node)
                lnew[node] = lrc * (n - 1)
            except nx.NetworkXError:
                
                lnew[node] = 0
        
        return lnew
    
    def validate_oracle(self):
        lnew_G = self.compute_lnew(self.G)
        lnew_G1 = self.compute_lnew(self.G1) if len(self.G1) > 0 else {}
        lnew_G2 = self.compute_lnew(self.G2) if len(self.G2) > 0 else {}
        
        violations = []
        
        for node in self.partition_V1:
            if node in lnew_G1 and node in lnew_G:
                if lnew_G[node] < lnew_G1[node] - self.eps:
                    violations.append({
                        'node': node,
                        'graph': 'G1',
                        'G_lnew': lnew_G[node],
                        'subgraph_lnew': lnew_G1[node],
                        'difference': lnew_G[node] - lnew_G1[node]
                    })
        
        for node in self.partition_V2:
            if node in lnew_G2 and node in lnew_G:
                if lnew_G[node] < lnew_G2[node] - self.eps:
                    violations.append({
                        'node': node,
                        'graph': 'G2',
                        'G_lnew': lnew_G[node],
                        'subgraph_lnew': lnew_G2[node],
                        'difference': lnew_G[node] - lnew_G2[node]
                    })
        
        if violations:
            lrc_G = {}
            lrc_G1 = {}
            lrc_G2 = {}
            
            for node in self.G.nodes():
                try:
                    lrc_G[node] = nx.local_reaching_centrality(self.G, node)
                except:
                    lrc_G[node] = 0
            
            for node in self.G1.nodes():
                try:
                    lrc_G1[node] = nx.local_reaching_centrality(self.G1, node)
                except:
                    lrc_G1[node] = 0
                    
            for node in self.G2.nodes():
                try:
                    lrc_G2[node] = nx.local_reaching_centrality(self.G2, node)
                except:
                    lrc_G2[node] = 0
            
            return False, {
                'violations': violations,
                'lnew_G': lnew_G,
                'lnew_G1': lnew_G1,
                'lnew_G2': lnew_G2,
                'lrc_G': lrc_G,
                'lrc_G1': lrc_G1,
                'lrc_G2': lrc_G2
            }
        
        return True, {
            'lnew_G': lnew_G,
            'lnew_G1': lnew_G1,
            'lnew_G2': lnew_G2
        }
    
    def test(self):
        self.test_cases_counter += 1
        
        try:
            
            _n = random.randint(1, self.max_nodes)
            _m = random.randint(0, min(self.max_edges, _n*(_n-1)))
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
                print(f"    Lnew in G: {violation['G_lnew']:.6f}")
                print(f"    Lnew in subgraph: {violation['subgraph_lnew']:.6f}")
                print(f"    Difference: {violation['difference']:.6f}")
            
            print("\nDetailed Lnew values:")
            print(f"G: {details['lnew_G']}")
            print(f"G1: {details['lnew_G1']}")
            print(f"G2: {details['lnew_G2']}")
            
            print("\nDetailed local_reaching_centrality values:")
            print(f"G: {details['lrc_G']}")
            print(f"G1: {details['lrc_G1']}")
            print(f"G2: {details['lrc_G2']}")
            
            print("\nEdges in G (first 10):")
            print(list(self.G.edges())[:10], "..." if len(self.G.edges()) > 10 else "")
    
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
    oracle_tester = LocalReachingCentralityOracle()
    oracle_tester.run_tests(1000)