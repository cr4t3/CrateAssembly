# Parse file into the expected functions
import libraries, errorhandler
from pathlib import Path
from typing import Callable
from functools import cache
import main

SOURCE_LIBRARIES_PATH: Path = Path(__file__).parent.absolute() / "libraries"

HOME_LIBRARIES_PATH: Path = Path.home() / ".casm/libraries"

line_number = 0

@cache
def load_function_data(callname: str) -> tuple[int, Callable]:
    """Load the function data

    Args:
        callname (str): Call name of the function

    Returns:
        tuple[int, Callable]: Arg count and the function executable
    """
    function_info: dict[str, Callable] = libraries.global_functions[callname]
    arg_count = function_info["args"]
    Function: Callable = function_info["function"]
    
    return arg_count, Function

def include(args: list[str], readUntil: int) -> bool:
    """Includes the asked library

    Args:
        args (list[str]): The arguments of the 'include' line

    Returns:
        bool: True if loaded
    """
    if (calculate_args(len(args), readUntil)) == 1:
        if libraries.scan_libraries(args[1], SOURCE_LIBRARIES_PATH) or libraries.scan_libraries(args[1], HOME_LIBRARIES_PATH):
            return True
        errorhandler.LibraryNotFoundError(args[1])
    else:
        errorhandler.LengthError("include", 1, len(args)-1)
@cache
def calculate_args(length: int, readUntil: int) -> int:
    """Calculates the readable args count

    Args:
        args (list[str]): Arguments
        readUntil (int): Read limit

    Returns:
        int: Readable args count
    """
    return ((length-1)-(length-readUntil) if readUntil != -1 else length-1)
@cache
def get_args(args: tuple, readUntil: int) -> list[str]:
    """Returns a function's arguments

    Args:
        args (list[str]): Script args
        readUntil (int): Read limit

    Returns:
        list[str]: Args for function
    """
    args = list(args)
    return [f"{arg}" for arg in args[1:readUntil if readUntil != -1 else len(args):] if arg]

def execute_function(args: list[str], readUntil: int, Function: Callable) -> bool:
    """Executes a function from a library

    Args:
        args (list[str]): 'To function' argument
        readUntil (int): Argument limit
        Function (Callable): Function

    Returns:
        bool: True if didn't crashes
    """
    arg_list: list[str] = get_args(tuple(args), readUntil)
    code = Function(*arg_list)
    if not (code == 0 or code == None) and not (main.args.ignore_status_codes):
        errorhandler.StatusCodeError(args[0])
    return True

def run_function(args: list[str], readUntil: int, arg: str) -> bool:
    """Verifies if the function can be executed

    Args:
        args (list[str]): Arguments
        readUntil (int): Max argument list
        arg (str): Function name

    Returns:
        bool: True if executed
    """
    arg_count, Function = load_function_data(arg)
    if (calculate_args(len(args), readUntil)) == arg_count:
        return execute_function(args, readUntil, Function)
    else:
        errorhandler.LengthError(arg, arg_count, calculate_args(len(args), readUntil))

def interpret_arg(args: list[str], arg: str, i: int, readUntil: int, functionDone: bool) -> str | None | bool:
    """Interprets an argument

    Args:
        args (list[str]): Arguments
        arg (str): Current argument
        i (int): Index
        readUntil (int): Argument read limit
        functionDone (bool): Has been function executed

    Returns:
        str: Returns "break" if it's a command, empty line or if it's not the first argument
        None: If function has been executed
        bool: If function has been sent to be executed ('include' or 'run_function')
    """
    if arg.startswith(";") or arg == "" or i != 0:
        return "break"
    elif functionDone:
        pass
    elif arg == "include":
        return include(args, readUntil)                        
    elif arg in list(libraries.global_functions.keys()):
        return run_function(args, readUntil, arg)                        
    else:
        errorhandler.DefinitionError(arg)
@cache
def skip_comments(arg: str, i: int) -> tuple[int, str]:
    """Verifies when each line has a comment

    Args:
        arg (str): Current argument
        i (int): Index

    Returns:
        tuple[int, str]: Arguments limit and "break"
    """
    if arg.startswith(";"):
        readUntil = i
        return readUntil, "break"

def get_read_until(args: list[str]) -> int:
    """Calculates where to end read in each line

    Args:
        args (list[str]): Arguments

    Returns:
        int: Max arguments limit
    """
    readUntil = 0
    for i, arg in enumerate(args):
        x: tuple[int, str] | None = skip_comments(arg, i)
        if x:
            readUntil, isBreaking = x[0], x[1]
            if isBreaking == "break":
                return readUntil
    else:
        readUntil = -1
        return readUntil
    

def interpret_args(args: list[str], readUntil: int, functionDone: bool) -> None:
    """Interprets arguments

    Args:
        args (list[str]): Arguments list
        readUntil (int): Max argument limit
        functionDone (bool): Has function been executed
    """
    for i, arg in enumerate(args):
        if interpret_arg(args, arg, i, readUntil, functionDone) == "break":
            return
@cache
def load_line_data(line: str) -> tuple[list[str], bool, int]:
    """Loads the information about the given line

    Args:
        line (str): Current line

    Returns:
        tuple[list[str], bool, int]: Returns the arguments, if the function has been executed and the argument read limit
    """
    args: list[str] = line.split(" ")
    functionDone: bool = False
    readUntil: int = get_read_until(args)
    return args, functionDone, readUntil

def interpret_line(line: str) -> None:
    """Interprets given line

    Args:
        line (str): Current line
    """
    if not line.startswith(";"):
        args, functionDone, readUntil = load_line_data(line)

        interpret_args(args, readUntil, functionDone)

def interpret_file(content: list[str]) -> None:
    """Interprets the file's content

    Args:
        content (list[str]): Content in list form
    """
    global line_number
    while line_number < len(content):
        line = content[line_number]
        interpret_line(line)
        
        line_number += 1
        

def load_file(File: str) -> None:
    """Loads the given file name

    Args:
        File (str): File name
    """
    try:
        with open(File, "r") as script:
            content: str = script.read().lower().rsplit("\n")
            interpret_file(content)
    except FileNotFoundError:
        errorhandler.FileNotFoundError_(File)