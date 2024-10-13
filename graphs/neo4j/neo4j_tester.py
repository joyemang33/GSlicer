from graphs.neo4j.client import Neo4jClient
from graphs.neo4j.graph import neo4j_load_graph
from graphs.basic_graph.gen import BasicGenerator

class Neo4jTester:
    def __init__(self):
        self.client = Neo4jClient()
        self.gds = self.client.gds
        self.basic_generator = BasicGenerator()
        self.load = neo4j_load_graph