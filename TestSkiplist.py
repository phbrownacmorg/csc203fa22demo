import random
import unittest
from Skiplist import Skiplist

class TestSkiplist(unittest.TestCase):

    def setUp(self):
        random.seed(144000) # Make "random" results predictable
        self._empty = Skiplist()

        self._1node = Skiplist()
        self._1node[37] = 'thirty-seven'

        self._2nodes = Skiplist()
        self._2nodes[37] = 'thirty-seven'
        self._2nodes[50] = 'fifty'

        self._3nodes = Skiplist()
        self._3nodes[37] = 'thirty-seven'
        self._3nodes[50] = 'fifty' # Insert at end
        self._3nodes[6] = 'six' # Insert at beginning

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

    def testSearch37(self):
        with self.assertRaises(KeyError):
            self._empty.search(37)
        self.assertEqual(self._1node.search(37), 'thirty-seven')
        self.assertEqual(self._2nodes.search(37), 'thirty-seven')
        self.assertEqual(self._3nodes.search(37), 'thirty-seven')

    def testSearch50(self):
        with self.assertRaises(KeyError):
            self._empty[50]
        with self.assertRaises(KeyError):
            self._1node[50]
        self.assertEqual(self._2nodes[50], 'fifty')
        self.assertEqual(self._3nodes[50], 'fifty')

    def testSearch6(self):
        with self.assertRaises(KeyError):
            self._empty[6]
        with self.assertRaises(KeyError):
            self._1node[6]
        with self.assertRaises(KeyError):
            self._2nodes[6]
        self.assertEqual(self._3nodes[6], 'six')

    def testSearch16(self):
        with self.assertRaises(KeyError):
            self._empty.search(16)
        with self.assertRaises(KeyError):
            self._1node.search(16)
        with self.assertRaises(KeyError):
            self._2nodes.search(16)
        with self.assertRaises(KeyError):
            self._3nodes.search(16)

    def testDelFromEmpty(self):
        with self.assertRaises(KeyError):
            self._empty.delete(37)

    def testDelOnly(self):
        self._1node.delete(37)
        self.assertEqual(self._1node._head, None) # Empty list

    def testDelFirst(self):
        self._3nodes.delete(6)
        head = self._3nodes._head
        self.assertTrue(head is not None)
        levels = 2 # 2 levels generated
        for i in range(levels):
            with self.subTest(i=i):
                if i == (levels-1): # bottom level has all nodes
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

    def testDelLast(self):
        self._3nodes.delete(50)
        head = self._3nodes._head
        self.assertTrue(head is not None)
        levels = 1 # 1 levels remaining
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
                    self.assertTrue(node37.next is None)

                if i == (levels-1): # bottom level has both node6 and node37
                    self.assertTrue(node6.down is None)
                    self.assertTrue(node37.down is None)
                    self.assertTrue(head.down is None)
                head = head.down

    def testDelMid(self):
        self._3nodes.delete(37)
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
                    node50 = node6.next
                else: # top level has only node50
                    node50 = head.next
                self.assertEqual(node50.key, 50)
                self.assertEqual(node50.data, 'fifty')
                self.assertTrue(node50.next is None)

                if i < (levels-1): # top level has only node50
                    self.assertTrue(node50.down is not None)
                    self.assertTrue(head.down.next.next is node50.down)
                elif i == (levels-1): # bottom level has both node6 and node50
                    self.assertTrue(node50.down is None)
                    self.assertTrue(node6.down is None)
                    self.assertTrue(head.down is None)
                head = head.down

    def testIter(self):
        self.assertEqual(list(iter(self._empty)), [])
        self.assertEqual(list(iter(self._1node)), [37])
        self.assertEqual(list(iter(self._2nodes)), [37, 50])
        self.assertEqual(list(iter(self._3nodes)), [6, 37, 50])

    def testLen(self):
        self.assertEqual(len(self._empty), 0)
        self.assertEqual(len(self._1node), 1)
        self.assertEqual(len(self._2nodes), 2)
        self.assertEqual(len(self._3nodes), 3)

if __name__ == '__main__':
    unittest.main()
