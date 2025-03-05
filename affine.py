from math import gcd
from collections import Counter

ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
FRENCH_FREQ_ORDER = "ESARTINULOMDPCVGBFHQYXJZK"
# function to calculate the modular inverse
def mod_inverse(a, m=26):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None  # modular inverse does not exist

# function to encrypt a text using affine cipher
def affine_encrypt(text, A, B):
    if gcd(A, 26) != 1:  # check if A is prime with 26
        raise ValueError("A doit être premier avec 26")
    
    encrypted_text = ""
    for char in text.upper():
        if char.isalpha():  # check if character is a letter
            P = ord(char) - ord('A')  # turns letter into number
            C = (A * P + B) % 26  # encryption formula
            encrypted_text += chr(C + ord('A'))  # turns number back to letter
        else:
            encrypted_text += char  # if not letter keeps the character as it is
    return encrypted_text

# function to decrypt a text using affine cipher
def affine_decrypt(cipher, A, B):
    A_inv = mod_inverse(A, 26)
    if A_inv is None:
        raise ValueError("A n'a pas d'inverse modulaire, choisissez un autre A.")
    
    decrypted_text = ""
    for char in cipher.upper():
        if char.isalpha(): # check if character is a letter
            C = ord(char) - ord('A') # turns letter into number
            P = (A_inv * (C - B)) % 26  # decryption formula
            decrypted_text += chr(P + ord('A')) # turns number back to letter
        else:
            decrypted_text += char  # if not letter keeps the character as it is
    return decrypted_text

# function to brute-force crack Affine Cipher
def affine_brute_force(cipher):
    possible_A_values = [a for a in range(1, 26) if gcd(a, 26) == 1]  # values coprime with 26
    # try all possible A values that are prime with 26 and all B values from 0 to 25
    for A in possible_A_values:
        for B in range(26):
            decrypted = affine_decrypt(cipher, A, B)
            if decrypted:
                print(f"trying A={A}, B={B} -> {decrypted}")

# frequency analysis attack on affine cipher
def affine_frequency_analysis(cipher,language="english"):
    letter_counts = Counter([char.upper() for char in cipher if char.isalpha()])
    if not letter_counts:
        return None  # no letters found

    # sort by frequency
    sorted_cipher_letters = [pair[0] for pair in letter_counts.most_common()]
    frequency_order = ENGLISH_FREQ_ORDER if language.lower() == "english" else FRENCH_FREQ_ORDER

    possible_A_values = [a for a in range(1, 26) if gcd(a, 26) == 1]

    for cipher_letter in sorted_cipher_letters[:3]:  # try the 3 most common cipher letters
        for expected_letter in frequency_order[:5]:  # try the 5 most common plaintext letters
            C = ord(cipher_letter) - ord('A')
            P = ord(expected_letter) - ord('A')

            for A in possible_A_values:
                B = ((C - A * P) % 26 + 26) % 26  # fix negative values
                decrypted_text = affine_decrypt(cipher, A, B)
                if decrypted_text:
                    print(f"Possible decryption (A={A}, B={B}): {decrypted_text}")


A = 5  # coeff 1
B = 8  # coeff 2

text = "BONJOUR LE MONDE"
cipher_text="DMVQR ADPHV PNLAA RTFHK ARMDX AKVUP ZMDUR INKSV KFSZP VERAR ENDSR ODKFM MIZIR DSXFH KNYDO DODVK "
encrypted = affine_encrypt(text, A, B)
print(f"Texte chiffré : {encrypted}")

decrypted = affine_decrypt(encrypted, A, B)
print(f"Texte déchiffré : {decrypted}")

print("Brute-force cracking Affine Cipher:")
affine_brute_force(cipher_text)

print("Frequency Analysis Attack on Affine Cipher:")
affine_frequency_analysis(cipher_text)