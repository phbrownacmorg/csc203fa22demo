class Matcher:
    """Class to do pattern-matching in strings."""

    def find(pattern, text):
        """Find the first occurrence of PATTERN in TEXT, and return
        the starting index.  If PATTERN does not occur in TEXT, return -1."""
        return Matcher.simple_matcher(pattern, text)

    def simple_matcher(pattern, text):
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
