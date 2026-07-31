import math


def _is_nan(value):
    """Return whether value is a numeric NaN."""
    try:
        return math.isnan(value)
    except TypeError:
        return False


def _node_dict_nan_error(G, G0, G1):
    """Return an error message if a compared node result contains NaN."""
    for result_name, subgraph_result in (("G0", G0), ("G1", G1)):
        for node, subgraph_value in subgraph_result.items():
            original_value = G[node]

            if _is_nan(subgraph_value) or _is_nan(original_value):
                return (
                    f"NaN result for node {node}: "
                    f"{result_name}[{node}] = {subgraph_value}, "
                    f"G[{node}] = {original_value}"
                )

    return ""

def _scalar_nan_error(G, G0, G1):
    """Return an error message if a scalar result contains NaN."""
    for result_name, value in (("G", G), ("G0", G0), ("G1", G1)):
        if _is_nan(value):
            return f"NaN result: {result_name} = {value}"

    return ""


def node_dict_smaller(G, G0, G1, eps = 1e-2):
    """Validates the algorithms that return a dictionary of nodes.
    Using G0 < G
    """
    error_msg = _node_dict_nan_error(G, G0, G1)
    if error_msg:
        return False, error_msg

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
    error_msg = _node_dict_nan_error(G, G0, G1)
    if error_msg:
        return False, error_msg

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
    error_msg = _node_dict_nan_error(G, G0, G1)
    if error_msg:
        return False, error_msg

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
    error_msg = _scalar_nan_error(G, G0, G1)
    if error_msg:
        return False, error_msg

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
    error_msg = _scalar_nan_error(G, G0, G1)
    if error_msg:
        return False, error_msg

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
    error_msg = _scalar_nan_error(G, G0, G1)
    if error_msg:
        return False, error_msg

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
    error_msg = _scalar_nan_error(G, G0, G1)
    if error_msg:
        return False, error_msg

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
    error_msg = _scalar_nan_error(G, G0, G1)
    if error_msg:
        return False, error_msg

    if G0 + G1 - G > eps:
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
    error_msg = _scalar_nan_error(G, G0, G1)
    if error_msg:
        return False, error_msg

    if abs(G0 + G1 - G) > eps:
        error_msg = "G0 + G1 = " + str(G0 + G1) + ", G = " + str(G)
        return False, error_msg
    
    # if G1 - G < -eps: 
    #     error_msg = "G1 = " + str(G1) + ", G = " + str(G)
    #     return False, error_msg
    
    return True, ""
