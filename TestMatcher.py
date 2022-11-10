import unittest
from Matcher import Matcher

class TestMatcher(unittest.TestCase):

    def setUp(self):
        self._ACATA = 'ACATA'
        self._bookText = 'ACGACACATAGTCACTTGGCA'
        self._bookText2 = 'ACGACACAGAGTCACTTGGCA'
        self._bookText3 = 'ACGACACACTACTCACTTGGCA'
        self._t8a1 = 'TTTTTTTTA'

        self._repeat2 = "ACTACT"
        self._repeatN = 'TTTTTTTA'
        self._ACACAT = 'ACACAT'


    def test_present(self):
        self.assertEqual(self._bookText.find(self._ACATA),
                        Matcher.simple_matcher(self._ACATA, self._bookText))
        self.assertEqual(self._bookText3.find(self._repeat2),
                        Matcher.simple_matcher(self._repeat2, self._bookText3))
        self.assertEqual(self._bookText.find(self._ACACAT),
                        Matcher.simple_matcher(self._ACACAT, self._bookText))
        self.assertEqual(self._t8a1.find(self._repeatN),
                        Matcher.simple_matcher(self._repeatN, self._t8a1))

    def test_absent(self):
        self.assertEqual(self._bookText2.find(self._ACATA),
                        Matcher.simple_matcher(self._ACATA, self._bookText2))
        self.assertEqual(self._bookText2.find(self._repeat2),
                        Matcher.simple_matcher(self._repeat2, self._bookText2))
        self.assertEqual(self._bookText3.find(self._ACACAT),
                        Matcher.simple_matcher(self._ACACAT, self._bookText3))
        self.assertEqual(self._bookText.find(self._repeatN),
                        Matcher.simple_matcher(self._repeatN, self._bookText))

    def test_DFA_present(self):
        self.assertEqual(self._bookText.find(self._ACATA),
                        Matcher.DFA_matcher(self._ACATA, self._bookText, 'ACGT'))
        self.assertEqual(self._bookText3.find(self._repeat2),
                        Matcher.DFA_matcher(self._repeat2, self._bookText3, 'ACGT'))
        self.assertEqual(self._bookText.find(self._ACACAT),
                        Matcher.DFA_matcher(self._ACACAT, self._bookText, 'ACGT'))
        self.assertEqual(self._t8a1.find(self._repeatN),
                        Matcher.DFA_matcher(self._repeatN, self._t8a1, 'ACGT'))

    def test_DFA_absent(self):
        self.assertEqual(self._bookText2.find(self._ACATA),
                        Matcher.DFA_matcher(self._ACATA, self._bookText2, 'ACGT'))
        self.assertEqual(self._bookText2.find(self._repeat2),
                        Matcher.DFA_matcher(self._repeat2, self._bookText2, 'ACGT'))
        self.assertEqual(self._bookText3.find(self._ACACAT),
                        Matcher.DFA_matcher(self._ACACAT, self._bookText3, 'ACGT'))
        self.assertEqual(self._bookText.find(self._repeatN),
                        Matcher.DFA_matcher(self._repeatN, self._bookText, 'ACGT'))

if __name__ == '__main__':
    unittest.main()