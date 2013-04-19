import argparse
import logging
import re
import os
from efront import iohelpers as io

DEV_DIR = r"c:\dev4.1"
TRUNK_DIR = r"c:\SVN\trunk4.1"
CONVERTER = "ProjectConverter"
CONVERTER_PATH = os.path.join(TRUNK_DIR, "tools", CONVERTER)
RSK_DIR = os.path.join(DEV_DIR, "srcrsk")

class SvnClient:

    def __init__(self):
        self.dry_run = True
        self.tasks = []
        self.taskNames = set()
        self.user = None
        self.log_base_path = None

    def task(self, *names):
        class TaskAction(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                map(self.taskNames.add, names)
        return TaskAction

    def cmd(self, cmd):
        io.cmd(cmd,
               dry_run=self.dry_run,
               logger=logging.getLogger("svn").debug)

    def merge(self, source, revisions, dest):
        logging.info("merging {}@{} to {}".format(source, ",".join(map(str,revisions)), dest))
        revision_cmd = " ".join("-c {}".format(r) for r in revisions)
        self.cmd("svn merge {} {} {} --accept postpone".format(revision_cmd, source, dest))

    def get_merge_commit_msg(self, url, revisions):
        blocks = []
        for revision in revisions:
            lines = []
            io.cmd("svn log {} -r {}".format(url, revision), logger=lines.append)
            blocks.append("\n".join(lines[4:-1]))
        return "\n".join(["merged from {}@{}".format(url, ",".join(map(str,revisions)))] + blocks)

    def update(self, repo):
        logging.info("updating {}".format(repo))
        self.cmd("svn update {}".format(repo))

    def compile(self, path):
        io.run_script(path, "build_rt.bat")
        io.run_script(path, "msbuild_RSK.bat")
        if os.path.exists(os.path.join(path, "msbuild_FrontCube.bat")):
            io.run_script(path, "msbuild_FrontCube.bat")
        if os.path.exists(os.path.join(RSK_DIR, "vs2008.srcrsk.All.xml")):
            logging.info("Running ProjectConverter")
            io.cmd(CONVERTER + ".exe " + os.path.join(RSK_DIR, "vs2008.srcrsk.All.xml"),
                   cwd=CONVERTER_PATH,
                   logger=logging.getLogger(CONVERTER).debug)
        logging.info("Generating vb model")
        frontAdminPath = os.path.join(DEV_DIR, "website", "bin")
        io.cmd("FrontAdmin.exe" + " /generatevbmodel /x",
               cwd=frontAdminPath,
               logger=logging.getLogger("FrontAdmin").debug)

    def write(self, suffix, lines):
        path = "{}.{}.log".format(self.log_base_path, suffix)
        logging.info("writing to {}".format(path))
        with open(path , "w") as fh:
            for msg in lines:
                fh.write('\n')
                fh.write(msg.strip())

    def get_last_commit_info(self, branch, log_depth=10):
        lines = []
        io.cmd("svn log {} -l {}".format(branch.svn_path, log_depth), logger=lines.append)
        return self.find_usr_commit(lines)

    def find_usr_commit(self, lines):
        usr_regex = re.compile("r(\w+?) \| (\w+?) \|.*")
        empty_line_it = filter(bool, lines) # iterator ignoring empty lines
        for line in empty_line_it:
            m = usr_regex.match(line)
            if m is None:
                continue
            if m.group(2) == self.user:
                break
        if m is None or m.group(2) != self.user:
            raise RuntimeError("could not find user {} in logs".format(self.user))
        description = next(empty_line_it)
        return {"user" : m.group(2),
                "revision" : int(m.group(1)),
                "description" : description}

    def run(self, source, dest, revisions):
        self.update(dest.disk_path)
        self.merge(
            source.svn_path,
            revisions,
            dest.disk_path)
        if "compile" in self.tasks:
            self.compile(dest.disk_path)
