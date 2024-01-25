import errorhandler
variables = {}

def mov(name: str, value):
    try:
        float(name)
        errorhandler.TypeError_(name, "string", "float")
        return False
    except:
        variables[name] = value
        return True

def get(name: str):
    try:
        variables[name]
        return variables[name]
    except KeyError:
        errorhandler.DefinitionError(name)
        return False