class Node:
    def __init__(self, key, parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent  # Parent pointer
        self.height = 1  # Height of this node
        pass