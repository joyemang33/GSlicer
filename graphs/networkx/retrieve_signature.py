import networkx.algorithms
import types
import json
import inspect

"""
This script is used to retrieve the signature of the algorithms in networkx.
"""

def list_functions(module):
    return [name for name, obj in module.__dict__.items() if isinstance(obj, types.FunctionType)]

def extract_return_type(doc_string):
    try:
        return_start_index = doc_string.index("Returns\n    -------\n    ") + 24
        return_end_index = doc_string.index("\n\n", return_start_index)
        return_type = doc_string[return_start_index: return_end_index]
        return_type = return_type.replace("\n    ", ", ")
    except:
        return_type = "Unknown"

    return return_type


if __name__ == "__main__":
    functions = list_functions(networkx.algorithms)

    res = []
    for function_name in functions:
        if function_name == "not_implemented_for":
            continue
        fun = getattr(networkx.algorithms, function_name)
        doc = fun.__doc__       
        return_type = extract_return_type(doc)
        parameter_type = str(inspect.signature(fun).parameters)
        res.append(function_name)
        # print(function_name + "|" + return_type + "|" + parameter_type)
    
    with open("algorithm_names.json", "w", encoding="utf-8") as file:
        json.dump(res, file)