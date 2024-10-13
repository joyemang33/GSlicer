import pandas as pd
import numpy as np
from graphs.neo4j.client import Neo4jClient


if __name__ == "__main__":
    nodes = pd.DataFrame(
        {
            "nodeId" : [0, 1, 2],
            "labels" : ["city", "city", "city"],
        }
    )

    relationships = pd.DataFrame(
        {
            "sourceNodeId" : [0, 1, 2, 1],
            "targetNodeId" : [1, 2, 3, 3],
            "relationshipType" : ["road", "road", "road", "road"],
            "cost" : [1, np.inf, -np.inf, np.nan]
        }
    )
    

    client = Neo4jClient()
    gds = client.gds
    try: 
        gds.graph.drop(gds.graph.get('test'), False)
    except:
        pass
    G = gds.graph.construct(
        graph_name="test",      
        nodes=nodes,           
        relationships=relationships,
        undirected_relationship_types=["road", "road"]
    )
    print(gds.beta.spanningTree.stream(G,
    sourceNode=0,
    relationshipWeightProperty='cost'
    ))
    # print(edges.loc[:, ["sourceNodeId", "targetNodeId"]].drop_duplicates())