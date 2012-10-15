import argparse
import io
import logging
import re

class SvnClient:

    def __init__(self):
        self.dry_run = True
        self.tasks = []
        self.taskNames = set()
        self.user = None
        self.log_base_path = None
        self.messages = []

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
        self.messages.append(self.get_commit_msg(source, revisions))

    def get_commit_msg(self, url, revisions):
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

    def write(self, suffix, lines):
        path = "{}.{}.log".format(self.log_base_path, suffix)
        logging.info("writing commit messages to {}".format(path))
        with open(path , "a") as fh:
            for msg in lines:
                fh.write('\n')
                fh.write(msg.strip())

    def write_commit_messages(self):
        self.write("commit_message", self.messages)

    def get_last_commit_info(self, branch, log_depth=10):
        lines = []
        io.cmd("svn log {} -v -l {}".format(branch.svn_path, log_depth), logger=lines.append)
        lines = list(self.parse_svn_log(lines))
        self.write("ticket_message", lines)

    def find_usr_commit(self, lines):
        usr_regex = re.compile("(\w*?) \| (\w*?) \|.*")
        for i, line in enumerate(lines):
            m = usr_regex.match(line)
            if m is None:
                continue
            if m.group(2) == self.user:
                return i
        raise RuntimeError("could not find user {} in logs".format(self.user))

    def parse_svn_log(self, lines):
        i = self.find_usr_commit(lines)
        for line in lines[i:]:
            if line.startswith("--"):
                yield ""
                yield "-" * 50
                yield ""
                return
            yield line
        return

    def run(self, source, dest, rev):
        self.update(dest.disk_path)
        self.merge(
            source.svn_path,
            rev,
            dest.disk_path)
        if "compile" in self.tasks:
            self.compile(dest.disk_path)
