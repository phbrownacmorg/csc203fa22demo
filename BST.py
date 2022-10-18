from typing import cast, List, Optional, TypeVar
from BinTree import BinTree

T = TypeVar('T') # Must support comparisons

class BST(BinTree[T]):
    """Class to represent a binary search tree.
    This class does not represent the empty tree;
    that is, a binary search tree must *always*
    have at least one node."""

    def __init__(self, data: T, parent: Optional['BST[T]'] = None):
        """Create a BST node with the given DATA and PARENT.
        Note that DATA cannot be None."""
        self._parent: Optional[BST[T]] = parent

        super().__init__(data)
        # Post: self._invariant() (checked by superclass constructor)

    def _invariant(self) -> bool:
        """Class invariant."""
        valid: bool = super()._invariant()
        valid = valid and self._data is not None

        if self.hasLeftChild():
            # Must be a BST, not just a BinTree
            valid = valid and isinstance(self.leftChild(), BST)

            # Child's parent link is correct
            valid = valid and self == cast(BST, self.leftChild()).parent()
            
            # Maximum value in the left subtree < this node's data
            maxLeftNode: BinTree[T] = self.leftChild() # Actually a BST, but...
            while maxLeftNode.hasRightChild():
                maxLeftNode = maxLeftNode.rightChild()
            valid = valid and maxLeftNode.data() < self.data() # type: ignore

            # Left subtree is a BST
            valid = valid and self.leftChild()._invariant()
            
        if self.hasRightChild():
            # Must be a BST, not just a BinTree
            valid = valid and isinstance(self.rightChild(), BST)

            # Child's parent link is correct
            valid = valid and self == cast(BST, self.rightChild()).parent()

            # Minimum value in the right subtree > this node's data
            minRightNode: BinTree[T] = self.rightChild() # Actually  BST, but...
            while minRightNode.hasLeftChild():
                minRightNode = minRightNode.leftChild()
            valid = valid and minRightNode.data() > self.data() # type: ignore

            # Right subtree is a BST
            valid = valid and self.rightChild()._invariant()
        return valid

    # Query methods are all the same as in BinTree, except...
    def isRoot(self) -> bool:
        """If the node has no parent, it's the root."""
        return self._parent is None

    def parent(self) -> 'BST[T]':
        """Return the node's parent."""
        # Pre:
        assert not self.isRoot()
        return cast(BST[T], self._parent)

    def __contains__(self, value: T) -> bool:
        """Boolean method to figure out whether or not a given VALUE is
        in the tree rooted at SELF.  This method overloads the 'in'
        operator."""
        inTree: bool = False
        if value == self.data():
            inTree = True
        elif value < self.data(): # type: ignore
            if self.hasLeftChild():
                inTree = value in cast(BST[T], self.leftChild())
            # If no left child, inTree will stay False
        elif value > self.data(): # type: ignore
            if self.hasRightChild():
                inTree = value in cast(BST[T], self.rightChild())
            # If no right child, inTree will stay False
        return inTree

    def findSuccessor(self) -> Optional['BST[T]']:
        """Find this node's successor in an inorder traversal of the tree.
        If this is the last node in an inorder traversal, return None.
        This method works for any position in the tree.

        Note that when this method is used in deleting a node N, then
        the successor of N (call it S) has to be in N's right subtree.
        When this method is used in deleting a node, N has two children.
        Therefore, N has a right child.

        If N has a right child C, then the successor of N (call
        it S) is somewhere in N's right subtree.  We know that the
        value of S > the value of N (write that S > N), and that S
        holds the *least* value in the tree for which S > N.  If S is
        *not* in N's right subtree, then S must be above N in the
        tree.  Now, for S to be above N in the tree, then N has to be
        the greatest node in S's left subtree.  But if N has a right
        child C, then C > N *and* C is in S's left subtree, so N can't
        be the greatest node in S's left subtree.  Therefore, if N has
        a right child, S is *not* above N, which means S is in N's right
        subtree.  In fact, since S is the smallest node in the tree for
        which S > N, S must be the smallest node in N's right subtree.

        Note also that if S is the smallest node in N's right subtree,
        S itself cannot have a left child.  If S had a left child L,
        then L < S.  But L is still in N's right subtree, so then S
        wouldn't be the smallest node in N's right subtree.  So S can't
        possibly have two children (it might have one, a right child).
        """
        # Successor node S
        successor: Optional[BST[T]] = None
        if self.hasRightChild():
            successor = cast(BST, self.rightChild()) # Root of N's right subtree
            # Follow down S's left subtree to find the smallest node in N's
            # right subtree
            while successor.hasLeftChild():
                successor = cast(BST, successor.leftChild())
        # At this point, we know self has no right subtree, so its successor
        # can't be in its right subtree.  Therefore, we have to go upwards.
        # If self is root and has no right subtree, it has no successor.
        elif not self.isRoot():
            # If self is in its parent's left subtree, its parent is its
            # successor.
            if self.parent().hasLeftChild() and self is self.parent().leftChild():
                successor = self.parent()
            else:
                # Self must be in its parent's right subtree, which means
                # self must be the largest item in its parent's right subtree
                # (if it weren't the largest, self would have a right subtree).
                # Its successor will be its parent's successor *excluding*
                # self (and self's descendants in the parent's right subtree).

                # Temporarily remove self (and its descendants) from the tree
                self.parent()._right = None
                successor = self.parent().findSuccessor()
                # Now, put self back to avoid fouling up the tree
                self.parent()._right = self
        return successor

    # Mutator methods
    def add(self, value: T) -> None:
        """Add a value to the tree, inserting in its proper place."""
        if value < self.data(): # type: ignore
            if self.hasLeftChild(): # Recursive 
                cast(BST[T], self.leftChild()).add(value)
            else:
                self._left = BST[T](value, self)
        elif value > self.data(): # type: ignore
            if self.hasRightChild(): # Recursive 
                cast(BST[T], self.rightChild()).add(value)
            else:
                self._right = BST[T](value, self)
        # Elif value == self.data(), don't re-insert it.
        # Just do nothing.
        assert self._invariant()

    def _removeLeaf(self) -> None:
        """Remove this node, in the case that this node is a leaf."""
        # Pre:
        assert (not self.hasLeftChild()) and (not self.hasRightChild())
        if self.isRoot():
            raise ValueError('Cannot delete the last node in the tree.')
        elif self == self.parent().leftChild():
            self.parent()._left = None
        elif self == self.parent().rightChild():
            self.parent()._right = None
        # Make this node the empty tree, so we know not to apply
        # the postcondition
        self._data = None
        # Post
        assert self._data is None
        # and no references to the current node remain in the tree

    def _removeParentOfOne(self) -> None:
        """Remove this node, in the case that this node has one child."""
        # Pre:
        assert (self.hasLeftChild() and not self.hasRightChild()) \
            or (not self.hasLeftChild() and self.hasRightChild())
        if self.hasLeftChild():
            child: BinTree[T] = self.leftChild() # Actually a BST
        else:
            child = self.rightChild()
        # Copy the data from the child up to this node
        self._data = child._data

        self._left = child._left
        if self._left is not None:
            cast(BST, self._left)._parent = self

        self._right = child._right
        if self._right is not None:
            cast(BST, self._right)._parent = self
        # Post:
        assert self.data() == child.data() \
            and self._left == child._left and self._right == child._right \
            and ((self._left is None) or (cast(BST[T], self._left).parent() == self)) \
            and ((self._right is None) or (cast(BST[T], self._right).parent() == self))   

    def _removeThisNode(self) -> None:
        """Remove the current node from the tree.  Returns None."""
        # Simple case: this node has no children
        # Just remove this node (invariant may not hold afterwards)
        if (not self.hasLeftChild()) and (not self.hasRightChild()):
            self._removeLeaf()
        # Slightly less simple case: this node has one child
        # Copy up this node's child in place of this node
        elif (not self.hasLeftChild()) or (not self.hasRightChild()):
            self._removeParentOfOne()
        # Two children.  This one's complicated.
        # Copy this node's successor to this node, and remove
        #     the successor from this node's right subtree
        else: 
            successor_data: T = cast(BST, self.findSuccessor()).data()
            self._data = successor_data
            # Remove it from the right subtree
            cast(BST, self.rightChild()).remove(successor_data)

    def remove(self, value: T) -> None:
        """Function to remove the given VALUE from the tree, and
        return the root of the resulting tree.  The tricky part here
        is making sure to preserve the BST property of the tree.
        Raise a ValueError if VALUE is not present."""
        if value < self.data(): # type: ignore
            # Check the left subtree, if it exists
            if self.hasLeftChild():
                cast(BST[T], self.leftChild()).remove(value)
            else: # No subtree, value isn't here
                raise ValueError('Value ' + str(value) + ' not in tree')
        elif value > self.data(): # type: ignore
            # Check the right subtree, if it exists
            if self.hasRightChild():
                cast(BST[T], self.rightChild()).remove(value)
            else: # No subtree, value isn't here
                raise ValueError('Value ' + str(value) + ' not in tree')
        else: # value == self.data(), remove this node
            self._removeThisNode()
        # Post:
        assert (self._data is None) or (value not in self and self._invariant())
