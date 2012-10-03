import unittest
import tree
import svn
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


if __name__ == '__main__':
    unittest.main()
