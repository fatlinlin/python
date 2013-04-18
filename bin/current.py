import argparse
import logging
from efront import iohelpers as io
from efront import repo

def add_args(parser):
    parser.add_argument("-l", "--dir_list", help="list available dirs", action="store_true")
    parser.add_argument("-v", "--verbose", help="control the output level", action="store_true")

def run(args):
    io.setup_log("c:/current", logging.DEBUG if args.verbose else logging.INFO)
    logging.info("currently on {}".format(repo.get_current_target()))
    if args.dir_list:
        repo.list_dirs(logging.info)

def setup():
    parser = argparse.ArgumentParser(description="Switch environnement")
    add_args(parser)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    run(setup())
