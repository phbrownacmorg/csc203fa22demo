import random
import unittest
from Skiplist import Skiplist

class TestSkiplist(unittest.TestCase):

    def setUp(self):
        random.seed(144000) # Make "random" results predictable
        self._empty = Skiplist()

        self._1node = Skiplist()
        self._1node.insert(37, 'thirty-seven')

        self._2nodes = Skiplist()
        self._2nodes.insert(37, 'thirty-seven')
        self._2nodes.insert(50, 'fifty')

        self._3nodes = Skiplist()
        self._3nodes.insert(37, 'thirty-seven')
        self._3nodes.insert(50, 'fifty') # Insert at end
        self._3nodes.insert(6, 'six') # Insert at beginning

    def testEmpty(self):
        self.assertTrue(self._empty._head is None)

    def test1Node(self):
        self.assertTrue(self._1node._head is not None)
        head = self._1node._head
        levels = 1 # only 1 level
        for i in range(levels): 
            with self.subTest(i=i):
                node37 = head.next
                self.assertEqual(node37.key, 37)
                self.assertEqual(node37.data, 'thirty-seven')
                self.assertTrue(node37.next is None)
                self.assertTrue(node37.down is None)
                self.assertTrue(head.down is None)
                head = head.down

    def test2Nodes(self):
        head = self._2nodes._head
        self.assertTrue(head is not None)
        levels = 2 # 2 levels generated
        for i in range(levels):
            with self.subTest(i=i):
                if i == (levels-1): # bottom level has node37
                    node37 = head.next
                    self.assertEqual(node37.key, 37)
                    self.assertEqual(node37.data, 'thirty-seven')
                    self.assertTrue(node37.next is not None)
                    node50 = node37.next
                else: # top level has only node50
                    node50 = head.next
                self.assertEqual(node50.key, 50)
                self.assertEqual(node50.data, 'fifty')
                self.assertTrue(node50.next is None)
                if i < (levels-1): # top level has only node50
                    self.assertTrue(node50.down is not None)
                    self.assertTrue(head.down.next.next is node50.down)
                elif i == (levels-1): # bottom level has both node37 and node50
                    self.assertTrue(node50.down is None)
                    self.assertTrue(node37.down is None)
                    self.assertTrue(head.down is None)
                head = head.down

    def test3Nodes(self):
        head = self._3nodes._head
        self.assertTrue(head is not None)
        levels = 2 # 2 levels generated
        for i in range(levels):
            with self.subTest(i=i):
                if i == (levels-1): # bottom level has all nodes
                    node6 = head.next
                    self.assertEqual(node6.key, 6)
                    self.assertEqual(node6.data, 'six')
                    self.assertTrue(node6.next is not None)
                    node37 = node6.next
                    self.assertEqual(node37.key, 37)
                    self.assertEqual(node37.data, 'thirty-seven')
                    self.assertTrue(node37.next is not None)
                    node50 = node37.next
                else: # top level has only node50
                    node50 = head.next
                self.assertEqual(node50.key, 50)
                self.assertEqual(node50.data, 'fifty')
                self.assertTrue(node50.next is None)
                if i < (levels-1): # top level has only node50
                    self.assertTrue(node50.down is not None)
                    self.assertTrue(head.down.next.next.next is node50.down)
                elif i == (levels-1): # bottom level has both node37 and node50
                    self.assertTrue(node50.down is None)
                    self.assertTrue(node37.down is None)
                    self.assertTrue(node6.down is None)
                    self.assertTrue(head.down is None)
                head = head.down

if __name__ == '__main__':
    unittest.main()