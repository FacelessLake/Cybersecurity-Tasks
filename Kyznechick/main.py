# Кузнечик (GOST R 34.12-2015)
from pygost import gost3412 as gost

# 4.1 Значения параметров
# 4.1.1 Нелинейное биективное преобразование

test_string = bytearray("sdndsa,dsa,dsamcnnaskjhckjahdiuhawiushwiuhdyjasbdaksguyjsdsdfhs", 'utf-8')
key = bytearray.fromhex('8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef')

block_size = 16
pi = bytearray((252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77, 233,
                119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 249, 24, 101,
                90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79, 5, 132, 2, 174, 227, 106, 143,
                160, 6, 11, 237, 152, 127, 212, 211, 31, 235, 52, 44, 81, 234, 200, 72, 171, 242, 42,
                104, 162, 253, 58, 206, 204, 181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156,
                183, 93, 135, 21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178,
                177, 50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87, 223,
                245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3, 224, 15, 236,
                222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74, 167, 151, 96, 115, 30, 0,
                98, 68, 26, 184, 56, 130, 100, 159, 38, 65, 173, 69, 70, 146, 39, 94, 85, 47, 140, 163,
                165, 125, 105, 213, 149, 59, 7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136,
                217, 231, 137, 225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133,
                97, 32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82, 89, 166,
                116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182,))

pi_reverse = bytearray((165, 45, 50, 143, 14, 48, 56, 192, 84, 230, 158,
                        57, 85, 126, 82, 145, 100, 3, 87, 90, 28, 96,
                        7, 24, 33, 114, 168, 209, 41, 198, 164, 63, 224,
                        39, 141, 12, 130, 234, 174, 180, 154, 99, 73, 229,
                        66, 228, 21, 183, 200, 6, 112, 157, 65, 117, 25,
                        201, 170, 252, 77, 191, 42, 115, 132, 213, 195, 175,
                        43, 134, 167, 177, 178, 91, 70, 211, 159, 253, 212,
                        15, 156, 47, 155, 67, 239, 217, 121, 182, 83, 127,
                        193, 240, 35, 231, 37, 94, 181, 30, 162, 223, 166,
                        254, 172, 34, 249, 226, 74, 188, 53, 202, 238, 120,
                        5, 107, 81, 225, 89, 163, 242, 113, 86, 17, 106,
                        137, 148, 101, 140, 187, 119, 60, 123, 40, 171, 210,
                        49, 222, 196, 95, 204, 207, 118, 44, 184, 216, 46,
                        54, 219, 105, 179, 20, 149, 190, 98, 161, 59, 22,
                        102, 233, 92, 108, 109, 173, 55, 97, 75, 185, 227,
                        186, 241, 160, 133, 131, 218, 71, 197, 176, 51, 250,
                        150, 111, 110, 194, 246, 80, 255, 93, 169, 142, 23,
                        27, 151, 125, 236, 88, 247, 31, 251, 124, 9, 13,
                        122, 103, 69, 135, 220, 232, 79, 29, 78, 4, 235,
                        248, 243, 62, 61, 189, 138, 136, 221, 205, 11, 19,
                        152, 2, 147, 128, 144, 208, 36, 52, 203, 237, 244,
                        206, 153, 16, 68, 64, 146, 58, 1, 38, 18, 26,
                        72, 104, 245, 129, 139, 199, 214, 32, 10, 8, 0,
                        76, 215, 116,))

c_arr = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]

galua_field = [bytearray(256) for _ in range(256)]
keys = []


def bytearray_xor(a, b):
    return bytearray(x ^ y for x, y in zip(a, b))


# 4.1.2 Линейное преобразование
# ℓ: (16x V8) → V8
# def linear_transformation(a):
#     # Работа с полиномами
#     def multiply_polynomials(x, y):
#         if x == 0 or y == 0:
#             return 0
#         z = 0
#         while x != 0:
#             if x & 1 == 1:
#                 z ^= y
#             y <<= 1
#             x >>= 1
#         return z
#
#     def mod_polynomial(x, m):
#         nbm = number_bits(m)
#         while True:
#             nbx = number_bits(x)
#             if nbx < nbm:
#                 return x
#             mshift = m << (nbx - nbm)
#             x ^= mshift
#
#     # Returns the number of bits that are used to store the positive integer x.
#     def number_bits(x):
#         nb = 0
#         while x != 0:
#             nb += 1
#             x >>= 1
#         return nb
#
#     c = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]  # значения взяты из ГОСТа
#     result = 0
#
#     while a != 0:
#         # 0b111000011, тк x8 + x7 + x6 + x + 1
#         result ^= mod_polynomial(multiply_polynomials(a & 0xff, c.pop()), 0b111000011)
#         a >>= 8
#     return result


def init_galua_field():
    def gf(a, b):
        c = 0
        while b:
            if b & 1:
                c ^= a
            if a & 0x80:
                a = (a << 1) ^ 0x1C3
            else:
                a <<= 1
            b >>= 1
        return c

    for x in range(256):
        for y in range(256):
            galua_field[x][y] = gf(x, y)


# 4.2 Преобразования

# подставляет значения из таблицы пи, используя биты из x
# V128 → V128
def s_permutation(a):
    return bytearray(pi[i] for i in a)


# V128 → V128
def s_reverse_permutation(a):
    return bytearray(pi_reverse[i] for i in a)


# V128 → V128
def r_permutation(x):
    temp = x[15]
    for i in range(14, -1, -1):
        x[i + 1] = x[i]
        temp ^= galua_field[x[i]][c_arr[i]]
    x[0] = temp
    return x


# V128 → V128
def r_reverse_permutation(x):
    temp = x[0]
    for i in range(15):
        x[i] = x[i + 1]
        temp ^= galua_field[x[i]][c_arr[i]]
    x[15] = temp
    return x


# V128 → V128
def l_permutation(x):
    for _ in range(16):
        x = r_permutation(x)
    return x


# V128 → V128
def l_reverse_permutation(x):
    for _ in range(16):
        x = r_reverse_permutation(x)
    return x


# 4.3 Алгоритм развертывания ключа
def key_deployment():
    a = bytearray(key[:16])
    b = bytearray(key[16:])
    keys.append(a)
    keys.append(b)
    for i in range(4):
        for j in range(8):
            y = bytearray(16)
            y[15] = 8 * i + j + 1
            c = l_permutation(y)
            k = l_permutation(s_permutation(bytearray_xor(a, c)))
            a, b = [bytearray_xor(k, b), a]
        keys.append(a)
        keys.append(b)


# 4.4 Базовый алгоритм шифрования
# 4.4.1 Алгоритм зашифрования
def encryption(x):
    for i in range(9):
        x = l_permutation(s_permutation(bytearray_xor(x, keys[i])))
    return bytearray_xor(x, keys[-1])


# 4.4.2 Алгоритм расшифрования
def decryption(x):
    for i in range(9):
        x = s_reverse_permutation(l_reverse_permutation(bytearray_xor(x, reversed_keys[i])))
    return bytearray_xor(x, reversed_keys[-1])


def pad_string(string, x, m):
    j = (-m - 1) % x
    string += b'\x80'
    for _ in range(j):
        string += b'\x00'
    return string


def block_encryption(array):
    byte_array = bytearray(array)
    n = len(byte_array)
    pad_string(byte_array, 16, n)
    block = []
    encrypted = []
    n = len(byte_array)
    for i in range(0, n, 16):
        block.append(byte_array[i:i + 16])
    for i in range(len(block)):
        encrypted.append(encryption(block[i]))
    return encrypted


def block_decryption(encrypted):
    decrypted = []
    for i in range(len(encrypted)):
        decrypted.append(decryption(encrypted[i]))
    while decrypted[-1][-1] == 0:
        decrypted[-1].pop()
    decrypted[-1].pop()
    return bytes(b''.join(decrypted))


def lib_block_encryption(array):
    byte_array = bytearray(array)
    n = len(byte_array)
    pad_string(byte_array, 16, n)
    block = []
    encrypted = []
    n = len(byte_array)
    for i in range(0, n, 16):
        block.append(byte_array[i:i + 16])
    for i in range(len(block)):
        encrypted.append(gost.GOST3412Kuznechik(key).encrypt(block[i]))
    return encrypted


def lib_block_decryption(encrypted):
    decrypted = []
    for i in range(len(encrypted)):
        decrypted.append(gost.GOST3412Kuznechik(key).decrypt(encrypted[i]))
    return bytes(b''.join(decrypted))


test = bytearray.fromhex('1122334455667700ffeeddccbbaa9988')
init_galua_field()
key_deployment()
reversed_keys = keys.copy()
reversed_keys.reverse()

# print('ref: ', hexdec("d456584dd0e3e84cc3166e4b7fa2890d"))
# print(keys)
enc = encryption(test)

print("=========================================")
print("Start string: ", test.hex())
print("My Test     : ", enc.hex())
print("Library     : ", gost.GOST3412Kuznechik(key).encrypt(test).hex())
print("Decrypt     : ", decryption(enc).hex())
print("=========================================")

enc = block_encryption(test_string)
enc_lib = lib_block_encryption(test_string)

print("Starting text:          ", test_string)
print("My encrypted text:      ", (b''.join(enc)))
print("Library encrypted text: ", (b''.join(enc_lib)))
print("My decrypted text:      ", block_decryption(enc))
print("Library decrypted text: ", lib_block_decryption(enc_lib))
print("=========================================")


def read_file(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    return data


def write_file(filename, data):
    with open(filename, 'wb') as file:
        file.write(data)


encrypted_file = block_encryption(read_file("test_1Mb.txt"))
encrypted_file_lib = block_encryption(read_file("test_1Mb.txt"))
write_file("my_encrypt.txt", bytes(b''.join(encrypted_file)))
write_file("my_decrypt.txt", block_decryption(encrypted_file))
write_file("lib_encrypt.txt", bytes(b''.join(encrypted_file_lib)))
write_file("lib_decrypt.txt", lib_block_decryption(encrypted_file_lib))
print("File encrypted and decrypted")
print("=========================================")
