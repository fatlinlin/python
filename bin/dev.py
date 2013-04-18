import argparse
import merge
import switch
import current

TOOLS = {
    "merge" : merge,
    "switch" : switch,
    "current" : current,
    }

def run():
    parser = argparse.ArgumentParser(description="environement management tool")
    subparsers = parser.add_subparsers(title="actions", dest="tool_name")
    for name, tool in TOOLS.items():
        tool.add_args(subparsers.add_parser(name))
    args = parser.parse_args()
    if args.tool_name is None:
        print("no command")
        return
    TOOLS[args.tool_name].run(args)

if __name__ == "__main__":
    run()
