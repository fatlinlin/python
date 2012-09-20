import argparse
import os
import logging
import io

DEV_DIR = r"c:\dev4.1"
ROOTS = [
    r"c:\svn",
    r"c:\git",
    ]

def remove_junction(junction_path):
    io.cmd("rmdir {}".format(junction_path))

def create_junction(dev_dir, srcdir):
    io.cmd("mklink /J {} {}".format(dev_dir, os.path.abspath(srcdir)))

def switch(srcdir):
    if os.path.exists(DEV_DIR):
        remove_junction(DEV_DIR)
    srcdir = find_src_dir(srcdir)
    create_junction(DEV_DIR, srcdir)
    if os.path.exists(os.path.join(DEV_DIR, "Switch.cmd")):
        logging.info("Running Switch.cmd")
        io.cmd("Switch.cmd", cwd=DEV_DIR, logger=logging.getLogger("Switch.cmd").debug)
    logging.info("success")

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Switch environnement")
    parser.add_argument("srcdir")
    args = parser.parse_args()
    io.setup_log("switch")
    switch(args.srcdir)

