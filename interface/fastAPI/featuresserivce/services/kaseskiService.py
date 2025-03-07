import re
from collections import Counter
from math import gcd
from functools import reduce

def find_repeated_sequences(text, min_length=3):
    sequences = {}
    for i in range(len(text) - min_length + 1):
        for j in range(min_length, len(text) - i + 1):
            seq = text[i:i + j]
            if seq in sequences:
                sequences[seq].append(i)
            else:
                sequences[seq] = [i]
    return {seq: pos for seq, pos in sequences.items() if len(pos) > 1}

def remove_duplicates(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

def find_distances(repeated_sequences):
    distances = []
    for positions in repeated_sequences.values():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                distances.append(positions[j] - positions[i])
    return remove_duplicates(distances)

def find_common_divisors(numbers):
    def get_divisors(n):
        return {i for i in range(2, n + 1) if n % i == 0}

    if len(numbers) == 1:
        return sorted(get_divisors(numbers[0]))

    all_divisors = []
    for num in numbers:
        all_divisors.extend(get_divisors(num))

    divisor_counts = Counter(all_divisors)
    sorted_divisors = sorted(divisor_counts.items(), key=lambda x: x[1], reverse=True)

    common_divisors = [div for div, count in sorted_divisors if count > 1]

    # Vérifier si les nombres sont premiers entre eux
    if not common_divisors and reduce(gcd, numbers) == 1:
        return {num: sorted(get_divisors(num)) for num in numbers}

    return common_divisors

def kasiski_test(ciphertext):
    ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())
    repeated_sequences = find_repeated_sequences(ciphertext)
    distances = find_distances(repeated_sequences)
    factors = find_common_divisors(distances)

    return {
        "repeated_sequences": repeated_sequences,
        "distances": distances,
        "common_factors": factors
    }
