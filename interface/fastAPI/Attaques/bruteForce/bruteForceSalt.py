import hashlib
import itertools
import string
import concurrent.futures
import threading
import os
import time
from hashlib import sha256
from passlib.hash import md5_crypt
from passlib.hash import sha1_crypt
from passlib.hash import sha256_crypt

# Fonction pour tester si un mot correspond au hachage
def est_bon_mot(mot, hash_a_trouver):
    global dernier_bouton_clique
    salt_hash=entry_salt2.get().strip()
    if var2.get()==1:
        if dernier_bouton_clique==1:
            return md5_crypt.using(salt=salt_hash,rounds=1).hash(mot) == hash_a_trouver
        elif dernier_bouton_clique==2:
           return sha1_crypt.using(salt=salt_hash,rounds=1).hash(mot) == hash_a_trouver
        else:
            return sha256_crypt.using(salt=salt_hash,rounds=1000).hash(mot) == hash_a_trouver
    else:
        if dernier_bouton_clique==1:
            return md5(mot) == hash_a_trouver
        elif dernier_bouton_clique==2:
            return sha1(mot) == hash_a_trouver
        else:
            return sha256(mot) == hash_a_trouver
    
    
password_found = False
password_lock = threading.Lock()
le_bon_MotDePasse = None  
# Function to generate passwords
def generate_passwords(characters, length):
    for combination in itertools.product(characters, repeat=length):
        yield ''.join(combination)

# Function to test each password
def thread_function(password_hash, characters, length, hash_function):
    global password_found
    global le_bon_MotDePasse

    for password in generate_passwords(characters, length):
        if password_found:
            return
        
    

        password_bytes = password.encode('utf-8')
        
        generated_hash =hash_function(password_bytes)
        if generated_hash == password_hash:
              with password_lock:
                 if not password_found:
                    password_found = True
                    le_bon_MotDePasse = password
                    return

# Hash function selector based on button click

def get_hash_function(dernier_bouton_clique,var2,salt_hash):
    
    
    if var2.get()==1:#avec salt
        if dernier_bouton_clique == 3:
             return lambda password_bytes: sha256_crypt.using(salt=salt_hash,rounds=1000).hash(password_bytes) 
             
        elif dernier_bouton_clique==2:
          return lambda password_bytes: sha1_crypt.using(salt=salt_hash).hash(password_bytes)
        else:
           return lambda password_bytes: md5_crypt.using(salt=salt_hash).hash(password_bytes) 
    else:#sans
        if dernier_bouton_clique == 1:
           return lambda password_bytes: hashlib.md5(password_bytes).hexdigest()
        elif dernier_bouton_clique == 2:
            return lambda password_bytes: hashlib.sha1(password_bytes).hexdigest()
        else:
            return lambda password_bytes: hashlib.sha256(password_bytes,round=1000).hexdigest()



# Main brute force function
def brute_force_password(password_hash, dernier_bouton_clique, var2,salt_hash,max_length=12, num_threads=None):
    global password_found
    global le_bon_MotDePasse

    # Reset the global variables
    password_found = False
    le_bon_MotDePasse = None

    characters = string.ascii_letters + string.digits + string.punctuation
    hash_function = get_hash_function(dernier_bouton_clique,var2,salt_hash)

    if num_threads is None:
        num_threads = min(24, os.cpu_count() * 2)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for length in range(1, max_length + 1):
            futures.append(executor.submit(thread_function, password_hash, characters, length, hash_function))

        for future in concurrent.futures.as_completed(futures):
            if password_found:
                break

    return le_bon_MotDePasse

# Function to retrieve password based on hash input
def retrouver_mot():
    global dernier_bouton_clique

    hash_input = entry_brut_force.get().strip()
    salt_hash=None
    if var2.get() == 1:#avec salt
        salt_hash = entry_salt2.get().strip()
        if messagebox_salt(salt_hash):
            return
        if dernier_bouton_clique == 1:
            if message_box_md5_crypt(hash_input):
                return
            hash_input = "$1$" + salt_hash + "$" + hash_input
        elif dernier_bouton_clique == 2:
            if message_box_sha1_crypt(hash_input):
                return
            hash_input = "$sha1$1$" + salt_hash + "$" + hash_input
        else:
            if message_box_sha256_crypt(hash_input):
                return
            hash_input = "$5$rounds=1000$" + salt_hash + "$" + hash_input
    else:
        if dernier_bouton_clique == 1:
            if message_box_md5(hash_input):
                return
        elif dernier_bouton_clique == 2:
            if message_box_sha1(hash_input):
                return
        else:
            if message_box_sha256(hash_input):
                return

    le_bon_MotDePasse = brute_force_password(hash_input, dernier_bouton_clique,var2,salt_hash)  # Call the brute_force_password function with the provided hash and method



       