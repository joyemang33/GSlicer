import random
from graphs.kuzu.graph_generator import *
from graphs.kuzu.pattern_generator import PatternGenerator

class QueryGenerator:
    def __init__(self, G : GraphData):
        '''
        max_clauses_num : maxinum of clauses for a query
        '''
        self.G = G
        self.max_clauses_num = 2
        
    def gen_basic_query(self):
        '''
        generate a query that only contains MATCH / OPTIONAL MATCH
        '''
        #Reset the pattern generator
        PG = PatternGenerator(self.G)
        clauses_num = random.randint(1, self.max_clauses_num)
        query = ""
        
        for i in range(0, clauses_num):
            #The first clause must be MATCH
            clause = "MATCH" if i == 0 else random.choice([" MATCH", " OPTIONAL MATCH", "WHERE"])
            if clause == "WHERE":
                query = query + clause + " " + PG.predicate_generator.gen_exp()
            else:
                query = query + clause + " " + PG.gen_pattern(existed = (i > 0))            
                if clause == "OPTIONAL MATCH":
                    #OPTIONAL MATCH must be followed by a WITH *
                    query = query + " WITH *"
        
        return query

if __name__ == "__main__":
    G = GraphData(_no_properties = 10, _no_node_labels = 5, _no_edge_labels = 5, _no_nodes = 5, _no_edges = 10)
    QG = QueryGenerator(G)
    