class Caesar:
    """Class to implement a Caesar cipher.  Defaults to rot13."""

    letters: str = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, offset: int = 13) -> None:
        """Create a Caesar cipher with a given offset, defaulting
        to 13."""
        self._offset = offset
        self._deoffset = 26 - self._offset

    def encrypt(self, plain: str) -> str:
        """Takes a message PLAIN in plaintext and returns the same message encrypted."""
        cipher: str = ''
        for c in plain:
            if not c.isalpha(): # Pass non-letters straight through
                cipher = cipher + c
            else: # Rotate letters, preserving case
                pos: int = Caesar.letters.find(c.lower())
                rot_c: str = Caesar.letters[(pos + self._offset) % 26]
                if c.isupper():
                    rot_c = rot_c.upper()
                cipher = cipher + rot_c
        return cipher

    def decrypt(self, cipher: str) -> str:
        """Takes a message CIPHER in cipher text and returns the same message in
            plaintext."""
        plain: str = ''
        for c in cipher:
            if not c.isalpha(): # Pass non-letters straight through
                plain = plain + c
            else: # Rotate letters, preserving case
                pos: int = Caesar.letters.find(c.lower())
                rot_c: str = Caesar.letters[(pos + self._deoffset) % 26]
                if c.isupper():
                    rot_c = rot_c.upper()
                plain = plain + rot_c
        return plain


def main() -> int:
    # Read a message from the keyboard, encrypt it, and decrypt it
    offset: int = int(input('Please enter an integer from 1 through 25 to use as an offset:'))
    caesar: Caesar = Caesar(offset)
    msg: str = input('Please enter the plaintext for our secret message:')
    cipher: str = caesar.encrypt(msg)
    print(cipher)
    plain: str = caesar.decrypt(cipher)
    print(plain)
    if plain == msg:
        print('The plaintext matches.')
    else:
        print('The plaintext does NOT match!')

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
