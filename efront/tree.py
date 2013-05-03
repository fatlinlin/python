import os
import logging

DEFAULT_SVN_ROOT = r"https://src.frontsrv.com/svn/repository/branches4/rsk"
DEFAULT_DISK_ROOT = r"c:\svn"

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

    def __repr__(self):
        return "{}(name={})".format(self.__class__.__name__, self.name)

    def __eq__(self, other):
        return self.name == other.name and type(self) == type(other)

class Trunk(Branch):

    def __init__(self):
        super(Trunk, self).__init__("trunk4.1")
        self.svn_root = r"https://src.frontsrv.com/svn/repository"

class MergePath(object):

    def __init__(self, paths):
        self.paths = paths

    def merge_targets(self, src_name):
        yield from self.merge_path_from(src_name)
        yield Trunk()

    def merge_path_from(self, src_name):
        if src_name not in self.paths:
            return
        dst = self.paths[src_name]
        yield Branch(dst)
        yield from self.merge_path_from(dst)

class BranchServer(object):

    def __init__(self):
        self.branches = {"trunk4.1" : Trunk()}

    def __getitem__(self, key):
        if key not in self.branches:
            self.branches[key] = Branch(key)
        return self.branches[key]

class Tree:

    def __init__(self, repo_graph, client):
        self.merge_path  = MergePath(repo_graph)
        self.branches = BranchServer()
        self.client = client

    def merge(self, src_name, revisions, target_names=None):
        branch = self.branches[src_name]
        commit_message = self.client.get_merge_commit_msg(branch.svn_path, revisions)
        logging.info(commit_message)
        if target_names is None:
            targets = self.merge_path.merge_targets(src_name)
        else:
            targets = (self.branches[name] for name in target_names)
        for dest_branch in targets:
            self.client.run(branch, dest_branch, revisions)

    def collect_logs(self, src_name):
        # broken
        raise NotImplementedError()
        branch = self.branches[src_name]
        messages = self.client.get_last_commit_info(branch)
        for dest_branch in branch.merge_targets():
            messages.extend(self.client.get_last_commit_info(dest_branch))
        self.client.write("ticket_message", messages)
        return messages

    def get_last_commit_revision(self, branch_name):
        return self.client.get_last_commit_revision(self.branches[branch_name])
