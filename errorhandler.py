import rich, sys

class Error:
    def __init__(self, error_type: str, error_message: str) -> None:
        """Prints a message and exits the program

        Args:
            error_type (str): Error type (ex: 'TypeError', 'ModuleError')
            error_message (str): Error message
        """
        rich.print(f"[#ff0000]{error_type}: {error_message}", file=sys.stderr)
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

class ScanError(Error):
    def __init__(self, e: Exception) -> None:
        super().__init__("ScanError", f"scan_libraries has thrown an error: {e}")

class LibraryNotFoundError(Error):
    def __init__(self, library: str) -> None:
        super().__init__("LibraryNotFoundError", f"Library \"{library}\" not found.")

class FileNotFoundError_(Error):
    def __init__(self, file_name: str) -> None:
        super().__init__("FileNotFoundError", f"File '{file_name}' not found.")

class StatusCodeError(Error):
    def __init__(self, function: str) -> None:
        super().__init__("StatusCodeError", f"Function {function} returned a error status code.")

class InvalidVariableName(Error):
    def __init__(self, name: str) -> None:
        super().__init__("InvalidVariableName", f"Variable name {name} is invalid.")

class Debug:
    def __init__(self, value) -> None:
        rich.print(f"[green]{value}")
