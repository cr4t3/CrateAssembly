import importlib.util
import json, os
from pathlib import Path

SOURCE_LIBRARIES_PATH = "libraries"

HOME_LIBRARIES_PATH = Path.home() / ".casm/libraries"

def ensure_casm_and_libraries_folders():
    home_dir = Path.home()
    casm_dir = home_dir / ".casm"
    libraries_dir = casm_dir / "libraries"
    libraries_file = libraries_dir / "libraries.json"

    if not casm_dir.exists():
            os.makedirs(casm_dir, exist_ok=True)
            os.makedirs(libraries_dir, exist_ok=True)
            with open(libraries_file, "w") as file:
                file.write("{\"libraries\":[]}")
    else:
        if not libraries_dir.exists():
            os.makedirs(libraries_dir, exist_ok=True)
            with open(libraries_file, "w") as file:
                file.write("{\"libraries\":[]}")
        else:
        # Check if libraries.json already exists
            if not libraries_file.exists():
                with open(libraries_file, "w") as file:
                    file.write("{\"libraries\":[]}")

ensure_casm_and_libraries_folders()

global_functions = {}

def scan_libraries_source(library_name):
    try:
        with open(f"{SOURCE_LIBRARIES_PATH}/libraries.json", "r") as file:
            library_data = json.load(file)
            libraries = library_data.get("libraries", [])

            for library in libraries:
                name = library.get("name")
                path = library.get("path")
                
                if name == library_name:
                    export = json.load(open(f"{SOURCE_LIBRARIES_PATH}/{path}/export.json", "r"))
                    file = export.get("file")

                    module_name = name.replace("-", "_")  # Convert hyphens to underscores
                    spec = importlib.util.spec_from_file_location(module_name, f"{SOURCE_LIBRARIES_PATH}/{path}/{file}")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    functions = export.get("functions")

                    for function_info in functions:
                        function_name = function_info.get("name")
                        args_count = function_info.get("args", 0)
                        call = function_info.get("call") if function_info.get("call") != None else function_name

                        if hasattr(module, function_name) and callable(getattr(module, function_name)):
                            # If the function exists, register it with its name in global_functions
                            global_functions[call if call else function_name] = {"function": getattr(module, function_name), "args": args_count}
                        else:
                            print(f"{name} module does not have the expected function: {function_name}")
                    return True
            else:
                return False
    except Exception as e:
        print(f"[library.py]: scan_libraries_source function has thrown an error: {e}")
        return False

def scan_libraries_home(library_name):
    try:
        with open(f"{HOME_LIBRARIES_PATH}/libraries.json", "r") as file:
            library_data = json.load(file)
            libraries = library_data.get("libraries", [])

            for library in libraries:
                name = library.get("name")
                path = library.get("path")

                if name == library_name:
                    export = json.load(open(f"{HOME_LIBRARIES_PATH}/{path}/export.json", "r"))
                    file = export.get("file")

                    module_name = name.replace("-", "_")  # Convert hyphens to underscores
                    spec = importlib.util.spec_from_file_location(module_name, f"{HOME_LIBRARIES_PATH}/{path}/{file}")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    functions = export.get("functions")

                    for function_info in functions:
                        function_name = function_info.get("name")
                        args_count = function_info.get("args", 0)
                        call = function_info.get("call") if function_info.get("call") != None else function_name

                        if hasattr(module, function_name) and callable(getattr(module, function_name)):
                            # If the function exists, register it with its name in global_functions
                            global_functions[call if call else function_name] = {"function": getattr(module, function_name), "args": args_count}
                        else:
                            print(f"{name} module does not have the expected function: {function_name}")
                    return True
                else:
                    return False
    except Exception as e:
        print(f"[library.py]: scan_libraries_home function has thrown an error: {e}")
        return False