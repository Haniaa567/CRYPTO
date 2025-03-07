# services.py
import string
from collections import Counter
from itertools import product
from typing import List, Tuple, Optional


class VigenereService:
    def __init__(self):
        self.alphabet = string.ascii_lowercase
        # Frequency distributions for analysis
        self.english_frequencies = [
            0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228,
            0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025,
            0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987,
            0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
            0.01974, 0.00074
        ]
        self.french_frequencies = [
            0.0764, 0.0090, 0.0326, 0.0367, 0.1472, 0.0106, 0.0110, 0.0074, 0.0759,
            0.0061, 0.0005, 0.0546, 0.0297, 0.0712, 0.0576, 0.0252, 0.0136, 0.0669,
            0.0795, 0.0724, 0.0631, 0.0183, 0.0004, 0.0042, 0.0028, 0.0012
        ]

    def preprocess(self, text: str) -> str:
        """Converts text to lowercase and removes non-alphabetic characters"""
        return ''.join(ch.lower() for ch in text if ch.isalpha())

    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypts plaintext using Vigenere cipher with the given key"""
        plaintext = self.preprocess(plaintext)
        key = self.preprocess(key)
        
        if not key:
            return plaintext
            
        cipher = []
        key_len = len(key)
        
        for i, p in enumerate(plaintext):
            shift = ord(key[i % key_len]) - ord('a')
            c = (ord(p) - ord('a') + shift) % 26
            cipher.append(chr(c + ord('a')))
            
        return ''.join(cipher)

    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypts ciphertext using Vigenere cipher with the given key"""
        ciphertext = self.preprocess(ciphertext)
        key = self.preprocess(key)
        
        if not key:
            return ciphertext
            
        plain = []
        key_len = len(key)
        
        for i, c in enumerate(ciphertext):
            shift = ord(key[i % key_len]) - ord('a')
            p = (ord(c) - ord('a') - shift) % 26
            plain.append(chr(p + ord('a')))
            
        return ''.join(plain)


class CryptanalysisService:
    def __init__(self):
        self.vigenere = VigenereService()
        
    def split_into_subtexts(self, ciphertext: str, key_length: int) -> List[str]:
        """Divides the text into key_length subtexts, each encrypted with a unique shift"""
        subtexts = ['' for _ in range(key_length)]
        for i, char in enumerate(ciphertext):
            subtexts[i % key_length] += char
        return subtexts
        
    def get_subtext_chi_scores(self, subtext: str) -> List[Tuple[int, float]]:
        """Calculates chi-square for each possible shift (0-25) on the subtext"""
        length = len(subtext)
        if length == 0:
            return [(shift, 9999.0) for shift in range(26)]

        # Count frequency of each letter in the subtext
        count = Counter(subtext)
        observed = [count.get(chr(i + ord('a')), 0) for i in range(26)]

        results = []
        for shift in range(26):
            # Apply inverse shift to simulate decryption
            freq = [0] * 26
            for i in range(26):
                sub_letter_index = (i + shift) % 26
                freq[i] = observed[sub_letter_index]

            # Normalize to compare with English frequencies
            chi = 0.0
            for i in range(26):
                expected = self.vigenere.english_frequencies[i] * length
                diff = freq[i] - expected
                chi += (diff * diff) / (expected + 1e-9)  # Avoid division by zero
            results.append((shift, chi))

        return results
        
    def get_top_shifts_for_subtext(self, subtext: str, top_n: int = 5) -> List[Tuple[int, float]]:
        """Returns the top_n most probable shifts for a subtext, sorted by chi"""
        scores = self.get_subtext_chi_scores(subtext)
        scores.sort(key=lambda x: x[1])  # Sort by chi
        return scores[:top_n]
        
    def get_all_keys_with_score(self, ciphertext: str, key_length: int, top_n: int = 5) -> List[Tuple[str, float, str]]:
        """
        For each position, get the top_n most probable shifts.
        Then generate all combinations (Cartesian product).
        For each key candidate, calculate a 'total score' = sum of chi values.
        """
        # Split into subtexts
        subtexts = self.split_into_subtexts(ciphertext, key_length)

        # Get top_n shifts per subtext
        top_shifts_per_position = []
        for sub in subtexts:
            best_shifts = self.get_top_shifts_for_subtext(sub, top_n=top_n)
            top_shifts_per_position.append(best_shifts)

        # Generate all combinations
        all_keys = []
        for combo in product(*top_shifts_per_position):
            # Calculate sum of chi values
            total_chi = sum(pair[1] for pair in combo)
            # Reconstruct the key
            shifts = [pair[0] for pair in combo]
            key = ''.join(chr(s + ord('a')) for s in shifts)

            # Decrypt
            plain = self.vigenere.decrypt(ciphertext, key)
            all_keys.append((key, total_chi, plain))

        return all_keys
        
    def analyze_by_key_length(self, ciphertext: str, key_length: int, top_n: int = 5, top_results: int = 10):
        """Analyze ciphertext using known key length"""
        ciphertext = self.vigenere.preprocess(ciphertext)
        
        # Get all possible keys with their scores
        candidates = self.get_all_keys_with_score(ciphertext, key_length, top_n=top_n)
        
        # Sort by total_chi (ascending)
        candidates.sort(key=lambda x: x[1])
        
        # Return results
        results = []
        for i in range(min(top_results, len(candidates))):
            k, sc, pl = candidates[i]
            results.append({"key": k, "score": sc, "plaintext": pl})
            
        if results:
            best_key, best_score, best_plain = candidates[0]
            return {
                "results": results,
                "best_key": best_key,
                "best_score": best_score,
                "best_plaintext": best_plain
            }
        return {
            "results": [],
            "best_key": "",
            "best_score": 0,
            "best_plaintext": ""
        }
        
    def add(self, x: str, y: str) -> str:
        """Add two characters in Vigenere cipher"""
        if x == "_" or y == "_":
            return "_"
        return chr((((ord(x)-65)+(ord(y)-65)) % 26)+65)
        
    def sub(self, x: str, y: str) -> str:
        """Subtract two characters in Vigenere cipher"""
        if x == "_" or y == "_":
            return "_"
        return chr((((ord(x)-65)-(ord(y)-65)) % 26)+65)
        
    def adds(self, a: str, b: str) -> str:
        """Add two strings character by character"""
        return "".join([self.add(x, y) for (x, y) in zip(a, b)])
        
    def subs(self, a: str, b: str) -> str:
        """Subtract two strings character by character"""
        return "".join([self.sub(x, y) for (x, y) in zip(a, b)])
        
    def clean(self, text: str) -> str:
        """Clean text to contain only uppercase letters and underscores"""
        return "".join(filter(lambda x: x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ_", text.upper()))
        
    def is_repetition(self, hay: str, needle: str) -> bool:
        """Check if string is a repetition"""
        hay, needle = self.clean(hay), self.clean(needle)
        if not hay or not needle:
            return True
        return hay[0] == needle[0] and self.is_repetition(hay[1:], needle[1:] + needle[0])
        
    def build_key_from_part(self, keypart: str, index: int, length: int) -> str:
        """Build a key from a part"""
        keypart = self.clean(keypart)
        keypart = keypart[:length]
        keypart = keypart[index:] + "_" * (length-len(keypart)) + keypart[:index]
        return keypart
        
    def guess_key(self, crypt: str, guess: str, length: int = 3) -> List[Tuple[str, str]]:
        """Returns list of tuples of guesses for given key length"""
        solutions = []
        for i in range(len(crypt)-len(guess)+1):
            crypart = crypt[i:i+len(guess)]
            keypart = self.subs(crypart, guess)
            if len(keypart) > length:
                if not self.is_repetition(keypart, keypart[:length]):
                    continue
            decoded = False
            for n in range(length):
                key = self.build_key_from_part(keypart, (i+n) % length, length)
                decoded = self.decode(crypt, key)
                if guess in decoded:
                    break
            if decoded and guess in decoded:
                solutions.append((decoded, key))
        return solutions
        
    def encode(self, text: str, key: str) -> str:
        """Encode text using Vigenere cipher with uppercase"""
        text, key = self.clean(text), self.clean(key)
        ret = ""
        while len(text) > len(key):
            ret += self.adds(text, key)
            text = text[len(key):]
        ret += self.adds(text, key[:len(text)])
        return ret
        
    def decode(self, text: str, key: str) -> str:
        """Decode text using Vigenere cipher with uppercase"""
        text, key = self.clean(text), self.clean(key)
        if len(key) > len(text):
            key = key[:len(text)]
        ret = ""
        while len(text) > len(key):
            ret += self.subs(text, key)
            text = text[len(key):]
        ret += self.subs(text, key[:len(text)])
        return ret
        
    def analyze_by_suspected_word(self, ciphertext: str, suspected_word: str, key_length: int) -> List[dict]:
        """Analyze ciphertext using a suspected word"""
        ciphertext = self.clean(ciphertext)
        suspected_word = self.clean(suspected_word)
        
        possible_plaintexts = self.guess_key(ciphertext, suspected_word, key_length)
        
        results = []
        for plaintext, key in possible_plaintexts:
            results.append({"key": key, "plaintext": plaintext})
            
        return results