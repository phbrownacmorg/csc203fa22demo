import unittest
from AVLTree import AVLTree

class TestAVLTree(unittest.TestCase):
    def setUp(self) -> None:
        self._1node:AVLTree[str] = AVLTree[str]('F')    #  F

        self._2nodesL: AVLTree[str] = AVLTree[str]('F') #     F
        self._2nodesL.add('D')                          #    /   
                                                        #   D

        self._2nodesR: AVLTree[str] = AVLTree[str]('F') #     F
        self._2nodesR.add('H')                          #      \
                                                        #       H
                                                        
        self._3nodes: AVLTree[str] = AVLTree[str]('F')  #     F
        self._3nodes.add('H')                           #    / \
        self._3nodes.add('D')                           #   D   H

        self._5nodes: AVLTree[str] = AVLTree[str]('F')  #       F
        self._5nodes.add('H')                           #      / \
        self._5nodes.add('D')                           #     D   H
        self._5nodes.add('B')                           #    /     \
        self._5nodes.add('J')                           #   B       J

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
        self.assertEqual(self._1node.inorder(), ['F'])
        self.assertEqual(self._1node.preorder(), ['F'])
        
    def test_invariant_2L(self) -> None:
        self.assertTrue(self._2nodesL._invariant())
        self.assertEqual(self._2nodesL.inorder(), ['D', 'F'])
        self.assertEqual(self._2nodesL.preorder(), ['F', 'D'])
        
    def test_invariant_2R(self) -> None:
        self.assertTrue(self._2nodesR._invariant())
        self.assertEqual(self._2nodesR.inorder(), ['F', 'H'])
        self.assertEqual(self._2nodesR.preorder(), ['F', 'H'])

    def test_invariant_3(self) -> None:
        self.assertTrue(self._3nodes._invariant())
        self.assertEqual(self._3nodes.inorder(), ['D', 'F', 'H'])
        self.assertEqual(self._3nodes.preorder(), ['F', 'D', 'H'])

    def test_invariant_5(self) -> None:
        self.assertTrue(self._5nodes._invariant())
        self.assertEqual(self._5nodes.inorder(), ['B', 'D', 'F', 'H', 'J'])
        self.assertEqual(self._5nodes.preorder(), ['F', 'D', 'B', 'H', 'J'])

    def test_invariant_3subsL(self) -> None:
        self.assertTrue(self._3subsL._invariant())
        self.assertEqual(self._3subsL.inorder(), ['B', 'C', 'D', 'E', 'F'])
        self.assertEqual(self._3subsL.preorder(), ['E', 'C', 'B', 'D', 'F'])

    def test_invariant_3subsR(self) -> None:
        self.assertTrue(self._3subsR._invariant())
        self.assertEqual(self._3subsR.inorder(), ['B', 'C', 'D', 'E', 'F'])
        self.assertEqual(self._3subsR.preorder(), ['C', 'B', 'E', 'D', 'F'])

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
        self._2nodesR.add('J') # Force a left rotation
        self.assertEqual(self._2nodesR.data(), 'H')
        self.assertEqual(self._2nodesR._balance_factor, 0)
        self.assertEqual(self._2nodesR.leftChild().data(), 'F')
        self.assertEqual(self._2nodesR.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._2nodesR.rightChild().data(), 'J')
        self.assertEqual(self._2nodesR.rightChild()._balance_factor, 0) # type: ignore

    def test_rotLlow(self) -> None:
        self._5nodes.add('K') # Force a left rotation
        self.assertEqual(self._5nodes.data(), 'F')
        self.assertEqual(self._5nodes._balance_factor, 0)
        self.assertEqual(self._5nodes.rightChild().data(), 'J')
        self.assertEqual(self._5nodes.rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.rightChild().rightChild().data(), 'K')
        self.assertEqual(self._5nodes.rightChild().rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.rightChild().leftChild().data(), 'H')
        self.assertEqual(self._5nodes.rightChild().leftChild()._balance_factor, 0) # type: ignore

    def test_rotR(self) -> None:
        self._2nodesL.add('B') # Force a right rotation
        self.assertEqual(self._2nodesL.data(), 'D')
        self.assertEqual(self._2nodesL._balance_factor, 0)
        self.assertEqual(self._2nodesL.leftChild().data(), 'B')
        self.assertEqual(self._2nodesL.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._2nodesL.rightChild().data(), 'F')
        self.assertEqual(self._2nodesL.rightChild()._balance_factor, 0) # type: ignore

    def test_rotRlow(self) -> None:
        self._5nodes.add('A') # Force a right rotation
        self.assertEqual(self._5nodes.data(), 'F')
        self.assertEqual(self._5nodes._balance_factor, 0)
        self.assertEqual(self._5nodes.leftChild().data(), 'B')
        self.assertEqual(self._5nodes.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.leftChild().rightChild().data(), 'D')
        self.assertEqual(self._5nodes.leftChild().rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.leftChild().leftChild().data(), 'A')
        self.assertEqual(self._5nodes.leftChild().leftChild()._balance_factor, 0) # type: ignore
    
    def test_rotLR(self) -> None:
        # Left followed by right
        self._2nodesL.add('E') # Force the double rotation
        self.assertEqual(self._2nodesL.data(), 'E')
        self.assertEqual(self._2nodesL._balance_factor, 0)
        self.assertEqual(self._2nodesL.leftChild().data(), 'D')
        self.assertEqual(self._2nodesL.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._2nodesL.rightChild().data(), 'F')
        self.assertEqual(self._2nodesL.rightChild()._balance_factor, 0) # type: ignore

    def test_rotRL(self) -> None:
        # Right followed by left
        self._2nodesR.add('G')
        self.assertEqual(self._2nodesR.data(), 'G')
        self.assertEqual(self._2nodesR._balance_factor, 0)
        self.assertEqual(self._2nodesR.leftChild().data(), 'F')
        self.assertEqual(self._2nodesR.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._2nodesR.rightChild().data(), 'H')
        self.assertEqual(self._2nodesR.rightChild()._balance_factor, 0) # type: ignore

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

    def test_rmAbsentL(self) -> None:
        with self.assertRaises(ValueError):
            self._1node.remove('A')

    def test_rmAbsentR(self) -> None:
        with self.assertRaises(ValueError):
            self._1node.remove('Z')

    def test_rmRootNoChildren(self) -> None:
        with self.assertRaises(ValueError):
            self._1node.remove('F')

    def test_rmRoot1ChildL(self) -> None:
        self._2nodesL.remove('F')
        self.assertEqual(self._2nodesL.inorder(), ['D'])
        self.assertEqual(self._2nodesL._balance_factor, 0)
        
    def test_rmRoot1ChildR(self) -> None:
        self._2nodesR.remove('F')
        self.assertEqual(self._2nodesR.inorder(), ['H'])
        self.assertEqual(self._2nodesR._balance_factor, 0)

    def test_rmLeafLNoRot(self) -> None:
        self._3subsR.remove('D')
        self.assertEqual(self._3subsR.inorder(), ['B', 'C', 'E', 'F'])
        self.assertEqual(self._3subsR._balance_factor, -1)
        self.assertEqual(self._3subsR.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsR.rightChild()._balance_factor, -1) # type: ignore
        self.assertEqual(self._3subsR.rightChild().rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsR.preorder(), ['C', 'B', 'E', 'F'])

    def test_rmLeafRNoRot(self) -> None:
        self._3subsL.remove('D')
        self.assertEqual(self._3subsL.inorder(), ['B', 'C', 'E', 'F'])
        self.assertEqual(self._3subsL.preorder(), ['E', 'C', 'B', 'F'])
        self.assertEqual(self._3subsL._balance_factor, 1)
        self.assertEqual(self._3subsL.leftChild()._balance_factor, 1) # type: ignore
        self.assertEqual(self._3subsL.rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsL.leftChild().leftChild()._balance_factor, 0) # type: ignore
        
    def test_rmLeafLRot(self) -> None:
        self._3subsR.remove('B')
        self.assertEqual(self._3subsR.inorder(), ['C', 'D', 'E', 'F'])
        self.assertEqual(self._3subsR.preorder(), ['E', 'C', 'D', 'F'])
        self.assertEqual(self._3subsR._balance_factor, 1)
        self.assertEqual(self._3subsR.leftChild()._balance_factor, -1) # type: ignore
        self.assertEqual(self._3subsR.rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsR.leftChild().rightChild()._balance_factor, 0) # type: ignore
        
    def test_rmLeafRRot(self) -> None:
        self._3subsL.remove('F')
        self.assertEqual(self._3subsL.inorder(), ['B', 'C', 'D', 'E'])
        self.assertEqual(self._3subsL.preorder(), ['C', 'B', 'E', 'D'])
        self.assertEqual(self._3subsL._balance_factor, -1)
        self.assertEqual(self._3subsL.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsL.rightChild()._balance_factor, 1) # type: ignore
        self.assertEqual(self._3subsL.rightChild().leftChild()._balance_factor, 0) # type: ignore

    def test_rm1childL(self) -> None:
        self._5nodes.remove('D')
        self.assertEqual(self._5nodes.inorder(), ['B', 'F', 'H', 'J'])
        self.assertEqual(self._5nodes.preorder(), ['F', 'B', 'H', 'J'])
        self.assertEqual(self._5nodes._balance_factor, -1)
        self.assertEqual(self._5nodes.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.rightChild()._balance_factor, -1) # type: ignore
        self.assertEqual(self._5nodes.rightChild().rightChild()._balance_factor, 0) # type: ignore
        
    def test_rm1childR(self) -> None:
        self._5nodes.remove('H')
        self.assertEqual(self._5nodes.inorder(), ['B', 'D', 'F', 'J'])
        self.assertEqual(self._5nodes.preorder(), ['F', 'D', 'B', 'J'])
        self.assertEqual(self._5nodes._balance_factor, 1)
        self.assertEqual(self._5nodes.leftChild()._balance_factor, 1) # type: ignore
        self.assertEqual(self._5nodes.rightChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._5nodes.leftChild().leftChild()._balance_factor, 0) # type: ignore
    
    def test_rm2kids(self) -> None:
        self._3subsR.remove('E')
        self.assertEqual(self._3subsR.inorder(), ['B', 'C', 'D', 'F'])
        self.assertEqual(self._3subsR.preorder(), ['C', 'B', 'F', 'D'])
        self.assertEqual(self._3subsR._balance_factor, -1)
        self.assertEqual(self._3subsR.leftChild()._balance_factor, 0) # type: ignore
        self.assertEqual(self._3subsR.rightChild()._balance_factor, 1) # type: ignore
        self.assertEqual(self._3subsR.rightChild().leftChild()._balance_factor, 0) # type: ignore

if __name__ == '__main__':
    unittest.main()
