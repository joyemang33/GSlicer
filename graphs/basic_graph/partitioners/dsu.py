class DSU:
    def __init__(self, n : int):
        self.n = n
        self.fa = [i for i in range(0, n)]
    
    def ask(self, x : int):
        if x == self.fa[x]: return x
        self.fa[x] = self.ask(self.fa[x])
        return self.fa[x]
    
    def merge(self, x : int, y : int):
        p, q = self.ask(x), self.ask(y)
        if p != q: self.fa[p] = q

    def listing_conected_components(self):
        res = dict()
        for i in range(0, self.n):
            p = self.ask(i)
            if p not in res.keys():
                res[p] = []
            res[p].append(i)
        return [x[1] for x in res.items()]