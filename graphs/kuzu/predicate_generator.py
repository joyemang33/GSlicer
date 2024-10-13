import random
from graphs.kuzu.graph_generator import GraphData

class BasicWhereGenerator:
    def __init__(self, G: GraphData):
        self.G = G
        self.vars = []

    def __gen_single_exp(self):
        v1 = random.choice(self.vars)
        p1 = random.sample(self.G.properties, 1)[0]
        if p1.type.name == "INT":
            sgn = random.choice(["=", ">", "<", ">=", "<=", "<>"])
        else:
            sgn = random.choice(["=", "<>"])

        res = v1 + "." + p1.name + " " + sgn
        if random.randint(0, 1) == 1:
            c = p1.type.gen_value_in_str()
            res = res + " " + c
        else:
            v2 = random.choice(self.vars)
            p2 = random.sample(self.G.properties, 1)[0]
            while p2.type.name != p1.type.name:
                p2 = random.sample(self.G.properties, 1)[0]
            res = res + " " + v2 + "." + p2.name
        if random.randint(1, 3) == 1:
            res = "NOT " + "(" + res + ")"
        return "(" + res + ")"

    def gen_exp(self):
        num = random.randint(1, 5)
        res = ""
        leftB = 0
        for i in range(0, num):
            not_count = 0
            if random.randint(1, 3) == 1: 
                res = res + "NOT " + "("
                not_count += 1
            if random.randint(1, 3) == 1:
                res = res + "("
                leftB += 1
            res = res + self.__gen_single_exp()
            while leftB > 0 and random.randint(1, 3) == 1:
                res = res + ")"
                leftB -= 1
            if i + 1 < num:
                res = res + " " + random.choice(["AND", "OR"]) + " "
            while not_count > 0:
                not_count -= 1
                res = res + ")"
        while leftB > 0:
            res = res + ")"
            leftB -= 1
        
        return res
