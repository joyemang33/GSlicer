# The main file that produce the query statements
import random
import copy
from databases.neo4j.generator.pattern_clause import PatternGenerator
from databases.neo4j.generator.schema import GraphSchema

class QueryGenerator:
    def __init__(self, output_file="test_case_1"):
        self.G = GraphSchema()
        self.G.gen(output_file = "./databases/neo4j/generator/output_files/" + output_file)
        self.pattern_generator = None

    def gen_match(self):
        if self.generated_match == True and random.randint(1, 3) > 1:
            res = "OPTIONAL MATCH "
        else:
            res = "MATCH "
            self.generated_match = True
        
        pattern1 = self.pattern_generator.gen_pattern()
        return res + pattern1
    
    def gen_where_predicate(self):
        res = "WHERE "
        predicate = self.pattern_generator.where_generator.gen_exp()
        return res + predicate
    
    def gen_where_pattern(self):
        res = "WHERE "
        pattern1 = self.pattern_generator.gen_path(no_new_variables = True, only_path = True)
        return res + pattern1
    
    def gen_where_exists_pattern(self):
        res = "WHERE EXISTS {"
        pattern1 = self.pattern_generator.gen_pattern(no_new_variables = True)
        return res + pattern1 + " }"
    
    def gen_return(self):
        if random.randint(1, 2) == 1: return "RETURN *"
        else:
            pattern1 = self.pattern_generator.gen_pattern(no_new_variables = True)
            res = "UNWIND COUNT { "
            return res + pattern1 + " } AS cnt1 RETURN *"
    
    def gen_query(self):        
        self.pattern_generator = PatternGenerator(self.G)
        self.generated_match = False

        query1, query2, last_funcs = "", "", None
        num = random.randint(1, 5)
        for _ in range(0, num):
            if last_funcs != self.gen_match:
                clause1 = self.gen_match()
                query1 += clause1 + " "
                last_funcs = self.gen_match
            else:
                funcs = [self.gen_match, self.gen_where_predicate, 
                        self.gen_where_exists_pattern, self.gen_where_pattern]
                random_funcs = random.choice(funcs)
                clause1 = random_funcs()
                query1 += clause1 + " "
                last_funcs = random_funcs

        clause1 = self.gen_return()
        return query1 + clause1

if __name__ == "__main__":
    query_generator = QueryGenerator()
    for _ in range(10):
        print(query_generator.gen_query())
