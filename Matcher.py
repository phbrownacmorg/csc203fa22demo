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
     
        # Loop finds a mismatch state for each state in the DFA
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
            # Handle a mismatch (if there is one)
            while (state > 0) and (text[i] != pattern[state-1]):
                state = mismatched[state]
            
            state = state + 1 # Advance the state by 1
            i = i + 1         # and read another character

            # If we've succeeded in finding our pattern, stop
            # Note this must be checked *between* incrementing state and
            #    checking whether i < len(text), to ensure that if state
            #    enters the accepting state the fact is recorded before
            #    leaving the loop.
            if state == len(pattern) + 1: # In the accepting state
                result = (i - (state-1)) # Record where the match starts
                break

            # Invariant:
            assert ((0 < i <= len(text)) 
                    and (0 < state <= len(pattern)))

        return result

    # BOYER-MOORE: this implementation comes from 
    # https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm,
    # downloaded 2022-11-17.
    
    # This version is sensitive to the English alphabet in ASCII for case-insensitive matching.
    # To remove this feature, define alphabet_index as ord(c), and replace instances of "26"
    # with "256" or any maximum code-point you want. For Unicode you may want to match in UTF-8
    # bytes instead of creating a 0x10FFFF-sized table.

    ALPHABET_SIZE = 26

    @staticmethod
    def alphabet_index(c: str) -> int:
        """Return the index of the given character in the English alphabet, counting from 0."""
        val = ord(c.lower()) - ord("a")
        assert val >= 0 and val < Matcher.ALPHABET_SIZE
        return val

    @staticmethod
    def match_length(S: str, idx1: int, idx2: int) -> int:
        """Return the length of the match of the substrings of S beginning at idx1 and idx2."""
        if idx1 == idx2:
            return len(S) - idx1
        match_count = 0
        while idx1 < len(S) and idx2 < len(S) and S[idx1] == S[idx2]:
            match_count += 1
            idx1 += 1
            idx2 += 1
        return match_count

    @staticmethod
    def fundamental_preprocess(S: str) -> List[int]:
        """Return Z, the Fundamental Preprocessing of S.

        Z[i] is the length of the substring beginning at i which is also a prefix of S.
        This pre-processing is done in O(n) time, where n is the length of S.
        """
        if len(S) == 0:  # Handles case of empty string
            return []
        if len(S) == 1:  # Handles case of single-character string
            return [1]
        z = [0 for x in S]
        z[0] = len(S)
        z[1] = Matcher.match_length(S, 0, 1)
        for i in range(2, 1 + z[1]):  # Optimization from exercise 1-5
            z[i] = z[1] - i + 1
        # Defines lower and upper limits of z-box
        l = 0
        r = 0
        for i in range(2 + z[1], len(S)):
            if i <= r:  # i falls within existing z-box
                k = i - l
                b = z[k]
                a = r - i + 1
                if b < a:  # b ends within existing z-box
                    z[i] = b
                else:  # b ends at or after the end of the z-box, we need to do an explicit match to the right of the z-box
                    z[i] = a + Matcher.match_length(S, a, r + 1)
                    l = i
                    r = i + z[i] - 1
            else:  # i does not reside within existing z-box
                z[i] = Matcher.match_length(S, 0, i)
                if z[i] > 0:
                    l = i
                    r = i + z[i] - 1
        return z

    @staticmethod
    def bad_character_table(S: str) -> List[List[int]]:
        """
        Generates R for S, which is an array indexed by the position of some character c in the
        English alphabet. At that index in R is an array of length |S|+1, specifying for each
        index i in S (plus the index after S) the next location of character c encountered when
        traversing S from right to left starting at i. This is used for a constant-time lookup
        for the bad character rule in the Boyer-Moore string search algorithm, although it has
        a much larger size than non-constant-time solutions.
        """
        if len(S) == 0:
            return [[] for a in range(Matcher.ALPHABET_SIZE)]
        R = [[-1] for a in range(Matcher.ALPHABET_SIZE)]
        alpha = [-1 for a in range(Matcher.ALPHABET_SIZE)]
        for i, c in enumerate(S):
            alpha[Matcher.alphabet_index(c)] = i
            for j, a in enumerate(alpha):
                R[j].append(a)
        return R

    @staticmethod
    def good_suffix_table(S: str) -> List[int]:
        """
        Generates L for S, an array used in the implementation of the strong good suffix rule.
        L[i] = k, the largest position in S such that S[i:] (the suffix of S starting at i) matches
        a suffix of S[:k] (a substring in S ending at k). Used in Boyer-Moore, L gives an amount to
        shift P relative to T such that no instances of P in T are skipped and a suffix of P[:L[i]]
        matches the substring of T matched by a suffix of P in the previous match attempt.
        Specifically, if the mismatch took place at position i-1 in P, the shift magnitude is given
        by the equation len(P) - L[i]. In the case that L[i] = -1, the full shift table is used.
        Since only proper suffixes matter, L[0] = -1.
        """
        L = [-1 for c in S]
        N = Matcher.fundamental_preprocess(S[::-1])  # S[::-1] reverses S
        N.reverse()
        for j in range(0, len(S) - 1):
            i = len(S) - N[j]
            if i != len(S):
                L[i] = j
        return L

    @staticmethod
    def full_shift_table(S: str) -> List[int]:
        """
        Generates F for S, an array used in a special case of the good suffix rule in the Boyer-Moore
        string search algorithm. F[i] is the length of the longest suffix of S[i:] that is also a
        prefix of S. In the cases it is used, the shift magnitude of the pattern P relative to the
        text T is len(P) - F[i] for a mismatch occurring at i-1.
        """
        F = [0 for c in S]
        Z = Matcher.fundamental_preprocess(S)
        longest = 0
        for i, zv in enumerate(reversed(Z)):
            longest = max(zv, longest) if zv == i + 1 else longest
            F[-i - 1] = longest
        return F

    @staticmethod
    def BM_matcher(P:str, T:str) -> int:
        """
        Implementation of the Boyer-Moore string search algorithm. This finds 
        the first occurrence of P in T, and incorporates numerous ways of 
        pre-processing the pattern to determine the optimal amount to shift the
        string and skip comparisons. In practice it runs in O(m) (and even
        sublinear) time, where m is the length of T. This implementation
        performs a case-insensitive search on ASCII alphabetic characters,
        spaces not included.
        """
        if len(P) == 0 or len(T) == 0 or len(T) < len(P):
            return -1

        matches = [-1]

        # Preprocessing
        R = Matcher.bad_character_table(P)
        L = Matcher.good_suffix_table(P)
        F = Matcher.full_shift_table(P)

        k = len(P) - 1      # Represents alignment of end of P relative to T
        previous_k = -1     # Represents alignment in previous phase (Galil's rule)
        while k < len(T):
            i = len(P) - 1  # Character to compare in P
            h = k           # Character to compare in T
            while i >= 0 and h > previous_k and P[i] == T[h]:  # Matches starting from end of P
                i -= 1
                h -= 1
            if i == -1 or h == previous_k:  # Match has been found (Galil's rule)
                matches[0] = k - len(P) + 1
                break
                #k += len(P) - F[1] if len(P) > 1 else 1
            else:  # No match, shift by max of bad character and good suffix rules
                char_shift = i - R[Matcher.alphabet_index(T[h])][i]
                if i + 1 == len(P):  # Mismatch happened on first attempt
                    suffix_shift = 1
                elif L[i + 1] == -1:  # Matched suffix does not appear anywhere in P
                    suffix_shift = len(P) - F[i + 1]
                else:               # Matched suffix appears in P
                    suffix_shift = len(P) - 1 - L[i + 1]
                shift = max(char_shift, suffix_shift)
                previous_k = k if shift >= i + 1 else previous_k  # Galil's rule
                k += shift
        return matches[0]
