import unittest
from efront import tree
from efront import svn
from mock import Mock

class TestTree(unittest.TestCase):

    def setUp(self):
        fakeClient = Mock()
        self.tree = tree.Tree({
                "1" : "2",
                "2" : "3"
                },
            fakeClient
            )

    def test_merge(self):
        self.tree.merge("1", 18)
        self.tree.client.run.assert_any_call(tree.Branch("1"), tree.Branch("2"), 18)
        self.tree.client.run.assert_any_call(tree.Branch("1"), tree.Branch("3"), 18)
        self.tree.client.run.assert_any_call(tree.Branch("1"), tree.Trunk(), 18)

    def test_merge_2(self):
        self.tree.merge("2", 18)
        self.tree.client.run.assert_any_call(tree.Branch("2"), tree.Branch("3"), 18)
        self.tree.client.run.assert_any_call(tree.Branch("2"), tree.Trunk(), 18)

    @unittest.skip("log collecting must be reimplemented")
    def test_logs(self):
        self.tree.collect_logs("1")
        self.tree.client.get_last_commit_info.assert_any_call(tree.Branch("2", None))
        self.tree.client.get_last_commit_info.assert_any_call(tree.Branch("3", None))

if __name__ == '__main__':
    unittest.main()
