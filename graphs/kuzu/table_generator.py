import random
import string
import numpy as np

class GraphType:
    def __init__(self, _name : str): 
        self.name = _name
    def gen_value_in_str(self):
        '''
        generate a random value in a string format based on the type name.
        e.g., self.name = "int" -> return "123" instead of 123.
        '''
        if self.name not in ["INT64", "DOUBLE", "BOOLEAN", "STRING"]:
            raise Exception("Invalid type name when generating constant value")
        if self.name == "INT64":
            return str(random.randint(-(2 ** 63), (2 ** 63) - 1))
        if self.name == "DOUBLE":
            value = random.random() * random.randint(-(2 ** 63), (2 ** 63) - 1)
            return format(value, '.20f')
        if self.name == "BOOLEAN":
            return "true" if random.randint(0, 1) == 1 else "false"
        if self.name == "STRING":
            length = random.randint(1, 20)
            ran = ''.join(random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))
            return "'" + ran + "'"

class GraphProperty:
    def __init__(self, _name : str, _type : str):
        self.name = _name
        self.type = GraphType(_type)

class NodeLabel:
    def __init__(self, _name : str, _properties):
        self.name = _name
        self.properties = _properties
        self.nodes = []

class EdgeLabel:
    def __init__(self, _name : str, _source : str, _target : str, _properties):
        self.name, self.source, self.target = _name, _source, _target
        self.properties = _properties
        self.edges = []

class TableSchema:
    def __init__(self, _no_properties : int, _no_node_labels : int, _no_edge_labels : int):
        self.no_properties = _no_properties
        self.no_node_labels = _no_node_labels
        self.no_edge_labels = _no_edge_labels
        self.properties = [
            GraphProperty(_name = f"p{i}", 
                _type = random.choice(["INT64", "DOUBLE", "BOOLEAN", "STRING"]))
            for i in range(0, _no_properties)
        ]
        type_of_id = GraphProperty("id", "INT64")
        self.node_labels = [
            NodeLabel(_name = f"L{i}", _properties = [type_of_id] + list(np.random.choice(
                self.properties, size=random.randint(_no_properties, _no_properties), replace=False
            ))) for i in range(0, _no_node_labels)
        ]
        self.edge_labels = [
            EdgeLabel(_name = f"T{i}", _source = random.choice(self.node_labels).name,
                _target = np.random.choice(self.node_labels).name,
                _properties = [type_of_id] + list(np.random.choice(
                self.properties, size=random.randint(_no_properties, _no_properties), replace=False
            ))) for i in range(0, _no_edge_labels)
        ]

    # T = TableShema(_no_properties = 10, _no_node_labels = 5, _no_edge_labels = 5)
