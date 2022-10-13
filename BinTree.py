from typing import cast, Generic, List, Optional, Sized, TypeVar

T = TypeVar('T')

class BinTree(Generic[T], Sized):
    """Class to represent a binary tree, defined as follows:
    A binary tree is either: (1) an empty tree, or (2) a node,
    with 0, 1, or 2 trees as its children.  An empty tree is
    represented *either* by a node with no children and the
    data set to None, *or* by None itself."""

    def __init__(self, data: Optional[T] = None):
        """Construct an empty tree."""
        self._data: Optional[T] = data
        self._left: Optional[BinTree[T]] = None
        self._right: Optional[BinTree[T]] = None
        assert self._invariant()

    # Internal methods

    def _invariant(self) -> bool:
        """Class invariant.  Effectively, this asserts that either
        self is an empty tree (_data, _left, and _right are all None) or
        self is a node within a tree (_data is not None)."""        
        return (self._data is not None) or \
            (self._data is None and self._left is None
                 and self._right is None)

    # Query methods

    def isEmpty(self) -> bool:
        """Query method that returns True when the tree is empty."""
        return self._data is None

    def hasLeftChild(self) -> bool:
        """Query method that returns True when the current node
        has a left child."""
        return self._left is not None

    def hasRightChild(self) -> bool:
        """Query method that returns True when the current node
        has a right child."""
        return self._right is not None

    def data(self) -> T:
        """Query method that returns the data from the current node."""
        if self.isEmpty():
            raise ValueError('Cannot get data from an empty tree.')
        else:
            return cast(T, self._data)

    def leftChild(self) -> 'BinTree[T]':
        """Query method that returns the left child of this node."""
        # Pre:
        assert self.hasLeftChild()
        return cast(BinTree[T], self._left)

    def rightChild(self) -> 'BinTree[T]':
        """Query method that returns the right child of this node."""
        # Pre:
        assert self.hasRightChild()
        return cast(BinTree[T], self._right)

    def __len__(self) -> int:
        """Find the number of nodes in the tree."""
        result: int = 0 # Handles the case of an empty tree
        if not self.isEmpty():
            result = 1 # Current node
            if self.hasLeftChild():
                result = result + len(self.leftChild())
            if self.hasRightChild(): # not elif!
                result = result + len(self.rightChild())
        return result

    def height(self) -> int:
        """Find the height of the tree."""
        result: int = 0 # Handles the case of an empty tree
        if not self.isEmpty():
            result = 1 # Current node
            
            leftSubtreeHeight: int = 0
            if self.hasLeftChild():
                leftSubtreeHeight = self.leftChild().height()

            rightSubtreeHeight: int = 0
            if self.hasRightChild():
                rightSubtreeHeight = self.rightChild().height()

            result += max(leftSubtreeHeight, rightSubtreeHeight)
        return result
            
    # Mutator methods

    def addLeft(self, item: T) -> None:
        """Add a new node containing ITEM as the current node's
        left child.  Any pre-existing left child becomes the 
        new node's left child."""
        if self.isEmpty():
            self._data = item
        else:
            newNode: BinTree[T] = BinTree[T](item)
            newNode._left = self._left
            self._left = newNode
        # Post:
        assert self._invariant()

    def addRight(self, item: T) -> None:
        """Add a new node containing ITEM as the current node's
        right child.  Any pre-existing right child becomes the 
        new node's right child."""
        if self.isEmpty():
            self._data = item
        else:
            newNode: BinTree[T] = BinTree[T](item)
            newNode._right = self._right
            self._right = newNode
        # Post:
        assert self._invariant()

    def removeLeft(self) -> None:
        """Remove the current node's left child.  If the left child has
        children, they are removed from the tree as well.  If
        the current node has no left child, do nothing."""
        self._left = None
        # Post:
        (self._left is None) and self._invariant()

    def removeRight(self) -> None:
        """Remove the current node's right child.  If the right child
        has children, they are removed from the tree as well.  If
        the current node has no right child, do nothing."""
        self._right = None
        # Post:
        (self._right is None) and self._invariant()

    # Traversals
    def preorder(self) -> List[T]:
        """Create and return a list of the values in the tree,
        ordered by a depth-first preorder traversal."""
        result: List[T] = []
        if not self.isEmpty():
            result.append(self.data())
            if self.hasLeftChild():
                result.extend(self.leftChild().preorder())
            if self.hasRightChild():
                result.extend(self.rightChild().preorder())
        return result

    def inorder(self) -> List[T]:
        """Create and return a list of the values in the tree,
        ordered by a depth-first inorder traversal."""
        result: List[T] = []
        if not self.isEmpty():
            if self.hasLeftChild():
                result.extend(self.leftChild().inorder())
            result.append(self.data())
            if self.hasRightChild():
                result.extend(self.rightChild().inorder())
        return result

    def postorder(self) -> List[T]:
        """Create and return a list of the values in the tree,
        ordered by a depth-first postorder traversal."""
        result: List[T] = []
        if not self.isEmpty():
            if self.hasLeftChild():
                result.extend(self.leftChild().postorder())
            if self.hasRightChild():
                result.extend(self.rightChild().postorder())
            result.append(self.data())
        return result
