import variables

def mov(var_name: str, value):
    try:
        float(value)    
        variables.mov(var_name, float(value))
    except:
        if not variables.get(value):
            return
        variables.mov(var_name, variables.get(value))

def add(var_name: str, value):
    if not variables.get(var_name):
        return
    try:
        float(value)    
        variables.mov(var_name, variables.get(var_name) + float(value))
    except:
        if not variables.get(value):
            return
        variables.mov(var_name, variables.get(var_name) + variables.get(value))

def sub(var_name: str, value):
    if not variables.get(var_name):
        return
    try:
        float(value)    
        variables.mov(var_name, variables.get(var_name) - float(value))
    except:
        if not variables.get(value):
            return
        variables.mov(var_name, variables.get(var_name) - variables.get(value))

def mul(var_name: str, value):
    if not variables.get(var_name):
        return
    try:
        float(value)    
        variables.mov(var_name, variables.get(var_name) * float(value))
    except:
        if not variables.get(value):
            return
        variables.mov(var_name, variables.get(var_name) * variables.get(value))

def div(var_name: str, value):
    if not variables.get(var_name):
        return
    try:
        float(value)    
        variables.mov(var_name, variables.get(var_name) / float(value))
    except:
        if not variables.get(value):
            return
        variables.mov(var_name, variables.get(var_name) / variables.get(value))

def elev(var_name: str, value):
    if not variables.get(var_name):
        return
    try:
        float(value)    
        variables.mov(var_name, variables.get(var_name) ** float(value))
    except:
        if not variables.get(value):
            return
        variables.mov(var_name, variables.get(var_name) ** variables.get(value))

def root(var_name: str, value):
    if not variables.get(var_name):
        return
    try:
        float(value)    
        variables.mov(var_name, variables.get(var_name) ** (1/float(value)))
    except:
        if not variables.get(value):
            return
        variables.mov(var_name, variables.get(var_name) ** (1/variables.get(value)))

def inc(var_name: str):
    add(var_name, 1)

def dec(var_name: str):
    sub(var_name, 1)

def prt(value):
    try:
        float(value)    
        print(float(value))
    except:
        if not variables.get(value) and variables.get(value) != 0.0:
            return
        print(variables.get(value))