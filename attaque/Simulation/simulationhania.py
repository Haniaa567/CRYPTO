import json
import base64
import socket
import threading
import os
import time
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh, rsa, padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Générer une paire de clés RSA
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Générer des paramètres Diffie-Hellman
def generate_dh_parameters():
    return dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())

# Sérialiser les paramètres Diffie-Hellman
def serialize_dh_parameters(parameters):
    return parameters.parameter_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.ParameterFormat.PKCS3
    )

# Désérialiser les paramètres Diffie-Hellman
def deserialize_dh_parameters(pem_data):
    return serialization.load_pem_parameters(pem_data, backend=default_backend())

# Dériver une clé AES à partir du secret partagé
def derive_key(shared_secret):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # Clé AES-256
        salt=None,
        info=b"handshake data",
        backend=default_backend()
    )
    return hkdf.derive(shared_secret)

# Chiffrement AES-GCM
def aes_gcm_encrypt(key, plaintext, associated_data=b""):
    nonce = os.urandom(12)  # Nonce de 12 octets pour GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    encryptor.authenticate_additional_data(associated_data)
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return nonce, ciphertext, encryptor.tag

# Déchiffrement AES-GCM
def aes_gcm_decrypt(key, nonce, ciphertext, tag, associated_data=b""):
    try:
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decryptor.authenticate_additional_data(associated_data)
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()
    except Exception as e:
        print(f"Erreur de déchiffrement: {e}")
        return None

# Signer un message avec RSA
def rsa_sign(message, private_key):
    return private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

# Vérifier une signature RSA
def rsa_verify(message, signature, public_key):
    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Erreur de vérification RSA: {e}")
        return False

# Sérialiser une clé publique
def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

# Désérialiser une clé publique
def deserialize_public_key(pem_data):
    return serialization.load_pem_public_key(pem_data, backend=default_backend())

# Fonction utilitaire pour recevoir des données complètes
def recv_all(conn, length):
    data = b""
    while len(data) < length:
        try:
            packet = conn.recv(min(4096, length - len(data)))
            if not packet:
                raise ConnectionError("Connexion interrompue")
            data += packet
        except socket.timeout:
            print(f"Timeout lors de la réception, données partielles: {len(data)}/{length}")
            break
    return data

# Serveur
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind(('localhost', 12345))
        server_socket.listen(1)
        print("Serveur en écoute sur localhost:12345...")
    except OSError as e:
        print(f"Erreur lors du bind du serveur: {e}")
        return

    server_rsa_private, server_rsa_public = generate_rsa_key_pair()
    dh_parameters = generate_dh_parameters()
    server_dh_private = dh_parameters.generate_private_key()
    server_dh_public = server_dh_private.public_key()

    try:
        conn, addr = server_socket.accept()
        # Supprimer le timeout pour les tests
        conn.settimeout(None)
        with conn:
            print(f"Connecté à {addr}")

            # Envoyer les paramètres DH, la clé publique DH et RSA du serveur
            data = {
                "dh_parameters": base64.b64encode(serialize_dh_parameters(dh_parameters)).decode(),
                "dh_public": base64.b64encode(serialize_public_key(server_dh_public)).decode(),
                "rsa_public": base64.b64encode(serialize_public_key(server_rsa_public)).decode()
            }
            message = json.dumps(data).encode()
            conn.send(len(message).to_bytes(4, byteorder='big') + message)

            # Recevoir la clé publique DH et RSA du client
            length = int.from_bytes(conn.recv(4), byteorder='big')
            client_data_raw = recv_all(conn, length)
            client_data = json.loads(client_data_raw)
            client_dh_public = deserialize_public_key(base64.b64decode(client_data["dh_public"]))
            client_rsa_public = deserialize_public_key(base64.b64decode(client_data["rsa_public"]))

            # Calculer la clé partagée
            shared_secret = server_dh_private.exchange(client_dh_public)
            aes_key = derive_key(shared_secret)

            # Recevoir le message chiffré
            length = int.from_bytes(conn.recv(4), byteorder='big')
            message_data_raw = recv_all(conn, length)
            message_data = json.loads(message_data_raw)
            nonce = base64.b64decode(message_data["nonce"])
            ciphertext = base64.b64decode(message_data["ciphertext"])
            tag = base64.b64decode(message_data["tag"])
            signature = base64.b64decode(message_data["signature"])
            message = aes_gcm_decrypt(aes_key, nonce, ciphertext, tag)

            if message and rsa_verify(message, signature, client_rsa_public):
                print(f"Message reçu du client: {message}")
                # Répondre au client
                response = "Salut, Client! Message bien reçu."
                nonce, ciphertext, tag = aes_gcm_encrypt(aes_key, response)
                signature = rsa_sign(response, server_rsa_private)
                response_data = {
                    "nonce": base64.b64encode(nonce).decode(),
                    "ciphertext": base64.b64encode(ciphertext).decode(),
                    "tag": base64.b64encode(tag).decode(),
                    "signature": base64.b64encode(signature).decode()
                }
                message = json.dumps(response_data).encode()
                conn.send(len(message).to_bytes(4, byteorder='big') + message)
            else:
                print("Échec de la vérification de la signature ou du déchiffrement")
    except Exception as e:
        print(f"Erreur serveur: {e}")
    finally:
        server_socket.close()

# Client
def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Supprimer le timeout pour les tests
    client_socket.settimeout(None)
    for attempt in range(5):
        try:
            client_socket.connect(('localhost', 12345))
            break
        except ConnectionRefusedError:
            print(f"Tentative {attempt + 1}/5: Connexion refusée, attente...")
            time.sleep(1)
    else:
        print("Échec de la connexion au serveur après 5 tentatives")
        return

    client_rsa_private, client_rsa_public = generate_rsa_key_pair()
    try:
        # Recevoir les paramètres DH, la clé publique DH et RSA du serveur
        length = int.from_bytes(client_socket.recv(4), byteorder='big')
        server_data_raw = recv_all(client_socket, length)
        server_data = json.loads(server_data_raw)
        dh_parameters = deserialize_dh_parameters(base64.b64decode(server_data["dh_parameters"]))
        server_dh_public = deserialize_public_key(base64.b64decode(server_data["dh_public"]))
        server_rsa_public = deserialize_public_key(base64.b64decode(server_data["rsa_public"]))

        # Générer la clé DH du client avec les mêmes paramètres
        client_dh_private = dh_parameters.generate_private_key()
        client_dh_public = client_dh_private.public_key()

        # Envoyer la clé publique DH et RSA du client
        data = {
            "dh_public": base64.b64encode(serialize_public_key(client_dh_public)).decode(),
            "rsa_public": base64.b64encode(serialize_public_key(client_rsa_public)).decode()
        }
        message = json.dumps(data).encode()
        client_socket.send(len(message).to_bytes(4, byteorder='big') + message)

        # Calculer la clé partagée
        shared_secret = client_dh_private.exchange(server_dh_public)
        aes_key = derive_key(shared_secret)

        # Envoyer un message chiffré
        message = "Salut, Serveur! Ceci est un message sécurisé."
        nonce, ciphertext, tag = aes_gcm_encrypt(aes_key, message)
        signature = rsa_sign(message, client_rsa_private)
        message_data = {
            "nonce": base64.b64encode(nonce).decode(),
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "tag": base64.b64encode(tag).decode(),
            "signature": base64.b64encode(signature).decode()
        }
        message = json.dumps(message_data).encode()
        client_socket.send(len(message).to_bytes(4, byteorder='big') + message)

        # Recevoir la réponse du serveur
        length = int.from_bytes(client_socket.recv(4), byteorder='big')
        response_data_raw = recv_all(client_socket, length)
        response_data = json.loads(response_data_raw)
        nonce = base64.b64decode(response_data["nonce"])
        ciphertext = base64.b64decode(response_data["ciphertext"])
        tag = base64.b64decode(response_data["tag"])
        signature = base64.b64decode(response_data["signature"])
        response = aes_gcm_decrypt(aes_key, nonce, ciphertext, tag)
        if response and rsa_verify(response, signature, server_rsa_public):
            print(f"Réponse reçue du serveur: {response}")
        else:
            print("Échec de la vérification de la signature ou du déchiffrement")
    except Exception as e:
        print(f"Erreur client: {e}")
    finally:
        client_socket.close()

# Exécuter le serveur et le client dans des threads séparés
if __name__ == "__main__":
    server_thread = threading.Thread(target=server)
    client_thread = threading.Thread(target=client)
    server_thread.start()
    time.sleep(5)  # Augmenter à 5 secondes pour plus de fiabilité
    client_thread.start()
    server_thread.join()
    client_thread.join()