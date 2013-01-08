import unittest
from efront import tree
from efront import svn
from mock import Mock

class TestTree(unittest.TestCase):

    def setUp(self):
        fakeClient = Mock()
        self.tree = tree.Tree((("1", []), ("2", []), ("3", [])), fakeClient)

    def test_merge(self):
        self.tree.merge("1", 18)
        self.tree.client.run.assert_any_call(tree.MainBranch("1", None), tree.MainBranch("2", None), 18)
        self.tree.client.run.assert_any_call(tree.MainBranch("1", None), tree.MainBranch("3", None), 18)
        self.tree.client.run.assert_any_call(tree.MainBranch("1", None), tree.Trunk(), 18)

    def test_merge_2(self):
        self.tree.merge("2", 18)
        self.tree.client.run.assert_any_call(tree.MainBranch("2", None), tree.MainBranch("3", None), 18)
        self.tree.client.run.assert_any_call(tree.MainBranch("2", None), tree.Trunk(), 18)

    def test_logs(self):
        self.tree.collect_logs("1")
        self.tree.client.get_last_commit_info.assert_any_call(tree.MainBranch("2", None))
        self.tree.client.get_last_commit_info.assert_any_call(tree.MainBranch("3", None))

if __name__ == '__main__':
    unittest.main()
