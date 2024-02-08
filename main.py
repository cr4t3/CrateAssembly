import argparse, interpreter

aparser = argparse.ArgumentParser()

aparser.add_argument("file", help="Files path")
aparser.add_argument("-v", "--version", action="version", version="CrateAssembly 0.1.0")

args = aparser.parse_args()

if args.file != None:
    interpreter.interpret_file(args.file)
else:
    print(args.file)