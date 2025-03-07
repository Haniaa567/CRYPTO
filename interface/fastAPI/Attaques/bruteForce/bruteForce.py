import hashlib
import itertools
import string
import concurrent.futures
import threading
import os
import time
# Global variables
password_found = False
password_lock = threading.Lock()
le_bon_MotDePasse = None

# Function executed by each thread
def generate_passwords(characters, length):
    for combination in itertools.product(characters, repeat=length):
        yield ''.join(combination)

def thread_function(password_hash, characters, length):
    global password_found
    global le_bon_MotDePasse

    for password in generate_passwords(characters, length):
        if password_found:
            return

        password_bytes = password.encode('utf-8')
        password_md5 = hashlib.md5(password_bytes).hexdigest()

        if password_md5 == password_hash:
            with password_lock:
                if not password_found:
                    password_found = True
                    le_bon_MotDePasse = password
            return

# Main brute force function
def brute_force_password(password_hash, max_length=12, num_threads=None):
    global le_bon_MotDePasse

    # Limiting to alphanumeric characters for better performance
    characters = string.ascii_letters + string.digits+ string.punctuation
    if num_threads is None:
        num_threads = min(24, os.cpu_count() * 2)  # Use up to 24 threads or twice the number of CPU cores

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for length in range(1, max_length + 1):
            futures.append(executor.submit(thread_function, password_hash, characters, length))

        for future in concurrent.futures.as_completed(futures):
            if password_found:
                break

    if le_bon_MotDePasse:
        print("Mot de passe trouvé !")
        print("Le bon mot de passe est :", le_bon_MotDePasse)
    else:
        print("Mot de passe non trouvé.")
        # Main function
def main():
    password_hash = input("Entrez le hash MD5 du mot de passe à cracker : ")
    brute_force_password(password_hash)

if __name__ == '__main__':
    start=time.time()
    main()
    end=time.time()
    print("temp",end-start)