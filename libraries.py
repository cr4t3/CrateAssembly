import importlib.util
import json, os
from pathlib import Path
from types import ModuleType
from io import TextIOWrapper
import errorhandler

def create_libraries_json(path: Path) -> None:
    """create_libraries_json creates the libraries.json file in the given path

    Args:
        path (Path): Path to create libraries.json
    """
    with open(path, "w") as file:
        file.write("{\"libraries\":[]}")

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
    home_dir = Path.home()
    casm_dir = home_dir / ".casm"
    libraries_dir = casm_dir / "libraries"
    libraries_file = libraries_dir / "libraries.json"

    path_verification(casm_dir, libraries_dir, libraries_file)

ensure_casm_and_libraries_folders()

global_functions = {}

def load_libraries_json(File: TextIOWrapper) -> list:
    """Loads the libraries.json file

    Args:
        File (TextIOWrapper): 'libraries.json' opened text

    Returns:
        list: The list of libraries in the 'libraries.json'
    """
    library_data: dict = json.load(File)
    libraries: list = library_data.get("libraries", [])
    return libraries

class Module:
    def __init__(self, name, libraries_path, path, library_file):
        self.name = name
        self.libraries_path = libraries_path
        self.path = path
        self.library_file = library_file
        
        
        module_name = name.replace("-", "_")  # Convert hyphens to underscores
        spec = importlib.util.spec_from_file_location(module_name, f"{libraries_path}/{path}/{library_file}")
        self.module: ModuleType = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
    
    def load_function(self, function_info: dict) -> None:
        """Loads the function from the loaded module (self.module)

        Args:
            function_info (dict): Function's name and arg count 
        """
        function_name = function_info.get("name")
        args_count = function_info.get("args", 0)
        call = function_info.get("call") if function_info.get("call") != None else function_name
        if hasattr(self.module, function_name) and callable(getattr(self.module, function_name)):
            # If the function exists, register it with its name in global_functions
            global_functions[call if call else function_name] = {"function": getattr(self.module, function_name), "args": args_count}
        else:
            errorhandler.ModuleError(self.name, function_name)

def scan_libraries(library_name: str, libraries_path: Path) -> bool:
    """Scan the libraries to search foor the asked library

    Args:
        library_name (str): Name of the library to find
        libraries_path (Path): 'libraries/' path

    Returns:
        bool: Returns 'true' for found and 'false' for not found or error.
    """
    try:
        with open(f"{libraries_path}/libraries.json", "r") as File:
            libraries = load_libraries_json(File)

            for library in libraries:
                name = library.get("name")
                path = library.get("path")
                
                if name == library_name:
                    export = json.load(open(f"{libraries_path}/{path}/export.json", "r"))
                    library_file = export.get("file")

                    module = Module(name, path, library_file, libraries_path)

                    functions = export.get("functions")

                    for function_info in functions:
                        module.load_function(function_info, name)
                    return True
            else:
                return False
    except Exception as e:
        print(f"[library.py]: scan_libraries function has thrown an error: {e}")
        return False