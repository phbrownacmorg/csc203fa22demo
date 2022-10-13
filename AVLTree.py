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
        # Must come before the call to super().__init__(), or the superclass
        # constructor's call to self._invariant() will fail.
        self._balance_factor = 0

        super().__init__(data, parent)
        # Postcondition: self._invariant() (checked by superclass constructor)

    def _invariant(self) -> bool:
        """Class invariant for the AVL tree."""
        # The AVL tree has to be a valid BST
        valid: bool = super()._invariant() 
        
        # Check the balance factor
        valid = valid and (-1 <= self._balance_factor <= 1)
        if not self.hasLeftChild() and not self.hasRightChild(): # If a leaf
            valid = valid and self._balance_factor == 0
        elif self.hasLeftChild() and not self.hasRightChild(): # Left child, no right child
            valid = valid and self._balance_factor == \
                (cast(AVLTree[T], self.leftChild())._balance_factor + 1)
        elif self.hasRightChild() and not self.hasLeftChild(): # Right child, no left child
            valid = valid and self._balance_factor == \
                (cast(AVLTree[T], self.rightChild())._balance_factor - 1)
        # Two children
        else:
            valid = valid and self._balance_factor == \
                (self.leftChild().height() - self.rightChild().height())
        
        return valid

    # Mutator methods
    def add(self, value: T) -> None:
        """Add a value to the tree, inserting in its proper place."""
        if value < self.data(): # type: ignore
            if self.hasLeftChild(): # Recursive 
                cast(AVLTree[T], self.leftChild()).add(value)
            else:
                self._left = AVLTree[T](value, self)
                self._left._update_balance()
        elif value > self.data(): # type: ignore
            if self.hasRightChild(): # Recursive 
                cast(AVLTree[T], self.rightChild()).add(value)
            else:
                self._right = AVLTree[T](value, self)
                self._right._update_balance()
        # Elif value == self.data(), don't re-insert it.
        # Just do nothing.
        #assert self._invariant()

    def _update_balance(self) -> None:
        """Called after adding a node to the tree.  If self is out of
        balance (abs(child._balance_factor > 1)), rebalance it.
        Otherwise, update self's parent's balance factor, based on
        self's."""
        if self._balance_factor < -1 or self._balance_factor > 1:
            self._rebalance()
        elif not self.isRoot():
            parent: AVLTree[T] = cast(AVLTree[T], self.parent())
            if parent.hasLeftChild() and self is parent.leftChild():
                parent._balance_factor += 1
            else: # self is parent's right child
                parent._balance_factor -= 1
                
            if parent._balance_factor != 0:
                parent._update_balance()

    def _rebalance(self) -> None:
        """Rebalance the tree at this node."""
        if self._balance_factor < 0:
            if self.hasRightChild():
                rightChild: AVLTree[T] = cast(AVLTree[T], self.rightChild())
                if rightChild._balance_factor > 0:
                    rightChild._rotate_right()
            self._rotate_left()
        elif self._balance_factor > 0:
            if self.hasLeftChild():
                leftChild: AVLTree[T] = cast(AVLTree[T], self.leftChild())
                if leftChild._balance_factor < 0:
                    leftChild._rotate_left()
            self._rotate_right()


    def _rotate_left(self) -> None:
        """Rotate the tree left to rebalance.  The node *object* that starts 
        as the root will remain as the root, with appropriate copying to 
        produce the effect of a classic rotation.  This means that 
        no references outside the rotation are affected.  In particular, 
        rotations can involve the root of the tree."""
        # Pre:
        assert self.hasRightChild()
        
        # new_root in Miller & Ranum
        rot_child: AVLTree[T] = cast(AVLTree[T], self.rightChild())

        # Shift the children
        self._right = rot_child._right
        if self.hasRightChild():
            cast(AVLTree[T], self._right)._parent = self
        rot_child._right = rot_child._left # Parent does not change
        rot_child._left = self._left
        if rot_child.hasLeftChild():
            cast(AVLTree[T], rot_child._left)._parent = rot_child
        self._left = rot_child # rot_child's parent does not change

        # Move the data
        self._data, rot_child._data = rot_child._data, self._data
        
        # Update the balance factors
        old_child_bal: int = rot_child._balance_factor
        rot_child._balance_factor = self._balance_factor + \
            1 - min(0, old_child_bal)
        self._balance_factor = old_child_bal + \
            1 + max(rot_child._balance_factor, 0)
        
        # Post:
        #assert self._invariant()

    def _rotate_right(self) -> None:
        """Rotate the tree right to rebalance.  The node *object* that starts 
        as the root will remain as the root, with appropriate copying to 
        produce the effect of a classic rotation.  This means that 
        no references outside the rotation are affected.  In particular, 
        rotations can involve the root of the tree."""
        # Pre:
        assert self.hasLeftChild()
    
        # new_root in Miller & Ranum
        rot_child: AVLTree[T] = cast(AVLTree[T], self.leftChild())

        # Shift the children
        self._left = rot_child._left
        if self.hasLeftChild():
            cast(AVLTree[T], self._left)._parent = self
        rot_child._left = rot_child._right # Parent does not change
        rot_child._right = self._right
        if rot_child.hasRightChild():
            cast(AVLTree[T], rot_child._right)._parent = rot_child
        self._right = rot_child # rot_child's parent does not change

        # Move the data
        self._data, rot_child._data = rot_child._data, self._data

        # Update balance factors
        old_child_bal: int = rot_child._balance_factor
        rot_child._balance_factor = self._balance_factor - 1 \
            - max(0, old_child_bal)
        self._balance_factor = old_child_bal - 1 + min(0, rot_child._balance_factor)