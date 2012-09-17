import argparse
import tree

def run():
    parser = argparse.ArgumentParser(description="merge tool")
    parser.add_argument("branch", help="the branch to merge")
    parser.add_argument("commit", help="the commit to merge")
    args = parser.parse_args()
    myTree = tree.Tree()
    myTree.load_tree([("40", []), ("50", []), ("60", [])])
    myTree.merge(args.branch, args.commit)
    
if __name__ == "__main__":
    run()
