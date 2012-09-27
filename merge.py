import argparse
import io
import tree
import svn
import logging

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
                        action=client.task("log"),
                        nargs=1)
    args = parser.parse_args()
    io.setup_log("merge", logging.DEBUG if args.verbose else logging.INFO)
    repo_graph = [("40", []), ("50", []), ("60", ["65-mercator"])]
    client.dry_run = args.dry_run
    client.log_base_path = "./merge"
    myTree = tree.Tree(repo_graph, client)
    myTree.merge(args.branch, args.commit)

if __name__ == "__main__":
    run()
