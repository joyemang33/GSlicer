import random
import networkx as nx

class ConnectedComponentsOracle:
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
        cc_G = list(nx.connected_components(self.G))
        
        cc_G1 = list(nx.connected_components(self.G1)) if len(self.G1) > 0 else []
        cc_G2 = list(nx.connected_components(self.G2)) if len(self.G2) > 0 else []
        
        violations = []
        
        for i, component in enumerate(cc_G1):
            parent_components = set()
            for node in component:
                for j, cc in enumerate(cc_G):
                    if node in cc:
                        parent_components.add(j)
                        break
            
            if len(parent_components) > 1:
                violations.append({
                    'subgraph': 'G1',
                    'component_index': i,
                    'component_nodes': component,
                    'parent_components': parent_components,
                    'parent_component_details': {j: cc_G[j] for j in parent_components}
                })
        
        for i, component in enumerate(cc_G2):
            parent_components = set()
            for node in component:
                for j, cc in enumerate(cc_G):
                    if node in cc:
                        parent_components.add(j)
                        break
            
            if len(parent_components) > 1:
                violations.append({
                    'subgraph': 'G2',
                    'component_index': i,
                    'component_nodes': component,
                    'parent_components': parent_components,
                    'parent_component_details': {j: cc_G[j] for j in parent_components}
                })
        
        if violations:
            return False, {
                'violations': violations,
                'cc_G': cc_G,
                'cc_G1': cc_G1,
                'cc_G2': cc_G2,
                'num_cc_G': nx.number_connected_components(self.G),
                'num_cc_G1': nx.number_connected_components(self.G1) if len(self.G1) > 0 else 0,
                'num_cc_G2': nx.number_connected_components(self.G2) if len(self.G2) > 0 else 0
            }
        
        return True, {
            'cc_G': cc_G,
            'cc_G1': cc_G1,
            'cc_G2': cc_G2
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
            
            print(f"\nNumber of connected components:")
            print(f"  G: {details['num_cc_G']}")
            print(f"  G1: {details['num_cc_G1']}")
            print(f"  G2: {details['num_cc_G2']}")
            
            print("\nViolations found:")
            for violation in details['violations']:
                print(f"\n  Violation in {violation['subgraph']}:")
                print(f"    Component {violation['component_index']} with nodes {violation['component_nodes']}")
                print(f"    Maps to {len(violation['parent_components'])} different components in G:")
                for parent_idx, parent_cc in violation['parent_component_details'].items():
                    print(f"      Component {parent_idx}: {parent_cc}")
            
            
            print("\nEdges in G (first 10):")
            print(list(self.G.edges())[:10], "..." if len(self.G.edges()) > 10 else "")
            
            
            print(f"\nIs G connected? {nx.is_connected(self.G)}")
            if len(self.G1) > 0:
                print(f"Is G1 connected? {nx.is_connected(self.G1)}")
            if len(self.G2) > 0:
                print(f"Is G2 connected? {nx.is_connected(self.G2)}")
    
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
    oracle_tester = ConnectedComponentsOracle()
    oracle_tester.run_tests(1000)