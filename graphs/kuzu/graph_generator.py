import random
import json
from graphs.kuzu.table_generator import *
from graphs.kuzu.client import KuzuClient

class Node:
    def __init__(self, _id : int, _label : NodeLabel):
        self.id = _id
        self.name = f"n{_id}"
        self.label = _label
        self.properties = {}
        for prop in self.label.properties:
            if prop.name == "id": self.properties[prop.name] = self.id
            else:
                if random.random() < 0.1: continue 
                # 0.1 probability setting NULL
                self.properties[prop.name] = prop.type.gen_value_in_str()

class Edge:
    def __init__(self, _id : int, _source : int, _target : int, _label : EdgeLabel):
        self.id = _id
        self.name = f"r{_id}"
        self.source = _source
        self.target = _target
        self.label = _label
        self.properties = {}
        for prop in self.label.properties:
            if prop.name == "id": self.properties[prop.name] = self.id
            else:
                if random.random() < 0.1: continue 
                # 0.1 probability setting NULL
                self.properties[prop.name] = prop.type.gen_value_in_str()

class GraphData(TableSchema):
    def __init__(self, _no_properties : int, _no_node_labels : int, _no_edge_labels : int,
                 _no_nodes : int, _no_edges : int):
        '''
        Randomly initialize the graph schema with (_no_properties) properties,
        ( _no_node_labels) labels for nodes, (_no_edge_labels) labels for edges,
        generating (_no_nodes) nodes and (_no_edges) edge in the schema.
        '''

        #checking validity
        if(_no_nodes < _no_node_labels):
            raise(Exception("Number of nodes must no less than the number of labels"))
        if(_no_nodes < _no_edge_labels):
            raise(Exception("Number of edges must no less than the number of labels"))

        TableSchema.__init__(self, _no_properties, _no_node_labels, _no_edge_labels)
        self.no_nodes = _no_nodes
        self.no_edges = _no_edges
        self.nodes, self.edges = [], []

        #Generating node entities
        #1. ensure having at least one nodes for each label.
        self.nodes_by_label = {}
        for i in range(0, self.no_node_labels):
            label = self.node_labels[i]
            node = Node(i, label)
            self.nodes_by_label[label.name] = [node]
            self.nodes.append(node)

        #2. Fill the remaining nodes
        for i in range(self.no_node_labels, self.no_nodes):
            label = random.choice(self.node_labels)
            node = Node(i, label)
            self.nodes_by_label[label.name] = [node]
            self.nodes.append(node)
        
        #Generating edge entities
        for i in range(0, self.no_edges):
            label = random.choice(self.edge_labels)
            source_label = label.source
            target_label = label.target
            source = random.choice(self.nodes_by_label[source_label])
            target = random.choice(self.nodes_by_label[target_label])
            edge = Edge(i, source.id, target.id, label)
            self.edges.append(edge)
    
    def init_from_table(self, _no_nodes : int, _no_edges : int, offset = 0):
        self.no_nodes = _no_nodes
        self.no_edges = _no_edges
        self.nodes, self.edges = [], []

        #Generating node entities
        #1. ensure having at least one nodes for each label.
        self.nodes_by_label = {}
        for i in range(0, self.no_node_labels):
            label = self.node_labels[i]
            node = Node(i + offset, label)
            self.nodes_by_label[label.name] = [node]
            self.nodes.append(node)

        #2. Fill the remaining nodes
        for i in range(self.no_node_labels, self.no_nodes):
            label = random.choice(self.node_labels)
            node = Node(i + offset, label)
            self.nodes_by_label[label.name] = [node]
            self.nodes.append(node)
        
        #Generating edge entities
        for i in range(0, self.no_edges):
            label = random.choice(self.edge_labels)
            source_label = label.source
            target_label = label.target
            source = random.choice(self.nodes_by_label[source_label])
            target = random.choice(self.nodes_by_label[target_label])
            edge = Edge(i, source.id, target.id, label)
            self.edges.append(edge)
    
    def export(self, database : KuzuClient, log_file = None):
        '''
        Exporting the graph data to the database.
        Need the database is empty before the export, otherwise will lead to failures.
        '''
        stmts = []
        
        #1. Define Node Table
        for label in self.node_labels:
            stmt = f"CREATE NODE TABLE {label.name}("
            for prop in label.properties:
                stmt += f"{prop.name} {prop.type.name}"
                stmt += ", "
            stmt += f"PRIMARY KEY(id))"
            stmts.append(stmt)
            database.run(stmt)
            
        #2. Define REL Table
        for label in self.edge_labels:
            stmt = f"CREATE REL TABLE {label.name}(FROM {label.source} TO {label.target}, "
            for prop in label.properties:
                stmt += f"{prop.name} {prop.type.name}"
                stmt += ", "
            stmt = stmt.rstrip(", ") + ")"
            stmts.append(stmt)
            database.run(stmt)
        
        #3. Creates Nodes
        for node in self.nodes:
            stmt = f"CREATE (n:{node.label.name} " + "{"
            for prop in node.properties.items():
                stmt += f"{prop[0]}: {prop[1]}"
                stmt += ", "
            stmt = stmt.rstrip(", ") + "})"
            stmts.append(stmt)
            database.run(stmt)

        #4. Create Relationships
        for edge in self.edges:
            stmt = f"MATCH (n1:{edge.label.source}), (n2:{edge.label.target}) WHERE n1.id = {edge.source} AND n2.id = {edge.target} CREATE (n1)-[:{edge.label.name} " + "{"
            for prop in edge.properties.items():
                stmt += f"{prop[0]}: {prop[1]}"
                stmt += ", "
            stmt = stmt.rstrip(", ") + "}]->(n2)"
            stmts.append(stmt)
            database.run(stmt)

        if log_file != None:
            with open(log_file, "w", encoding = "utf-8") as f:
                json.dump(stmts, f)
            


if __name__ == "__main__":
    #unit test
    G = GraphData(_no_properties = 10, _no_node_labels = 5, _no_edge_labels = 5, _no_nodes = 5, _no_edges = 10)
    client = KuzuClient()
    G.export(client)

