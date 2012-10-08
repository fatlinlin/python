import argparse
import re
import os
import logging
import io
import svn

DEV_DIR = r"c:\dev4.1"
ROOTS = [
    r"c:\svn",
    r"c:\git",
    ]

def get_current_target():
    regex = re.compile("<JUNCTION> +dev4\.1 \[(.*)\]")
    matches = []
    def get_match(line):
        m = regex.search(line)
        if m is None:
            return
        matches.append(m.group(1))
    io.cmd("dir", cwd="c:\\", logger=get_match)
    assert len(matches) == 1
    return matches[0]

def remove_junction(junction_path):
    io.cmd("rmdir {}".format(junction_path), logger=logging.debug)

def create_junction(dev_dir, srcdir):
    logging.info("creating a junction to the repository between {} and {}".format(dev_dir, srcdir))
    io.cmd("mklink /J {} {}".format(dev_dir, os.path.abspath(srcdir)), logger=logging.debug)

def switch(srcdir):
    if os.path.exists(DEV_DIR):
        remove_junction(DEV_DIR)
    create_junction(DEV_DIR, srcdir)
    if os.path.exists(os.path.join(DEV_DIR, "Switch.cmd")):
        logging.info("Running Switch.cmd")
        io.cmd("Switch.cmd", cwd=DEV_DIR, logger=logging.getLogger("Switch.cmd").debug)

def find_src_dir(path):
    true_dirs = filter(os.path.exists, [os.path.join(root, path) for root in ROOTS] + [os.path.abspath(path)])
    true_dirs = list(set(true_dirs))
    if len(true_dirs) == 0:
        raise Exception("{} not found".format(path))
    if len(true_dirs) > 1:
        print "\n".join("{} - {}".format(i, p) for i, p in enumerate(true_dirs))
        selection = int(raw_input("please select source: "))
    else:
        selection = 0
    return true_dirs[selection]

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
    io.setup_log("switch", logging.DEBUG if args.verbose else logging.INFO)
    return args
    
def list_dirs(log):
    log("available dirs:")
    dirs = []
    for root in ROOTS:
        for dirname in os.listdir(root):
            if not os.path.exists(os.path.join(root, dirname, "msbuild_RSK.bat")):
                continue
            dirs.append(dirname)
    dirs = list(set(dirs))
    dirs.sort()
    for dirname in dirs:
        log("- {}".format(dirname))
    
def run(args):
    if args.srcdir is None:
        logging.info("currently on {}".format(get_current_target()))
        if args.dir_list:
            list_dirs(logging.info)
        return
    path = find_src_dir(args.srcdir)
    client = svn.SvnClient()
    client.dry_run = args.dry_run
    client.log_base_path = "c:/merge"
    if args.update:
        client.update(path)
    switch(path)
    if args.build:
        client.compile(DEV_DIR)
    
if __name__ == "__main__":
    run(setup())
