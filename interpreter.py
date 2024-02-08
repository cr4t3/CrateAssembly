# Parse file into the expected functions
import libraries, errorhandler

def interpret_file(file: str):
    with open(file, "r") as script:
        content = script.read().rsplit("\n")

        for line in content:
            if not line.startswith(";"):
                args = line.split(" ")
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
                    elif functionDone:
                        pass
                    elif arg == "include":
                        functionDone = True
                        if len(args) == 2:
                            found = libraries.scan_libraries_source(args[1])
                            if not found:
                                found2 = libraries.scan_libraries_home(args[1])
                                if not found2:
                                    print(f"Library \"{args[1]}\" not found")
                                    exit()
                        else:
                            errorhandler.LengthError("include", 1, len(args)-1)
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
                            errorhandler.LengthError(arg, arg_count, ((len(args)-1)-(len(args)-readUntil) if readUntil != -1 else len(args)-1))
                            exit()
                    else:
                        errorhandler.DefinitionError(arg)
                        exit()