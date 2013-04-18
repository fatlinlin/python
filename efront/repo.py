import logging
import re
import os
from efront import iohelpers as io

DEV_DIR = r"c:\dev4.1"
ROOTS = [
    r"c:\svn",
    r"c:\git",
    ]

def get_current_target():
    regex = re.compile("<JUNCTION> +dev4\.1 \[(.*)\]")
    matches = []
    def get_match(line):
        m = regex.search(str(line))
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
        print("\n".join("{} - {}".format(i, p) for i, p in enumerate(true_dirs)))
        selection = int(raw_input("please select source: "))
    else:
        selection = 0
    return true_dirs[selection]


class Target:

    root_names = list(map(os.path.basename, ROOTS))
    root_names.sort()

    def __init__(self, name):
        self.name = name
        self.srcs = set()

    def add(self, root):
        self.srcs.add(os.path.basename(root))

    def _get_src(self, root):
        return root if root in self.srcs else " " * len(root)

    def __str__(self):
        return " ".join([self._get_src(root) for root in self.root_names] + [self.name])

def list_dirs(log):
    log("available dirs:")
    dirs = {}
    for root in ROOTS:
        for dirname in os.listdir(root):
            if not os.path.exists(os.path.join(root, dirname, "msbuild_RSK.bat")):
                continue
            if not dirname in dirs:
                dirs[dirname] = Target(dirname)
            dirs[dirname].add(root)

    dirs_list = list(set(dirs))
    dirs_list.sort()
    for dirname in dirs_list:
        log(str(dirs[dirname]))
