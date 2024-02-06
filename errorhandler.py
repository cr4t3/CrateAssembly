class Error:
    def __init__(self, error_type: str, error_message: str):
        print(f"{error_type}: {error_message}")
        exit()

class LengthError:
    def __init__(self, function: str, expected: int, recived: int):
        Error("LengthError", f"{function} required {expected} arguments and recieved {recived}")

class DefinitionError:
    def __init__(self, name: str):
        Error("DefinitionError", f"{name} is not defined")

class TypeError_:
    def __init__(self, value: str, expected: str, recived: str):
        Error("TypeError", f"{value} was expected to be a {expected} but it was given a {recived}")