import random
from typing import List, Tuple

def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)

def ext_gcd(x: int, y: int) -> Tuple[int, int, int]:
    if y == 0:
        return (x, 1, 0)
    else:
        (d, a, b) = ext_gcd(y, x % y)
        return (d, b, a - (x // y) * b)

def str_to_chunks(msg: str, chunk_size: int):
    msg_bytes = bytes(msg, "utf-8")
    hex_str = "".join([f"{b:02x}" for b in msg_bytes])
    num_chunks = len(hex_str) // chunk_size
    chunk_list = []
    for i in range(
        0, num_chunks * chunk_size + 1, chunk_size
    ):
        chunk_list.append(hex_str[i : i + chunk_size])
    chunk_list = [
        eval("0x" + x) for x in chunk_list if x
    ]
    return chunk_list


def chunks_to_str(chunk_list: List[int], chunk_size: int) -> str:
    """Given a list of chunks CHUNK_LIST and a chunk size CHUNK_SIZE,
    split the contents of CHUNK_LIST into appropriately-sized chunks.
    Leave the chunks on CHUNK_LIST."""
    hex_list = []
    for chunk in chunk_list:
        hex_str = hex(chunk)[2:]
        clen = len(hex_str)
        hex_list.append(hex_str)
#        hex_list.append(
#            "0" * ((chunk_size - clen) % 2) + hex_str
#        )
    # The zero-padding has the effect of causing a crash whenever there
    # are 3k+1 characters in the plaintext, for integer k, when
    # chunk_size=3.
    hstring = "".join(hex_list)
    msg_array = bytearray.fromhex(hstring)
    return msg_array.decode("utf-8")
    # STILL fails with error "invalid start byte"

def modexp(x: int, n: int, p: int) -> int:
    """Calculate and return x ** p % n."""
    if n == 0:
        return 1
    t = (x * x) % p
    tmp = modexp(t, n // 2, p)
    if n % 2 != 0:
        tmp = (tmp * x) % p
    return tmp

#(5563, 8191)

def gen_keys(p: int, q: int) -> Tuple[int, int, int]:
    n = p * q
    m = (p - 1) * (q - 1)
    e = int(random.random() * n)
    while gcd(m, e) != 1:
        e = int(random.random() * n)
    d, a, b = ext_gcd(m, e)
    if b < 0:
        d = m + b
    else:
        d = b
    return (e, d, n)

def encrypt(msg: str, e: int, n: int) -> List[int]:
    """Given an encryption key E and a modulus N,
       encrypt the given message M."""
    chunk_size: int = n.bit_length() // 8
    all_chunks: List[int] = str_to_chunks(msg, chunk_size)
    return [
        modexp(msg_chunk, e, n)
        for msg_chunk in all_chunks
    ]

def decrypt(cipher_chunks: List[int], d: int, n: int) -> str:
    """Given a decryption key D and a modulus N, 
        decrypt the given ciphertext in CIPHER_CHUNKS."""
    chunk_size: int = n.bit_length() // 8
    plain_chunks: List[int] = [
        modexp(cipher_chunk, d, n)
        for cipher_chunk in cipher_chunks
    ]
    return chunks_to_str(plain_chunks, chunk_size)

def main() -> int:
    # Read a message from the keyboard, encrypt it, and decrypt it
    e, d, n = gen_keys(5563, 8191)
    msg: str = input('Please enter the plaintext for our secret message: ')
    cipher: List[int] = encrypt(msg, e, n)
    print(cipher)
    plain: str = decrypt(cipher, d, n)
    print(plain)
    if plain == msg:
        print('The plaintext matches.')
    else:
        print('The plaintext does NOT match!')

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
