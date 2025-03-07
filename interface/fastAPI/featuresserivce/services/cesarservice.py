from collections import Counter

# English and French alphabet frequency order
ENGLISH_FREQUENCY_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
FRENCH_FREQUENCY_ORDER = "ESARTINULOMDPCVGBFHQYXJZK"

def caesar_encryption(text, shift):
    """
    Encrypt text using Caesar cipher with specified shift
    """
    result = ""
    shift = shift % 26  # To make sure the shift is between 0-25 for handling negative or big shifts
    
    for char in text:
        if char.isalpha():  # Check if character is a letter
            ascii_offset = 65 if char.isupper() else 97  # 65 for uppercase A and 97 for lowercase a
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    
    return result

def caesar_decryption(text, shift):
    """
    Decrypt text using Caesar cipher with specified shift
    """
    result = ""
    shift = shift % 26  # To make sure the shift is between 0-25 for handling negative or big shifts
    
    for char in text:
        if char.isalpha():  # Check if character is a letter
            ascii_offset = 65 if char.isupper() else 97  # 65 for uppercase A and 97 for lowercase a
            result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
        else:
            result += char
    
    return result

def get_brute_force_results(cipher):
    """
    Generate all possible Caesar decryptions by trying shifts from 1 to 25
    """
    results = []
    for shift in range(1, 26):
        results.append({"shift": shift, "text": caesar_decryption(cipher, shift)})
    return results

def frequency_analysis(cipher, language="english"):
    """
    Use frequency analysis to determine possible shifts for a Caesar cipher
    """
    letter_counts = Counter([char.upper() for char in cipher if char.isalpha()])
    if not letter_counts:
        return []  # If no letters exist, return empty list
    
    most_common_cipher_letter = letter_counts.most_common(1)[0][0]
    # Use english or french frequency order
    frequency_order = ENGLISH_FREQUENCY_ORDER if language.lower() == "english" else FRENCH_FREQUENCY_ORDER
    
    possible_shifts = set()  # Use a set to remove duplicates if right and left shifts give the same number
    for expected_letter in frequency_order[:5]:  # Check E, T, A, O, I or E, S, A, R, T
        shift_guess = (ord(most_common_cipher_letter) - ord(expected_letter)) % 26
        possible_shifts.add(shift_guess)  # Right shift
        possible_shifts.add((-shift_guess) % 26)  # Left shift (handling negatives)

    return sorted(possible_shifts)  # Return sorted list

def get_frequency_analysis_results(cipher, language="english"):
    """
    Generate decryptions based on frequency analysis results
    """
    guessed_shifts = frequency_analysis(cipher, language)
    results = []
    
    for shift in guessed_shifts:
        results.append({
            "shift": shift,
            "text": caesar_decryption(cipher, shift)
        })
    
    return {"possible_shifts": guessed_shifts, "decryptions": results}