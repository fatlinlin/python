import argparse
import io
import tree

def run():
    io.setup_log("merge")
    tasks = set()
    parser = argparse.ArgumentParser(description="merge tool")
    parser.add_argument("branch", help="the branch to merge")
    parser.add_argument("commit", help="the commit to merge", type=int)
    parser.add_argument("-d",
                        "--dry_run",
                        help="do not actually run the command",
                        action="store_true")
    parser.add_argument("-u",
                        "--update",
                        help="updates the merged working copies",
                        action=tree.task("update"),
                        nargs=0)
    parser.add_argument("-c",
                        "--compile",
                        help="compiles the merged working copies",
                        action=tree.task("compile"),
                        nargs=0)
    args = parser.parse_args()
    myTree = tree.Tree()
    myTree.load_tree([("40", []), ("50", []), ("60", [])])
    myTree.merge(args.branch, args.commit, args.dry_run, tasks, "./merge.message.log")

if __name__ == "__main__":
    run()
