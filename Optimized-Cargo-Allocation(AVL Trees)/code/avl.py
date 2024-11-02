from node import Node



    # Comparator function to compare MyObject objects based on size
def compare_by_size(obj1, obj2):
    if obj1.size < obj2.size:
        return -1
    elif obj1.size > obj2.size:
        return 1
    else:
        return 0
    
def compare_by_bin_ID(obj1, obj2):
    if obj1.bin_id < obj2.bin_id:
        return -1
    elif obj1.bin_id > obj2.bin_id:
        return 1
    else:
        return 0
    
def compare_by_capacity(obj1, obj2):
    if obj1.capacity < obj2.capacity:
        return -1
    elif obj1.capacity > obj2.capacity:
        return 1
    else:
        return 0
def compare_by_ObjID(obj1, obj2):
    if obj1.object_id < obj2.object_id:
        return -1
    elif obj1.object_id > obj2.object_id:
        return 1
    else:
        return 0



class AVLTree:
    def __init__(self, comparator):
        self.root = None
        self.comparator = comparator  # Comparator function

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left:
            y.left.parent = x
        
        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

        self.update_height(x)
        self.update_height(y)
        return y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right

        if x.right:
            x.right.parent = y
        
        x.parent = y.parent

        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

        self.update_height(y)
        self.update_height(x)
        return x

    def rebalance(self, node):
        self.update_height(node)
        balance = self.get_balance(node)

        # Left-heavy
        if balance > 1:
            if self.get_balance(node.left) < 0:
                node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right-heavy
        if balance < -1:
            if self.get_balance(node.right) > 0:
                node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def insert(self, key):
        if not self.root:
            self.root = Node(key)
        else:
            self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return Node(key)

        # Use the comparator function to decide where to insert
        if self.comparator(key, node.key) < 0:
            if node.left is None:
                node.left = Node(key, parent=node)
            else:
                node.left = self._insert(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key, parent=node)
            else:
                node.right = self._insert(node.right, key)

        return self.rebalance(node)

    def delete(self, key):
        if not self.root:
            return
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if self.comparator(key, node.key) < 0:
            node.left = self._delete(node.left, key)
        elif self.comparator(key, node.key) > 0:
            node.right = self._delete(node.right, key)
        else:
            # Node to be deleted has one or no children
            if not node.left or not node.right:
                temp = node.left if node.left else node.right
                if temp is None:  # No child case
                    temp = node
                    node = None
                else:  # One child case
                    node = temp
                    node.parent = temp.parent
            else:
                # Node with two children: Get the in-order successor (smallest in the right subtree)
                temp = self.get_min_value_node(node.right)
                node.key = temp.key
                node.right = self._delete(node.right, temp.key)

        if not node:
            return node

        return self.rebalance(node)

    def get_min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.get_min_value_node(node.left)

    def pre_order(self, node):
        if not node:
            return
        print(node.key.val, end=" ")
        self.pre_order(node.left)
        self.pre_order(node.right)
    
    # New search function
    def search(self, key):
        return self._search(self.root, key)
    
    def _search(self, node, key):
        if not node:
            return None
        
        # Use the comparator function to decide where to search
        comparison = self.comparator(key, node.key)
        
        if comparison == 0:
            return node.key  # Return the key instead of the node
        elif comparison < 0:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def level_order(self):
        if not self.root:
            return
        
        # Initialize a list with a tuple (node, height)
        queue = [(self.root, 1)]  # Start with height 1 for the root node
        current_height = 1

        while queue:
            node, height = queue.pop(0)  # Get the front element from the list
            
            # If we're on a new height level, print a newline
            if height > current_height:
                current_height = height
                print()  # Move to the next line
            
            # Print the value of the current node
            print(node.key.value(), end=" ")

            # Add the left and right children to the queue with their respective heights
            if node.left:
                queue.append((node.left, height + 1))
            if node.right:
                queue.append((node.right, height + 1))

        print()  # Ensure the final output ends with a newline
        
    def get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def print_tree(self):
        if not self.root:
            print("Tree is empty")
            return
        
        height = self.get_height(self.root)
        max_width = 2 ** height - 1  # Maximum number of nodes at the bottom level
        
        # Initialize levels to store nodes at each level
        levels = [[] for _ in range(height)]
        
        # Fill levels with the nodes
        self._fill_levels(self.root, 0, levels, height)
        
        # Print each level with appropriate spacing
        for i in range(height):
            level_str = ""
            gap = max_width // (2 ** i + 1)  # Calculate the gap for this level
            
            # Increase spacing factor for better readability
            gap = gap * 4 if gap > 1 else 4
            
            for node in levels[i]:
                if node is None:
                    level_str += " " * gap + "null" + " " * gap  # Add "null" for empty nodes
                else:
                    value_str = str(node.key.value())  # Get the node's value
                    total_padding = max(0, gap - len(value_str) // 2)
                    # Adjust the padding to be symmetric around the value
                    left_padding = total_padding // 2
                    right_padding = total_padding - left_padding
                    level_str += " " * left_padding + value_str + " " * right_padding
            
            print(level_str.center(max_width * 10))  # Adjust centering for larger spacing

    def _fill_levels(self, node, level, levels, height):
        """ Helper function to fill the levels list with node values up to the given height """
        if level < height:
            if node is None:
                levels[level].append(None)
                # Recursively add None for both left and right children
                if level + 1 < height:  # Ensure we only add 'null' up to the correct height
                    self._fill_levels(None, level + 1, levels, height)
                    self._fill_levels(None, level + 1, levels, height)
            else:
                levels[level].append(node)
                self._fill_levels(node.left, level + 1, levels, height)
                self._fill_levels(node.right, level + 1, levels, height)
               
                
    def get_min_value(self):
        """ Returns the minimum value in the AVL tree based on the comparator """
        if not self.root:
            return None  # Return None if the tree is empty

        return self._get_min_value(self.root).key  # Return the key of the minimum node

    def _get_min_value(self, node):
        """ Helper function to find the node with the minimum value """
        current = node
        while current.left:
            current = current.left
        return current

    def get_max_value(self):
        """ Returns the maximum value in the AVL tree based on the comparator """
        if not self.root:
            return None  # Return None if the tree is empty

        return self._get_max_value(self.root).key  # Return the key of the maximum node

    def _get_max_value(self, node):
        """ Helper function to find the node with the maximum value """
        current = node
        while current.right:
            current = current.right
        return current
    
    def in_order_traversal(self):
        """
        Perform an in-order traversal of the AVL tree.
        Returns:
            A list containing the keys of the nodes in in-order.
        """
        result = []
        self._in_order_helper(self.root, result)
        return result

    def _in_order_helper(self, node, result):
        """
        Helper function to recursively perform in-order traversal.
        Args:
            node: The current node being visited.
            result: The list collecting keys in in-order.
        """
        if node:
            # Traverse the left subtree
            self._in_order_helper(node.left, result)
            
            # Visit the current node
            result.append(node.key)
            
            # Traverse the right subtree
            self._in_order_helper(node.right, result)
    
    def get_least_greater_or_equal(self, key):
        """ Returns the least key greater than or equal to the given key in the AVL tree """
        current = self.root
        candidate = None

        while current:
            comparison = self.comparator(key, current.key)
            
            if comparison == 0:
                # If the key matches exactly, return it immediately
                return current.key
            elif comparison < 0:
                # If the given key is smaller, this could be a candidate
                candidate = current.key
                current = current.left
            else:
                # Move to the right subtree if the given key is greater
                current = current.right

        return candidate  # This will be the least key >= the given key, or None if not found

    # def bfs_traversal(self):
    #     """
    #     Perform a level-order traversal (BFS) of the tree and return the result as a list of levels.
    #     Each level is a list containing the node values or None if the node is missing.
    #     """
    #     if not self.root:
    #         return []

    #     queue = [self.root]
    #     result = []

    #     while queue:
    #         level = []
    #         next_queue = []

    #         for node in queue:
    #             if node:
    #                 level.append(node.key)  # Append the node's key (or key.value() if required)
    #                 next_queue.append(node.left)
    #                 next_queue.append(node.right)
    #             else:
    #                 level.append(None)

    #         result.append(level)
    #         queue = next_queue

    #     return result
    
    # def print_bfs_triangle(self):
    #     """
    #     Print the BFS result in a triangular format for better visual representation of the tree.
    #     """
    #     bfs_result = self.bfs_traversal()

    #     if not bfs_result:
    #         print("Tree is empty")
    #         return

    #     max_level = len(bfs_result)
    #     max_width = 2 ** (max_level - 1) * 4  # Approximate width for the bottom level

    #     for level in range(max_level):
    #         level_width = 2 ** level * 4
    #         spacing = (max_width - level_width) // 2
    #         line = ' ' * spacing
    #         between_spacing = ' ' * (spacing // (2 ** level))
            
    #         for value in bfs_result[level]:
    #             if value is None:
    #                 line += " null " + between_spacing
    #             else:
    #                 line += f" {value.value() if hasattr(value, 'value') else value} " + between_spacing

    #         print(line.rstrip())  # Remove trailing spaces

    

# Example Usage
# if __name__ == "__main__":
    # avl_tree = AVLTree(compare_by_size)

    # # Create some MyObject objects with different sizes
    # objects = [MyObject("Object1", 300), MyObject("Object2", 150), MyObject("Object3", 500), MyObject("Object4", 200), MyObject("Object5", 400)]

    # # Insert objects into the AVL tree
    # for obj in objects:
    #     avl_tree.insert(obj)

    # print("Pre-order traversal of the AVL tree (sorted by size):")
    # avl_tree.pre_order(avl_tree.root)
    # print("\n")

    # # Delete an object and perform pre-order traversal again
    # avl_tree.delete(MyObject("Object2", 150))  # Assume object with name "Object2" and size "150" to delete
    # print("Pre-order traversal after deleting Object2 (size 150):")
    # avl_tree.pre_order(avl_tree.root)
    # print("\n")
    # Make a function which searches a given key in avl tree
    
    
    
