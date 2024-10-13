
def node_dict_smaller(G, G0, G1, eps = 1e-2):
    """Validates the algorithms that return a dictionary of nodes.
    Using G0 < G
    """
    for v in G0.keys():
        if G0[v] - G[v] > eps:
            error_msg = "G0[" + str(v) + "] = " + str(G0[v]) + ", G[" + str(v) + "] = " + str(G[v])
            return False, error_msg
    for v in G1.keys():
        if G1[v] - G[v] > eps: 
            error_msg = "G1[" + str(v) + "] = " + str(G1[v]) + ", G[" + str(v) + "] = " + str(G[v])
            return False, error_msg
    return True, ""

def node_dict_equal(G, G0, G1, eps = 1e-2):
    """Validates the algorithms that return a dictionary of nodes.
    Using G0 = G
    """
    for v in G0.keys():
        if abs(G0[v] - G[v]) > eps:
            error_msg = "G0[" + str(v) + "] = " + str(G0[v]) + ", G[" + str(v) + "] = " + str(G[v])
            return False, error_msg
    for v in G1.keys():
        if abs(G1[v] - G[v]) > eps: 
            error_msg = "G1[" + str(v) + "] = " + str(G1[v]) + ", G[" + str(v) + "] = " + str(G[v])
            return False, error_msg
    return True, ""

def node_dict_greater(G, G0, G1, eps = 1e-2):
    """Validates the algorithms that return a dictionary of nodes.
    Using G0 > G
    """
    for v in G0.keys():
        if G0[v] - G[v] < -eps:
            error_msg = "G0[" + str(v) + "] = " + str(G0[v]) + ", G[" + str(v) + "] = " + str(G[v])
            return False, error_msg
    for v in G1.keys():
        if G1[v] - G[v] < -eps: 
            error_msg = "G1[" + str(v) + "] = " + str(G1[v]) + ", G[" + str(v) + "] = " + str(G[v])
            return False, error_msg
    return True, ""

def value_smaller(G, G0, G1, eps = 1e-2):
    """Validates the algorithms that return a dictionary of nodes.
    Using G0 > G
    """
    if G0 - G > eps:
        error_msg = "G0 = " + str(G0) + ", G = " + str(G)
        return False, error_msg
    
    if G1 - G > eps: 
        error_msg = "G1 = " + str(G1) + ", G = " + str(G)
        return False, error_msg
    
    return True, ""

def value_equal(G, G0, G1, eps = 1e-2):
    """Validates the algorithms that return a dictionary of nodes.
    Using G0 > G
    """
    if abs(G0 - G) > eps:
        error_msg = "G0 = " + str(G0) + ", G = " + str(G)
        return False, error_msg
    
    if abs(G1 - G) > eps: 
        error_msg = "G1 = " + str(G1) + ", G = " + str(G)
        return False, error_msg
    
    return True, ""

def value_greater(G, G0, G1, eps = 1e-2):
    """Validates the algorithms that return a dictionary of nodes.
    Using G0 > G
    """
    if G0 - G < -eps:
        error_msg = "G0 = " + str(G0) + ", G = " + str(G)
        return False, error_msg
    
    if G1 - G < -eps: 
        error_msg = "G1 = " + str(G1) + ", G = " + str(G)
        return False, error_msg
    
    return True, ""

def sum_greater(G, G0, G1, eps = 1e-2):
    """Validates the algorithms that return a dictionary of nodes.
    Using G0 + G1 > G
    """
    if G0 + G1 - G < -eps:
        error_msg = "G0 + G1 = " + str(G0 + G1) + ", G = " + str(G)
        return False, error_msg
    
    # if G1 - G < -eps: 
    #     error_msg = "G1 = " + str(G1) + ", G = " + str(G)
    #     return False, error_msg
    
    return True, ""

def sum_smaller(G, G0, G1, eps = 1e-2):
    """Validates the algorithms that return a dictionary of nodes.
    Using G0 + G1 > G
    """
    if G0 + G1 - G > -eps:
        error_msg = "G0 + G1 = " + str(G0 + G1) + ", G = " + str(G)
        return False, error_msg
    
    # if G1 - G < -eps: 
    #     error_msg = "G1 = " + str(G1) + ", G = " + str(G)
    #     return False, error_msg
    
    return True, ""

def sum_equal(G, G0, G1, eps = 1e-2):
    """Validates the algorithms that return a dictionary of nodes.
    Using G0 + G1 > G
    """
    if abs(G0 + G1 - G) > eps:
        error_msg = "G0 + G1 = " + str(G0 + G1) + ", G = " + str(G)
        return False, error_msg
    
    # if G1 - G < -eps: 
    #     error_msg = "G1 = " + str(G1) + ", G = " + str(G)
    #     return False, error_msg
    
    return True, ""