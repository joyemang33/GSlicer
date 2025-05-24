import random
import networkx as nx
from itertools import combinations

class TestNetworkxBridge:
    def __init__(self):
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0
        self.max_nodes = 100
        self.max_edges = 1000
    
    def create_test_case(self, n, m):
        """Create a random graph and its partition for testing"""
        # Generate a random graph
        self.G = nx.gnm_random_graph(n, m)
        
        # Ensure the graph is connected (for meaningful bridge test)
        if not nx.is_connected(self.G):
            # Add edges to make it connected
            components = list(nx.connected_components(self.G))
            for i in range(len(components)-1):
                u = random.choice(list(components[i]))
                v = random.choice(list(components[i+1]))
                self.G.add_edge(u, v)
        
        # Randomly partition nodes into two groups
        all_nodes = list(self.G.nodes())
        random.shuffle(all_nodes)
        split_point = random.randint(1, len(all_nodes)-1)  # Ensure both partitions have at least one node
        
        self.partition_A = set(all_nodes[:split_point])
        self.partition_B = set(all_nodes[split_point:])
        
        # Create the two subgraphs
        self.G_A = self.G.subgraph(self.partition_A).copy()
        self.G_B = self.G.subgraph(self.partition_B).copy()
        
        # Identify cross edges between partitions
        self.cross_edges = set()
        for u, v in self.G.edges():
            if (u in self.partition_A and v in self.partition_B) or \
               (u in self.partition_B and v in self.partition_A):
                self.cross_edges.add((u, v) if u < v else (v, u))  # Canonical form for undirected edges
    
    def bridge_oracle_smaller(self, bridges_G, bridges_A, bridges_B):
        """Validates the bridge detection algorithm using graph partition property.
        
        The oracle checks if: B(G) \ E(A,B) ⊆ B(G[A]) ∪ B(G[B])
        Where:
        - B(G) is the set of bridges in the original graph
        - E(A,B) is the set of edges crossing between subgraphs A and B
        - B(G[A]) is the set of bridges in subgraph A
        - B(G[B]) is the set of bridges in subgraph B
        """
        # Calculate left side of relation: B(G) \ E(A,B)
        left_side = bridges_G - self.cross_edges
        
        # Calculate right side of relation: B(G[A]) ∪ B(G[B])
        right_side = bridges_A | bridges_B
        
        # Check if the oracle relation holds
        if not left_side.issubset(right_side):
            # Find the problematic edges
            problematic_edges = left_side - right_side
            if problematic_edges:
                edge = next(iter(problematic_edges))
                error_msg = f"Edge {edge} is a bridge in G (not crossing subgraphs) but not a bridge in either subgraph"
                return False, error_msg
        
        return True, ""
    
    def validate(self):
        """Validate the bridge detection algorithm"""
        self.test_cases_counter += 1
        
        # Find bridges in the original graph and the subgraphs
        # We need to canonicalize the edges for undirected graphs
        bridges_G = {(u, v) if u < v else (v, u) for u, v in nx.bridges(self.G)}
        bridges_A = {(u, v) if u < v else (v, u) for u, v in nx.bridges(self.G_A)} 
        bridges_B = {(u, v) if u < v else (v, u) for u, v in nx.bridges(self.G_B)}
        
        # Check if the bridge oracle relation holds
        result, error_msg = self.bridge_oracle_smaller(bridges_G, bridges_A, bridges_B)
        
        if not result:
            self.bugs_cases_counter += 1
            print(f"Test case {self.test_cases_counter} failed: {error_msg}")
            print(f"Graph G: {self.G.edges()}")
            print(f"Graph G_A: {self.G_A.edges()}")
            print(f"Graph G_B: {self.G_B.edges()}")
            print(f"Bridges in G: {bridges_G}")
            print(f"Bridges in G_A: {bridges_A}")
            print(f"Bridges in G_B: {bridges_B}")
            print(f"Cross edges: {self.cross_edges}")
            return False
        
        return True
    
    def test(self):
        """Run a single test case"""
        try:
            _n = random.randint(5, self.max_nodes)  # At least 5 nodes for meaningful tests
            _m = random.randint(_n-1, min(self.max_edges, _n*(_n-1)//2))  # Ensure m is valid
            self.create_test_case(n=_n, m=_m)
        except Exception as e:
            print(f"Error creating test case: {e}")
            return
        
        self.validate()
    
    def run_tests(self, num_tests=100):
        """Run multiple test cases"""
        for i in range(num_tests):
            self.test()
        
        print(f"Bug-triggering tests/all tests = {self.bugs_cases_counter} / {self.test_cases_counter}")
        return self.bugs_cases_counter == 0

if __name__ == "__main__":
    random.seed(42)
    tester = TestNetworkxBridge()
    all_passed = tester.run_tests(100)
    
    if all_passed:
        print("All tests passed successfully!")
    else:
        print(f"Found {tester.bugs_cases_counter} test failures.")