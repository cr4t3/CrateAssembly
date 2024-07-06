import importlib.util
import ujson, os
from pathlib import Path
from types import ModuleType
from io import TextIOWrapper
import errorhandler
from typing import Callable
from functools import cache
import utils

def create_libraries_json(path: Path) -> None:
    """create_libraries_json creates the libraries.json file in the given path

    Args:
        path (Path): Path to create libraries.json
    """
    with open(path, "w") as File:
        File.write("{\"libraries\":[]}")

def path_verification(casm_dir: Path, libraries_dir: Path, libraries_file: Path) -> None:
    """Verifies if the libraries.json exists in the passed dirs

    Args:
        casm_dir (Path): '.casm' dir
        libraries_dir (Path): 'SOURCE/libraries' dir
        libraries_file (Path): '.casm/libraries.json' or 'SOURCE/libraries/libraries.json' file
    """
    if not casm_dir.exists():
            os.makedirs(casm_dir, exist_ok=True)
            os.makedirs(libraries_dir, exist_ok=True)
            create_libraries_json(libraries_file)
    else:
        if not libraries_dir.exists():
            os.makedirs(libraries_dir, exist_ok=True)
            create_libraries_json(libraries_file)
        else:
        # Check if libraries.json already exists
            if not libraries_file.exists():
                create_libraries_json(libraries_file)

def ensure_casm_and_libraries_folders() -> None:
    """Ensures that the libraries folder and libraries.json file exists
    """
    home_dir: Path = Path.home()
    casm_dir: Path = home_dir / ".casm"
    libraries_dir: Path = casm_dir / "libraries"
    libraries_file: Path = libraries_dir / "libraries.json"

    path_verification(casm_dir, libraries_dir, libraries_file)

ensure_casm_and_libraries_folders()

global_functions: dict[dict[Callable, int]] = {}


@cache
def load_libraries_json(File: str) -> list[dict[str, str]]:
    """Loads the libraries.json file

    Args:
        File (TextIOWrapper): 'libraries.json' opened text

    Returns:
        list: The list of libraries in the 'libraries.json'
    """
    library_data: dict = ujson.load(File)
    libraries: list = library_data.get("libraries", [])
    return libraries

class Module:
    def __init__(self, name: str, libraries_path: Path, path: str, library_file: str) -> None:
        self.name: str = name
        self.libraries_path: Path = libraries_path
        self.path: str = path
        self.library_file: str = library_file
        
        
        module_name: str = name.replace("-", "_")  # Convert hyphens to underscores
        spec = importlib.util.spec_from_file_location(module_name, f"{self.libraries_path}/{self.path}/{self.library_file}")
        self.module: ModuleType = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
    @cache
    def load_function(self, function_info: tuple) -> None:
        """Loads the function from the loaded module (self.module)

        Args:
            function_info (tuple): Function's name and arg count 
        """
        function_info = utils.td(function_info)
        function_name: str = function_info.get("name").lower()
        args_count: int = function_info.get("args", 0)
        call: Callable = function_info.get("call").lower() if function_info.get("call") != None else function_name
        if hasattr(self.module, function_name) and callable(getattr(self.module, function_name)):
            # If the function exists, register it with its name in global_functions
            global_functions[call if call else function_name] = {"function": getattr(self.module, function_name), "args": args_count}
        else:
            errorhandler.ModuleError(self.name, function_name)
    
    def load_functions(self, functions: list) -> None:
        for function_info in functions:
            self.load_function(utils.dt(function_info))
@cache
def load_export(libraries_path: Path, path: str) -> tuple[dict[str, list], str]:
    """Loads the export.json file of a library

    Args:
        libraries_path (Path): Path of the 'libraries/'
        path (str): Path of the library

    Returns:
        tuple[dict[str, list], str]: Returns the 'export.json' as a dict, and the library file .py name.
    """
    export: dict[str, list] = ujson.load(open(f"{libraries_path}/{path}/export.json", "r"))
    library_file: str = export.get("file")
    
    return export, library_file


def load_library_data(library: tuple) -> tuple[str, str]:
    """Loads the library's data

    Args:
        library (dict[str, str]): Library dict data

    Returns:
        tuple[str, str]: Name and path (separated)
    """
    library = utils.td(library)
    name: str = library.get("name")
    path: str = library.get("path")
    
    return name, path

def library_found(name: str, path: str, libraries_path: Path) -> None:
    """Function that's activated when the library has been found

    Args:
        name (str): Library's name
        path (str): Path to library
        libraries_path (Path): Path to 'libraries/'
    """
    export, library_file = load_export(libraries_path, path)

    module: Module = Module(name, libraries_path, path, library_file)

    functions: list = export.get("functions")

    module.load_functions(functions)

def scan_library(library: dict[str, str], library_name: str, libraries_path: Path) -> bool | None:
    """Scans a library to verify if it's the searched one

    Args:
        library (dict[str, str]): Library data
        library_name (str): Searched library name
        libraries_path (Path): 'libraries/' path

    Returns:
        bool: Returned if found
        None: Returned if not found
    """
    name, path = load_library_data(utils.dt(library))
                
    if name == library_name:
                    
        library_found(name, path, libraries_path)
                    
        return True

def scan_libraries(library_name: str, libraries_path: Path) -> bool:

    """Scan the libraries to search for the asked library

    Args:
        library_name (str): Name of the library to find
        libraries_path (Path): 'libraries/' path

    Returns:
        bool: Returns 'true' for found and loaded and 'false' for not found.
    """
    try:
        with open(f"{libraries_path}/libraries.json", "r") as File:
            libraries: list = load_libraries_json(File)

            for library in libraries:
                result: bool | None = scan_library(library, library_name, libraries_path)
                if result:
                    return result
            else:
                return False
    except Exception as e:
        raise e
    #    errorhandler.ScanError(e)