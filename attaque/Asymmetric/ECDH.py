from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization

def generate_keys():
    """Génère une paire de clés ECDH"""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_key(private_key, peer_public_key):
    """Dérive une clé partagée en utilisant la clé privée locale et la clé publique du pair"""
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)
    return derived_key

def save_key_to_file(key, filename, is_private=False):
    """Enregistre une clé privée ou publique dans un fichier"""
    with open(filename, "wb") as key_file:
        if is_private:
            pem = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        else:
            pem = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        key_file.write(pem)

def load_key_from_file(filename, is_private=False):
    """Charge une clé privée ou publique depuis un fichier"""
    with open(filename, "rb") as key_file:
        pem_data = key_file.read()
        if is_private:
            return serialization.load_pem_private_key(pem_data, password=None)
        else:
            return serialization.load_pem_public_key(pem_data)

# Générer les paires de clés ECDH pour les deux parties
private_key_a, public_key_a = generate_keys()
private_key_b, public_key_b = generate_keys()

# Enregistrer les clés dans des fichiers
save_key_to_file(private_key_a, "ecdh_private_key_a.pem", is_private=True)
save_key_to_file(public_key_a, "ecdh_public_key_a.pem", is_private=False)
save_key_to_file(private_key_b, "ecdh_private_key_b.pem", is_private=True)
save_key_to_file(public_key_b, "ecdh_public_key_b.pem", is_private=False)

# Charger les clés depuis des fichiers
loaded_private_key_a = load_key_from_file("ecdh_private_key_a.pem", is_private=True)
loaded_public_key_a = load_key_from_file("ecdh_public_key_a.pem", is_private=False)
loaded_private_key_b = load_key_from_file("ecdh_private_key_b.pem", is_private=True)
loaded_public_key_b = load_key_from_file("ecdh_public_key_b.pem", is_private=False)

# Dériver les clés partagées
shared_key_a = derive_shared_key(loaded_private_key_a, loaded_public_key_b)
shared_key_b = derive_shared_key(loaded_private_key_b, loaded_public_key_a)

# Les clés partagées devraient être identiques
print(f"Clé partagée A: {shared_key_a.hex()}")
print(f"Clé partagée B: {shared_key_b.hex()}")
print(f"Les clés partagées sont identiques: {shared_key_a == shared_key_b}")
