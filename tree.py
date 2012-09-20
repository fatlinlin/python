import os
import argparse
import io
import logging

DEFAULT_SVN_ROOT = r"https://src.frontsrv.com/svn/repository/branches4/rsk"
DEFAULT_DISK_ROOT = r"c:\svn"


def task(*names):
    class TaskAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            map(tasks.add, names)
    return TaskAction

class Branch(object):

    def __init__(self, name):
        self.name = name
        self.disk_root = DEFAULT_DISK_ROOT
        self.svn_root = DEFAULT_SVN_ROOT

    @property
    def svn_path(self):
        return "{}/{}".format(self.svn_root, self.name)

    @property
    def disk_path(self):
        return os.path.join(self.disk_root, self.name)

    def next(self):
        raise NotImplementedError()

    def __repr__(self):
        return "{}(name={})".format(self.__class__.__name__, self.name)

class ClientBranch(Branch):

    def __init__(self, name, parent):
        super(ClientBranch, self).__init__(name)
        self.parent = parent

    def next(self):
        return self.parent.next_version

class MainBranch(Branch):

    def __init__(self, name, next_version):
        super(MainBranch, self).__init__(name)
        self.next_version = next_version

    def next(self):
        return self.next_version

class Trunk(Branch):

    def __init__(self):
        super(Trunk, self).__init__("trunk4.1")
        self.svn_root = r"https://src.frontsrv.com/svn/repository"

    def next(self):
        raise StopIteration()
        
class Tree:

    def __init__(self):
        self.branches = {"trunk4.1" : Trunk()}

    def load_main_branches(self, names, head):
        try:
            name = names.pop()
        except IndexError:
            return []
        branch = MainBranch(name, head)
        self.branches[name] = branch
        return self.load_main_branches(names, branch) + [branch]

    def load_client_branches(self, client_grps, main_branches):
        for main, clients in zip(main_branches, client_grps):
            for client in clients:
                self.branches[client] = ClientBranch(client, main)
   
    def load_tree(self, branches):
        main_branches_names, clients_grps = zip(*branches)
        main_branches = self.load_main_branches(list(main_branches_names), self.branches["trunk4.1"])
        self.load_client_branches(clients_grps, main_branches)
        
    def merge(self, src_name, commit, dry_run, tasks, message_log_path):
        branch = self.branches[src_name]
        dest_branch = branch.next()
        client = SvnClient(dry_run)
        try:
            while True:
                client.update(dest_branch.disk_path)
                client.merge(
                    branch.svn_path,
                    commit,
                    dest_branch.disk_path)
                if "compile" in tasks:
                    io.cmd(
                        "msbuild_RSK.bat",
                        cwd=dest_branch.disk_path,
                        logger=logging.getLogger("msbuild_RSK.bat").debug)
                dest_branch = dest_branch.next()
        except StopIteration:
            logging.info("trunk reached")
            
class SvnClient:

    def __init__(self, dry_run):
        self.dry_run = dry_run

    def cmd(self, cmd):
        io.cmd(cmd,
               dry_run=self.dry_run,
               logger=logging.getLogger("svn").debug)

    def merge(self, source, revision, dest):
        logging.info("merging {}@{} to {}".format(source, revision, dest))
        self.cmd("svn merge -r {}:{} {} {}".format(revision - 1, revision, source, dest))

    def update(self, repo):
        logging.info("updating {}".format(repo))
        self.cmd("svn update {}".format(repo))

if __name__ == "__main__":
    tree = Tree()
    tree.load_tree([("40", []), ("50", []), ("60", [])])
    print "merging 40"
    tree.merge("40", None)
    
