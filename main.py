import argparse, interpreter

aparser = argparse.ArgumentParser()

version = "CrateAssembly 0.1.0"

aparser.add_argument("file", help="Files path")
aparser.add_argument("-v", "--version", action="version", version=version)

args = aparser.parse_args()

if args.file != None:
    interpreter.load_file(args.file)
else:
    print(args.file)