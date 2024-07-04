## B-tree
An implementation of B-Tree in python. A B Tree is a balanced tree data structure commonly used in databases and file systems to maintain sorted data and allow efficient insertion, deletion, and search operations.

### Features

- **Insertion**: Add keys to the B-Tree, ensuring the tree remains balanced.
- **Deletion**: Remove keys from the B-Tree, maintaining the tree's properties.
- **Search**: Find keys within the B-Tree efficiently.
- **Display**: Visualize the structure of the B-Tree.

### Classes and Methods

#### `BTreeNode`

Represents a node in the B-Tree.

- **Attributes**:
  - `keys`: List of keys in the node.
  - `child`: List of child nodes.
  - `leaf`: Boolean flag indicating if the node is a leaf.

#### `BTree`

Represents the B-Tree itself.

- **Attributes**:
  - `root`: The root node of the B-Tree.
  - `t`: The minimum degree of the B-Tree (defines the range for the number of keys).

- **Methods**:
  - `insert(k)`: Insert a key `k` into the B-Tree.
  - `insert_not_full(x, k)`: Helper method to insert a key into a non-full node.
  - `split_child(x, i)`: Split a full child node.
  - `delete(k)`: Delete a key `k` from the B-Tree.
  - `delete_process(x, k)`: Helper method to process deletion.
  - `get_predecessor(x)`: Get the predecessor of a key.
  - `get_successor(x)`: Get the successor of a key.
  - `merge_nodes(x, i, y, z)`: Merge two child nodes.
  - `fix_child(x, i)`: Ensure a child has enough keys by borrowing or merging.
  - `borrow_from_left(x, i)`: Borrow a key from the left sibling.
  - `borrow_from_right(x, i)`: Borrow a key from the right sibling.
  - `search(k, x=None)`: Search for a key `k` starting from node `x`.
  - `display_tree()`: Display the structure of the B-Tree.

### Usage

1. **Clone the repository**:
   ```sh
   https://github.com/itsknk/btree.git
   cd btree
   ```

2. **Run the test script**:
   The test script demonstrates the B-Tree operations: insertion, search, deletion, and visualization.
   ```sh
   python btree.py
   ```

3. **Example Output**:
   The output will display the B-Tree structure after each operation, helping you understand the changes in the tree.

### Example

```python
# Create a B-Tree with minimum degree 3
b_tree = BTree(3)

# Insert keys
keys = [10, 20, 5, 6, 12, 30, 7, 17]
for key in keys:
    b_tree.insert(key)
    b_tree.display_tree()

# Search for keys
search_keys = [6, 12, 30, 100]
for key in search_keys:
    result = b_tree.search(key)
    if result:
        node, index = result
        print(f"Key {key} found in node {node.keys} at index {index}")
    else:
        print(f"Key {key} not found in the tree")

# Delete keys
delete_keys = [6, 12, 30, 7]
for key in delete_keys:
    b_tree.delete(key)
    b_tree.display_tree()
```

### Contributing

Feel free to submit issues, fork the repository, and send pull requests.

### License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/itsknk/btree/blob/master/LICENSE) file for details.
