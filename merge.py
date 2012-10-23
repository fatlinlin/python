import argparse
import os
import json
import logging
import io
import tree
import svn
import repo

def setup_client(client, args, conf):
    client.dry_run = args.dry_run
    client.log_base_path = conf["log"]
    client.user = conf["user"]

def load_conf():
    with open(os.path.join(os.path.dirname(__file__), "merge.json")) as conf:
        return json.load(conf)

def add_args(parser, client):
    parser.add_argument("-b",
                        "--branch",
                        help="the branch to merge")
    parser.add_argument("-r",
                        "--revisions",
                        help="the commits to merge",
                        type=int,
                        nargs='+')
    parser.add_argument("-t",
                        "--targets",
                        help="the targets of the merge",
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
                        action=client.task("compile"),
                        nargs=0)
    parser.add_argument("-l",
                        "--getlog",
                        help="collect the last logs of a user",
                        action="store_true")

def run():
    client = svn.SvnClient()
    parser = argparse.ArgumentParser(description="merge tool")
    add_args(parser, client)
    args = parser.parse_args()
    conf = load_conf()
    setup_client(client, args, conf)
    io.setup_log(conf["log"], logging.DEBUG if args.verbose else logging.INFO)
    myTree = tree.Tree(conf["repo"], client)
    if args.branch is None:
        args.branch = os.path.basename(repo.get_current_target())
        logging.info("using current branch: {}".format(args.branch))
    if args.revisions is None:
        args.revisions = [myTree.get_last_commit_revision(args.branch)]
        logging.info("using last commit from {}: {}".format(client.user, args.revisions[0]))
    if args.getlog:
        myTree.collect_logs(args.branch)
    elif args.targets:
        myTree.merge(args.branch, args.revisions, args.targets)
    else:
        myTree.merge(args.branch, args.revisions)

if __name__ == "__main__":
    run()
