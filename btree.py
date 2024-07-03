
class BTreeNode:
    """
    This class represents a node in the B-tree.
    keys: A list to store the keys in the node.
    child: A list to store the child nodes of the current node.
    leaf: A boolean flag indicating whether the node is a leaf node (a node with no children).
    """
    def __init__(self, leaf=False):
        self.keys = []
        self.child = []
        self.leaf = leaf


class BTree:
    """
    This class represents the B-tree itself.
   root: The root node of the B-tree, initialized as a leaf node.
    t: The minimum degree of the B-tree. This value determines the maximum number of children a node can have.
    """
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t
