from collections import Counter
# english alphabet frequency order
ENGLISH_FREQUENCY_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

# function to encrypt a text
def ceasar_encryption(text,shift):
    result=""
    shift=shift%26 # to make sure the shift is between 0-25 for handling negative or big shifts
    for char in text:
        if char.isalpha(): # check if character is a letter
            ascii_offset = 65 if char.isupper() else 97 #65 for uppercase A and 97 for lowercase a
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result
# function to decrypt a text
def ceasar_decryption(text,shift):
    result=""
    shift=shift%26 # to make sure the shift is between 0-25 for handling negative or big shifts
    for char in text:
        if char.isalpha(): # check if character is a letter
            ascii_offset = 65 if char.isupper() else 97 #65 for uppercase A and 97 for lowercase a
            result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
        else:
            result += char
    return result

# function to crack caesar cipher using brute force by testing shifts from 1 to 25
def brute_force_ceasar(cipher):
    print("brute force attack on ceasar cipher:")
    for shift in range(1,26):
        print(f"Shift: {shift} -> {ceasar_decryption(cipher,shift)}")

# function to crack caesar cipher using frequency analysis by 
def frequency_analysis(cipher):
    letter_counts = Counter([char.upper() for char in cipher if char.isalpha()])
    if not letter_counts:
        return 0  # If no letters exist, return 0
    
    most_common_cipher_letter = letter_counts.most_common(1)[0][0]
    
    # Test multiple common letters in English
    possible_shifts = []
    for expected_letter in ENGLISH_FREQUENCY_ORDER[:5]:  # Check E, T, A, O, I
        shift_guess = (ord(most_common_cipher_letter) - ord(expected_letter)) % 26
        possible_shifts.append(shift_guess)

    return possible_shifts


if __name__ == "__main__":
    text="lorem ipsum dolores sit amet"
    shift=3
    enc=ceasar_encryption(text,shift)
    print(f"encrypted text:{enc}")

    dec=ceasar_decryption(enc,shift)
    print(f"decrypted text:{dec}")

    brute_force_ceasar(enc)
    guessed_shifts = frequency_analysis(enc)
    print(f"Possible shifts: {guessed_shifts}")

    # Try each guessed shift
    for shift in guessed_shifts:
        print(f"Decryption with shift {shift}: {ceasar_decryption(enc, shift)}")