import unittest
import tree
import svn
from mock import Mock

class TestTree(unittest.TestCase):

    def setUp(self):
        fakeClient = svn.SvnClient()
        fakeClient.run = Mock()
        fakeClient.write_commit_messages = Mock()
        fakeClient.get_last_commit_info = Mock()
        self.tree = tree.Tree((("1", []), ("2", []), ("3", [])), fakeClient)

    def test_merge(self):
        self.tree.merge("1", 18)
        self.tree.client.run.assert_called_with(self.tree.branches["1"], self.tree.branches["trunk4.1"], 18)


if __name__ == '__main__':
    unittest.main()
