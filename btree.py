
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


    def delete(self, k):
        """
        Initiates the deletion process by calling the delete_process method on the root node.
        """
        self.delete_process(self.root, k)

    
    def delete_process(self, x, k):
        """
        - The initial loop finds the position i where the key k should be in the current node x. 
            It stops when it finds a key greater than or equal to k, or when it reaches the end of the keys list.
        - Check if the key k is actually present in the current node.
        - If the node is a leaf, we can simply remove the key from the list.
        - For an internal node, we identify the two children surrounding the key to be deleted: y(left child) and z(right child).
        - If the let child has enough keys(at least t), we replace the key to be deleted with its 
           predecessor(the largest key in the left subtree) from the left subtree.
        - Similarly, if the right child has enough keys, we use the successor(the smallest key in the right subtree) instead.
        - If both the children have the minimum number of keys, we merge them and then recursively delete the key from the merged node.
        - If the key is not found and we're at a leaf, it means the key is not in the tree.
        - If we're not at a leaf, we need to continue the search in the appropriate child. Before doing so, we ensure that the child has at least
           t keys (calling fix_child if necessary), then recursively call delete_process on that child.
        """
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1

        if i < len(x.keys) and k == x.keys[i]:
            if x.leaf:
                x.keys.pop(i)
            else:
                y = x.child[i]
                z = x.child[i + 1]
                if len(y.keys) >= self.t:
                    predecessor = self.get_predecessor(y)
                    x.keys[i] = predecessor
                    self.delete_process(y, predecessor)
                elif len(z.keys) >= self.t:
                    successor = self.get_successor(z)
                    x.keys[i] = successor
                    self.delete_process(z, successor)
                else:
                    self.merge_nodes(x, i, y, z)
                    self.delete_process(y, k)
        else:
            if x.leaf:
                print(f"Key {k} does not exist")
            else:
                if len(x.child[i].keys) < self.t:
                    self.fix_child(x, i)
                self.delete_process(x.child[i], k)

    
    ## Helper methods for deletion
    def get_predecessor(self, x):
        """
        Start from the given node x. 
        Keep moving to the rightmost child until reaching a leaf node. 
        Once at a leaf, return the last key in that leaf, which is the predecessor.
        """
        while not x.leaf:
            x = x.child[-1]
        return x.keys[-1]
    

    def get_successor(self, x):
        """
        Start from the given node x. 
        Keep moving to the leftmost child until reaching a leaf node. 
        Once at a leaf, return the first key in that leaf, which is the successor.
        """
        while not x.leaf:
            x = x.child[0]
        return x.keys[0]
    

    def merge_nodes(self, x, i, y, z):
        """
        Move the key at index i from the parent x into y.
        Append all keys from z to y.
        If the nodes aren't leaves, move all child pointers from z to y.
        Remove the key at index i from the parent x.
        Remove the child pointer to z from the parent x.
        If the parent x becomes empty after this operation, it means x was the root. In this case, y becomes the new root.
        """
        y.keys.append(x.keys[i])
        y.keys.extend(z.keys)
        y.child.extend(z.child)
        x.keys.pop(i)
        x.child.pop(i + 1)

        if len(x.keys) == 0:  
            self.root = y

    
    def fix_child(self, x, i):
        """
        If the left sibling has enough keys, borrow from the left.
        If the right sibling has enough keys, borrow from the right.
        If neither sibling has enough keys, merge the child with one of its siblings.
        """
        if i > 0 and len(x.child[i - 1].keys) >= self.t:
            self.borrow_from_left(x, i)
        elif i < len(x.child) - 1 and len(x.child[i + 1].keys) >= self.t:
            self.borrow_from_right(x, i)
        else:
            if i > 0:
                self.merge_nodes(x, i - 1, x.child[i - 1], x.child[i])
                i -= 1
            else:
                self.merge_nodes(x, i, x.child[i], x.child[i + 1])

    
    def borrow_from_left(self, x, i):
        """
        Move the parent's key at index i-1 down to the child.
        It then move the rightmost key from the left sibling up to the parent.
        If the nodes aren't leaves, move the rightmost child pointer from the left sibling to the child.
        """
        child = x.child[i]
        sibling = x.child[i - 1]

        child.keys.insert(0, x.keys[i - 1])
        x.keys[i - 1] = sibling.keys.pop()
        if not child.leaf:
            child.child.insert(0, sibling.child.pop())
    

    def borrow_from_right(self, x, i):
        """
        Move the parent's key at index i down to the child.
        Move the leftmost key from the right sibling up to the parent.
        If the nodes aren't leaves, move the leftmost child pointer from the right sibling to the child.
        """
        child = x.child[i]
        sibling = x.child[i + 1]

        child.keys.append(x.keys[i])
        x.keys[i] = sibling.keys.pop(0)
        if not child.leaf:
            child.child.append(sibling.child.pop(0))

    
    def search(self, k, x=None):
        """
        - The function takes two parameters:
            k: The key we're searching for
            x: The node to start the search from (optional, defaults to None)
        - If x is None (i.e., not provided), we start the search from the root of the tree.
        - If x is actually a B-tree node. If not, we restart the search from the root (last line of the function).
        - The loop finds the correct position for k in the current node's keys.
        - If we found the key, we return the current node and the index of the key.
        - If we're at a leaf node and haven't found the key, it doesn't exist in the tree, so we return None.
        - If we're not at a leaf, we recursively search in the appropriate child node.
        - The last else clause handles the case where x isn't a BTreeNode (e.g., if it's None), restarting the search from the root.
        """
        x = x or self.root
        if isinstance(x, BTreeNode):
            i = 0
            while i < len(x.keys) and k > x.keys[i]:
                i += 1
            if i < len(x.keys) and k == x.keys[i]:
                return x, i
            elif x.leaf:
                return None
            else:
                return self.search(k, x.child[i])
        else:
            return self.search(k, self.root)


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

    # Test searching
    search_keys = [6, 12, 30, 100]
    for key in search_keys:
        result = b_tree.search(key)
        if result:
            node, index = result
            print(f"\nKey {key} found in node {node.keys} at index {index}")
        else:
            print(f"\nKey {key} not found in the tree")

    # Test deletion
    delete_keys = [6, 12, 30, 7]
    for key in delete_keys:
        print(f"\nDeleting {key}:")
        b_tree.delete(key)
        b_tree.display_tree()

    # Test deleting a non-existent key
    print("\nTrying to delete non-existent key 100:")
    b_tree.delete(100)
    b_tree.display_tree()

    # Insert more keys to test complex scenarios
    insert_more = [1, 2, 3, 4, 40, 50, 60]
    for key in insert_more:
        print(f"\nInserting {key}:")
        b_tree.insert(key)
        b_tree.display_tree()

    # Delete more keys to test complex scenarios
    delete_more = [4, 20, 50]
    for key in delete_more:
        print(f"\nDeleting {key}:")
        b_tree.delete(key)
        b_tree.display_tree()

    # Test searching after modifications
    search_keys = [5, 40, 100]
    for key in search_keys:
        result = b_tree.search(key)
        if result:
            node, index = result
            print(f"\nKey {key} found in node {node.keys} at index {index}")
        else:
            print(f"\nKey {key} not found in the tree")


# Run the test
test_btree()
