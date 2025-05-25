import random
import networkx as nx
from networkx.algorithms.richclub import rich_club_coefficient

class RichClubOracle:
    def __init__(self):
        self.test_cases_counter = 0
        self.bugs_cases_counter = 0
        self.max_nodes = 50
        self.max_edges = 200
        self.eps = 1e-10  
    
    def create_test_case(self, n, m):
        self.G = nx.gnm_random_graph(n, m)
        
        self.G.remove_edges_from(nx.selfloop_edges(self.G))
        
        all_nodes = list(self.G.nodes())
        random.shuffle(all_nodes)
        split_point = random.randint(1, len(all_nodes)-1) if len(all_nodes) > 1 else 1
        
        self.partition_V1 = set(all_nodes[:split_point])
        self.partition_V2 = set(all_nodes[split_point:])
        
        self.G1 = self.G.subgraph(self.partition_V1).copy()
        self.G2 = self.G.subgraph(self.partition_V2).copy()
    
    def compute_rich_club_details(self, G):
        """使用NetworkX的rich_club_coefficient计算富人俱乐部系数"""
        if G.number_of_edges() == 0 or G.number_of_nodes() < 2:
            return {}, {}
        
        try:
            rc = rich_club_coefficient(G, normalized=False)
            
            deghist = nx.degree_histogram(G)
            total = sum(deghist)
            
            denominator = {}
            for k in rc.keys():
                nk = sum(deghist[k+1:]) 
                denominator[k] = nk * (nk - 1)
            
            return rc, denominator
            
        except nx.NetworkXError:
            return {}, {}
    
    def validate_oracle(self):
        rc_G, denom_G = self.compute_rich_club_details(self.G)
        rc_G1, denom_G1 = self.compute_rich_club_details(self.G1)
        rc_G2, denom_G2 = self.compute_rich_club_details(self.G2)
        
        if not rc_G:  
            return True, {}
        
        for k in rc_G.keys():
            g1_contribution = 0
            if k in rc_G1 and denom_G1.get(k, 0) > 0:
                g1_contribution = rc_G1[k] * denom_G1[k]
            
            g2_contribution = 0
            if k in rc_G2 and denom_G2.get(k, 0) > 0:
                g2_contribution = rc_G2[k] * denom_G2[k]
            
            g_total = rc_G[k] * denom_G[k]
            
            sum_contributions = g1_contribution + g2_contribution
            
            if sum_contributions > g_total + self.eps:
                return False, {
                    "degree": k,
                    "G_rc": rc_G[k],
                    "G_denom": denom_G[k],
                    "G_total": g_total,
                    "G1_rc": rc_G1.get(k, 0),
                    "G1_denom": denom_G1.get(k, 0),
                    "G1_contribution": g1_contribution,
                    "G2_rc": rc_G2.get(k, 0),
                    "G2_denom": denom_G2.get(k, 0),
                    "G2_contribution": g2_contribution,
                    "sum_contributions": sum_contributions,
                    "difference": sum_contributions - g_total
                }
        
        return True, {}
    
    def test(self):
        self.test_cases_counter += 1
        
        try:
            _n = random.randint(10, self.max_nodes)
            _m = random.randint(_n, min(self.max_edges, _n*(_n-1)//2))
            self.create_test_case(n=_n, m=_m)
        except Exception as e:
            print(f"Error creating test case: {e}")
            return
        
        result, details = self.validate_oracle()
        
        if not result:
            self.bugs_cases_counter += 1
            print(f"Test case {self.test_cases_counter} failed:")
            print(f"Graph G: {len(self.G.nodes())} nodes, {len(self.G.edges())} edges")
            print(f"Graph G1: {len(self.G1.nodes())} nodes, {len(self.G1.edges())} edges")
            print(f"Graph G2: {len(self.G2.nodes())} nodes, {len(self.G2.edges())} edges")
            print(f"Details: {details}")
    
    def run_tests(self, num_tests=100):
        for i in range(num_tests):
            if i % 10 == 0:
                print(f"Running test {i}/{num_tests}")
            self.test()
        
        print(f"Bug-triggering tests/all tests = {self.bugs_cases_counter} / {self.test_cases_counter}")
        if self.bugs_cases_counter == 0:
            print("All tests passed successfully!")
        else:
            print(f"Found {self.bugs_cases_counter} test failures.")

if __name__ == "__main__":
    random.seed(42)  
    oracle_tester = RichClubOracle()
    oracle_tester.run_tests(1000)