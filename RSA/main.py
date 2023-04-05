# electronic signature and RSA implementation

import random
import math
import hashlib
from random import randrange, getrandbits
import rsa.core as core

input_string = "Hello world"
random.seed(11)


# RSA implementation
def my_rsa():
    # generate prime numbers
    p = generate_prime()
    while True:
        q = generate_prime()
        if q != p:
            break
    n = p * q
    phi = (p - 1) * (q - 1)
    e = generate_e(phi)
    d = generate_d(e, phi)
    # return RSA keys
    return n, e, d, p, q


# generate 100-digit prime number
def generate_prime(length=350):
    def is_prime(n, k):
        # Test if n is not even.
        # But care, 2 is prime !
        if n == 2 or n == 3:
            return True
        if n <= 1 or n % 2 == 0:
            return False
        # find r and s
        s = 0
        r = n - 1
        while r & 1 == 0:
            s += 1
            r //= 2
        # do k tests
        for _ in range(k):
            a = randrange(2, n - 1)
            x = pow(a, r, n)
            if x != 1 and x != n - 1:
                j = 1
                while j < s and x != n - 1:
                    x = pow(x, 2, n)
                    if x == 1:
                        return False
                    j += 1
                if x != n - 1:
                    return False
        return True

    def generate_prime_candidate(length_bits):
        # generate random bits
        number = getrandbits(length_bits)
        number |= (1 << length_bits - 1) | 1
        return number

    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p


def generate_e(phi):
    e = random.randint(2, phi - 1)
    while not is_coprime(e, phi):
        e = random.randint(2, phi - 1)
    return e


def is_coprime(num1, num2):
    return math.gcd(num1, num2) == 1


def generate_d(e, phi):
    # return modular inverse of e
    return mod_inverse(e, phi)


def mod_inverse(a, m):
    # calculate gcd
    g, x, y = extended_euclid(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x % m


def extended_euclid(a, b):
    # base case
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_euclid(b % a, a)
    return gcd, y1 - (b // a) * x1, x1


def my_rsa_int_encrypt(message, e, n):
    return pow(message, e, n)


def my_rsa_int_decrypt(cipher, d, n):
    return pow(cipher, d, n)


def generate_hash(message):
    return hashlib.sha256(message.encode()).hexdigest()


def sign_message(message, d, n):
    hash_message = int(generate_hash(message), 16)
    sign = my_rsa_int_encrypt(hash_message, d, n)
    return sign


# verify signature
def verify_signature(message, signature, e, n):
    # generate hash
    hash_message = int(generate_hash(message), 16) % n
    check = my_rsa_int_decrypt(signature, e, n)
    if check == hash_message:
        print("Signature is valid")
    else:
        print("Signature is not valid")


def int2bytes(number: int, fill_size: int = 0) -> bytes:
    bytes_required = max(1, math.ceil(number.bit_length() / 8))

    if fill_size > 0:
        return number.to_bytes(fill_size, "big")

    return number.to_bytes(bytes_required, "big")


def main():
    n, e, d, p, q = my_rsa()
    wrong = 74378987873429834689326938273489719847692817298646386782738734764891262432983689326824639
    input_number = int.from_bytes(input_string.encode(), byteorder='big', signed=False)
    print("=========================================")
    print("RSA keys generated:")
    print("n =", n)
    print("e =", e)
    print("d =", d)
    print("p =", p)
    print("q =", q)
    print("=========================================")
    my_encrypted = my_rsa_int_encrypt(input_number, e, n)
    my_decrypted = int2bytes(my_rsa_int_decrypt(my_encrypted, d, n)).decode()
    print("My RSA encryption test:")
    print("Input string: ", input_string)
    print("Encrypted string: ", my_encrypted)
    print("Decrypted string: ", my_decrypted)
    print("=========================================")

    encrypted = core.encrypt_int(input_number, e, n)
    decrypted = int2bytes(core.decrypt_int(encrypted, d, n)).decode()
    print("Reference RSA encryption test:")
    print("Input string: ", input_string)
    print("Encrypted string: ", encrypted)
    print("Decrypted string: ", decrypted)
    print("=========================================")

    signature = sign_message(input_string, d, n)
    print("=========================================")
    print("Signature: ", signature)
    verify_signature(input_string, signature, e, n)
    print("Wrong signature: ", wrong)
    verify_signature(input_string, wrong, e, n)
    print("=========================================")

    # file signature test
    big_file = open("test_1Mb.txt", "r")
    file_string = big_file.read()
    file_signature = sign_message(file_string, d, n)
    print("Signature for file: ", file_signature)
    verify_signature(file_string, file_signature, e, n)
    print("Wrong signature for file: ", wrong)
    verify_signature(file_string, wrong, e, n)
    print("=========================================")


if __name__ == "__main__":
    main()
