import variables, sys, main

def inff(var_name: str):
    while True:
        value = ""
        try:
            value = float(input(f"{main.args.file} requires a float: "))
            variables.mov(var_name, value)
            break
        except ValueError:
            pass
        except:
            return 1

def infi(var_name: str):
    while True:
        value = ""
        try:
            value = float(input(f"{main.args.file} requires a float: "))
            variables.mov(var_name, value)
            break
        except ValueError:
            pass
        except:
            return 1

def exit_(code):
    try:
        int(code)
    except:
        return 1
    sys.exit(int(code))

def prt(value):
    try:
        print(float(value))
    except ValueError:
        if not variables.is_variable(value):
            return 1
        print(variables.get(value))