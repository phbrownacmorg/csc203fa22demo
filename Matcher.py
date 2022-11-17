from typing import Dict, List, Tuple

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
        result = 0
        for i in range(state+1, 0, -1):
            if (pattern[:state] + symbol)[-i:] == pattern[:i]:
                result = i
                break
        return result

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
        result: int = -1
        while i < len(text) and state < len(pattern):
            key = (state, text[i])
            state = DFA[key]
            i = i + 1
        if state == len(pattern):
            result = (i - len(pattern))
        return result

    @staticmethod
    def mismatched_links(pattern: str) -> List[int]:
        aug_pattern: str = "0" + pattern
        # Initialize links to all 0's
        links: List[int] = [0] * len(pattern) 
        for k in range(2, len(aug_pattern)):
            s = links[k - 1]
            while s >= 1:
                if aug_pattern[s] == aug_pattern[k - 1]:
                    break
                else:
                    s = links[s]
            links[k] = s + 1
        return links

    @staticmethod
    def KMP_matcher(pattern:str, text: str) -> int:
        mismatched: List[int] = Matcher.mismatched_links(pattern)
        state: int = 1
        i: int = 0
        result: int = -1

        while i < len(text) and state < len(pattern):
            while (state > 0) and (text[i] != pattern[state-1]):
                state = mismatched[state]
            state = state + 1
            i = i + 1
        if i == len(pattern):
            result = (i - state)


        return result

