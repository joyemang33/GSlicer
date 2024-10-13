import random
from graphs.kuzu.graph_generator import *
from graphs.kuzu.predicate_generator import *


def random_string():
    length = random.randint(1, 20)
    ran = ''.join(random.choices(
        string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))
    if not ran.startswith(string.ascii_uppercase):
        ran = random.choice(string.ascii_uppercase) + ran
    return ran

class PatternGenerator:
    def __init__(self, G : GraphData):
        '''
        G : the graph data for the graph-aware generator
        n : the current number of nodes
        m : the current number of relationships
        p_new : the probability of adding new nodes
        '''
        
        self.G = G
        self.n = 0
        self.m = 0
        self.p_new = 0.2
        self.node_id_to_name = {}
        self.edge_id_to_name = {}
        self.predicate_generator = BasicWhereGenerator(G)
        
    def random_node_name(self, existed_name = False):
        if existed_name:
            id = random.randint(0, self.n - 1)
            return self.node_id_to_name[id]
        if self.n == 0 or random.random() <= self.p_new:
            #adding a new node
            id = self.n
            self.n += 1
            name = random_string()
            while name in self.node_id_to_name.keys():
                name = random_string()
            self.node_id_to_name[id] = name 
            self.predicate_generator.vars.append(name)
            return self.node_id_to_name[id]            
        else:
            #return a existing node
            id = random.randint(0, self.n - 1)
            return self.node_id_to_name[id]
    
    def random_edge_name(self):
        #relationship will always be new
        id = self.m
        self.m += 1
        name = random_string()
        while name in self.edge_id_to_name.keys():
            name = random_string()
        self.edge_id_to_name[id] = name
        self.predicate_generator.vars.append(name)
        return self.edge_id_to_name[id]
    
    def random_predicate(self):
        #TODO
        pass
    
    def random_path_variable(self):
        #TODO avoid generate 0..0 and *..0
        op = random.randint(1, 4)
        if op == 1: # Case1: l <= length <= r
            x = random.randint(0, 15)
            y = random.randint(0, 15)
            if x > y: x, y = y, x
            return "*" + str(x) + ".." + str(y)
        if op == 2: #Case2: l <= length
            x = random.randint(0, 15)
            return "*" + str(x) + ".."
        if op == 3: #Case3: length <= r
            x = random.randint(0, 15)
            return "*" + ".." + str(x)
        if op == 4: #Case4: any length
            return "*"
        
    def gen_node_pattern(self, existed = False):
        res = "(" + self.random_node_name(existed_name = existed)
        #add node labels
        node_labels = random.sample(self.G.node_labels, random.randint(0, self.G.no_node_labels))
        for (i, label) in enumerate(node_labels):
            if i > 0: res += ":" + label.name
        res += ")"
        return res
        #TODO add the constraints of the properties
    
    def gen_edge_pattern(self, p_name = 0.5, p_var = 0.5):
        '''
        p_name : the probability of adding a name for the edge
        p_var : the probability of adding a path variable for the edge
        '''
        
        res = "["
        #adding name (optional)
        has_name = False
        if random.random() < p_name:
            has_name = True
            res += self.random_edge_name()
        #adding edge labels
        edge_labels = random.sample(self.G.edge_labels, random.randint(0, self.G.no_edge_labels))
        for (i, label) in enumerate(edge_labels):
            if i > 0: res += "|"
            res += ":" + label.name
            
        #adding a path varibale (optional)
        if has_name == False and random.random() < p_var:
            res += self.random_path_variable()
        res += "]"
        #adding the direction
        direction = random.choice(
            [("-", "-"), ("<-", "-"), ("-", "->")]
        )
        res = direction[0] + res + direction[1]
        return res        
    
    def gen_pattern(self, existed = False, max_no_chains = 3, max_chain_length = 4):
        '''
        max_no_chains : the maximum number of chains
        max_chain_length : the maximum number of nodes in a chain
        '''
        res = ""
        no_chain = random.randint(1, max_no_chains)
        for i in range(0, no_chain):
            if i > 0: res += ", "
            no_nodes = random.randint(1, max_chain_length)
            for j in range(0, no_nodes):
                if j > 0: #add an edge
                    res = res + self.gen_edge_pattern()
                res = res + self.gen_node_pattern(existed = (existed or (j == 0 and i != 0)))
        return res

if __name__ == "__main__":
    #unit test
    G = GraphData(_no_properties = 10, _no_node_labels = 5, _no_edge_labels = 5, _no_nodes = 5, _no_edges = 10)
    PG = PatternGenerator(G)
    PG.gen_node_pattern()