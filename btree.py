
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


    ## Insertion
    def insert (self, k):
        """
        Start at the root node.
        Check if the root is full.
            - If the root contains 2t-1 keys, split it into two child nodes
                and promote the middle key to a new root.
        Determine the appropirate child node to descend.
        Check if the selected child node is full.
            - If it is, split it recursively as in step 2.
        Descend to the appropriate child node.
        Insert the key into the leaf node.
            - Place the key in its appropirate position, maintaining the keys in ascending order.
        Handle the overflow in the leaf node.
            - If the insertion causes the leaft node to become full, split it and promote the middle key to the parent.
        Repeat the above two steps as necessary.
        """
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.child.insert(0, root)
            self.split_child(temp, 0)
            self.insert_not_full(temp, k)
        else:
            self.insert_not_full(root, k)


    def insert_not_full(self, x, k):
        """
        If the node is a leaf, find the correct position for the new key, shift existing keys if necessary, and insert the new key.
        If the node is not a leaf:
        - Find the correct child node to descent time.
        - If the child node is full, split it.
        - Continue the insertion process recursively on the appropriate child node.
        """
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            
            self.insert_not_full(x.child[i], k)


    def split_child(self, x, i):
        """
        Create a new node z that will contain the second half of y's keys.
        Insert z as a child of x and promote the middle  key from y to x.
        Distribute y's keys and children between y and z.    
        """
        t = self.t
        y = x.child[i]
        z = BTreeNode(y.leaf)
        x.child.insert(i+1, z)
        x.keys.insert(i, y.keys[t-1])
        z.keys = y.keys[t:(2 * t) - 1]                 
        y.keys = y.keys[0:t-1]
        if not y.leaf:
            z.child = y.child[t:(2 * t)]
            y.child = y.child[0:t-1]

    ## Testing till now
    def display_tree(self):
        def display_node(node, level, prefix):
            print(' ' * (level * 4) + prefix + str(node.keys))
            if not node.leaf:
                for i, child in enumerate(node.child):
                    display_node(child, level + 1, f'Child {i}: ')

        print("B-Tree Structure:")
        display_node(self.root, 0, 'Root: ')

# Test the BTree implementation
def test_btree():
    b_tree = BTree(3)  # Create a B-tree with minimum degree 3

    # Insert keys into the B-tree
    keys = [10, 20, 5, 6, 12, 30, 7, 17]
    for key in keys:
        print(f"\nInserting {key}:")
        b_tree.insert(key)
        b_tree.display_tree()

# Run the test
test_btree()
