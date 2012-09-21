import argparse
import io
import logging

class SvnClient:

    def __init__(self):
        self.dry_run = True
        self.tasks = []
        self.taskNames = set()
        self.user = None

    def task(self, *names):
        class TaskAction(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                map(self.taskNames.add, names)
        return TaskAction

    def cmd(self, cmd):
        io.cmd(cmd,
               dry_run=self.dry_run,
               logger=logging.getLogger("svn").debug)

    def merge(self, source, revision, dest):
        logging.info("merging {}@{} to {}".format(source, revision, dest))
        self.cmd("svn merge -r {}:{} {} {}".format(revision - 1, revision, source, dest))
        return self.get_commit_msg(source, revision)

    def get_commit_msg(self, url, revision):
        lines = []
        io.cmd("svn log {} -r {}".format(url, revision), logger=lines.append)
        return "\n".join(["merged from {}@{}".format(url, revision)] + lines[4:-1])

    def update(self, repo):
        logging.info("updating {}".format(repo))
        self.cmd("svn update {}".format(repo))

    def run(self, source, dest, rev):
        self.update(dest.disk_path)
        self.messages.append(self.client.merge(
            source.svn_path,
            rev,
            dest.disk_path))
        if "compile" in self.tasks:
            io.cmd(
                "msbuild_RSK.bat",
                cwd=dest_branch.disk_path,
                logger=logging.getLogger("msbuild_RSK.bat").debug)
