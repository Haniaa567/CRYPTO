'''''
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 12345))
s.listen(1)
print("Attaquant en attente...")

conn_a, addr_a = s.accept()
print(f"Connecté à A : {addr_a}")

# Connexion au récepteur
conn_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_b.connect(('127.0.0.1', 54321))
print("Connecté à B.")

# Relayer la clé publique de B à A
public_key_b_b64 = conn_b.recv(4096).decode()
conn_a.send(public_key_b_b64.encode())

# Recevoir la longueur des données de A
data_len = int.from_bytes(conn_a.recv(4), byteorder='big')
data = b""
while len(data) < data_len:
    packet = conn_a.recv(data_len - len(data))
    if not packet:
        break
    data += packet

# Extraire les composants
encrypted_aes_key, ciphertext, signature, dsa_public_key_bytes = data.split(b"||")

# Modifier le message
ciphertext_modifie = ciphertext[:-1] + b"X"
print("Message modifié par l'attaquant !")

# Relayer les données modifiées à B
modified_data = encrypted_aes_key + b"||" + ciphertext_modifie + b"||" + signature + b"||" + dsa_public_key_bytes
conn_b.send(data_len.to_bytes(4, byteorder='big') + modified_data)

conn_a.close()
conn_b.close()
s.close()
'''
import socket

# Étape 1 : Démarrage du serveur de l'attaquant
print("Étape 1 : Démarrage du serveur de l'attaquant sur 127.0.0.1:54321...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 54321))
s.listen(1)
print("Étape 1 : Serveur démarré avec succès.")

# Étape 2 : Attente de connexion de A
print("Étape 2 : Attente de connexion de A...")
conn_a, addr_a = s.accept()
print(f"Étape 2 : Connecté à A : {addr_a}")

# Étape 3 : Connexion au récepteur B
print("Étape 3 : Connexion au récepteur B sur 127.0.0.1:12345...")
conn_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_b.connect(('127.0.0.1', 12345))
print("Étape 3 : Connecté à B avec succès.")

# Étape 4 : Relayer la clé publique de B à A
print("Étape 4 : Relayer la clé publique de B à A...")
public_key_b_b64 = conn_b.recv(4096).decode()
conn_a.send(public_key_b_b64.encode())
print("Étape 4 : Clé publique relayée avec succès.")

# Étape 5 : Recevoir la longueur des données de A
print("Étape 5 : Recevoir la longueur des données de A...")
data_len = int.from_bytes(conn_a.recv(4), byteorder='big')
print(f"Étape 5 : Longueur des données : {data_len} octets.")

# Étape 6 : Recevoir les données de A
print("Étape 6 : Recevoir les données de A...")
data = b""
while len(data) < data_len:
    packet = conn_a.recv(data_len - len(data))
    if not packet:
        raise ValueError("Connexion interrompue par A.")
    data += packet
print("Étape 6 : Données reçues avec succès.")

# Étape 7 : Extraire les composants
print("Étape 7 : Extraire les composants des données...")
try:
    encrypted_aes_key, ciphertext, signature, dsa_public_key_bytes = data.split(b"||")
    print(f"Étape 7 : Composants extraits avec succès.")
    print(f"Longueur encrypted_aes_key : {len(encrypted_aes_key)}")
    print(f"Longueur ciphertext : {len(ciphertext)}")
    print(f"Longueur signature : {len(signature)}")
    print(f"Longueur dsa_public_key_bytes : {len(dsa_public_key_bytes)}")
except ValueError as e:
    print(f"Étape 7 : Erreur lors de l'extraction des composants : {e}")
    conn_a.close()
    conn_b.close()
    s.close()
    exit()

# Étape 8 : Modifier le message
print("Étape 8 : Modifier le message en remplaçant le dernier octet par 'X'...")
ciphertext_modifie = ciphertext[:-1] + b"X"
print(f"Étape 8 : Message modifié avec succès. Ancien dernier octet : {ciphertext[-1:]} | Nouveau dernier octet : {ciphertext_modifie[-1:]}")

# Étape 9 : Relayer les données modifiées à B
print("Étape 9 : Relayer les données modifiées à B...")
modified_data = encrypted_aes_key + b"||" + ciphertext_modifie + b"||" + signature + b"||" + dsa_public_key_bytes
conn_b.send(data_len.to_bytes(4, byteorder='big') + modified_data)
print("Étape 9 : Données modifiées envoyées à B avec succès.")

# Étape 10 : Fermer les connexions
print("Étape 10 : Fermer les connexions...")
conn_a.close()
conn_b.close()
s.close()
print("Étape 10 : Connexions fermées avec succès.")