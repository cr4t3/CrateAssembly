import argparse, interpreter

aparser = argparse.ArgumentParser()

unstable = True

version = "CrateAssembly 0.3.0" + " (Unstable)" if unstable else ""

aparser.add_argument("file", help="Files path")
aparser.add_argument("-v", "--version", action="version", version=version)
aparser.add_argument("--ignore-status-codes", action="store_true")

args = aparser.parse_args()

if __name__ == "__main__":
    if args.file != None:
        interpreter.load_file(args.file)
    else:
        print(args.file)