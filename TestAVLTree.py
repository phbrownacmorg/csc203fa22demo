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
                                                        
        self._3nodes: AVLTree[int] = AVLTree[int](34)   #     34
        self._3nodes.add(47)                            #    /  \
        self._3nodes.add(31)                            #  31    47

        self._5nodes: AVLTree[int] = AVLTree[int](34)   #       34
        self._5nodes.add(47)                            #      /  \
        self._5nodes.add(31)                            #    31    47
        self._5nodes.add(6)                             #   /        \
        self._5nodes.add(70)                            #  6          70

        # Tree from Miller & Ranum 6.17, Fig. 4
        self._3subsL: AVLTree[str] = AVLTree[str]('E')  #       E   
        self._3subsL.add('C')                           #      / \
        self._3subsL.add('F')                           #     C   F
        self._3subsL.add('B')                           #    / \  
        self._3subsL.add('D')                           #   B   D

        # Same tree but reflected
        self._3subsR: AVLTree[str] = AVLTree[str]('C')  #     C
        self._3subsR.add('B')                           #    / \
        self._3subsR.add('E')                           #   B   E
        self._3subsR.add('D')                           #      / \
        self._3subsR.add('F')                           #     D   F
        
        # self._10nodes:AVLTree[int] = AVLTree[int](17)
        # self._10nodes.add(14)
        # self._10nodes.add(11)
        # self._10nodes.add(15)
        # self._10nodes.add(20)
        # self._10nodes.add(27)
        # self._10nodes.add(32)
        # self._10nodes.add(28)
        # self._10nodes.add(22)
        # self._10nodes.add(18)

    def test_invariant_1(self) -> None:
        self.assertTrue(self._1node._invariant())

    def test_invariant_2L(self) -> None:
        self.assertTrue(self._2nodesL._invariant())

    def test_invariant_2R(self) -> None:
        self.assertTrue(self._2nodesR._invariant())

    def test_invariant_3(self) -> None:
        self.assertTrue(self._3nodes._invariant())

    def test_invariant_5(self) -> None:
        self.assertTrue(self._5nodes._invariant())

    def test_invariant_3subsL(self) -> None:
        self.assertTrue(self._3subsL._invariant())

    def test_invariant_3subsR(self) -> None:
        self.assertTrue(self._3subsR._invariant())

    def test_balance_factors_1(self) -> None:
        self.assertEqual(self._1node._balance_factor, 0)

    def test_balance_factors_2L(self) -> None:
        self.assertEqual(self._2nodesL._balance_factor, 1)
        self.assertEqual(self._2nodesL.leftChild()._balance_factor, 0) # type: ignore
        
    def test_balance_factors_2R(self) -> None:
        self.assertEqual(self._2nodesR._balance_factor, -1)
        self.assertEqual(self._2nodesR.rightChild()._balance_factor, 0) # type: ignore

    def test_balance_factors_3(self) -> None:
        self.assertEqual(self._3nodes._balance_factor, 0)
        self.assertEqual(self._3nodes.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3nodes.rightChild()._balance_factor, 0) # type: ignore

    def test_balance_factors_5(self) -> None:
        self.assertEqual(self._5nodes._balance_factor, 0)
        self.assertEqual(self._5nodes.leftChild()._balance_factor, 1) # type: ignore
        self.assertEqual(self._5nodes.rightChild()._balance_factor, -1) # type: ignore
        self.assertEqual(self._5nodes.leftChild().leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.rightChild().rightChild()._balance_factor, 0) # type: ignore

    def test_balance_factors_3subsL(self) -> None:
        self.assertEqual(self._3subsL._balance_factor, 1)
        self.assertEqual(self._3subsL.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsL.rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsL.leftChild().leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsL.leftChild().rightChild()._balance_factor, 0) # type: ignore

    def test_balance_factors_3subsR(self) -> None:
        self.assertEqual(self._3subsR._balance_factor, -1)
        self.assertEqual(self._3subsR.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsR.rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsR.rightChild().leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsR.rightChild().rightChild()._balance_factor, 0) # type: ignore
        
    def test_rotL(self) -> None:
        self._2nodesR.add(70) # Force a left rotation
        self.assertEqual(self._2nodesR.data(), 47)
        self.assertEqual(self._2nodesR._balance_factor, 0)
        self.assertEqual(self._2nodesR.leftChild().data(), 34)
        self.assertEqual(self._2nodesR.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._2nodesR.rightChild().data(), 70)
        self.assertEqual(self._2nodesR.rightChild()._balance_factor, 0) # type: ignore
    def test_rotLlow(self) -> None:
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

    def test_rotRlow(self) -> None:
        self._5nodes.add(3) # Force a right rotation
        self.assertEqual(self._5nodes.data(), 34)
        self.assertEqual(self._5nodes._balance_factor, 0)
        self.assertEqual(self._5nodes.leftChild().data(), 6)
        self.assertEqual(self._5nodes.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.leftChild().rightChild().data(), 31)
        self.assertEqual(self._5nodes.leftChild().rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.leftChild().leftChild().data(), 3)
        self.assertEqual(self._5nodes.leftChild().leftChild()._balance_factor, 0) # type: ignore
    
    def test_rotLR(self) -> None:
        # Left followed by right
        self._2nodesL.add(32) # Force the double rotation
        self.assertEqual(self._2nodesL.data(), 32)
        self.assertEqual(self._2nodesL._balance_factor, 0)
        self.assertEqual(self._2nodesL.leftChild().data(), 31)
        self.assertEqual(self._2nodesL.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._2nodesL.rightChild().data(), 34)
        self.assertEqual(self._2nodesL.rightChild()._balance_factor, 0) # type: ignore
    def test_rotRL(self) -> None:
        # Right followed by left
        self._2nodesR.add(41)
        self.assertEqual(self._2nodesR.data(), 41)
        self.assertEqual(self._2nodesR._balance_factor, 0)
        self.assertEqual(self._2nodesR.leftChild().data(), 34)
        self.assertEqual(self._2nodesR.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._2nodesR.rightChild().data(), 47)
        self.assertEqual(self._2nodesR.rightChild()._balance_factor, 0) # type:         
    def test_rotL_3subs(self) -> None:
        self._3subsR.add('G') # Force the rotation
        self.assertEqual(self._3subsR.data(), 'E')
        self.assertEqual(self._3subsR._balance_factor, 0) 
        self.assertEqual(self._3subsR.leftChild().data(), 'C')
        self.assertEqual(self._3subsR.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsR.rightChild().data(), 'F')
        self.assertEqual(self._3subsR.rightChild()._balance_factor, -1) # type: ignore
        self.assertEqual(self._3subsR.leftChild().leftChild().data(), 'B')
        self.assertEqual(self._3subsR.leftChild().leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsR.leftChild().rightChild().data(), 'D')
        self.assertEqual(self._3subsR.leftChild().rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsR.rightChild().rightChild().data(), 'G')
        self.assertEqual(self._3subsR.rightChild().rightChild()._balance_factor, 0) # type: ignore
        
    def test_rotR_3subs(self) -> None:
        self._3subsL.add('A') # Force the rotation
        self.assertEqual(self._3subsL.data(), 'C')
        self.assertEqual(self._3subsL._balance_factor, 0) 
        self.assertEqual(self._3subsL.leftChild().data(), 'B')
        self.assertEqual(self._3subsL.leftChild()._balance_factor, 1) # type: ignore
        self.assertEqual(self._3subsL.rightChild().data(), 'E')
        self.assertEqual(self._3subsL.rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsL.leftChild().leftChild().data(), 'A')
        self.assertEqual(self._3subsL.leftChild().leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsL.rightChild().leftChild().data(), 'D')
        self.assertEqual(self._3subsL.rightChild().leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsL.rightChild().rightChild().data(), 'F')
        self.assertEqual(self._3subsL.rightChild().rightChild()._balance_factor, 0) # type: ignore


if __name__ == '__main__':
    unittest.main()
