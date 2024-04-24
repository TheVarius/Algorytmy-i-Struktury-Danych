import math

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

    def insert(self, *keys):
        for key in keys:
            current = self
            while True:
                if key < current.key:
                    if current.left is None:
                        current.left = Node(key)
                        break
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = Node(key)
                        break
                    else:
                        current = current.right
                
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self.root.insert(key)

    def find_min(self):
        current = self.root
        while current.left:
            current = current.left
        return current.key

    def find_max(self):
        current = self
        while current.right:
            current = current.right
        return current.key
        
    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(node.key, end=' ')
            self.inorder_traversal(node.right)

    def preorder_traversal(self, node):
        if node:
            print(node.key, end=' ')
            self.preorder_traversal(node.left)
            self.preorder_traversal(node.right)
            
    def postorder_traversal(self, node):
        if node:
            self.postorder_traversal(node.left)
            self.postorder_traversal(node.right)
            print(node.key, end=' ')

    def _remove(self, node, key):
        if not node:
            return None

        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:  # znaleziono węzeł do usunięcia
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:  # węzeł ma obu dzieci
                successor = node.right.find_min()
                node.key = successor
                node.right = self._remove(node.right, successor)

        return node

    def rebalance(self):
        grand = Node(0)
        grand.right = self.root
        count = self.bst_to_vine(grand)
        h = int(math.log2(count + 1))
        m = 2**h - 1
        self.compress(grand, count - m)
        while m > 0:
            m //= 2
            self.compress(grand, m)
        self.root = grand.right

    def bst_to_vine(self, grand):
        count = 0
        tmp = grand.right
        while tmp:
            if tmp.left:
                old_tmp = tmp
                tmp = tmp.left
                old_tmp.left = tmp.right
                tmp.right = old_tmp
                grand.right = tmp
            else:
                count += 1
                grand = tmp
                tmp = tmp.right
        return count

    def compress(self, grand, count):
        tmp = grand.right
        for _ in range(count):
            if tmp.right:
                old_tmp = tmp
                tmp = tmp.right
                old_tmp.right = tmp.left
                tmp.left = old_tmp
                grand.right = tmp
                grand = tmp
                tmp = tmp.right

class AVLNode(Node):
    def __init__(self, key):
        super().__init__(key)

class AVLTree(BinarySearchTree):
    def __init__(self):
        super().__init__()

    def insert(self, key):
        if self.root is None:
            self.root = AVLNode(key)
        else:
            self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        # Aktualizacja wysokości i balansowanie drzewa AVL
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._get_balance(node)

        if balance > 1:
            if key < node.left.key:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        if balance < -1:
            if key > node.right.key:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def _height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        x = y.left
        t = x.right

        x.right = y
        y.left = t

        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))

        return x

    def _rotate_left(self, x):
        y = x.right
        t = y.left

        y.left = x
        x.right = t

        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y

def main():
    bst = BinarySearchTree()
    bst.insert(10)
    bst.insert(5)
    bst.insert(15)
    bst.insert(3)
    bst.insert(7)
    bst.insert(12)
    bst.insert(20)

    avl = AVLTree()
    avl.insert(10)
    avl.insert(5)
    avl.insert(15)
    avl.insert(3)
    avl.insert(7)
    avl.insert(12)
    avl.insert(20)

    while True:
        print("\nMenu:")
        print("1. Insert node (BST)")
        print("2. Insert node (AVL)")
        print("3. Print BST (Inorder)")
        print("4. Print BST (Preorder)")
        print("5. Print BST (Postorder)")
        print("6. Print AVL (Inorder)")
        print("7. Print AVL (Preorder)")
        print("8. Print AVL (Postorder)")
        print("9. Remove node (BST)")
        print("10. Remove node (AVL)")
        print("11. Export BST")
        print("12. Export AVL")
        print("13. Rebalance AVL using DSW")
        print("14. Rebalance BST using DSW")
        print("15. Remove all nodes (BST)")
        print("16. Remove all nodes (AVL)")
        print("17. Find Min (BST)")
        print("18. Find Max (BST)")
        print("19. Find Min (AVL)")
        print("20. Find Max (AVL)")
        print("21. Exit")

        choice = input("nodes> ")

        if choice == "1":
            keys = input("Enter node values separated by spaces: ").split()
            keys = [int(key) for key in keys]
            bst.insert(*keys)
        elif choice == "2":
            keys = input("Enter node values separated by spaces: ").split()
            keys = [int(key) for key in keys]
            avl.root.insert(*keys)
        elif choice == "3":
            print("BST Tree (Inorder):")
            bst.inorder_traversal(bst.root)
        elif choice == "4":
            print("BST Tree (Preorder):")
            bst.preorder_traversal(bst.root)
        elif choice == "5":
            print("BST Tree (Postorder):")
            bst.postorder_traversal(bst.root)
        elif choice == "6":
            print("AVL Tree (Inorder):")
            avl.inorder_traversal(avl.root)  
        elif choice == "7":
            print("AVL Tree (Preorder):")
            avl.preorder_traversal(avl.root)
        elif choice == "8":
            print("AVL Tree (Postorder):")
            avl.postorder_traversal(avl.root)
        elif choice == "9":
            key = int(input("Enter node value to remove: "))
            bst.remove(key)
            print("Node removed from BST.")
        elif choice == "10":
            key = int(input("Enter node value to remove: "))
            avl.remove(key)
            print("Node removed from AVL.")
        elif choice == "11":
            print("BST Export:")
            print(bst.export())
        elif choice == "12":
            print("AVL Export:")
            print(avl.export())
        elif choice == "13":
            avl.rebalance()
            print("AVL Tree rebalanced using DSW.")
        elif choice == "14":
            bst.rebalance()
            print("BST rebalanced using DSW.")
        elif choice == "15":
            bst.remove_all()
            print("All nodes removed from BST.")
        elif choice == "16":
            avl.remove_all()
            print("All nodes removed from AVL.")
        elif choice == "17":
            min_key = bst.find_min()
            if min_key is not None:
                print("Minimum key in BST:", min_key)
            else:
                print("BST is empty.")
        elif choice == "18":
            max_key = bst.find_max()
            if max_key is not None:
                print("Maximum key in BST:", max_key)
            else:
                print("BST is empty.")
        elif choice == "19":
            min_key = avl.find_min()
            if min_key is not None:
                print("Minimum key in AVL:", min_key)
            else:
                print("AVL is empty.")
        elif choice == "20":
            max_key = avl.find_max()
            if max_key is not None:
                print("Maximum key in AVL:", max_key)
            else:
                print("AVL is empty.")
        elif choice == "21":
            break
        else:
            print("Invalid choice. Try again!")

if __name__ == "__main__":
    main()
