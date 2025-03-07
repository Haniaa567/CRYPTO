import hashlib
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
    """Applique différentes transformations sur un mot de passe de base."""
    # Vous pouvez ajouter autant de transformations que vous le souhaitez
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

def dictionary_attack(hash_target, filename):
    """Effectue une attaque par dictionnaire améliorée."""
    password_list = load_password_list(filename)
    for base_password in password_list:
        if generate_hash(base_password) == hash_target:
                print(f"Mot de passe trouvé : {base_password}")
                return base_password
            
    for base_password in password_list:
        transformations = apply_transformations(base_password)
        for password in transformations:
            if generate_hash(password) == hash_target:
                print(f"Mot de passe trouvé : {password}")
                return password
    print("Aucun mot de passe correspondant trouvé.")
    return None
## fonction generale: avec 3 type de hachage et avec ou sans salt
def launch_dic_aml_attack():

    hashed_password = entry_dic_aml.get().strip()
    salt_hash=entry_aml_salt.get().strip()
    if var3.get()==0: #verification hachage valide
        if dernier_bouton_clique==1:# dernier_bouton_clique c'est quelle hachage 
            if message_box_md5(hashed_password)==True:
             return
        elif dernier_bouton_clique==2:
            if message_box_sha1(hashed_password)==True:
               return
        else:
            if message_box_sha256(hashed_password)==True:
               return
    else: 
        if dernier_bouton_clique==1: #concatiner le salt avec hachage car la bib passlib marche comme ca

           chaine_inter = "$1$" + salt_hash + "$"
           hashed_password=chaine_inter+hashed_password
        elif dernier_bouton_clique==2:
            hashed_password="$sha1$1$"+salt_hash+"$"+hashed_password
        else:
            hashed_password="$5$rounds=1000$"+salt_hash+"$"+hashed_password
            
    with open("liste.txt", "r") as file:
     password_list = [line.strip() for line in file]
    for base_password in password_list:
        transformations = apply_transformations(base_password)
        
    if var3.get()==0: #non salt
                if dernier_bouton_clique == 1:
                   for password in password_list:
                       if hashed_password == hashlib.md5(password.encode()).hexdigest():
                        return password
                   for password in transformations:
                      md5_hash = hashlib.md5(password.encode()).hexdigest()
                      if hashed_password == md5_hash:
                        return password
                
                elif dernier_bouton_clique==2:
                    for password in password_list:
                       if hashed_password == hashlib.sha1(password.encode()).hexdigest():
                        return password
                    for password in transformations:
                      sha1_hash = hashlib.sha1(password.encode()).hexdigest()
                      if hashed_password == sha1_hash:
                        return password
                else: 
                    for password in password_list:
                       if hashed_password == hashlib.sha256(password.encode()).hexdigest():
                        return password
                    for password in transformations:
                      sha256_hash = hashlib.sha256(password.encode()).hexdigest()
                      if hashed_password == sha256_hash:
                        return password
    else:#salt
                if dernier_bouton_clique == 1:
                    for password in password_list:
                       if hashed_password == md5_crypt.using(salt=salt_hash).hash(password):
                        return password
                    for password in transformations:
                       md5_hash = md5_crypt.using(salt=salt_hash).hash(password)
                       if hashed_password == md5_hash:
                        return password
                elif dernier_bouton_clique==2:
                    for password in password_list:
                       if hashed_password == sha1_crypt.using(salt=salt_hash,rounds=1).hash(password):
                        return password
                    for password in transformations:
                       sha1_hash = sha1_crypt.using(salt=salt_hash,rounds=1).hash(password)
                       if hashed_password == sha1_hash:
                        return password
                else:
                    for password in password_list:
                       if hashed_password == sha256_crypt.using(salt=salt_hash,rounds=1000).hash(password):
                        return password
                    for password in transformations:
                      sha256_hash = sha256_crypt.using(salt=salt_hash,rounds=1000).hash(password)
                      if hashed_password == sha256_hash:
                        return password    

    return None

# Exemple d'utilisation
hash_target = generate_hash("hamad123456")  # Simuler un hash cible
filename = 'liste.txt'  # Nom du fichier contenant les mots de passe potentiels

found_password = dictionary_attack(hash_target, filename)