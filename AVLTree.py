from typing import cast, Optional, TypeVar
from BST import BST

T = TypeVar('T') # Must support comparisons

class AVLTree(BST[T]):
    """Class to represent an AVL tree.  This class does not
    represent the empty tree; that is, a AVL tree must *always*
    have at least one node."""

    def __init__(self, data: T, parent: Optional['AVLTree[T]'] = None):
        """Create a AVL node with the given DATA and PARENT.
        Note that DATA cannot be None."""
        super().__init__(data, parent)
        self._balance_factor = 0
        assert self._invariant()

    def _invariant(self) -> bool:
        """Class invariant for the AVL tree."""
        # The AVL tree has to be a valid BST
        valid: bool = super()._invariant() 

        # Check the balance factor
        valid = valid and (-1 <= self._balance_factor <= 1)
        if not self.hasLeftChild() and not self.hasRightChild(): # If a leaf
            valid = valid and self._balance_factor == 0
        elif self.hasLeftChild() and not self.hasRightChild(): # Left child, no right child
            valid = valid and self._balance_factor == (cast(AVLTree[T], self.rightChild())._balance_factor + 1)
        elif self.hasRightChild() and not self.hasLeftChild(): # Right child, no left child
            valid = valid and self._balance_factor == (cast(AVLTree[T], self.leftChild())._balance_factor - 1)
        # Two children

        return valid
