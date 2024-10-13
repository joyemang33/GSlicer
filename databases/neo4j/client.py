from configs.conf import *
from neo4j import GraphDatabase, basic_auth

class Neo4jClient:
    def __init__(self, uri = config.get("neo4j", "uri"), 
        username = config.get("neo4j", "username"), 
        password = config.get("neo4j", "password"), 
        database = "neo4j",
        ):
        self.database = database
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(username, password))
        self.session = self.driver.session(database=database)
    
    def clear(self):
        self.run("MATCH (n) DETACH DELETE n")

    def run(self, query: str):
        result = self.session.run(query)
        di = result.data()
        res = result.consume()
        t1 = res.result_available_after
        return di, t1

