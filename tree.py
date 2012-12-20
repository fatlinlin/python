import os
import logging

DEFAULT_SVN_ROOT = r"https://src.frontsrv.com/svn/repository/branches4/rsk"
DEFAULT_DISK_ROOT = r"c:\svn"

class BranchIterator(object):

    def __init__(self, branch):
        self.branch = branch

    def __iter__(self):
        return self

    def next(self):
        self.branch = self.branch.next()
        return self.branch

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

    def merge_targets(self):
        return BranchIterator(self)

    def next(self):
        raise NotImplementedError()

    def __repr__(self):
        return "{}(name={})".format(self.__class__.__name__, self.name)

    def __eq__(self, other):
        return self.name == other.name and type(self) == type(other)

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

    def __init__(self, repo_graph, client):
        self.branches = {"trunk4.1" : Trunk()}
        self.load_tree(repo_graph)
        self.client = client

    def _load_main_branches(self, names, head):
        try:
            name = names.pop()
        except IndexError:
            return []
        branch = MainBranch(name, head)
        self.branches[name] = branch
        return self._load_main_branches(names, branch) + [branch]

    def _load_client_branches(self, client_grps, main_branches):
        for main, clients in zip(main_branches, client_grps):
            for client in clients:
                self.branches[client] = ClientBranch(client, main)

    def load_tree(self, branches):
        main_branches_names, clients_grps = zip(*branches)
        main_branches = self._load_main_branches(list(main_branches_names), self.branches["trunk4.1"])
        self._load_client_branches(clients_grps, main_branches)
        # hack!!!
        # move to xml mergeinfo to fix
        #
        if "65-mercator" in self.branches:
            self.branches["65-mercator"].next = lambda : self.branches["65-mercator2"]

    def merge(self, src_name, commits, target_names=None):
        branch = self.branches[src_name]
        if target_names is None:
            targets = branch.merge_targets()
        else:
            targets = (self.branches[name] for name in target_names)
        for dest_branch in targets:
            self.client.run(branch, dest_branch, commits)
        self.client.write_commit_messages()

    def collect_logs(self, src_name):
        branch = self.branches[src_name]
        messages = self.client.get_last_commit_info(branch)
        for dest_branch in branch.merge_targets():
            messages.extend(self.client.get_last_commit_info(dest_branch))
        self.client.write("ticket_message", messages)
        return messages

    def get_last_commit_revision(self, branch_name):
        return self.client.get_last_commit_revision(self.branches[branch_name])
