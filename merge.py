import argparse
import os
import json
import io
import tree
import svn
import logging

def setup_client(client, args):
    client.dry_run = args.dry_run
    client.log_base_path = "c:/merge"
    client.user = "sberg"

def get_repo_graph():
    with open(os.path.join(os.path.dirname(__file__), "merge.json")) as conf:
        return json.load(conf)

def run():
    client = svn.SvnClient()
    parser = argparse.ArgumentParser(description="merge tool")
    parser.add_argument("branch", help="the branch to merge")
    parser.add_argument("commit", help="the commit to merge", type=int)
    parser.add_argument("-d",
                        "--dry_run",
                        help="do not actually run the command",
                        action="store_true")
    parser.add_argument("-v",
                        "--verbose",
                        help="control the output level",
                        action="store_true")
    parser.add_argument("-c",
                        "--compile",
                        help="compiles the merged working copies",
                        action=client.task("compile"),
                        nargs=0)
    parser.add_argument("-l",
                        "--getlog",
                        help="collect the last logs of a user",
                        action="store_true")
    args = parser.parse_args()
    setup_client(client, args)
    io.setup_log("merge", logging.DEBUG if args.verbose else logging.INFO)
    myTree = tree.Tree(get_repo_graph(), client)
    if args.getlog:
        myTree.collect_logs(args.branch)
    else:
        myTree.merge(args.branch, args.commit)

if __name__ == "__main__":
    run()
