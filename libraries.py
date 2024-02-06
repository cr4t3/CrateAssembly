import importlib.util
import json

LIBRARIES_PATH = "libraries"

global_functions = {}

def scan_libraries(library_name):
    try:
        with open(f"{LIBRARIES_PATH}/libraries.json", "r") as file:
            library_data = json.load(file)
            libraries = library_data.get("libraries", [])

            for library in libraries:
                name = library.get("name")
                path = library.get("path")

                if name == library_name:
                    export = json.load(open(f"{LIBRARIES_PATH}/{path}/export.json", "r"))
                    file = export.get("file")

                    module_name = name.replace("-", "_")  # Convert hyphens to underscores
                    spec = importlib.util.spec_from_file_location(module_name, f"{LIBRARIES_PATH}/{path}/{file}")
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

    except Exception as e:
        print(f"[library.py]: scan_libraries function has thrown an error: {e}")