import sys

# Every vertex in this BST is an object instance
class BSTVertex:
    def __init__(self):
        # All these attributes remain public to slightly simplify the code
        # although this may not be the best practice
        self.parent = None
        self.left = None
        self.right = None
        self.key = 0
        self.height = 0  # will be used in AVL lecture


# This is just a sample implementation
# There are other ways to implement BST concepts...
class BST:
    def __init__(self):
        self.root = None

    def _insert(self, T, v):
        if T is None:  # insertion point is found
            T = BSTVertex()
            T.key = v
            T.parent = T.left = T.right = None
            T.height = 0  # used in AVL lecture
        elif T.key < v:  # search to the right
            T.right = self._insert(T.right, v)
            T.right.parent = T
        else:  # search to the left
            T.left = self._insert(T.left, v)
            T.left.parent = T
        return T  # return the updated BST

    def _inorder(self, T):
        if T is None:
            return
        self._inorder(T.left)  # recursively go to the left
        print(f" {T.key}", end="")  # visit this BST node
        self._inorder(T.right)  # recursively go to the right

    def _preorder(self, T):
        if T is None:
            return
        print(f" {T.key}", end="")  # visit this BST node
        self._preorder(T.left)  # recursively go to the left
        self._preorder(T.right)  # recursively go to the right

    def _findMin(self, T):
        if T is None:
            return -1  # BST is empty, no minimum
        elif T.left is None:
            return T.key  # this is the min
        else:
            return self._findMin(T.left)  # go to the left

    def _findMax(self, T):
        if T is None:
            return -1  # BST is empty, no maximum
        elif T.right is None:
            return T.key  # this is the max
        else:
            return self._findMax(T.right)  # go to the right

    def _search(self, T, v):
        if T is None:
            return T  # not found
        elif T.key == v:
            return T  # found
        elif T.key < v:
            return self._search(T.right, v)  # search to the right
        else:
            return self._search(T.left, v)  # search to the left

    def _successor_node(self, T):
        if T.right is not None:  # we have right subtree
            return self._findMin(T.right)  # this is the successor
        else:
            par = T.parent
            cur = T
            # if par(ent) is not root and cur(rent) is its right children
            while (par is not None) and (cur == par.right):
                cur = par  # continue moving up
                par = cur.parent
            return -1 if par is None else par.key  # this is the successor of T

    def _predecessor_node(self, T):
        if T.left is not None:  # we have left subtree
            return self._findMax(T.left)  # this is the predecessor
        else:
            par = T.parent
            cur = T
            # if par(ent) is not root and cur(rent) is its left children
            while (par is not None) and (cur == par.left):
                cur = par  # continue moving up
                par = cur.parent
            return -1 if par is None else par.key  # this is the successor of T

    def _remove(self, T, v):
        if T is None:
            return T  # cannot find the item
        if T.key == v:  # the node to be deleted
            if T.left is None and T.right is None:  # this is a leaf
                T = None  # simply erase this node
            elif T.left is None and T.right is not None:  # only one child at right
                T.right.parent = T.parent  # ma, take care of my child
                T = T.right  # bypass T
            elif T.left is not None and T.right is None:  # only one child at left
                T.left.parent = T.parent  # ma, take care of my child
                T = T.left  # bypass T
            else:  # has two children, find successor to avoid quarrel
                successorV = self.successor(v)  # predecessor is also OK btw
                T.key = successorV  # replace with successorV
                T.right = self._remove(T.right, successorV)  # delete the old successorV
        elif T.key < v:  # search to the right
            T.right = self._remove(T.right, v)
        else:  # search to the left
            T.left = self._remove(T.left, v)
        return T  # return the updated BST

    # will be used in AVL lecture
    def _getHeight(self, T):
        if T is None:
            return -1
        else:
            return max(self._getHeight(T.left), self._getHeight(T.right)) + 1

    # Public API methods
    def insert(self, v):
        self.root = self._insert(self.root, v)

    def inorder(self):
        self._inorder(self.root)
        print()

    def preorder(self):
        self._preorder(self.root)
        print()

    def findMin(self):
        return self._findMin(self.root)

    def findMax(self):
        return self._findMax(self.root)

    def search(self, v):
        res = self._search(self.root, v)
        return -1 if res is None else res.key

    def successor(self, v):
        vPos = self._search(self.root, v)
        return -1 if vPos is None else self._successor_node(vPos)

    def predecessor(self, v):
        vPos = self._search(self.root, v)
        return -1 if vPos is None else self._predecessor_node(vPos)

    def remove(self, v):
        self.root = self._remove(self.root, v)

    # will be used in AVL lecture
    def getHeight(self):
        return self._getHeight(self.root)


class AVL(BST):  # another example of inheritance
    def __init__(self):
        super().__init__()

    def _h(self, T):
        return -1 if T is None else T.height

    def _rotateLeft(self, T):
        # T must have a right child
        w = T.right
        w.parent = T.parent
        T.parent = w
        T.right = w.left
        if w.left is not None:
            w.left.parent = T
        w.left = T
        T.height = max(self._h(T.left), self._h(T.right)) + 1
        w.height = max(self._h(w.left), self._h(w.right)) + 1
        return w

    def _rotateRight(self, T):
        # T must have a left child
        w = T.left
        w.parent = T.parent
        T.parent = w
        T.left = w.right
        if w.right is not None:
            w.right.parent = T
        w.right = T
        T.height = max(self._h(T.left), self._h(T.right)) + 1
        w.height = max(self._h(w.left), self._h(w.right)) + 1
        return w

    def _rebalance(self, T):
        balance = self._h(T.left) - self._h(T.right)
        if balance == 2:  # left heavy
            balance2 = self._h(T.left.left) - self._h(T.left.right)
            if balance2 >= 0:
                T = self._rotateRight(T)
            else:  # -1
                T.left = self._rotateLeft(T.left)
                T = self._rotateRight(T)
        elif balance == -2:  # right heavy
            balance2 = self._h(T.right.left) - self._h(T.right.right)
            if balance2 <= 0:
                T = self._rotateLeft(T)
            else:  # 1
                T.right = self._rotateRight(T.right)
                T = self._rotateLeft(T)
        T.height = max(self._h(T.left), self._h(T.right)) + 1
        return T

    def _insert(self, T, v):  # override insert in BST class
        if T is None:  # insertion point is found
            T = BSTVertex()
            T.key = v
            T.parent = T.left = T.right = None
            T.height = 0  # will be used in AVL lecture
        elif T.key < v:  # search to the right
            T.right = self._insert(T.right, v)
            T.right.parent = T
        else:  # search to the left
            T.left = self._insert(T.left, v)
            T.left.parent = T
        T = self._rebalance(T)
        return T  # return the updated AVL

    def _remove(self, T, v):
        if T is None:
            return T  # cannot find the item
        if T.key == v:  # the node to be deleted
            if T.left is None and T.right is None:  # this is a leaf
                T = None  # simply erase this node
            elif T.left is None and T.right is not None:  # only one child at right
                T.right.parent = T.parent
                T = T.right  # bypass T
            elif T.left is not None and T.right is None:  # only one child at left
                T.left.parent = T.parent
                T = T.left  # bypass T
            else:  # find successor
                successorV = self.successor(v)
                T.key = successorV  # replace with successorV
                T.right = self._remove(T.right, successorV)  # delete the old successorV
        elif T.key < v:  # search to the right
            T.right = self._remove(T.right, v)
        else:  # search to the left
            T.left = self._remove(T.left, v)
        if T is not None:
            T = self._rebalance(T)
        return T  # return the updated BST


# --- Main Driver Script (Replicating main() in AVL.cpp) ---
if __name__ == "__main__":
    # let's contrast and compare
    T = BST()  # an empty BST
    A = AVL()  # an empty AVL
    n = 12
    arr = [15, 32, 100, 6, 23, 4, 7, 71, 5, 50, 3, 1]
    
    for i in range(n):
        T.insert(arr[i])
        A.insert(arr[i])

    # Example of Python polymorphism / method overriding: method getHeight() returns different value
    print(T.getHeight())  # 4, taller tree
    print(A.getHeight())  # 3, shorter tree

    # Another polymorphism: method inorder() returns similar value
    print("The BST:", end="")
    T.inorder()  # The BST: 1 3 4 5 6 7 15 23 32 50 71 100
    print("The AVL:", end="")
    A.inorder()  # The AVL: 1 3 4 5 6 7 15 23 32 50 71 100
    print("---")

    print(A.search(71))  # found, 71
    print(A.search(7))   # found, 7
    print(A.search(22))  # not found, -1
    print(A.findMin())   # 1
    print(A.findMax())   # 100

    arr.sort()
    print("---")
    for i in range(n):
        print(f"{A.predecessor(arr[i])} {arr[i]} {A.successor(arr[i])}")

    # deletion demo
    print("---")
    print("Current BST/AVL:", end="")
    A.inorder()

    deletionorder = [23, 100, 32, 71, 50, 7, 5, 1, 3, 6, 15, 4]
    for i in range(n):
        print(f"Deleting: {deletionorder[i]}")
        A.remove(deletionorder[i])
        print(f"AVL, height: {A.getHeight()}, inorder traversal:", end="")
        A.inorder()
        
        T.remove(deletionorder[i])
        print(f"BST, height: {T.getHeight()}, inorder traversal:", end="")  # equal or taller than A.getHeight()
        T.inorder()  # should be the same as A.inorder()
