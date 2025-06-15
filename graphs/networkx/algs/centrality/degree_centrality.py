import random
import networkx as nx

class DegreeCentralityOracle:
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
    
    def compute_dnew(self, graph):
        """计算 dnew = d * (n-1) 的值"""
        dc = nx.degree_centrality(graph)
        dnew = {}
        
        n = len(graph)
        for node in graph.nodes():
            if n > 1:
                # degree_centrality = degree / (n-1)
                dnew[node] = dc[node] * (n - 1)
            else:
                dnew[node] = 0  
        
        return dnew
    
    def validate_oracle(self):
        dnew_G = self.compute_dnew(self.G)
        dnew_G1 = self.compute_dnew(self.G1) if len(self.G1) > 0 else {}
        dnew_G2 = self.compute_dnew(self.G2) if len(self.G2) > 0 else {}
        
        violations = []
        
        for node in self.partition_V1:
            if node in dnew_G1 and node in dnew_G:
                if dnew_G[node] < dnew_G1[node] - self.eps:
                    violations.append({
                        'node': node,
                        'graph': 'G1',
                        'G_dnew': dnew_G[node],
                        'subgraph_dnew': dnew_G1[node],
                        'difference': dnew_G[node] - dnew_G1[node],
                        'G_degree': self.G.degree(node),
                        'subgraph_degree': self.G1.degree(node)
                    })
        
        for node in self.partition_V2:
            if node in dnew_G2 and node in dnew_G:
                if dnew_G[node] < dnew_G2[node] - self.eps:
                    violations.append({
                        'node': node,
                        'graph': 'G2',
                        'G_dnew': dnew_G[node],
                        'subgraph_dnew': dnew_G2[node],
                        'difference': dnew_G[node] - dnew_G2[node],
                        'G_degree': self.G.degree(node),
                        'subgraph_degree': self.G2.degree(node)
                    })
        
        if violations:
            return False, {
                'violations': violations,
                'dnew_G': dnew_G,
                'dnew_G1': dnew_G1,
                'dnew_G2': dnew_G2,
                'dc_G': nx.degree_centrality(self.G),
                'dc_G1': nx.degree_centrality(self.G1) if len(self.G1) > 0 else {},
                'dc_G2': nx.degree_centrality(self.G2) if len(self.G2) > 0 else {}
            }
        
        return True, {
            'dnew_G': dnew_G,
            'dnew_G1': dnew_G1,
            'dnew_G2': dnew_G2
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
                print(f"    dnew in G: {violation['G_dnew']:.6f}")
                print(f"    dnew in subgraph: {violation['subgraph_dnew']:.6f}")
                print(f"    Actual degree in G: {violation['G_degree']}")
                print(f"    Actual degree in subgraph: {violation['subgraph_degree']}")
                print(f"    Difference: {violation['difference']:.6f}")
            
            print("\nDetailed dnew values:")
            print(f"G: {details['dnew_G']}")
            print(f"G1: {details['dnew_G1']}")
            print(f"G2: {details['dnew_G2']}")
            
            print("\nDetailed degree centrality values:")
            print(f"G: {details['dc_G']}")
            print(f"G1: {details['dc_G1']}")
            print(f"G2: {details['dc_G2']}")
            
            print("\nEdges in G:")
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
    oracle_tester = DegreeCentralityOracle()
    oracle_tester.run_tests(1000)