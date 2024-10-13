from databases.neo4j.client import Neo4jClient
from databases.neo4j.oracle import *
from databases.neo4j.generator.query_generator import QueryGenerator

class Neo4jTester:
    def __init__(self):
        self.session_G = Neo4jClient(database="datag")
        self.session_G0 = Neo4jClient(database="datag0")
        self.session_G1 = Neo4jClient(database="datag1")
        self.validator = BasicValidator(node_num=30)

    def clear(self):
        self.session_G.clear()
        self.session_G0.clear()
        self.session_G1.clear()
    
    def test(self, test_cases_name : str, query_num : int):
        self.clear()
        QG = QueryGenerator(output_file=test_cases_name)

        for session, suffix in [(self.session_G, "-G"), (self.session_G0, "-G0"), (self.session_G1, "-G1")]:
            with open("./databases/neo4j/generator/output_files/" + test_cases_name + suffix, 'r') as f:
                content = f.read().strip().split('\n')
                for line in content:
                    session.run(line)

        print("Successfully Create Data")

        for _ in range(0, query_num):
            query = QG.gen_query()
            print(query)
            try:
                res, ti = self.session_G.run(query)
                res0, ti0 = self.session_G0.run(query)
                res1, ti1 = self.session_G1.run(query)
            except:
                continue
                
            print(res, ti, res0, ti0, res1, ti1)
            if self.validator.validate(res, ti, res0, ti0, res1, ti1) == False:
                print("Query: " + query)
                print("")

if __name__ == "__main__":
    session = Neo4jTester()
    for _ in range(0, 100):
        session.test("test", 1000)


