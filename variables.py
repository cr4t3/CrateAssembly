variables = {}

def mov(name: str, value):
    variables[name] = value

def get(name: str):
    return variables[name]