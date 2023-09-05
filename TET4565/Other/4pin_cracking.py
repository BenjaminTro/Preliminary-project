"""
--- A4 ---
This script will decode the SHA-1 code in A4.
What we know about the code:
 - it is encoded with SHA-1
 - it contains 4 symbols
 - the symbols ar all digits
"""

import hashlib
from time import time

def bruteforce(original_code):
    """
    try all possibilities for four digits (abcd) and
    see if we find a corresponding code
    """
    start = time()
    for a in range(10):
        for b in range(10):
            for c in range(10):
                for d in range(10):
                    pin = f'{a}{b}{c}{d}'
                    test_code = hashlib.sha1(pin.encode()).hexdigest()
                    if test_code == original_code:
                        end = time()
                        print(f'cracked code in {end - start} seconds')
                        return pin

#here is the SHA-1 code:
code = "4170ac2a2782a1516fe9e13d7322ae482c1bd594"
pin_code = bruteforce(code)
print(f'pin code is: {pin_code}')
