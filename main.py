import argparse, parser

aparser = argparse.ArgumentParser()

aparser.add_argument("-f", "--file")
aparser.add_argument("-v", "--version", action="version", version="CrateAssembly 0.0.1")

args = aparser.parse_args()

if args.file != None:
    parser.parse_file(args.file)
else:
    print(args.file)