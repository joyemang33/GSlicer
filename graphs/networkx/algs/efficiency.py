import random
import networkx as nx
from itertools import combinations

class TestEfficiencyOracle:
    def __init__(self):
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0
        self.max_nodes = 50  # Smaller for efficiency calculations
        self.max_edges = 500
    
    def create_test_case(self, n, m):
        """Create a random graph and its partition for testing"""
        # Generate a random graph
        self.G = nx.gnm_random_graph(n, m)
        
        # Ensure the graph is connected (for meaningful efficiency test)
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
    
    def calculate_efficiency_sum(self, G):
        """Calculate the sum of efficiencies for all node pairs in graph G using nx.efficiency"""
        efficiency_sum = 0
        for u in G:
            for v in G:
                if u != v:
                    efficiency_sum += nx.efficiency(G, u, v)
        return efficiency_sum
    
    def efficiency_oracle(self):
        """Validates that the efficiency sum satisfies the oracle property.
        
        The oracle checks if:
        efficiency_sum(G) - cross_efficiency_sum ≥ efficiency_sum(G_A) + efficiency_sum(G_B)
        
        Where:
        - efficiency_sum(G) is the sum of efficiencies for all node pairs in G
        - cross_efficiency_sum is the sum of efficiencies for node pairs with one node in A and one in B
        - efficiency_sum(G_A) is the sum of efficiencies for all node pairs in subgraph A
        - efficiency_sum(G_B) is the sum of efficiencies for all node pairs in subgraph B
        """
        try:
            # Calculate efficiency sums for G, G_A, and G_B
            efficiency_sum_G = self.calculate_efficiency_sum(self.G)
            efficiency_sum_A = self.calculate_efficiency_sum(self.G_A)
            efficiency_sum_B = self.calculate_efficiency_sum(self.G_B)
            
            # Calculate cross-efficiency sum (for node pairs with one node in A, one in B)
            cross_efficiency_sum = 0
            for u in self.partition_A:
                for v in self.partition_B:
                    cross_efficiency_sum += nx.efficiency(self.G, u, v)
                    cross_efficiency_sum += nx.efficiency(self.G, v, u)  # Add both directions to match our calculation approach
            
            # Since we double counted in our pair-wise approach, divide by 2
            cross_efficiency_sum /= 2
            
            # The oracle property: efficiency_sum(G) - cross_efficiency_sum ≥ efficiency_sum(G_A) + efficiency_sum(G_B)
            left_side = efficiency_sum_G - cross_efficiency_sum
            right_side = efficiency_sum_A + efficiency_sum_B
            
            if left_side < right_side - 1e-10:  # Allow for small floating-point errors
                return False, f"Oracle violated: {left_side} < {right_side}"
            
            return True, ""
            
        except Exception as e:
            return False, f"Error in efficiency calculation: {e}"
    
    def validate(self):
        """Validate the efficiency oracle"""
        self.test_cases_counter += 1
        
        try:
            # Check if the efficiency oracle relation holds
            result, error_msg = self.efficiency_oracle()
            
            if not result:
                self.bugs_cases_counter += 1
                print(f"Test case {self.test_cases_counter} failed: {error_msg}")
                print(f"Graph G: {len(self.G.nodes())} nodes, {len(self.G.edges())} edges")
                print(f"Graph G_A: {len(self.G_A.nodes())} nodes, {len(self.G_A.edges())} edges")
                print(f"Graph G_B: {len(self.G_B.nodes())} nodes, {len(self.G_B.edges())} edges")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error in validate: {e}")
            return False
    
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
            if i % 10 == 0:
                print(f"{i} / {num_tests}")
            self.test()
        
        print(f"Bug-triggering tests/all tests = {self.bugs_cases_counter} / {self.test_cases_counter}")
        
        # Return True if all tests passed
        return self.bugs_cases_counter == 0

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Create test instance and run tests
    tester = TestEfficiencyOracle()
    all_passed = tester.run_tests(100)
    
    if all_passed:
        print("All tests passed successfully!")
    else:
        print(f"Found {tester.bugs_cases_counter} test failures.")