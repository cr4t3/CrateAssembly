import errorhandler, string
from functools import cache
variables = {}

def is_variable(name):
    try:
        variables[name]
        return True
    except KeyError:
        return False
@cache    
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
@cache
def is_int(string):
    try:
        int(string)
        return True
    except:
        return False
@cache
def is_number(string):
    return is_int(string) or is_float(string)

def mov(name: str, value):
    if True in [punctuation in name for punctuation in list(string.punctuation)]:
        errorhandler.InvalidVariableName(name)
        return False # This returns false if there is punctuation in the var name, so vars cant be called things like "." or "/"
    
    try:
        float(name)
        errorhandler.TypeError_(name, "string", "float")
        return False
    except:
        variables[name] = value
        return True

def get(name: str):
    if True in [punctuation in name for punctuation in list(string.punctuation)]:
        return False # This returns false if there is punctuation in the var name, so vars cant be called things like "." or "/"

    try:
        variables[name]
        return variables[name]
    except KeyError:
        errorhandler.DefinitionError(name)