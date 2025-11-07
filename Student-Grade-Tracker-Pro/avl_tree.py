# -------------------------------------------------
# avl_tree.py
# AVL Tree (self-balancing binary search tree)
# -------------------------------------------------

class AVLNode:
    """One student record"""
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade
        self.left = None
        self.right = None
        self.height = 1          # height of the subtree rooted at this node


class AVLTree:
    """All operations on the tree"""

    # ---------- helpers ----------
    @staticmethod
    def _height(node):
        return node.height if node else 0

    @staticmethod
    def _update_height(node):
        node.height = 1 + max(AVLTree._height(node.left), AVLTree._height(node.right))

    @staticmethod
    def _balance_factor(node):
        return AVLTree._height(node.left) - AVLTree._height(node.right)

    # ---------- rotations ----------
    @staticmethod
    def _rotate_right(y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        AVLTree._update_height(y)
        AVLTree._update_height(x)
        return x

    @staticmethod
    def _rotate_left(x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        AVLTree._update_height(x)
        AVLTree._update_height(y)
        return y

    # ---------- insert ----------
    def insert(self, root, student_id, name, grade):
        """Return new root (may change after balancing)"""
        # 1. Normal BST insert
        if not root:
            return AVLNode(student_id, name, grade)

        if student_id < root.student_id:
            root.left = self.insert(root.left, student_id, name, grade)
        elif student_id > root.student_id:
            root.right = self.insert(root.right, student_id, name, grade)
        else:                                   # update existing
            root.name = name
            root.grade = grade
            return root

        # 2. Update height
        AVLTree._update_height(root)

        # 3. Get balance factor
        balance = AVLTree._balance_factor(root)

        # 4. Re-balance
        # Left-Left
        if balance > 1 and student_id < root.left.student_id:
            return AVLTree._rotate_right(root)
        # Left-Right
        if balance > 1 and student_id > root.left.student_id:
            root.left = AVLTree._rotate_left(root.left)
            return AVLTree._rotate_right(root)
        # Right-Right
        if balance < -1 and student_id > root.right.student_id:
            return AVLTree._rotate_left(root)
        # Right-Left
        if balance < -1 and student_id < root.right.student_id:
            root.right = AVLTree._rotate_right(root.right)
            return AVLTree._rotate_left(root)

        return root

    # ---------- search ----------
    def search(self, root, student_id):
        if not root or root.student_id == student_id:
            return root
        if student_id < root.student_id:
            return self.search(root.left, student_id)
        return self.search(root.right, student_id)

    # ---------- delete ----------
    def _min_value_node(self, node):
        cur = node
        while cur.left:
            cur = cur.left
        return cur

    def delete(self, root, student_id):
        # 1. BST delete
        if not root:
            return root

        if student_id < root.student_id:
            root.left = self.delete(root.left, student_id)
        elif student_id > root.student_id:
            root.right = self.delete(root.right, student_id)
        else:
            # node to delete found
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            # two children
            temp = self._min_value_node(root.right)
            root.student_id = temp.student_id
            root.name = temp.name
            root.grade = temp.grade
            root.right = self.delete(root.right, temp.student_id)

        # 2. Update height
        AVLTree._update_height(root)

        # 3. Balance
        balance = AVLTree._balance_factor(root)

        # Left heavy
        if balance > 1:
            if AVLTree._balance_factor(root.left) >= 0:
                return AVLTree._rotate_right(root)
            else:
                root.left = AVLTree._rotate_left(root.left)
                return AVLTree._rotate_right(root)

        # Right heavy
        if balance < -1:
            if AVLTree._balance_factor(root.right) <= 0:
                return AVLTree._rotate_left(root)
            else:
                root.right = AVLTree._rotate_right(root.right)
                return AVLTree._rotate_left(root)

        return root

    # ---------- inorder traversal (sorted order) ----------
    def inorder(self, root, result_list):
        if root:
            self.inorder(root.left, result_list)
            result_list.append(f"ID: {root.student_id} | {root.name} | Grade: {root.grade}")
            self.inorder(root.right, result_list)