import string
from collections import Counter
import itertools

# Fréquences des lettres en anglais et en français
FREQ_LANG = {
    "EN": {
        'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228, 'G': 0.02015,
        'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749,
        'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056, 'U': 0.02758,
        'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 'Z': 0.00074
    },
    "FR": {
        'A': 0.07636, 'B': 0.00901, 'C': 0.03260, 'D': 0.03669, 'E': 0.14715, 'F': 0.01066, 'G': 0.00866,
        'H': 0.00737, 'I': 0.07529, 'J': 0.00613, 'K': 0.00074, 'L': 0.05456, 'M': 0.02968, 'N': 0.07114,
        'O': 0.05796, 'P': 0.02521, 'Q': 0.01347, 'R': 0.06693, 'S': 0.07948, 'T': 0.07244, 'U': 0.06311,
        'V': 0.01838, 'W': 0.00049, 'X': 0.00427, 'Y': 0.00308, 'Z': 0.00121
    }
}

def analyze_frequencies(text):
    text = text.upper()
    letter_counts = Counter(filter(str.isalpha, text))
    total_letters = sum(letter_counts.values())
    frequencies = {letter: (letter_counts[letter] / total_letters) for letter in string.ascii_uppercase}
    return frequencies

def detect_language(frequencies):
    scores = {}
    for lang, lang_freq in FREQ_LANG.items():
        score = sum(abs(frequencies.get(letter, 0) - lang_freq.get(letter, 0)) for letter in string.ascii_uppercase)
        scores[lang] = score
    return min(scores, key=scores.get)

def shift_text(text, shift):
    letters = string.ascii_uppercase
    return "".join(
        letters[(letters.index(c) + shift) % 26] if c in letters else c
        for c in text.upper()
    )

def detect_caesar_key(text, lang="EN"):
    lang_freq = FREQ_LANG[lang]
    best_shift, best_score = 0, float("inf")
    for shift in range(26):
        decrypted_text = shift_text(text, -shift)
        frequencies = analyze_frequencies(decrypted_text)
        score = sum(abs(frequencies.get(letter, 0) - lang_freq.get(letter, 0)) for letter in string.ascii_uppercase)
        if score < best_score:
            best_score, best_shift = score, shift
    return best_shift

def decrypt_caesar(text):
    lang = detect_language(analyze_frequencies(text))
    key = detect_caesar_key(text, lang)
    return key, shift_text(text, -key)

def find_vigenere_key_length(text, max_key_length=20):
    text = ''.join(filter(str.isalpha, text.upper()))
    avg_distances = {}
    for key_len in range(1, max_key_length + 1):
        substrings = [''.join(text[i::key_len]) for i in range(key_len)]
        coincidence_indexes = [sum(n * (n - 1) for n in Counter(sub).values()) / (len(sub) * (len(sub) - 1)) for sub in substrings if len(sub) > 1]
        if coincidence_indexes:
            avg_distances[key_len] = sum(coincidence_indexes) / len(coincidence_indexes)
        else:
            avg_distances[key_len] = 0  # Valeur neutre pour éviter l'erreur

    return max(avg_distances, key=avg_distances.get)

def detect_vigenere_key(text, key_length, lang="EN"):
    text = ''.join(filter(str.isalpha, text.upper()))
    key = ""
    for i in range(key_length):
        substring = ''.join(text[j] for j in range(i, len(text), key_length))
        best_shift = detect_caesar_key(substring, lang)
        key += string.ascii_uppercase[best_shift]
    return key

def decrypt_vigenere(text, key):
    key_shifts = [string.ascii_uppercase.index(k) for k in key]
    decrypted_text = "".join(
        shift_text(c, -key_shifts[i % len(key)]) if c.isalpha() else c
        for i, c in enumerate(text.upper())
    )
    return decrypted_text

def detect_substitution_key(text, lang="EN"):
    text_freq = analyze_frequencies(text)
    sorted_text_letters = sorted(text_freq, key=text_freq.get, reverse=True)
    sorted_lang_letters = sorted(FREQ_LANG[lang], key=FREQ_LANG[lang].get, reverse=True)
    return dict(zip(sorted_text_letters, sorted_lang_letters))

def decrypt_substitution(text):
    lang = detect_language(analyze_frequencies(text))
    mapping = detect_substitution_key(text, lang)
    return "".join(mapping.get(c, c) for c in text.upper())

# Exemple d'utilisation
encrypted_text = "Wklv lv d whvw phvvdjh hqfubswh'"
key_caesar, decrypted_caesar = decrypt_caesar(encrypted_text)
print("Clé César trouvée:", key_caesar)
print("Texte déchiffré César:", decrypted_caesar)

encrypted_vigenere = "twdpwy hm ohjdl zmuam ll evmth"
key_length = find_vigenere_key_length(encrypted_vigenere)
key_vigenere = detect_vigenere_key(encrypted_vigenere, key_length)
decrypted_vigenere = decrypt_vigenere(encrypted_vigenere, key_vigenere)
print("Longueur clé Vigenère:", key_length)
print("Clé Vigenère trouvée:", key_vigenere)
print("Texte déchiffré Vigenère:", decrypted_vigenere)

encrypted_substitution = "QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD"
decrypted_substitution = decrypt_substitution(encrypted_substitution)
print("Texte déchiffré Substitution:", decrypted_substitution)
