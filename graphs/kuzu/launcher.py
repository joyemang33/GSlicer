import os
import sys
import time
import json
import random
import pandas as pd
from graphs.kuzu.client import KuzuClient
from graphs.kuzu.graph_generator import GraphData
from graphs.kuzu.graph_partitioner import *
from graphs.kuzu.query_generator import QueryGenerator

def test_count_star(max_iteration = 100, id = 0):
    #generate the graph data
    G = GraphData(_no_properties = random.randint(1, 100), _no_node_labels = random.randint(1, 5), \
        _no_edge_labels = random.randint(1, 5), \
        _no_nodes = random.randint(2, 10), _no_edges = random.randint(0, 30))
    
    G1, G2, cuts = partition(G)
    client_G = KuzuClient(f"./graphs/kuzu/data/G_{id}")
    client_G1 = KuzuClient(f"./graphs/kuzu/data/G1_{id}")
    client_G2 = KuzuClient(f"./graphs/kuzu/data/G2_{id}")
    
    #import the GraphData to the database
    G.export(client_G, f"./graphs/kuzu/logs/G_{id}.json")
    G1.export(client_G1, f"./graphs/kuzu/logs/G1_{id}.json")
    G2.export(client_G2, f"./graphs/kuzu/logs/G2_{id}.json")
    print(client_G.run("CALL db_version() RETURN version").get_as_df())
    
    QG = QueryGenerator(G)
    
    client_G.run("CALL timeout = 1000;")
    client_G1.run("CALL timeout = 1000;")
    client_G2.run("CALL timeout = 1000;")
    
    #run testing
    non_binder = 0
    buggy_queries = []
    exceptions = []
    
    print("Running ...")
    for i in range(1, max_iteration + 1):
        
        print(f"Executed {i} test cases: {non_binder} not be binded.")
        query = QG.gen_basic_query()
        query = query + "RETURN COUNT (*)"
        print(query)
        try: res_G = client_G.run(query).get_as_df().values.tolist()[0][0]
        except Exception as e:
            msg = str(e)
            print(e)
            if "Parser exception" not in msg and "Binder exception" not in msg and "Interrupted" not in msg:
                exceptions.append((query, msg))        
            continue
        try: res_G1 = client_G1.run(query).get_as_df().values.tolist()[0][0]
        except Exception as e:
            if "Parser exception" not in msg and "Binder exception" not in msg and "Interrupted" not in msg:
                exceptions.append((query, msg))   
            continue
        try: res_G2 = client_G2.run(query).get_as_df().values.tolist()[0][0]
        except Exception as e:
            if "Parser exception" not in msg and "Binder exception" not in msg and "Interrupted" not in msg:
                exceptions.append((query, msg))   
            continue
        if res_G < res_G1 + res_G2:
            buggy_queries.append(query)
            
        non_binder += 1
        
        if len(buggy_queries) > 0:
            with open(f"./graphs/kuzu/data/kuzu_logic_{id}.json", "w", encoding="utf-8") as f:
                json.dump(buggy_queries, f)
    
        if len(exceptions) > 0:
            with open(f"./graphs/kuzu/data/kuzu_exception_{id}.json", "w", encoding="utf-8") as f:
                json.dump(exceptions, f)
    
    # print(Hello)
    
def test_count_star_2CC(max_iteration = 100, id = 0):
    #generate the graph data
    no_label = random.randint(1, 10)
    G = GraphData(_no_properties = random.randint(1, 100), _no_node_labels = no_label, \
        _no_edge_labels = random.randint(1, 10), \
        _no_nodes = random.randint(no_label, 50), _no_edges = random.randint(0, 100))
    
    G, G1, G2 = partition_2CC(G)
    client_G = KuzuClient(f"./graphs/kuzu/data/G_{id}")
    client_G1 = KuzuClient(f"./graphs/kuzu/data/G1_{id}")
    client_G2 = KuzuClient(f"./graphs/kuzu/data/G2_{id}")
    
    #import the GraphData to the database
    G.export(client_G, f"./graphs/kuzu/logs/G_{id}.json")
    G1.export(client_G1, f"./graphs/kuzu/logs/G1_{id}.json")
    G2.export(client_G2, f"./graphs/kuzu/logs/G2_{id}.json")
    print(client_G.run("CALL db_version() RETURN version").get_as_df())

    
    QG = QueryGenerator(G)
    
    client_G.run("CALL timeout = 1000;")
    client_G1.run("CALL timeout = 1000;")
    client_G2.run("CALL timeout = 1000;")
    
    print(client_G.run("CALL db_version() RETURN version").get_as_df())
    
    #run testing
    non_binder = 0
    buggy_queries = []
    exceptions = []
    
    print("Running ...")
    for i in range(1, max_iteration + 1):
        
        print(f"Executed {i} test cases: {non_binder} not be binded.")
        query = QG.gen_basic_query()
        query = query + "RETURN COUNT (*)"
        print(query)
        try: res_G = client_G.run(query).get_as_df().values.tolist()[0][0]
        except Exception as e:
            msg = str(e)
            print(e)
            if "Parser exception" not in msg and "Binder exception" not in msg and "Interrupted" not in msg:
                exceptions.append((query, msg))        
            continue
        try: res_G1 = client_G1.run(query).get_as_df().values.tolist()[0][0]
        except Exception as e:
            if "Parser exception" not in msg and "Binder exception" not in msg and "Interrupted" not in msg:
                exceptions.append((query, msg))   
            continue
        try: res_G2 = client_G2.run(query).get_as_df().values.tolist()[0][0]
        except Exception as e:
            if "Parser exception" not in msg and "Binder exception" not in msg and "Interrupted" not in msg:
                exceptions.append((query, msg))   
            continue
        print(res_G, res_G1, res_G2)
        if res_G != res_G1 + res_G2:
            buggy_queries.append(query)
            
        non_binder += 1
        
        if len(buggy_queries) > 0:
            with open(f"./graphs/kuzu/data/kuzu_logic_{id}.json", "w", encoding="utf-8") as f:
                json.dump(buggy_queries, f)
    
        if len(exceptions) > 0:
            with open(f"./graphs/kuzu/data/kuzu_exception_{id}.json", "w", encoding="utf-8") as f:
                json.dump(exceptions, f)
    
    # print(Hello)

def reproduce():
    with open("./graphs/kuzu/data/kuzu_logic_1.json") as f:
        L = json.load(f)
        print(L)
   
    print(query)
    client.run(query)



if __name__ == "__main__":
    # reproduce()
    # reproduce("MATCH (n) WHERE n.p IS NULL RETURN COUNT(*)")
    graph_id = int(sys.argv[1])
    for i in range(graph_id, graph_id + 1):
        if graph_id % 2 == 0:
            try: test_count_star_2CC(id = i)
            except: pass
        else:
            try: test_count_star(id = i)
            except: pass
    # no_label = 10
    # G = GraphData(_no_properties = random.randint(1, 100), _no_node_labels = no_label, \
    #     _no_edge_labels = random.randint(1, 10), \
    #     _no_nodes = random.randint(no_label, 50), _no_edges = random.randint(0, 100))
    # client = KuzuClient(f"/home/mqy/GraphGenie/GraphGenie0923")
    # G.export(client, f"./graphs/kuzu/logs/GraphGenie0923.json")
    # print([x.name for x in G.node_labels])
    # print([x.name for x in G.edge_labels])