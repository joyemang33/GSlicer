import random
import networkx as nx

class TestIsolatesOracle:
    def __init__(self):
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0
        self.max_nodes = 100
        self.max_edges = 1000
    
    def create_test_case(self, n, m):
        """Create a random graph and its partition for testing"""
        # Generate a random graph
        self.G = nx.gnm_random_graph(n, m)
        
        # Randomly add some isolated nodes
        num_isolates = random.randint(0, n // 5)  # Add up to 20% more isolates
        for i in range(num_isolates):
            self.G.add_node(n + i)
        
        # Randomly partition nodes into two groups
        all_nodes = list(self.G.nodes())
        random.shuffle(all_nodes)
        split_point = random.randint(1, len(all_nodes)-1)  # Ensure both partitions have at least one node
        
        self.partition_A = set(all_nodes[:split_point])
        self.partition_B = set(all_nodes[split_point:])
        
        # Create the two subgraphs
        self.G_A = self.G.subgraph(self.partition_A).copy()
        self.G_B = self.G.subgraph(self.partition_B).copy()
    
    def isolates_oracle(self):
        """Validates the isolates oracle:
        
        The number of isolates in the original graph G is less than or equal to
        the sum of isolates in the subgraphs G_A and G_B.
        
        This is because:
        1. Any node that was isolated in G remains isolated in its respective subgraph
        2. Non-isolated nodes in G may become isolated in subgraphs if all their 
           neighbors are in the other subgraph
        """
        # Count isolates in original graph
        isolates_G = nx.number_of_isolates(self.G)
        
        # Count isolates in subgraphs
        isolates_A = nx.number_of_isolates(self.G_A)
        isolates_B = nx.number_of_isolates(self.G_B)
        
        # Oracle: isolates in G <= isolates in G_A + isolates in G_B
        if isolates_G > isolates_A + isolates_B:
            return False, f"Oracle violated: {isolates_G} > {isolates_A} + {isolates_B}"
        
        return True, ""
    
    def validate(self):
        """Validate the isolates oracle"""
        self.test_cases_counter += 1
        
        try:
            # Check if the isolates oracle relation holds
            result, error_msg = self.isolates_oracle()
            
            if not result:
                self.bugs_cases_counter += 1
                print(f"Test case {self.test_cases_counter} failed: {error_msg}")
                print(f"Graph G: {len(self.G.nodes())} nodes, {len(self.G.edges())} edges")
                print(f"Graph G_A: {len(self.G_A.nodes())} nodes, {len(self.G_A.edges())} edges")
                print(f"Graph G_B: {len(self.G_B.nodes())} nodes, {len(self.G_B.edges())} edges")
                # Print isolates in each graph for debugging
                print(f"Isolates in G: {list(nx.isolates(self.G))}")
                print(f"Isolates in G_A: {list(nx.isolates(self.G_A))}")
                print(f"Isolates in G_B: {list(nx.isolates(self.G_B))}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error in validate: {e}")
            return False
    
    def test(self):
        """Run a single test case"""
        try:
            _n = random.randint(5, self.max_nodes)  # At least 5 nodes for meaningful tests
            _m = random.randint(0, min(self.max_edges, _n*(_n-1)//2))  # Allow for 0 edges to test empty graphs
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
    tester = TestIsolatesOracle()
    all_passed = tester.run_tests(100)
    
    if all_passed:
        print("All tests passed successfully!")
    else:
        print(f"Found {tester.bugs_cases_counter} test failures.")