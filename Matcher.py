from typing import Dict, Tuple

class Matcher:
    """Class to do pattern-matching in strings."""

    @staticmethod
    def find(pattern:str, text:str) -> int:
        """Find the first occurrence of PATTERN in TEXT, and return
        the starting index.  If PATTERN does not occur in TEXT, return -1."""
        return Matcher.simple_matcher(pattern, text)

    @staticmethod
    def simple_matcher(pattern:str, text:str) -> int:
        i = j = 0

        while True:
            while j < len(pattern) and text[i+j] == pattern[j]:
                j = j + 1
            
            if j == len(pattern): # Found it!
                return i
            else: # Try again for i = i + 1
                j = 0
            i = i + 1

            if (i + (len(pattern)-1)) == len(text): # Didn't find the pattern
                return -1    

    @staticmethod
    def _find_next_state(pattern, state, symbol) -> int:
        for i in range(state+1, 0, -1):
            if (pattern[:state] + symbol)[:-i] == pattern[:i]:
                break
        return i

    @staticmethod
    def _make_DFA(pattern, alphabet) -> Dict[Tuple[int, str], int]:
        DFA: Dict[Tuple[int, str], int] = {}
        for state in range(len(pattern)):
            for symbol in alphabet:
                key: Tuple[int, str] = (state, symbol)
                DFA[key] = Matcher._find_next_state(pattern, state, symbol)
        return DFA

    @staticmethod
    def DFA_matcher(pattern: str, text: str, alphabet: str) -> int:
        DFA: Dict[Tuple[int, str], int] = Matcher._make_DFA(pattern, alphabet)
        state: int = 0
        i: int = 0
        result = -1
        while i < len(text) and state < len(pattern):
            key = (state, text[i])
            state = DFA[key]
            i = i + 1
        if state == len(pattern):
            result = (i - len(pattern))
        return result