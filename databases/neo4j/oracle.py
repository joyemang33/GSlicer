from help.hash_nested_dict import hash_dictionary

class BasicValidator:
    def __init__(self, node_num):
        self.time_ths0, self.time_ths1 = 2, 500
        self.node_num = node_num
        # max(t + time_ths1, time_ths0 * t) > max(t0, t1)

    def compare_time(self, t : int, t0 : int, t1 : int):
        if max(t + self.time_ths1, self.time_ths0 * t) < max(t0, t1):
            print(f"Performance Bug: Query(G) = {t}ms, Query(G0) = {t0}ms, Query(G1) = {t1}ms")
            return False
        return True

    def compare_count(self, c : int, c0 : int, c1 : int):
        if c < c0 + c1:
            print(f"Count Bug: Query(G) = {c}, Query(G0) = {c0}, Query(G1) = {c1}")
            return False
        return True
    
    def compare_list(self, l : list, l0 : list, l1 : list):
        for row in l + l0 + l1:
            for x in row.keys():
                if type(row[x]) == type((0, 0)):
                    d = {
                        0 : row[x][0],
                        1 : row[x][1],
                        2 : row[x][2]
                    }
                    row[x] = d
        
        _l, pure_l = list(), list() 
        for row in l:
            contains_G0, contains_G1 = False, False 
            for item in list(row.values()):
                if type(item) != type({}): continue
                if "id" not in item.keys(): continue
                if item["id"] < self.node_num: contains_G0 = True
                if self.node_num <= item["id"] < 2 * self.node_num: contains_G1 = True
            if not (contains_G0 and contains_G1):
                _l.append(hash_dictionary(row))
                pure_l.append(row)

        _l0 = [hash_dictionary(row) for row in l0]
        _l1 = [hash_dictionary(row) for row in l1]
        if sorted(_l) != sorted(_l0 + _l1):
            print("Logic Bug:")
            print("Query(G): ", l)
            print("Query(G0): ", l0)
            print("Query(G1): ", l1)
            return False
        return True

    def validate(self, res : list, t : int, res0 : list, t0 : int, res1 : list, t1 : int):
        validate_result = True
        validate_result &= self.compare_time(t, t0, t1)
        if len(res) == 1 and "cnt" in res[0].keys():
            validate_result &= self.compare_count(res[0]["cnt"], res0[0]["cnt"], res1[0]["cnt"])
        else:
            validate_result &= self.compare_list(res, res0, res1)
        return validate_result
