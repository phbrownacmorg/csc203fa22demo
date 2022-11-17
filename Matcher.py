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
        """Construct and return the table of links to follow
        when a mismatch occurs, as a list of integers.  This
        code assumes that state[k] corresponds to the character
        at pattern[k-1].  Thus, state 0 is the initial state
        that matches nothing and just reads a character."""
        # Extend the pattern to make the indices line up
        aug_pattern: str = "0" + pattern 
        
        # Initialize links to all 0's
        links: List[int] = [0] * len(aug_pattern)
     
        # Loop finds a mismatch state for each state
        for state in range(2, len(aug_pattern)):
            # s is the candidate state to go to
            # Start s as the previous state's mismatch destination
            s = links[state - 1]
            while s >= 1: # If there's a common prefix...
                # See if it can be extended by a character
                if aug_pattern[s] == aug_pattern[state-1]:
                    break
                # If the prefix doesn't extend...
                else:
                    # try going where state s went.  If it's
                    # not state 0, maybe we can extend *that*
                    # common prefix.
                    s = links[s]
                # Invariant:
                assert 0 <= s < state 
            links[state] = s + 1
            # A link can never go forward
            assert 0 <= links[state] < state
        return links

    @staticmethod
    def KMP_matcher(pattern:str, text: str) -> int:
        """Matching using the Knuth-Morris-Pratt algorithm.
        Note that in this implementation, state k corresponds
        to the character pattern[k-1].  The special state that
        always reads a character is state 0."""
        mismatched: List[int] = Matcher.mismatched_links(pattern)
        state: int = 1
        i: int = 0
        result: int = -1

        while i < len(text):
            # If we've succeeded in finding our pattern, stop
            if state > len(pattern):
                break
            # Handle a mismatch (if there is one)
            while (state > 0) and (text[i] != pattern[state-1]):
                state = mismatched[state]
            
            state = state + 1 # Advance the state by 1
            i = i + 1         # and read another character
            # Invariant:
            assert ((0 < i <= len(text)) 
                    and (0 < state <= (len(pattern)+1)))
        # If we found the pattern, return where it starts
        if state > len(pattern):
            result = (i - (state-1))

        return result

