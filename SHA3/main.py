# Keccak algorythm
import hashlib
import bitarray

input_str = "hello world"
sha = 512
logarithm = 6
w = 2 ** logarithm
b = 25 * w
cap = sha * 2
rate = b - cap


# 1. Pad the input string
def pad_string(x, m):
    j = (-m - 2) % x
    return "1" + "0" * j + "1"


def rnd(arr_3d, ir):
    # 1. Theta
    def theta(input_arr_3d):
        # 1.1. C
        c = [[0 for _ in range(w)] for _ in range(5)]
        for x in range(5):
            for z in range(w):
                for y in range(5):
                    c[x][z] = c[x][z] ^ input_arr_3d[x][y][z]
        # print(c)

        # 1.2. D
        d = [[0 for _ in range(w)] for _ in range(5)]
        for x in range(5):
            for z in range(w):
                d[x][z] = c[(x - 1) % 5][z] ^ c[(x + 1) % 5][(z - 1) % w]
        # print(d)

        output_arr_3d = [[[0 for _ in range(w)] for _ in range(5)] for _ in range(5)]
        for y in range(5):
            for x in range(5):
                for z in range(w):
                    output_arr_3d[x][y][z] = input_arr_3d[x][y][z] ^ d[x][z]
        # print("theta ", array_to_string(output_arr_3d))
        return output_arr_3d

    # 2. Rho and Pi
    # 2.1. Rho
    def rho(input_arr_3d):
        output_arr_3d = [[[0 for _ in range(w)] for _ in range(5)] for _ in range(5)]
        for z in range(w):
            output_arr_3d[0][0][z] = input_arr_3d[0][0][z]
        x = 1
        y = 0
        for t in range(24):
            for z in range(w):
                output_arr_3d[x][y][z] = input_arr_3d[x][y][(z - (t + 1) * (t + 2) // 2) % w]
            # temp_x = x
            # temp_y = y
            # x = y
            # y = (2 * temp_x + 3 * temp_y) % 5
            x, y = y, (2 * x + 3 * y) % 5
        # print("rho ", array_to_string(output_arr_3d))
        return output_arr_3d

    # 2.2. Pi
    def pi(input_arr_3d):
        output_arr_3d = [[[0 for _ in range(w)] for _ in range(5)] for _ in range(5)]
        for y in range(5):
            for x in range(5):
                for z in range(w):
                    output_arr_3d[x][y][z] = input_arr_3d[(x + 3 * y) % 5][x][z]
        # print("pi ", array_to_string(output_arr_3d))
        return output_arr_3d

    # 3. Chi
    def chi(input_arr_3d):
        output_arr_3d = [[[0 for _ in range(w)] for _ in range(5)] for _ in range(5)]
        for y in range(5):
            for x in range(5):
                for z in range(w):
                    output_arr_3d[x][y][z] = input_arr_3d[x][y][z] ^ (
                            (input_arr_3d[(x + 1) % 5][y][z] ^ 1) & input_arr_3d[(x + 2) % 5][y][z])
        # print("chi ", array_to_string(output_arr_3d))
        return output_arr_3d

    # 4. Iota
    def iota(input_arr_3d, i_rnd):
        def rc(t):
            if t % 255 == 0:
                return 1
            else:
                r = [1, 0, 0, 0, 0, 0, 0, 0]
                for i in range(1, t % 255 + 1):
                    r.insert(0, 0)
                    r[0] = r[0] ^ r[8]
                    r[4] = r[4] ^ r[8]
                    r[5] = r[5] ^ r[8]
                    r[6] = r[6] ^ r[8]
                    r = r[:8]
                return r[0]

        output_arr_3d = [[[0 for _ in range(w)] for _ in range(5)] for _ in range(5)]
        for y in range(5):
            for x in range(5):
                for z in range(w):
                    output_arr_3d[x][y][z] = input_arr_3d[x][y][z]
        rc_arr = [0 for _ in range(w)]
        for j in range(logarithm + 1):
            rc_arr[2 ** j - 1] = rc(j + 7 * i_rnd)
        for z in range(w):
            output_arr_3d[0][0][z] = output_arr_3d[0][0][z] ^ rc_arr[z]
        # print("iota ", array_to_string(output_arr_3d))
        return output_arr_3d

    return iota(chi(pi(rho(theta(arr_3d)))), ir)


def string_to_array(string):
    # creating 3d array, filling it
    arr_3d = [[[0 for _ in range(w)] for _ in range(5)] for _ in range(5)]
    for y in range(5):
        for x in range(5):
            for z in range(w):
                arr_3d[x][y][z] = int(string[(y * 5 + x) * w + z])
    return arr_3d


def array_to_string(arr_3d):
    string = ""
    for y in range(5):
        for x in range(5):
            for z in range(w):
                string += str(arr_3d[x][y][z])
    return string


def keccak_p(string):
    arr_3d = string_to_array(string)
    for i in range(12 + 2 * logarithm):
        arr_3d = rnd(arr_3d, i)
        # print(array_to_string(arr_3d))
    string = array_to_string(arr_3d)
    return string


def sponge(r, string):
    p = string + pad_string(r, len(string))
    # print(hex(int(p, 2)))
    n = len(p) // r
    c = b - r
    blocks = [p[i:i + r] for i in range(0, len(p), r)]
    s = "0" * b
    for i in range(0, n):
        # print(p, 2)
        s = keccak_p(format(int(s, 2) ^ int(blocks[i] + "0" * c, 2), '0' + str(b) + 'b'))
    z = s[:r]
    while len(z) < sha:
        s = keccak_p(s)
        z = z + s[:r]
    return z[:sha]


# i hate endianness
def binary_string_to_hex(string):
    reverse = string[::-1]
    # hex keep loosing leading zeros, so I used this one
    hex_string = '%.*x' % (sha // 4, int('0b' + reverse, 0))
    hex_list = list(hex_string)
    n = len(hex_string) - 1
    for i in range(0, n // 2, 2):
        hex_list[i], hex_list[n - i - 1] = hex_list[n - i - 1], hex_list[i]
        hex_list[i + 1], hex_list[n - i] = hex_list[n - i], hex_list[i + 1]
    return "".join(hex_list)


def keccak(string):
    # convert string to binary
    array = bitarray.bitarray(endian='little')
    array.frombytes(string.encode('utf-8'))
    binary_str = array.to01()

    # need to add 01 to the end of the string...
    binary_str += "01"
    output_str = sponge(rate, binary_str)
    # print(output_str)
    return binary_string_to_hex(output_str)


def read_file(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')
    return data


print("My SHA-3:  ", keccak(input_str))
print("Ref SHA-3: ", hashlib.sha3_512(input_str.encode()).hexdigest())
# print("My SHA-3 with file:  ", keccak(read_file("test_1Mb.txt")))
# print("Ref SHA-3 with file: ", hashlib.sha3_512(read_file("test_1Mb.txt").encode()).hexdigest())
