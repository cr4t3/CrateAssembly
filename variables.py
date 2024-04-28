import errorhandler, string
variables = {}

def is_variable(name):
    try:
        variables[name]
        return True
    except KeyError:
        return False

def mov(name: str, value):
    if True in [punctuation in name for punctuation in list(string.punctuation)]    :
        return False # This returns false if there is punctuation in the var name, so vars cant be called things like "." or "/"
    
    try:
        float(name)
        errorhandler.TypeError_(name, "string", "float")
        return False
    except:
        variables[name] = value
        return True

def get(name: str):
    if True in [punctuation in name for punctuation in list(string.punctuation)]    :
        return False # This returns false if there is punctuation in the var name, so vars cant be called things like "." or "/"

    try:
        variables[name]
        return variables[name]
    except KeyError:
        errorhandler.DefinitionError(name)
        return False