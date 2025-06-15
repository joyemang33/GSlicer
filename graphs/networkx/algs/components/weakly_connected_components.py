import random
import networkx as nx

class WeaklyConnectedComponentsOracle:
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
    
    def validate_oracle(self):
        wcc_G = list(nx.weakly_connected_components(self.G))
        
        wcc_G1 = list(nx.weakly_connected_components(self.G1)) if len(self.G1) > 0 else []
        wcc_G2 = list(nx.weakly_connected_components(self.G2)) if len(self.G2) > 0 else []
        
        violations = []
        
        for i, component in enumerate(wcc_G1):
            parent_components = []
            for j, wcc in enumerate(wcc_G):
                if component.issubset(wcc):
                    parent_components.append(j)
            
            if len(parent_components) == 0:
                violations.append({
                    'subgraph': 'G1',
                    'component_index': i,
                    'component_nodes': component,
                    'error': 'Not a subset of any weakly connected component in G'
                })
        
        for i, component in enumerate(wcc_G2):
            parent_components = []
            for j, wcc in enumerate(wcc_G):
                if component.issubset(wcc):
                    parent_components.append(j)
            
            if len(parent_components) == 0:
                violations.append({
                    'subgraph': 'G2',
                    'component_index': i,
                    'component_nodes': component,
                    'error': 'Not a subset of any weakly connected component in G'
                })
        
        if violations:
            return False, {
                'violations': violations,
                'wcc_G': wcc_G,
                'wcc_G1': wcc_G1,
                'wcc_G2': wcc_G2,
                'num_wcc_G': nx.number_weakly_connected_components(self.G),
                'num_wcc_G1': nx.number_weakly_connected_components(self.G1) if len(self.G1) > 0 else 0,
                'num_wcc_G2': nx.number_weakly_connected_components(self.G2) if len(self.G2) > 0 else 0
            }
        
        return True, {
            'wcc_G': wcc_G,
            'wcc_G1': wcc_G1,
            'wcc_G2': wcc_G2
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
            
            print(f"\nNumber of weakly connected components:")
            print(f"  G: {details['num_wcc_G']}")
            print(f"  G1: {details['num_wcc_G1']}")
            print(f"  G2: {details['num_wcc_G2']}")
            
            print("\nViolations found:")
            for violation in details['violations']:
                print(f"\n  Violation in {violation['subgraph']}:")
                print(f"    Component {violation['component_index']} with nodes {violation['component_nodes']}")
                print(f"    Error: {violation['error']}")
            
            print("\nWeakly connected components in G:")
            for i, wcc in enumerate(details['wcc_G']):
                print(f"  Component {i}: {wcc}")
            
            print(f"\nWeakly connected components in {violation['subgraph']}:")
            wcc_list = details['wcc_G1'] if violation['subgraph'] == 'G1' else details['wcc_G2']
            for i, wcc in enumerate(wcc_list):
                print(f"  Component {i}: {wcc}")
            
            print(f"\nIs G weakly connected? {nx.is_weakly_connected(self.G)}")
            if len(self.G1) > 0:
                print(f"Is G1 weakly connected? {nx.is_weakly_connected(self.G1)}")
            if len(self.G2) > 0:
                print(f"Is G2 weakly connected? {nx.is_weakly_connected(self.G2)}")
    
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
    oracle_tester = WeaklyConnectedComponentsOracle()
    oracle_tester.run_tests(1000)