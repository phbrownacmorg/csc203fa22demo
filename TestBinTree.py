# Empty unit-testing class
# Peter Brown, 26 Jan 2017

import unittest
from BinTree import BinTree

class TestBinTree(unittest.TestCase):

    def setUp(self) -> None:
        self._empty = BinTree[str]()

        self._one = BinTree[str]('animal')

        self._leftOnly = BinTree[str]('animal')
        self._leftOnly.addLeft('mammal')

        self._rightOnly = BinTree[str]('animal')
        self._rightOnly.addRight('bird')

        self._full = BinTree[str]('animal')
        self._full.addLeft('mammal')
        self._full.addRight('bird')
        self._full.leftChild().addLeft('carnivore')
        self._full.leftChild().addRight('ungulate')
        self._full.rightChild().addRight('passerine')
        self._full.leftChild().leftChild().addLeft('feline')
        self._full.leftChild().leftChild().addRight('canine')
        self._full.leftChild().rightChild().addRight('bovid')
        self._full.rightChild().rightChild().addRight('corvid')
        self._full.leftChild().leftChild().leftChild().addLeft('lion')
        self._full.leftChild().leftChild().leftChild().addRight('cat')
        self._full.leftChild().leftChild().rightChild().addRight('wolf')
        self._full.leftChild().rightChild().rightChild().addRight('gazelle')
        self._full.rightChild().rightChild().rightChild().addRight('crow')

    # All methods whose names start with "test"
    # will be treated as tests
    def test_isEmpty(self) -> None:
        self.assertTrue(self._empty.isEmpty())
        self.assertFalse(self._leftOnly.isEmpty())
        self.assertFalse(self._rightOnly.isEmpty())
        self.assertFalse(self._full.isEmpty())

    def test_hasLeft(self) -> None:
        self.assertFalse(self._empty.hasLeftChild())
        self.assertTrue(self._leftOnly.hasLeftChild())
        self.assertFalse(self._rightOnly.hasLeftChild())
        self.assertTrue(self._full.hasLeftChild())

    def test_hasRight(self) -> None:
        self.assertFalse(self._empty.hasRightChild())
        self.assertFalse(self._leftOnly.hasRightChild())
        self.assertTrue(self._rightOnly.hasRightChild())
        self.assertTrue(self._full.hasRightChild())

    def test_data(self) -> None:
        with self.assertRaises(ValueError):
            self._empty.data()
        self.assertEqual(self._leftOnly.data(), 'animal')
        self.assertEqual(self._rightOnly.data(), 'animal')
        self.assertEqual(self._full.data(), 'animal')

    def test_leftChild(self) -> None:
        self.assertEqual(self._leftOnly.leftChild().data(), 'mammal')
        self.assertEqual(self._full.leftChild().data(), 'mammal')

    def test_rightChild(self) -> None:
        self.assertEqual(self._rightOnly.rightChild().data(), 'bird')
        self.assertEqual(self._full.rightChild().data(), 'bird')

    def test_len(self) -> None:
        self.assertEqual(len(self._empty), 0)
        self.assertEqual(len(self._leftOnly), 2)
        self.assertEqual(len(self._rightOnly), 2)
        self.assertEqual(len(self._full), 15)

    def test_addLeft(self) -> None:
        self._empty.addLeft('animal')
        self.assertEqual(len(self._empty), 1)
        self.assertEqual(self._empty.data(), 'animal')
        self._rightOnly.addLeft('mammal')
        self.assertEqual(len(self._rightOnly), 3)
        self.assertEqual(self._rightOnly.leftChild().data(), 'mammal')
        self._full.addLeft('concrete')
        self.assertEqual(len(self._full), 16)
        self.assertEqual(self._full.leftChild().data(), 'concrete')

    def test_addRight(self) -> None:
        self._empty.addRight('animal')
        self.assertEqual(len(self._empty), 1)
        self.assertEqual(self._empty.data(), 'animal')
        self._leftOnly.addRight('bird')
        self.assertEqual(len(self._leftOnly), 3)
        self.assertEqual(self._leftOnly.rightChild().data(), 'bird')
        self._full.addRight('concrete')
        self.assertEqual(len(self._full), 16)
        self.assertEqual(self._full.rightChild().data(), 'concrete')

    def test_removeLeft(self) -> None:
        self._leftOnly.removeLeft()
        self.assertEqual(len(self._leftOnly), 1)
        self.assertFalse(self._leftOnly.hasLeftChild())
        self._full.removeLeft()
        self.assertEqual(len(self._full), 5)
        self.assertFalse(self._full.hasLeftChild())

    def test_removeRight(self) -> None:
        self._rightOnly.removeRight()
        self.assertEqual(len(self._rightOnly), 1)
        self.assertFalse(self._rightOnly.hasRightChild())
        self._full.removeRight()
        self.assertEqual(len(self._full), 11)
        self.assertFalse(self._full.hasRightChild())

    def test_preorder(self) -> None:
        self.assertEqual(self._empty.preorder(), [])
        self.assertEqual(self._leftOnly.preorder(), ['animal', 'mammal'])
        self.assertEqual(self._rightOnly.preorder(), ['animal', 'bird'])
        self.assertEqual(self._full.preorder(), ['animal', 'mammal', 'carnivore', 'feline', 'lion', 'cat', 'canine', 'wolf', 'ungulate', 'bovid', 'gazelle', 'bird', 'passerine', 'corvid', 'crow'])

    def test_postorder(self) -> None:
        self.assertEqual(self._empty.postorder(), [])
        self.assertEqual(self._leftOnly.postorder(), ['mammal', 'animal'])
        self.assertEqual(self._rightOnly.postorder(), ['bird', 'animal'])
        self.assertEqual(self._full.postorder(), ['lion', 'cat', 'feline', 'wolf', 'canine', 'carnivore', 'gazelle', 'bovid', 'ungulate', 'mammal', 'crow', 'corvid', 'passerine', 'bird', 'animal'])

    def test_inorder(self) -> None:
        self.assertEqual(self._empty.inorder(), [])
        self.assertEqual(self._leftOnly.inorder(), ['mammal', 'animal'])
        self.assertEqual(self._rightOnly.inorder(), ['animal', 'bird'])
        self.assertEqual(self._full.inorder(), ['lion', 'feline', 'cat', 'carnivore', 'canine', 'wolf', 'mammal', 'ungulate', 'bovid', 'gazelle', 'animal', 'bird', 'passerine', 'corvid', 'crow'])


if __name__ == '__main__':
    unittest.main()
