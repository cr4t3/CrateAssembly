import variables as v
import interpreter

compare = False

def mov(value1, value2):
    if v.is_number(value1):
        return 1
    
    v.mov(value1, (float(value2) if v.is_float(value2) else int(value2)) if v.is_number(value2) and not v.is_variable(value2) else v.get(value2))

def add(value1, value2):
    if not v.is_variable(value1):
        return 1
    
    v.mov(value1, v.get(value1) + (float(value2) if v.is_float(value2) else int(value2)) if v.is_number(value2) and not v.is_variable(value2) else v.get(value2))

def sub(value1, value2):
    if not v.is_variable(value1):
        return 1
    
    v.mov(value1, v.get(value1) - (float(value2) if v.is_float(value2) else int(value2)) if v.is_number(value2) and not v.is_variable(value2) else v.get(value2))

def mul(value1, value2):
    if not v.is_variable(value1):
        return 1
    
    v.mov(value1, v.get(value1) * (float(value2) if v.is_float(value2) else int(value2)) if v.is_number(value2) and not v.is_variable(value2) else v.get(value2))

def div(value1, value2):
    if not v.is_variable(value1):
        return 1
    
    v.mov(value1, v.get(value1) / (float(value2) if v.is_float(value2) else int(value2)) if v.is_number(value2) and not v.is_variable(value2) else v.get(value2))

def and_(value1, value2):
    if v.is_variable(value1) and (v.is_variable(value2) or v.is_int(value2)):
        value2_int = int(v.get(value2)) if v.is_variable(value2) else int(value2)
        v.mov(value1, int(v.get(value1)) & value2_int)
    else:
        return 1  # Error indication

def or_(value1, value2):
    if v.is_variable(value1) and (v.is_variable(value2) or v.is_int(value2)):
        value2_int = int(v.get(value2)) if v.is_variable(value2) else int(value2)
        v.mov(value1, int(v.get(value1)) | value2_int)
    else:
        return 1  # Error indication

def xor(value1, value2):
    if v.is_variable(value1) and (v.is_variable(value2) or v.is_int(value2)):
        value2_int = int(v.get(value2)) if v.is_variable(value2) else int(value2)
        v.mov(value1, int(v.get(value1)) ^ value2_int)
    else:
        return 1  # Error indication

def not_(value1):
    if v.is_variable(value1):
        v.mov(value1, ~int(v.get(value1)))
    else:
        return 1  # Error indication

def cmp(value1, value2):
    global compare
    if v.is_variable(value1):
        compare = v.get(value1) == v.get(value2) if v.is_variable(value2) else v.get(value1) == float(value2)
    elif v.is_variable(value2):
        compare = v.get(value2) == float(value1)
    else:
        compare = float(value1) == float(value2)
    
def jmp(line):
    if not v.is_int(line):
        return 1
    
    if int(line) >= 0:
        interpreter.line_number = int(line)-2

def je(line):
    if compare:
        return jmp(line)

def jne(line):
    if not compare:
        return jmp(line)
    
def inc(var):
    if not v.is_variable(var):
        return 1
    
    add(var, 1)

def dec(var):
    if not v.is_variable(var):
        return 1
    
    sub(var, 1)