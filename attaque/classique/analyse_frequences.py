import string

# Fréquence relative des lettres en anglais
EN_REL_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228, 'G': 0.02015,
    'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749,
    'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056, 'U': 0.02758,
    'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 'Z': 0.00074
}

def get_letter_counts(text):
    text_upper = text.upper()
    return {letter: text_upper.count(letter) for letter in string.ascii_uppercase}

def _get_letter_frequencies(text):
    letter_counts = get_letter_counts(text)
    return {letter: count / len(text) for letter, count in letter_counts.items()}

def shift(text, amount):
    letters = string.ascii_uppercase
    shifted = ''.join(
        letters[(letters.index(letter) - amount) % len(letters)] if letter in letters else letter
        for letter in text
    )
    return shifted

def _corr(text, lf):
    return sum(lf.get(letter, 0) * EN_REL_FREQ.get(letter, 0) for letter in text)

def _find_key_letter(text, lf):
    key_letter = ''
    max_corr = 0
    for count, letter in enumerate(string.ascii_uppercase):
        shifted = shift(text, amount=count)
        corr = _corr(text=shifted, lf=lf)
        if corr > max_corr:
            max_corr = corr
            key_letter = letter
    return key_letter

def get_blocks(text, size):
    return [text[i:i + size] for i in range(0, len(text), size)]

def get_columns(blocks):
    group_size = len(blocks[0])
    return [''.join(block[i] for block in blocks if i < len(block)) for i in range(group_size)]

def to_blocks(cols):
    col_size = len(cols[0])
    return [''.join(cols[col][i] for col in range(len(cols)) if i < len(cols[col])) for i in range(col_size)]

def restore_key(cyphertext, key_len):
    key = ''
    blocks = get_blocks(text=cyphertext, size=key_len)
    columns = get_columns(blocks)
    frequencies = _get_letter_frequencies(text=cyphertext)
    for column in columns:
        key += _find_key_letter(text=column, lf=frequencies)
    return key

def _decypher(cyphertext, key):
    letters = string.ascii_uppercase
    shifts = [letters.index(letter) for letter in key]
    blocks = get_blocks(text=cyphertext, size=len(key))
    cols = get_columns(blocks)
    
    # Correction ici : éviter la confusion avec shift()
    decyphered_blocks = to_blocks([shift(col, amount) for col, amount in zip(cols, shifts)])
    
    return ''.join(decyphered_blocks)

# Exemple d'utilisation
cyphertext = "XPOJSVVGJZDUKSIYIUMZIESIXXZUWLQSXGMTLHATLWFLTFRVXJVLJIZJHPMJYYINSUFSUEPZTFUIIOPMWJHYGZBNTEHGSMCJIGKJMIJLBTPRSIRINJZDUKSIYIUMZIOVLJWEI"
key_len = 7

key = restore_key(cyphertext, key_len)
decyphered = _decypher(cyphertext, key)

print('Chosen key length: ' + str(key_len))
print('Restored key: ' + str(key))
print('Plaintext: ' + str(decyphered))
