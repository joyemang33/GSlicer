import string
import random

class Neo4jConstant:
    def gen_type(self):
        return random.choice(["int", "float"])

    def gen_constant(self, type : str):
        assert type in ["int", "float"]
        if type == "int":
            return random.randint(-(2 ** 63), (2 ** 63) - 1)
        if type == "float":
            return random.random() * random.randint(-(2 ** 63), (2 ** 63) - 1)