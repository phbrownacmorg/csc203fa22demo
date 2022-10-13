import unittest
from AVLTree import AVLTree

class TestAVLTree(unittest.TestCase):
    def setUp(self) -> None:
        self._1node:AVLTree[int] = AVLTree[int](34)     #  34

        self._2nodesL: AVLTree[int] = AVLTree[int](34)  #     34
        self._2nodesL.add(31)                           #    /   
                                                        #  31

        self._2nodesR: AVLTree[int] = AVLTree[int](34)  #     34
        self._2nodesR.add(47)                           #       \
                                                        #        47
                                                        
        self._3nodes:AVLTree[int] = AVLTree[int](34)    #     34
        self._3nodes.add(47)                            #    /  \
        self._3nodes.add(31)                            #  31    47

        self._5nodes:AVLTree[int] = AVLTree[int](34)    #       34
        self._5nodes.add(47)                            #      /  \
        self._5nodes.add(31)                            #    31    47
        self._5nodes.add(6)                             #   /        \
        self._5nodes.add(70)                            #  6          70

        self._10nodes:AVLTree[int] = AVLTree[int](17)
        # self._10nodes.add(14)
        # self._10nodes.add(11)
        # self._10nodes.add(15)
        # self._10nodes.add(20)
        # self._10nodes.add(27)
        # self._10nodes.add(32)
        # self._10nodes.add(28)
        # self._10nodes.add(22)
        # self._10nodes.add(18)

    def test_invariant(self) -> None:
        self.assertTrue(self._1node._invariant())
        self.assertTrue(self._2nodesL._invariant())
        self.assertTrue(self._2nodesR._invariant())
        self.assertTrue(self._3nodes._invariant())
        self.assertTrue(self._5nodes._invariant())

    def test_balance_factors(self) -> None:
        self.assertEqual(self._1node._balance_factor, 0)

        self.assertEqual(self._2nodesL._balance_factor, 1)
        self.assertEqual(self._2nodesL.leftChild()._balance_factor, 0) # type: ignore
        
        self.assertEqual(self._2nodesR._balance_factor, -1)
        self.assertEqual(self._2nodesR.rightChild()._balance_factor, 0) # type: ignore

        self.assertEqual(self._3nodes._balance_factor, 0)
        self.assertEqual(self._3nodes.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3nodes.rightChild()._balance_factor, 0) # type: ignore

        self.assertEqual(self._5nodes._balance_factor, 0)
        self.assertEqual(self._5nodes.leftChild()._balance_factor, 1) # type: ignore
        self.assertEqual(self._5nodes.rightChild()._balance_factor, -1) # type: ignore
        self.assertEqual(self._5nodes.leftChild().leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.rightChild().rightChild()._balance_factor, 0) # type: ignore

        self.assertEqual(self._10nodes._balance_factor, 0)

    def test_rotL(self) -> None:
        self._2nodesR.add(70) # Force a left rotation
        self.assertEqual(self._2nodesR.data(), 47)
        self.assertEqual(self._2nodesR._balance_factor, 0)
        self.assertEqual(self._2nodesR.leftChild().data(), 34)
        self.assertEqual(self._2nodesR.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._2nodesR.rightChild().data(), 70)
        self.assertEqual(self._2nodesR.rightChild()._balance_factor, 0) # type: ignore

        self._5nodes.add(76) # Force a left rotation
        self.assertEqual(self._5nodes.data(), 34)
        self.assertEqual(self._5nodes._balance_factor, 0)
        self.assertEqual(self._5nodes.rightChild().data(), 70)
        self.assertEqual(self._5nodes.rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.rightChild().rightChild().data(), 76)
        self.assertEqual(self._5nodes.rightChild().rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.rightChild().leftChild().data(), 47)
        self.assertEqual(self._5nodes.rightChild().leftChild()._balance_factor, 0) # type: ignore

    def test_rotR(self) -> None:
        self._2nodesL.add(6) # Force a right rotation
        self.assertEqual(self._2nodesL.data(), 31)
        self.assertEqual(self._2nodesL._balance_factor, 0)
        self.assertEqual(self._2nodesL.leftChild().data(), 6)
        self.assertEqual(self._2nodesL.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._2nodesL.rightChild().data(), 34)
        self.assertEqual(self._2nodesL.rightChild()._balance_factor, 0) # type: ignore

        self._5nodes.add(3) # Force a right rotation
        self.assertEqual(self._5nodes.data(), 34)
        self.assertEqual(self._5nodes._balance_factor, 0)
        self.assertEqual(self._5nodes.leftChild().data(), 6)
        self.assertEqual(self._5nodes.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.leftChild().rightChild().data(), 31)
        self.assertEqual(self._5nodes.leftChild().rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.leftChild().leftChild().data(), 3)
        self.assertEqual(self._5nodes.leftChild().leftChild()._balance_factor, 0) # type: ignore
    

        
if __name__ == '__main__':
    unittest.main()
