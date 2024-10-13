import pandas as pd
from graphs.neo4j.client import Neo4jClient


if __name__ == "__main__":
    nodes = pd.read_csv('./graphs/neo4j/algorithms/triangle_counting/bugs/tmp/G_node.csv')
    edges = pd.read_csv('./graphs/neo4j/algorithms/triangle_counting/bugs/tmp/G_edge.csv')
    client = Neo4jClient()
    gds = client.gds
    try: 
        gds.graph.drop(gds.graph.get('test'), False)
    except:
        pass

    G = gds.graph.construct(
        graph_name="test",      
        nodes=nodes,           
        relationships=edges,
        undirected_relationship_types= ["T0", "T1", "T2", "T3", "T4"]  
    )
    print(gds.alpha.triangles(G))
    # print(edges.loc[:, ["sourceNodeId", "targetNodeId"]].drop_duplicates())
    # 8
    # 
    