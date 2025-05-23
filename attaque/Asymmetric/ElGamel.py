try:
    from cryptography.hazmat.primitives.asymmetric import dh
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
except ImportError:
    raise ImportError("The 'cryptography' library is required but not installed. Install it using: pip install cryptography")

import os
import hashlib
import argparse
from datetime import datetime
from random import randint

# Note: This script requires the 'cryptography' library for cryptographic operations.
# Install it with: pip install cryptography

def gcd(a, b):
    """Compute the Greatest Common Divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def find_primitive_root(p, max_attempts=100):
    """
    Find a primitive root modulo p (optimized for safe primes).
    Since p is a safe prime (p = 2q + 1, q prime), g is a primitive root if:
    - g^2 ≠ 1 mod p
    - g^q ≠ 1 mod p
    """
    q = (p - 1) // 2  # Since p is a safe prime, p-1 = 2q
    print(f"Finding primitive root for p (bit length: {p.bit_length()})...")

    for g in range(2, 100):  # Search small numbers for efficiency
        if g >= p:
            break
        if max_attempts <= 0:
            raise ValueError("No primitive root found within attempt limit")
        
        # Check if g is a primitive root
        if pow(g, 2, p) == 1:
            continue
        if pow(g, q, p) == 1:
            continue
        
        print(f"Found primitive root g = {g}")
        return g
    
    raise ValueError("No primitive root found within search range")

def generate_keys(bits=1024):
    """
    Generate ElGamal private and public keys.
    Using a 1024-bit size for better compatibility with larger data.
    """
    print(f"Generating keys with {bits}-bit prime...")
    # Generate a large safe prime using cryptography's DH parameters
    parameters = dh.generate_parameters(generator=2, key_size=bits, backend=default_backend())
    p = parameters.parameter_numbers().p
    print(f"Generated prime p (bit length: {p.bit_length()})")
    
    g = find_primitive_root(p)
    private_key = randint(2, p - 2)
    public_key = pow(g, private_key, p)
    print("Key generation complete.")
    return p, g, private_key, public_key

def save_key(filename, data):
    """Save key data to a file."""
    try:
        with open(filename, 'w') as file:
            file.write(','.join(map(str, data)))
    except IOError as e:
        raise IOError(f"Failed to save key to {filename}: {e}")

def load_key(directory, filename, is_private=False):
    """Load public or private key from a file in the specified directory."""
    try:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            parts = list(map(int, file.read().split(',')))
        if len(parts) != 3:
            raise ValueError("Invalid key format")
        return parts  # (p, g, x) for private, (p, g, y) for public
    except (IOError, ValueError) as e:
        raise ValueError(f"Failed to load key from {filename}: {e}")

def determine_decrypted_file_path(file_path):
    """Determine the file path for the decrypted file."""
    if file_path.endswith(".enc"):
        return file_path[:-4]  # Remove '.enc' from the file path
    else:
        return file_path + ".decrypted"  # Add '.decrypted' if no '.enc' extension

def encrypt_file(file_path, public_key, password):
    """Encrypt a file using the ElGamal public key and a password."""
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
    except IOError as e:
        raise IOError(f"Failed to read file {file_path}: {e}")

    hash_before = hashlib.sha256(file_data).hexdigest()
    file_data_with_hash_and_password = file_data + hash_before.encode() + password.encode()
    print(f"Encrypting data of size {len(file_data_with_hash_and_password)} bytes")

    p, g, y = public_key

    # Ensure k is coprime with p-1 for secure ElGamal encryption
    max_attempts = 100
    for _ in range(max_attempts):
        k = randint(1, p - 1)
        if gcd(k, p - 1) == 1:
            break
    else:
        raise ValueError("Failed to find a valid k coprime with p-1 after multiple attempts")

    # Convert data to integer for encryption
    data_int = int.from_bytes(file_data_with_hash_and_password, byteorder='big')
    if data_int >= p:
        raise ValueError(f"Data too large for modulus p (data: {data_int.bit_length()} bits, p: {p.bit_length()} bits)")
    c1 = pow(g, k, p)
    c2 = (data_int * pow(y, k, p)) % p
    print(f"c1 length: {len(str(c1))}, c2 length: {len(str(c2))}")
    
    # Prefix c1 and c2 with their lengths for reliable parsing
    c1_bytes = c1.to_bytes((c1.bit_length() + 7) // 8, byteorder='big')
    c2_bytes = c2.to_bytes((c2.bit_length() + 7) // 8, byteorder='big')
    c1_len = len(c1_bytes).to_bytes(4, byteorder='big')
    c2_len = len(c2_bytes).to_bytes(4, byteorder='big')
    encrypted_data = c1_len + c1_bytes + c2_len + c2_bytes

    encrypted_file_path = file_path + ".enc"
    try:
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_data)
    except IOError as e:
        raise IOError(f"Failed to write encrypted file {encrypted_file_path}: {e}")

    hash_after = hashlib.sha256(encrypted_data).hexdigest()
    return encrypted_file_path, hash_before, hash_after

def decrypt_file(file_path, private_key, password):
    """Decrypt a file using the ElGamal private key and password."""
    p, g, x = private_key
    try:
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
    except IOError as e:
        raise IOError(f"Failed to read encrypted file {file_path}: {e}")
    print(f"Decrypting data of size {len(encrypted_data)} bytes")

    # Parse c1 and c2 using length prefixes
    c1_len = int.from_bytes(encrypted_data[:4], byteorder='big')
    c1_bytes = encrypted_data[4:4 + c1_len]
    c2_len = int.from_bytes(encrypted_data[4 + c1_len:4 + c1_len + 4], byteorder='big')
    c2_bytes = encrypted_data[4 + c1_len + 4:]

    c1 = int.from_bytes(c1_bytes, byteorder='big')
    c2 = int.from_bytes(c2_bytes, byteorder='big')
    print(f"Decrypted c1 length: {len(c1_bytes)}, c2 length: {len(c2_bytes)}")

    s = pow(c1, x, p)
    # Compute modular inverse of s modulo p
    def mod_inverse(a, m):
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        _, x, _ = extended_gcd(a, m)
        return (x % m + m) % m

    plaintext_int = (c2 * mod_inverse(s, p)) % p
    plaintext_with_hash_and_password = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, byteorder='big')
    print(f"Decrypted data size: {len(plaintext_with_hash_and_password)} bytes")

    hash_length = 64  # SHA-256 hex length
    password_length = len(password.encode())
    try:
        original_data = plaintext_with_hash_and_password[:-hash_length - password_length]
        embedded_hash = plaintext_with_hash_and_password[-hash_length - password_length:-password_length].decode()
        embedded_password = plaintext_with_hash_and_password[-password_length:].decode()
    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid data format or corrupted file: {e}")

    if embedded_password != password:
        raise ValueError("Incorrect password")

    computed_hash = hashlib.sha256(original_data).hexdigest()
    if computed_hash != embedded_hash:
        raise ValueError("Data integrity check failed: The data has been altered or corrupted.")

    return original_data, computed_hash

def get_file_metadata(file_path):
    """Extract metadata from the file."""
    try:
        metadata = {
            'File Name': os.path.basename(file_path),
            'Size': os.path.getsize(file_path),
            'Creation Time': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
            'Last Modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        }
        return metadata
    except OSError as e:
        raise OSError(f"Failed to get metadata for {file_path}: {e}")

def log_operation(file_path, hash_before, hash_after, metadata, operation="encryption", log_file="operation.log"):
    """Log encryption or decryption details."""
    try:
        with open(log_file, 'a') as log:
            log.write("-" * 105 + "\n")
            log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}: {operation.capitalize()} '{file_path}'\n"
            log_entry += f"Hash Before: {hash_before}\n"
            log_entry += f"File Name: {metadata['File Name']}\n"
            log_entry += f"Size: {metadata['Size']}\n"
            log_entry += f"Creation Time: {metadata['Creation Time']}\n"
            log_entry += f"Last Modified: {metadata['Last Modified']}\n"
            log_entry += f"Hash After: {hash_after}\n"
            log.write(log_entry)
            log.write("-" * 105 + "\n")
    except IOError as e:
        raise IOError(f"Failed to write to log file {log_file}: {e}")

def main():
    """Main function to handle key generation, encryption, or decryption based on command-line arguments."""
    parser = argparse.ArgumentParser(description="ElGamal Encryption/Decryption Program (requires cryptography)")
    parser.add_argument("mode", choices=["generate", "encrypt", "decrypt"], help="Operation mode")
    parser.add_argument("--file", help="File to encrypt/decrypt")
    parser.add_argument("--password", help="Password for encryption/decryption")
    args = parser.parse_args()

    keys_directory = "Keys"
    public_key_file = "elgamal_public_key.txt"  # Just the filename, not the full path
    private_key_file = "elgamal_private_key.txt"  # Just the filename, not the full path

    if args.mode == "generate":
        os.makedirs(keys_directory, exist_ok=True)
        p, g, private_key, public_key = generate_keys()
        save_key(os.path.join(keys_directory, public_key_file), (p, g, public_key))
        save_key(os.path.join(keys_directory, private_key_file), (p, g, private_key))
        print("Keys generated and saved to the 'Keys' directory.")

    elif args.mode == "encrypt":
        if not args.file or not args.password:
            print("Error: --file and --password are required for encryption")
            return
        try:
            public_key = load_key(keys_directory, public_key_file)
            encrypted_file_path, hash_before, hash_after = encrypt_file(args.file, public_key, args.password)
            metadata = get_file_metadata(args.file)
            log_operation(args.file, hash_before, hash_after, metadata, operation="encryption")
            os.remove(args.file)
            print(f"File encrypted and saved as {encrypted_file_path}. Original file deleted.")
        except Exception as e:
            print(f"Encryption failed: {e}")

    elif args.mode == "decrypt":
        if not args.file or not args.password:
            print("Error: --file and --password are required for decryption")
            return
        try:
            private_key = load_key(keys_directory, private_key_file, is_private=True)
            decrypted_data, original_hash = decrypt_file(args.file, private_key, args.password)
            decrypted_file_path = determine_decrypted_file_path(args.file)
            with open(decrypted_file_path, 'wb') as f:
                f.write(decrypted_data)
            decrypted_hash = hashlib.sha256(decrypted_data).hexdigest()
            metadata = get_file_metadata(decrypted_file_path)
            log_operation(args.file, original_hash, decrypted_hash, metadata, operation="decryption")
            os.remove(args.file)
            print(f"File decrypted successfully. Saved to {decrypted_file_path}. Encrypted file deleted.")
        except Exception as e:
            print(f"Decryption failed: {e}")

if __name__ == "__main__":
    main()