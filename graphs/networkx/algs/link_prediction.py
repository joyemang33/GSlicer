import random
import networkx as nx
from networkx.algorithms import link_prediction

class TestLinkPredictionOracles:
    def __init__(self):
        self.test_cases_counter = 0
        self.common_neighbors_bugs = 0
        self.preferential_attachment_bugs = 0
        self.max_nodes = 100
        self.max_edges = 1000
    
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
    
    def common_neighbors_oracle(self):
        """Test the common neighbors oracle:
        
        For any two nodes u and v that are both in the same subgraph (G_A or G_B),
        the number of common neighbors in the subgraph is less than or equal to
        the number of common neighbors in the original graph G.
        
        This is because some common neighbors in G might be in the other subgraph.
        """
        # Test for nodes in subgraph A
        for u in self.G_A:
            for v in self.G_A:
                if u >= v:  # Avoid testing the same pair twice
                    continue
                
                # Count common neighbors in original graph
                cn_G = len(list(nx.common_neighbors(self.G, u, v)))
                
                # Count common neighbors in subgraph
                cn_G_A = len(list(nx.common_neighbors(self.G_A, u, v)))
                
                # Oracle: cn_G_A <= cn_G
                if cn_G_A > cn_G:
                    return False, f"Common neighbors oracle violated for nodes {u} and {v} in G_A: {cn_G_A} > {cn_G}"
        
        # Test for nodes in subgraph B
        for u in self.G_B:
            for v in self.G_B:
                if u >= v:  # Avoid testing the same pair twice
                    continue
                
                # Count common neighbors in original graph
                cn_G = len(list(nx.common_neighbors(self.G, u, v)))
                
                # Count common neighbors in subgraph
                cn_G_B = len(list(nx.common_neighbors(self.G_B, u, v)))
                
                # Oracle: cn_G_B <= cn_G
                if cn_G_B > cn_G:
                    return False, f"Common neighbors oracle violated for nodes {u} and {v} in G_B: {cn_G_B} > {cn_G}"
        
        return True, ""
    
    def preferential_attachment_oracle(self):
        """Test the preferential attachment oracle:
        
        For any two nodes u and v that are both in the same subgraph (G_A or G_B),
        the preferential attachment score in the subgraph is less than or equal to
        the preferential attachment score in the original graph G.
        
        This is because the degree of a node in a subgraph is less than or equal to
        its degree in the original graph.
        
        This implementation uses NetworkX's link_prediction.preferential_attachment function.
        """
        # Test for nodes in subgraph A
        node_pairs_A = [(u, v) for u in self.G_A for v in self.G_A if u < v]
        if node_pairs_A:
            # Calculate PA scores in original graph using link_prediction
            pa_scores_G = {}
            for u, v, score in link_prediction.preferential_attachment(self.G, node_pairs_A):
                pa_scores_G[(u, v)] = score
            
            # Calculate PA scores in subgraph using link_prediction
            pa_scores_G_A = {}
            for u, v, score in link_prediction.preferential_attachment(self.G_A, node_pairs_A):
                pa_scores_G_A[(u, v)] = score
            
            # Check oracle: pa_G_A <= pa_G for each pair
            for u, v in node_pairs_A:
                if pa_scores_G_A.get((u, v), 0) > pa_scores_G.get((u, v), 0):
                    return False, f"Preferential attachment oracle violated for nodes {u} and {v} in G_A: {pa_scores_G_A.get((u, v), 0)} > {pa_scores_G.get((u, v), 0)}"
        
        # Test for nodes in subgraph B
        node_pairs_B = [(u, v) for u in self.G_B for v in self.G_B if u < v]
        if node_pairs_B:
            # Calculate PA scores in original graph using link_prediction
            pa_scores_G = {}
            for u, v, score in link_prediction.preferential_attachment(self.G, node_pairs_B):
                pa_scores_G[(u, v)] = score
            
            # Calculate PA scores in subgraph using link_prediction
            pa_scores_G_B = {}
            for u, v, score in link_prediction.preferential_attachment(self.G_B, node_pairs_B):
                pa_scores_G_B[(u, v)] = score
            
            # Check oracle: pa_G_B <= pa_G for each pair
            for u, v in node_pairs_B:
                if pa_scores_G_B.get((u, v), 0) > pa_scores_G.get((u, v), 0):
                    return False, f"Preferential attachment oracle violated for nodes {u} and {v} in G_B: {pa_scores_G_B.get((u, v), 0)} > {pa_scores_G.get((u, v), 0)}"
        
        return True, ""
    
    def validate(self):
        """Validate both oracles"""
        self.test_cases_counter += 1
        
        try:
            # Check common neighbors oracle
            cn_result, cn_error_msg = self.common_neighbors_oracle()
            
            if not cn_result:
                self.common_neighbors_bugs += 1
                print(f"Test case {self.test_cases_counter} failed CN oracle: {cn_error_msg}")
            
            # Check preferential attachment oracle
            pa_result, pa_error_msg = self.preferential_attachment_oracle()
            
            if not pa_result:
                self.preferential_attachment_bugs += 1
                print(f"Test case {self.test_cases_counter} failed PA oracle: {pa_error_msg}")
            
            return cn_result and pa_result
            
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
        
        print("Test results:")
        print(f"Common Neighbors Oracle: Bug-triggering tests/all tests = {self.common_neighbors_bugs} / {self.test_cases_counter}")
        print(f"Preferential Attachment Oracle: Bug-triggering tests/all tests = {self.preferential_attachment_bugs} / {self.test_cases_counter}")
        
        # Return True if all tests passed
        return self.common_neighbors_bugs == 0 and self.preferential_attachment_bugs == 0

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Create test instance and run tests
    tester = TestLinkPredictionOracles()
    all_passed = tester.run_tests(100)
    if all_passed:
        print("All tests passed successfully!")
    else:
        print("Found test failures.")