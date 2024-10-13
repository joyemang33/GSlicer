import json
from graphs.kuzu.client import KuzuClient

def load_graph(file_name, name = ""):
    with open(file_name, "r", encoding = "utf-8") as f:
        stmts = json.load(f)
    
    client = KuzuClient(name = f"./graphs/kuzu/data/reproducee{name}")
    for s in stmts: client.run(s) 
    return client
    