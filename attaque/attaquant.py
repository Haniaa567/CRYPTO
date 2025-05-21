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
