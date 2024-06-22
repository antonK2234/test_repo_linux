import json
import csv
import psutil
import os
import sys
from sage.all_cmdline import *

# Задаем константу N
N = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141"

# Функция для конвертации числа в 64-значную строку hex
def rrr(i):
    tmpstr = hex(i)
    hexstr = tmpstr.replace('0x','').replace('L','').replace(' ','').zfill(64)
    return hexstr

# Функция для расширенного алгоритма Евклида
def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

# Функция для нахождения обратного элемента по модулю m
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    return x % m

def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def perform_algorithm(signatures, bit_length, limit):
    order = int(N, 16)
    keys = []

    for signature in signatures:
        msgn = int(signature['Z'], 16)
        rn = int(signature['R'], 16)
        sn = int(signature['S'], 16)

        rnsn_inv = rn * modinv(sn, order)
        mnsn_inv = msgn * modinv(sn, order)

        def make_matrix(msgs, sigs):
            m = len(msgs)
            matrix = Matrix(QQ, m + 2, m + 2)

            for i in range(m):
                matrix[i, i] = order

            for i in range(m):
                x0 = (int(sigs['R'], 16) * modinv(int(sigs['S'], 16), order)) - rnsn_inv
                x1 = (int(msgs[i], 16) * modinv(int(sigs['S'], 16), order)) - mnsn_inv
                matrix[m, i] = x0
                matrix[m + 1, i] = x1

            matrix[m, i + 1] = (2 ** int(bit_length)) // order
            matrix[m, i + 2] = 0
            matrix[m + 1, i + 1] = 0
            matrix[m + 1, i + 2] = 2 ** int(bit_length)

            return matrix

        def try_reduce_matrix(m):
            keys = []
            for row in m:
                try:
                    potential_nonce_diff = row[0]
                    potential_priv_key = (sn * msgn) - (int(signature['S'], 16) * msgn) - (int(signature['S'], 16) * sn * potential_nonce_diff)
                    potential_priv_key *= modinv((rn * int(signature['S'], 16)) - (int(signature['R'], 16) * sn), order)
                    key = potential_priv_key % order
                    if key not in keys:
                        keys.append(key)
                except Exception as e:
                    pass
            return keys

        matrix = make_matrix([signature['Z']], signature)
        new_matrix = matrix.LLL(early_red=True, use_siegel=True)
        keys.extend(try_reduce_matrix(new_matrix))

    return keys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python LLL.py <bit_value>")
        sys.exit(1)

    bit_value = sys.argv[1]

    transaction_data = {}
    signatures = load_json("output_data.json")

    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage before processing bit_value {bit_value}: {mem_before:.2f} MB")

    keys = perform_algorithm(signatures, bit_value, 1)

    with open("RESULTS.csv", 'a', newline='') as result_file:
        csv_writer = csv.writer(result_file)
        for key in keys:
            csv_writer.writerow([bit_value, key])

    mem_after = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage after processing bit_value {bit_value}: {mem_after:.2f} MB")

    # Промежуточное сохранение после каждого значения bit_value
    with open(f"INTERMEDIATE_RESULTS_{bit_value}.csv", 'w', newline='') as intermediate_file:
        csv_writer = csv.writer(intermediate_file)
        for key in keys:
            csv_writer.writerow([bit_value, key])

    print(f"Запись результатов для {bit_value} завершена.")
