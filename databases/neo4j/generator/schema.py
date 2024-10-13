import random
from databases.neo4j.generator.constant import ConstantGenerator


class GraphSchema:
    def __init__(self):
        self.label_num = None
        self.edge_prop_val = None
        self.types2prop = None
        self.node_prop_val = None
        self.prop = None
        self.CG = ConstantGenerator()

    def gen(self, output_file="./databases/neo4j/generator/output_files/1", 
            node_num=30, edge_num=150, prop_num=30, label_num=8):

        '''
        generate two disconnected sub-graphs that contain node_num nodes aned edge_num edges
        G0 with node-id between 0 and node_num - 1, edge-id between 0 and edge_num - 1 
        G1 with node-id between node_num and 2 * node_num - 1, edge-id between edge_num and 2 * edge_num - 1 
        '''

        self.label_num = label_num
        self.prop = dict()
        self.node_prop_val = dict()
        self.edge_prop_val = dict()
        self.types2prop = {
            "int": [],
            "float": [],
            "bool": [],
            "string": []
        }

        types = ["int", "float", "bool", "string"]

        for i in range(0, prop_num):
            self.prop["p" + str(i)] = random.choice(types)
            self.node_prop_val["p" + str(i)] = []
            self.edge_prop_val["p" + str(i)] = []
            self.types2prop[self.prop["p" + str(i)]].append("p" + str(i))

        output_G = open(output_file + "-G", "w", encoding="utf-8")
        output_G0 = open(output_file + "-G0", "w", encoding="utf-8")
        output_G1 = open(output_file + "-G1", "w", encoding="utf-8")

        for node_offset, edge_offset, output_sub in [(0, 0, output_G0), (node_num, edge_num, output_G1)]:
            for i in range(0, node_num):
                statement = "CREATE(n0"
                num = random.randint(0, label_num)
                labels = random.sample(list(range(0, label_num)), num)
                for label in labels:
                    statement = statement + ":L" + str(label)
                statement = statement + "{id : " + str(i + node_offset)
                num = random.randint(0, prop_num)
                properties = random.sample(list(self.prop.keys()), num)
                for x in properties:
                    statement = statement + ", " + x + " : "
                    y = self.CG.gen(self.prop[x])
                    statement = statement + y
                    self.node_prop_val[x].append(y)
                statement = statement + "});"
                print(statement, file=output_G)
                print(statement, file=output_sub)


            for i in range(0, edge_num):
                id0, id1 = random.randint(0, node_num), random.randint(0, node_num)
                id0 += node_offset
                id1 += node_offset
                statement = "MATCH (n0 {id : " + str(id0) + "}), (n1 {id : " + str(id1) + "}) "
                statement = statement + "MERGE(n0)-["
                num = 1
                labels = random.sample(list(range(0, label_num)), num)
                for label in labels:
                    statement = statement + ":T" + str(label)
                statement = statement + "{id : " + str(i + 2 * node_num + edge_offset)
                num = random.randint(0, prop_num)
                properties = random.sample(list(self.prop.keys()), num)
                for prop in properties:
                    statement = statement + ", " + prop + " : "
                    val = self.CG.gen(self.prop[prop])
                    statement = statement + val
                    self.edge_prop_val[prop].append(val)
                statement = statement + "}]->(n1);"
                print(statement, file=output_G)
                print(statement, file=output_sub)


if __name__ == "__main__":
    G = GraphSchema()
    G.gen()

