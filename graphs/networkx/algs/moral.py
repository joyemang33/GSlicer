import random
import networkx as nx
from itertools import combinations
import time

class TestNetworkxMoralGraph:
    def __init__(self):
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0
        self.max_nodes = 100  # Smaller than bridge test because moral graphs are denser
        self.max_edges = 500
    
    def create_test_case(self, n, m):
        """Create a random directed graph and its partition for testing"""
        # Generate a random directed graph
        self.G = nx.gnm_random_graph(n, m, directed=True)
        
        # Ensure the graph has no isolated nodes (for meaningful moral graph test)
        for node in list(self.G.nodes()):
            if self.G.degree(node) == 0:
                target = random.choice([v for v in self.G.nodes() if v != node])
                self.G.add_edge(node, target) if random.random() < 0.5 else self.G.add_edge(target, node)
        
        # Randomly partition nodes into two groups
        all_nodes = list(self.G.nodes())
        random.shuffle(all_nodes)
        split_point = random.randint(1, len(all_nodes)-1)  # Ensure both partitions have at least one node
        
        self.partition_V1 = set(all_nodes[:split_point])
        self.partition_V2 = set(all_nodes[split_point:])
        
        # Create the two subgraphs
        self.G1 = self.G.subgraph(self.partition_V1).copy()
        self.G2 = self.G.subgraph(self.partition_V2).copy()
    
    def moral_graph_oracle(self, H, H1, H2):
        """Validates the moral graph property with respect to graph partitioning.
        
        The oracle checks if: H1 ∪ H2 ⊂ H
        Where:
        - H is the moral graph of G
        - H1 is the moral graph of G[V1]
        - H2 is the moral graph of G[V2]
        """
        # Create H1 ∪ H2
        H_union = nx.Graph()
        H_union.add_nodes_from(self.G.nodes())
        H_union.add_edges_from(H1.edges())
        H_union.add_edges_from(H2.edges())
        
        # Check if H1 ∪ H2 is a subset of H
        H_edges = set(H.edges())
        H_union_edges = set(H_union.edges())
        
        if not H_union_edges.issubset(H_edges):
            extra_edges = H_union_edges - H_edges
            error_msg = f"Edges in H1 ∪ H2 but not in H: {extra_edges}\n"
            return False, error_msg
        
        return True, ""

    def validate(self):
        """Validate the moral graph algorithm"""
        self.test_cases_counter += 1
        
        # Compute moral graphs
        try:
            H = nx.moral_graph(self.G)
            H1 = nx.moral_graph(self.G1)
            H2 = nx.moral_graph(self.G2)
        except Exception as e:
            print(f"Error computing moral graphs: {e}")
            return False
        
        # Check if the moral graph oracle relation holds
        result, error_msg = self.moral_graph_oracle(H, H1, H2)
        
        if not result:
            self.bugs_cases_counter += 1
            print(f"Test case {self.test_cases_counter} failed:")
            print(error_msg)
            print(f"Directed Graph G: {self.G.edges()}")
            print(f"Partition V1: {self.partition_V1}")
            print(f"Partition V2: {self.partition_V2}")
            print(f"Moral Graph H edges: {list(H.edges())}")
            print(f"Moral Graph H1 edges: {list(H1.edges())}")
            print(f"Moral Graph H2 edges: {list(H2.edges())}")
            return False
        
        return True
    
    def test(self):
        """Run a single test case"""
        try:
            _n = random.randint(5, self.max_nodes)  # At least 5 nodes for meaningful tests
            _m = random.randint(_n, min(self.max_edges, _n*(_n-1)))  # Ensure m is valid for directed graphs
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
    random.seed(time.time())
    tester = TestNetworkxMoralGraph()
    all_passed = tester.run_tests(100)
    
    if all_passed:
        print("All tests passed successfully!")
    else:
        print(f"Found {tester.bugs_cases_counter} test failures.")