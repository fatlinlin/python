import argparse
import logging
from efront import iohelpers as io
from efront import svn
from efront import repo

def add_args(parser):
    parser.add_argument("srcdir", help="branch to switch to")
    parser.add_argument("-b", "--build", help="launch msbuild_RSK.bat", action="store_true")
    parser.add_argument("-u", "--update", help="update the repository", action="store_true")
    parser.add_argument("-d", "--dry_run", help="do not perform svn operations", action="store_true")
    parser.add_argument("-v", "--verbose", help="control the output level", action="store_true")

def run(args):
    io.setup_log("c:/switch", logging.DEBUG if args.verbose else logging.INFO)
    client = svn.SvnClient()
    path = repo.find_src_dir(args.srcdir)
    client = svn.SvnClient()
    client.dry_run = args.dry_run
    client.log_base_path = "c:/switch"
    if args.update:
        client.update(path)
    repo.switch(path)
    if args.build:
        client.compile(repo.DEV_DIR)

def setup():
    parser = argparse.ArgumentParser(description="Switch environnement")
    add_args(parser)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    run(setup())
