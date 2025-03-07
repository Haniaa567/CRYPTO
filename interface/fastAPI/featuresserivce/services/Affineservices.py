from math import gcd
from collections import Counter

ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
FRENCH_FREQ_ORDER = "ESARTINULOMDPCVGBFHQYXJZK"

def mod_inverse(a, m=26):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt(text, A, B):
    if gcd(A, 26) != 1:
        raise ValueError("A doit être premier avec 26")

    encrypted_text = ""
    for char in text.upper():
        if char.isalpha():
            P = ord(char) - ord('A')
            C = (A * P + B) % 26
            encrypted_text += chr(C + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text

def affine_decrypt(cipher, A, B):
    A_inv = mod_inverse(A, 26)
    if A_inv is None:
        raise ValueError("A n'a pas d'inverse modulaire")

    decrypted_text = ""
    for char in cipher.upper():
        if char.isalpha():
            C = ord(char) - ord('A')
            P = (A_inv * (C - B)) % 26
            decrypted_text += chr(P + ord('A'))
        else:
            decrypted_text += char
    return decrypted_text

def affine_brute_force(cipher):
    possible_A_values = [a for a in range(1, 26) if gcd(a, 26) == 1]
    results = []
    for A in possible_A_values:
        for B in range(26):
            decrypted = affine_decrypt(cipher, A, B)
            results.append((A, B, decrypted))
    return results

def affine_frequency_analysis(cipher, language="english"):
    letter_counts = Counter([char.upper() for char in cipher if char.isalpha()])
    if not letter_counts:
        return None

    sorted_cipher_letters = [pair[0] for pair in letter_counts.most_common()]
    frequency_order = ENGLISH_FREQ_ORDER if language.lower() == "english" else FRENCH_FREQ_ORDER

    possible_A_values = [a for a in range(1, 26) if gcd(a, 26) == 1]

    results = []
    for cipher_letter in sorted_cipher_letters[:3]:
        for expected_letter in frequency_order[:5]:
            C = ord(cipher_letter) - ord('A')
            P = ord(expected_letter) - ord('A')

            for A in possible_A_values:
                B = ((C - A * P) % 26 + 26) % 26
                decrypted_text = affine_decrypt(cipher, A, B)
                results.append((A, B, decrypted_text))
    return results