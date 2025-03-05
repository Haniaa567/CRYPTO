def ceasar_encryption(text,shift):
    result=""
    shift=shift%26
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def ceasar_decryption(text,shift):
    result=""
    shift=shift%26
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
        else:
            result += char
    return result


def brute_force_ceasar(cipher):
    print("brute force attack on ceasar cipher:")
    for shift in range(1,26):
        print(f"Shift: {shift} -> {ceasar_decryption(cipher,shift)}")

if __name__ == "__main__":
    text="helloworld"
    shift=60
    enc=ceasar_encryption(text,shift)
    print(f"encrypted text:{enc}")

    dec=ceasar_decryption(enc,shift)
    print(f"decrypted text:{dec}")

    brute_force_ceasar(enc)