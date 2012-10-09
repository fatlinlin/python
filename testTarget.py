import unittest
import switch
from mock import Mock

class TestTarget(unittest.TestCase):

    def setUp(self):
        self.target = switch.Target("myTarget")
        self.target.root_names = ["git", "svn"]

    def test_print_svn(self):
        self.target.add("svn")
        self.assertEqual(str(self.target), "    svn myTarget")

    def test_print_git(self):
        self.target.add("git")
        self.assertEqual(str(self.target), "git     myTarget")

    def test_print_both(self):
        self.target.add("git")
        self.target.add("svn")
        self.assertEqual(str(self.target), "git svn myTarget")

if __name__ == '__main__':
    unittest.main()
