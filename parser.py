# Parse file into the expected functions
import libraries

def parse_file(file: str):
    with open(file, "r") as script:
        content = script.read().rsplit("\n")

        for line in content:
            if not line.startswith(";"):
                args = line.split(" ")
                lineImport = False
                functionDone = False
                readUntil = 0

                for i in range(len(args)):
                    arg = args[i]
                    if arg.startswith(";"):
                        readUntil = i
                        break
                else:
                    readUntil = -1

                for i in range(len(args)):
                    arg = args[i]
                    if arg.startswith(";") or arg == "":
                        break
                    elif arg == "include":
                        lineImport = True
                        if len(args) == 2:
                            libraries.scan_libraries(args[1])
                        else:
                            print(f"Error: {arg} required {2} arguments and recieved {len(args)}")
                            exit()
                    elif arg in list(libraries.global_functions.keys()):
                        function_info = libraries.global_functions[arg]
                        arg_count = function_info["args"]
                        function = function_info["function"]

                        if ((len(args)-1)-(len(args)-readUntil) if readUntil != -1 else len(args)-1) == arg_count:
                            arg_list = []
                            for i in range((len(args)-1)-(len(args)-readUntil) if readUntil != -1 else len(args)-1):
                                arg_list.append("'" + (args[i+1]) + "'")
                            eval(f"function({', '.join(arg_list)})")
                            functionDone = True
                        else:
                            print(f"Error: {arg} required {arg_count} arguments and recived {((len(args)-1)-(len(args)-readUntil) if readUntil != -1 else len(args)-1)}")
                            exit()
                    elif lineImport or functionDone:
                        pass
                    else:
                        print(f"Error: {arg} not found!")
                        exit()