
IP = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]

IP_inverse = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

expand = [32, 1, 2, 3, 4, 5, 4, 5,
          6, 7, 8, 9, 8, 9, 10, 11,
          12, 13, 12, 13, 14, 15, 16, 17,
          16, 17, 18, 19, 20, 21, 20, 21,
          22, 23, 24, 25, 24, 25, 26, 27,
          28, 29, 28, 29, 30, 31, 32, 1,
          15, 11, 19, 4, 3, 16, 23, 18,
          27, 32, 7, 5, 12, 30, 20, 1]

sbox = [[4, 1, 2, 3, 6, 5, 0, 7],
        [2, 4, 1, 7, 5, 3, 0, 6]]

per = [16,  7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2,  8, 24, 14,
       32, 27,  3,  9,
       19, 13, 30,  6,
       22, 11,  4, 25]


def permute(k, arr, n):
    permutation = ""
    for i in range(0, n):
        permutation = permutation + k[arr[i] - 1]
    return permutation

def round_key(key, round):
    new_key = ""
    for i in range(0,len(key)):
        if (i+1) % 8 != round % 8:
            new_key += key[i]

    return new_key

def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans


def bin2dec(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal

key = "0110001001100101011010000110010101110011011010000111010001101001"
plaintext = "0100110101001111010101000100010101010010010000010101001101000101"

# Initial Permutation
plaintext = permute(plaintext, IP, 64)
print("After initial permutation:", plaintext)

l = plaintext[0:32]
r = plaintext[32:64]

for i in range(0, 8):
    # Expanding the 32 bits data into 56 bits
    right_expanded = permute(r, expand, 56)

    Kr = round_key(key, i+1)

    xor_k_r = xor(right_expanded, Kr)

    xor1 = xor_k_r[0:28]
    xor2 = xor_k_r[28:56]

    new_xor = xor(xor2, xor1)
    sbox_str = new_xor
    for j in range(0, 4):
        index = (j+1) * 6 + j
        row = int(new_xor[index])
        col = bin2dec(int(new_xor[index - 3] + new_xor[index - 2] + new_xor[index - 1]))
        val = sbox[row][col]
        new_index = index - (7 - val)
        sbox_str = sbox_str[:new_index] + new_xor[index] + sbox_str[new_index:]

    sbox_str = permute(sbox_str, per, 32)

    # XOR left and sbox_str
    result = xor(l, sbox_str)
    l = result

    if (i != 8):
        l, r = r, l
    print("Round", i + 1, " ", l,
          " ", r)


combine = l + r

# Final permutation
cipher_text = permute(combine, IP_inverse, 64)

print("cipher text:", cipher_text)