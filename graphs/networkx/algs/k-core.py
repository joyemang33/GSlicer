import random
import networkx as nx
from itertools import combinations

class TestNetworkxKCore:
    def __init__(self):
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0
        self.max_nodes = 100
        self.max_edges = 1000
        self.k_values = [2, 3, 4, 5]  # Different k values to test
    
    def create_test_case(self, n, m):
        """Create a random graph and its partition for testing"""
        # Generate a random graph
        self.G = nx.gnm_random_graph(n, m)
        
        # Randomly partition nodes into two groups
        all_nodes = list(self.G.nodes())
        random.shuffle(all_nodes)
        split_point = random.randint(1, len(all_nodes)-1)  # Ensure both partitions have at least one node
        
        self.partition_A = set(all_nodes[:split_point])
        self.partition_B = set(all_nodes[split_point:])
        
        # Create the two subgraphs
        self.G_A = self.G.subgraph(self.partition_A).copy()
        self.G_B = self.G.subgraph(self.partition_B).copy()
        
        # Randomly select a k value to test
        self.k = random.choice(self.k_values)
    
    def kcore_oracle(self, core_G, core_A, core_B):
        """Validates the k-core detection algorithm using graph partition property.
        
        The oracle checks if: Core_k(G) ⊇ Core_k(G[A]) ∪ Core_k(G[B])
        Where:
        - Core_k(G) is the k-core of the original graph
        - Core_k(G[A]) is the k-core of the subgraph G[A]
        - Core_k(G[B]) is the k-core of the subgraph G[B]
        """
        # Calculate right side of relation: Core_k(G[A]) ∪ Core_k(G[B])
        right_side = core_A | core_B
        
        # Check if the oracle relation holds
        if not right_side.issubset(core_G):
            # Find the problematic nodes
            problematic_nodes = right_side - core_G
            if problematic_nodes:
                node = next(iter(problematic_nodes))
                error_msg = f"Node {node} is in a subgraph {self.k}-core but not in the original graph's {self.k}-core"
                return False, error_msg
        
        return True, ""
    
    def validate(self):
        """Validate the k-core detection algorithm"""
        self.test_cases_counter += 1
        
        # Find k-cores in the original graph and the subgraphs
        try:
            # Get the k-core for the original graph
            k_core_G = nx.k_core(self.G, k=self.k)
            core_G = set(k_core_G.nodes())
            
            # Get the k-core for subgraph A
            k_core_A = nx.k_core(self.G_A, k=self.k)
            core_A = set(k_core_A.nodes())
            
            # Get the k-core for subgraph B
            k_core_B = nx.k_core(self.G_B, k=self.k)
            core_B = set(k_core_B.nodes())
            
            # Check if the k-core oracle relation holds
            result, error_msg = self.kcore_oracle(core_G, core_A, core_B)
            
            if not result:
                self.bugs_cases_counter += 1
                print(f"Test case {self.test_cases_counter} failed: {error_msg}")
                print(f"k = {self.k}")
                print(f"Graph G nodes: {self.G.nodes()}")
                print(f"Graph G_A nodes: {self.G_A.nodes()}")
                print(f"Graph G_B nodes: {self.G_B.nodes()}")
                print(f"k-core of G: {core_G}")
                print(f"k-core of G_A: {core_A}")
                print(f"k-core of G_B: {core_B}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error in validate: {e}")
            return False
    
    def test(self):
        """Run a single test case"""
        try:
            _n = random.randint(10, self.max_nodes)  # At least 10 nodes for meaningful k-core tests
            _m = random.randint(_n, min(self.max_edges, _n*(_n-1)//2))  # Ensure enough edges for k-cores
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
        
        # Return True if all tests passed
        return self.bugs_cases_counter == 0

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Create test instance and run tests
    tester = TestNetworkxKCore()
    all_passed = tester.run_tests(100)  # Reduced to 100 tests
    
    if all_passed:
        print("All tests passed successfully!")
    else:
        print(f"Found {tester.bugs_cases_counter} test failures.")