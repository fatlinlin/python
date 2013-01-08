import argparse
import logging
import io
import svn
import repo

def setup():
    client = svn.SvnClient()
    parser = argparse.ArgumentParser(description="Switch environnement")
    parser.add_argument("srcdir", help="branch to switch to", default=None, nargs="?")
    parser.add_argument("-b", "--build", help="launch msbuild_RSK.bat", action="store_true")
    parser.add_argument("-u", "--update", help="update the repository", action="store_true")
    parser.add_argument("-d", "--dry_run", help="do not perform svn operations", action="store_true")
    parser.add_argument("-v", "--verbose", help="control the output level", action="store_true")
    parser.add_argument("-l", "--dir_list", help="list available dirs", action="store_true")
    args = parser.parse_args()
    io.setup_log("c:/switch", logging.DEBUG if args.verbose else logging.INFO)
    return args

def run(args):
    if args.srcdir is None:
        logging.info("currently on {}".format(repo.get_current_target()))
        if args.dir_list:
            repo.list_dirs(logging.info)
        return
    path = repo.find_src_dir(args.srcdir)
    client = svn.SvnClient()
    client.dry_run = args.dry_run
    client.log_base_path = "c:/switch"
    if args.update:
        client.update(path)
    repo.switch(path)
    if args.build:
        client.compile(repo.DEV_DIR)

if __name__ == "__main__":
    run(setup())
