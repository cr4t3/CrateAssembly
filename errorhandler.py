import rich, sys

class Error:
    def __init__(self, error_type: str, error_message: str) -> None:
        """Prints a message and exits the program

        Args:
            error_type (str): Error type (ex: 'TypeError', 'ModuleError')
            error_message (str): Error message
        """
        print(f"{error_type}: {error_message}", file=sys.stderr)
        exit()

class LengthError(Error):
    def __init__(self, function: str, expected: int, recived: int) -> None:
        super().__init__("LengthError", f"{function} required {expected} arguments and recieved {recived}")

class DefinitionError(Error):
    def __init__(self, name: str) -> None:
        super().__init__("DefinitionError", f"{name} is not defined")

class TypeError_(Error):
    def __init__(self, value: str, expected: str, recived: str) -> None:
        super().__init__("TypeError", f"{value} was expected to be a {expected} but it was given a {recived}")

class ModuleError(Error):
    def __init__(self, module: str, name: str) -> None:
        super().__init__("ModuleError", f"{module} module does not have the expected function: {name}")

class Debug:
    def __init__(self, value) -> None:
        rich.print(f"[green]{value}")