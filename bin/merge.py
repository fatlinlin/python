import argparse
import os
import json
import logging
from efront import iohelpers as io
from efront import tree
from efront import svn
from efront import repo

CLIENT = svn.SvnClient()

def setup_client(args, conf):
    CLIENT.dry_run = args.dry_run
    CLIENT.log_base_path = conf["log"]
    CLIENT.user = conf["user"]

def load_conf():
    with open(os.path.join(os.path.dirname(__file__), "merge.json")) as conf:
        return json.load(conf)

def add_args(parser):
    parser.add_argument("-b",
                        "--branch",
                        help="the branch to merge (default: the current branch in dev4.1)")
    parser.add_argument("-r",
                        "--revisions",
                        help="the commits to merge (defaults: the last commit by the user in the branch to be merged)",
                        type=int,
                        nargs='+')
    parser.add_argument("-t",
                        "--targets",
                        help="the targets of the merge (default: the list of more recent main branches)",
                        nargs='+')
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
                        action=CLIENT.task("compile"),
                        nargs=0)
    parser.add_argument("-l",
                        "--getlog",
                        help="collect the last logs of a user",
                        action="store_true")

def run(args):
    conf = load_conf()
    setup_client(args, conf)
    io.setup_log(conf["log"], logging.DEBUG if args.verbose else logging.INFO)
    myTree = tree.Tree(conf["repo"], CLIENT)
    if args.branch is None:
        args.branch = os.path.basename(repo.get_current_target())
        logging.info("using current branch: {}".format(args.branch))
    if args.revisions is None:
        args.revisions = [myTree.get_last_commit_revision(args.branch)]
        logging.info("using last commit from {}: {}".format(CLIENT.user, args.revisions[0]))
    args.revisions.sort()
    if args.getlog:
        myTree.collect_logs(args.branch)
    elif args.targets:
        myTree.merge(args.branch, args.revisions, args.targets)
    else:
        myTree.merge(args.branch, args.revisions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="merge tool")
    add_args(parser)
    args = parser.parse_args()
    run(args)
