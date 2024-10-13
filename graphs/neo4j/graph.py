import pandas
import random
import numpy as np
from graphs.neo4j.client import Neo4jClient
from graphs.basic_graph.schema import *
from graphs.neo4j.constant import Neo4jConstant
from graphs.basic_graph.gen import BasicGenerator

def neo4j_load_graph(G : BasicGraph, partition_arr,
    is_directed = True,
    num_of_nodeLabels = 5,
    num_of_relLabels = 5,
    num_of_properties = 5):

    client = Neo4jClient()
    gds = client.gds
    try: 
        gds.graph.drop(gds.graph.get('G'), False)
    except:
        pass

    try:
        gds.graph.drop(gds.graph.get('G0'), False)
    except:
        pass

    try:
        gds.graph.drop(gds.graph.get('G1'), False)
    except:
        pass
    
    Cons = Neo4jConstant()

    nodeLabels = ["L" + str(i) for i in range(0, num_of_nodeLabels)]
    relLabels = ["T" + str(i) for i in range(0, num_of_relLabels)]
    properties = [["p" + str(i), Cons.gen_type()] for i in range(0, num_of_properties)]
    e_properties = [["q" + str(i), Cons.gen_type()] for i in range(0, num_of_properties)]


    G_nodes = dict()
    G_nodes["nodeId"] = list(range(0, G.n))
    G_nodes["labels"] = [random.choice(nodeLabels) for _ in range(0, G.n)]
    for prop in properties:
        G_nodes[prop[0]] = [
            np.nan if random.randint(1, 4) == 4 
            else Cons.gen_constant(prop[1])
            for _ in range(0, G.n)
        ]
    
    G_edges = dict()
    G_edges["sourceNodeId"] = [G.edges[i].node_x for i in range(0, G.m)]
    G_edges["targetNodeId"] = [G.edges[i].node_y for i in range(0, G.m)]
    G_edges["relationshipType"] = [random.choice(relLabels) for _ in range(0, G.m)]
    G_edges["edgeId"] = list(range(0, G.m))
    for prop in e_properties:
        G_edges[prop[0]] = [
            np.nan if random.randint(1, 4) == 4 
            else Cons.gen_constant(prop[1])
            for _ in range(0, G.m)
        ]

    Neo4j_G = gds.graph.construct(
        graph_name="G",      
        nodes=pandas.DataFrame(G_nodes),           
        relationships=pandas.DataFrame(G_edges),
        undirected_relationship_types=(None if is_directed else relLabels)  
    )
    
    subG_nodes = [dict(), dict()]
    subG_edges = [dict(), dict()]
    for id in range(0, 2):
        subG_nodes[id]["nodeId"] = []
        subG_nodes[id]["labels"] = []
        for prop in properties:
            subG_nodes[id][prop[0]] = []
        for i in range(0, G.n):
            if partition_arr[i] == id:
                subG_nodes[id]["nodeId"].append(i)
                subG_nodes[id]["labels"].append(G_nodes["labels"][i])
                for prop in properties:
                    subG_nodes[id][prop[0]].append(G_nodes[prop[0]][i]) 

        subG_edges[id]["sourceNodeId"] = []
        subG_edges[id]["targetNodeId"] = []
        subG_edges[id]["relationshipType"] = []
        subG_edges[id]["edgeId"] = []
        for prop in e_properties:
            subG_edges[id][prop[0]] = []
        for i in range(0, G.m):
            if partition_arr[G.edges[i].node_x] == id and partition_arr[G.edges[i].node_y] == id:
                subG_edges[id]["edgeId"].append(i)
                subG_edges[id]["sourceNodeId"].append(G.edges[i].node_x)
                subG_edges[id]["targetNodeId"].append(G.edges[i].node_y)
                subG_edges[id]["relationshipType"].append(G_edges["relationshipType"][i])
                for prop in e_properties:
                    subG_edges[id][prop[0]].append(G_edges[prop[0]][i])

    Neo4j_G0 = gds.graph.construct(
        graph_name="G0",      
        nodes=pandas.DataFrame(subG_nodes[0]),           
        relationships=pandas.DataFrame(subG_edges[0]),
        undirected_relationship_types=(None if is_directed else relLabels)  
    )


    Neo4j_G1 = gds.graph.construct(
        graph_name="G1",      
        nodes=pandas.DataFrame(subG_nodes[1]),           
        relationships=pandas.DataFrame(subG_edges[1]),
        undirected_relationship_types=(None if is_directed else relLabels)  
    )

    return Neo4j_G, Neo4j_G0, Neo4j_G1, G_nodes, G_edges, \
        subG_nodes[0], subG_edges[0], subG_nodes[1], subG_edges[1]

if __name__ == "__main__":
    basic_generator = BasicGenerator()
    basic_G, partition_arr = basic_generator.gen(6, 10)
    G, G0, G1 = neo4j_load_graph(basic_G, partition_arr)
    print("OK")


