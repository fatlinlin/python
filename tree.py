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

    def __init__(self, repo_graph, client):
        self.branches = {"trunk4.1" : Trunk()}
        self.load_tree(repo_graph)
        self.client = client
        
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
        
                
    def merge(self, src_name, commit):
        branch = self.branches[src_name]
        dest_branch = branch.next()
        messages = []
        try:
            while True:
                messages.append(self.client.run(branch, dest_branch, commit))
                dest_branch = dest_branch.next()
        except StopIteration:
            logging.info("trunk reached")
        finally:
            self.client.write_commit_messages()

if __name__ == "__main__":
    tree = Tree()
    tree.load_tree([("40", []), ("50", []), ("60", [])])
    print "merging 40"
    tree.merge("40", None)
    
