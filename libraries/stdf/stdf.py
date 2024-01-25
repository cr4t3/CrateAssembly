import variables

def mov(var_name: str, value):
    try:
        float(value)    
        variables.mov(var_name, float(value))
    except:
        variables.mov(var_name, variables.get(value))

def add(var_name: str, value):
    try:
        float(value)    
        variables.mov(var_name, variables.get(var_name) + float(value))
    except:
        variables.mov(var_name, variables.get(var_name) + variables.get(value))

def sub(var_name: str, value):
    try:
        float(value)    
        variables.mov(var_name, variables.get(var_name) - float(value))
    except:
        variables.mov(var_name, variables.get(var_name) - variables.get(value))

def inc(var_name: str):
    add(var_name, 1)

def dec(var_name: str):
    sub(var_name, 1)

def prt(value):
    try:
        float(value)    
        print(float(value))
    except:
        print(variables.get(value))