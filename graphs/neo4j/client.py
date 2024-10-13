from configs.conf import *
from graphdatascience import GraphDataScience

class Neo4jClient:
    def __init__(self, uri = config.get("neo4j", "uri"), 
        username = config.get("neo4j", "username"), 
        password = config.get("neo4j", "password"), 
        db_session = "neo4j",
        ):

        self.gds = GraphDataScience(
            uri, 
            auth = (username, password),
            database = db_session
        )

    def run(self, stmt : str):
        result = self.gds.run_cypher(stmt)
        return result

    def clear(self):
        self.run(
            stmt = "MATCH (n) DETACH DELETE n"
        )

if __name__ == "__main__":
    Neo4j = Neo4jClient()
    print(Neo4j.gds.version())
