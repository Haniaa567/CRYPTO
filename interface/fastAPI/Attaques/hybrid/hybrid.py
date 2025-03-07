import hashlib
import itertools
from hashlib import sha256
from passlib.hash import md5_crypt
from passlib.hash import sha1_crypt
from passlib.hash import sha256_crypt

def generate_hash(password):
    """Génère un hash SHA-256 pour un mot de passe donné."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_password_list(filename):
    """Charge la liste des mots de passe depuis un fichier."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def apply_transformations(base_password):
    """Applique différentes transformations sur un mot de base."""
    transformations = [
        base_password.upper(),
        base_password.lower(),
        base_password.capitalize(),
        base_password + "123",
        base_password + "!",
        "123" + base_password,
        "!"+ base_password,
    ]
    return transformations

def brute_force_extension(base_password, charset, max_length=2):
    """Génère des extensions de force brute pour un mot de base."""
    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            yield base_password + ''.join(combo)

def hybrid_attack(target_hash, filename, charset="0123456789!@#"):
    """Effectue une attaque hybride sur le hash cible."""
    password_list = load_password_list(filename)

    for base_password in password_list:
        if generate_hash(base_password) == target_hash:
                print(f"Mot de passe trouvé : {base_password}")
                return base_password
            
    for base_password in password_list:
        # Appliquer les transformations simples
        transformations = apply_transformations(base_password)
        for password in transformations:
            if generate_hash(password) == target_hash:
                print(f"Mot de passe trouvé : {password}")
                return password

        # Appliquer la force brute avec extensions sur chaque transformation
        for password in transformations:
            for extended_password in brute_force_extension(password, charset):
                if generate_hash(extended_password) == target_hash:
                    print(f"Mot de passe trouvé avec extension : {extended_password}")
                    return extended_password

    print("Aucun mot de passe correspondant trouvé.")
    return None
#fonction generale avec tout les hachage et avec ou sans salt
def launch_hybride_attack():
    charset="0123456789!@#"
    hashed_password = entry_dic_hyb.get().strip()
    salt_hash=entry_hyb_salt.get().strip()
    if var4.get()==0: #sans salt
        if dernier_bouton_clique==1:
            if message_box_md5(hashed_password)==True:
             return
        elif dernier_bouton_clique==2:
            if message_box_sha1(hashed_password)==True:
               return
        else:
            if message_box_sha256(hashed_password)==True:
               return
    else:
        if messagebox_salt(salt_hash)== True :
          return
        if dernier_bouton_clique==1:
           if message_box_md5_crypt(hashed_password)==True:
            return
           chaine_inter = "$1$" + salt_hash + "$"
           hashed_password=chaine_inter+hashed_password
        elif dernier_bouton_clique==2:
            if message_box_sha1_crypt(hashed_password)==True:
             return
            hashed_password="$sha1$1$"+salt_hash+"$"+hashed_password
        else:
            if message_box_sha256_crypt(hashed_password)==True:
             return
            hashed_password="$5$rounds=1000$"+salt_hash+"$"+hashed_password
    with open("liste.txt", "r") as file:
        password_list = [line.strip() for line in file]
    for base_password in password_list:
        transformations = apply_transformations(base_password)
        if var4.get()==0:
            if dernier_bouton_clique == 1:
                   for password in password_list:
                       if hashed_password == hashlib.md5(password.encode()).hexdigest():
                        return password
                   for password in transformations:
                      md5_hash = hashlib.md5(password.encode()).hexdigest()
                      if hashed_password == md5_hash:
                        return password
                   for password in transformations:
                     for extended_password in brute_force_extension(password, charset):
                       md5_hash = hashlib.md5(extended_password.encode()).hexdigest()
                       if hashed_password == md5_hash:
                        return extended_password
                
                
            elif dernier_bouton_clique==2:
                    for password in password_list:
                       if hashed_password == hashlib.sha1(password.encode()).hexdigest():
                        return password
                    for password in transformations:
                      sha1_hash = hashlib.sha1(password.encode()).hexdigest()
                      if hashed_password == sha1_hash:
                        return password
                    for password in transformations:
                     for extended_password in brute_force_extension(password, charset):
                      sha1_hash = hashlib.sha1(extended_password.encode()).hexdigest()
                      if hashed_password == sha1_hash:
                        return extended_password
            else:
                    for password in password_list:
                       if hashed_password == hashlib.sha256(password.encode()).hexdigest():
                        return password
                    for password in transformations:
                      sha256_hash = hashlib.sha256(password.encode()).hexdigest()
                      if hashed_password == sha256_hash:
                        return password
                    for password in transformations:
                     for extended_password in brute_force_extension(password, charset):
                      sha256_hash = hashlib.sha256(extended_password.encode()).hexdigest()
                      if hashed_password == sha256_hash:
                        return extended_password
        else:
            if dernier_bouton_clique == 1:
                    for password in password_list:
                       if hashed_password == md5_crypt.using(salt=salt_hash).hash(password):
                        return password
                    for password in transformations:
                       md5_hash = md5_crypt.using(salt=salt_hash).hash(password)
                       if hashed_password == md5_hash:
                        return password
                    for password in transformations:
                      for extended_password in brute_force_extension(password, charset):
                       md5_hash = md5_crypt.using(salt=salt_hash).hash(extended_password)
                       if hashed_password == md5_hash:
                        return extended_password
            elif dernier_bouton_clique==2:
                    for password in password_list:
                       if hashed_password == sha1_crypt.using(salt=salt_hash,rounds=1).hash(password):
                        return password
                    for password in transformations:
                       sha1_hash = sha1_crypt.using(salt=salt_hash,rounds=1).hash(password)
                       if hashed_password == sha1_hash:
                        return password
                    for password in transformations:
                      for extended_password in brute_force_extension(password, charset):
                       sha1_hash = sha1_crypt.using(salt=salt_hash,rounds=1).hash(extended_password)
                       if hashed_password == sha1_hash:
                        return extended_password
            else:
                    for password in password_list:
                       if hashed_password == sha256_crypt.using(salt=salt_hash,rounds=1000).hash(password):
                        return password
                    for password in transformations:
                      sha256_hash = sha256_crypt.using(salt=salt_hash,rounds=1000).hash(password)
                      if hashed_password == sha256_hash:
                        return password
                    for password in transformations:
                     for extended_password in brute_force_extension(password, charset):
                      sha256_hash = sha256_crypt.using(salt=salt_hash,rounds=1000).hash(extended_password)
                      if hashed_password == sha256_hash:
                        return extended_password    

    return None
        
  

# Exemple d'utilisation
target_password = "aaa"
target_hash = generate_hash(target_password)  # Simuler un hash cible
filename = 'liste.txt'  # Nom du fichier contenant les mots de base

found_password = hybrid_attack(target_hash, filename)