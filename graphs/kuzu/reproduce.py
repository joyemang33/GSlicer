import json
from graphs.kuzu.load_graph import load_graph
from graphs.kuzu.client import KuzuClient

# "MATCH (MnCHDRXXsJPTLnI)<-[:T3|:T5|:T1|:T2]-(MnCHDRXXsJPTLnI)-[ZFRWwelI67iuBuZW:T6|:T2|:T5|:T1|:T4|:T3|:T0]->(MnCHDRXXsJPTLnI)-[:T2|:T3|:T4|:T1*..13]->(MnCHDRXXsJPTLnI), (MnCHDRXXsJPTLnI)-[VrgoGdGco2Y:T1|:T2|:T3|:T5|:T6]-(NGkzA) MATCH (MnCHDRXXsJPTLnI), (MnCHDRXXsJPTLnI)<-[BLcN:T5|:T2|:T0]-(MnCHDRXXsJPTLnI)<-[:T3|:T0|:T2|:T6|:T5|:T4*11..]-(NGkzA), (MnCHDRXXsJPTLnI)RETURN COUNT (*)"

def reproduce(query_file, graph_id, is_exist = False):
    if not is_exist:
        G = load_graph(f"./graphs/kuzu/logs/G_{graph_id}.json")
        G1 = load_graph(f"./graphs/kuzu/logs/G1_{graph_id}.json", 1)
        G2 =  load_graph(f"./graphs/kuzu/logs/G2_{graph_id}.json", 2)
    else:
        pass
    
    with open(query_file, "r", encoding="utf-8") as f:
        queries = json.load(f)
    G.run("CALL timeout = 5000;")
    G1.run("CALL timeout = 5000;")
    G2.run("CALL timeout = 5000;")
    print(G.run("CALL db_version() RETURN version").get_as_df())
    for query in queries:
        G.run(query)
    
if __name__ == "__main__":
    reproduce("./graphs/kuzu/data/kuzu_logic_28.json", 47)
