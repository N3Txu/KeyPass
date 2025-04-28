import random
import hashlib
import secrets
import json

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def simulate_bb84_key(num_bits=64):
    # Simular QKD usando protocolo BB84
    bits = [random.randint(0, 1) for _ in range(num_bits)]
    bases_sender = [random.choice(['Z', 'X']) for _ in range(num_bits)]
    bases_receiver = [random.choice(['Z', 'X']) for _ in range(num_bits)]
    sifted = []
    for bit, bs, br in zip(bits, bases_sender, bases_receiver):
        if bs == br:
            sifted.append(bit)
    # Devolver una clave de longitud deseada (aproximadamente la mitad de los bits)
    return sifted[: num_bits // 2]


def simulate_diffie_hellman():
    # Usar un primo grande predefinido para Diffie-Hellman (DH: protocolo de intercambio de claves seguro, usando prime secp256k1)
    p = 0xFFFFFFFEFFFFFC2F
    g = 2
    a = secrets.randbelow(p - 2) + 1
    b = secrets.randbelow(p - 2) + 1
    A = pow(g, a, p)
    B = pow(g, b, p)
    shared1 = pow(B, a, p)
    shared2 = pow(A, b, p)
    if shared1 != shared2:
        raise ValueError("DH key exchange failed")
    return shared1


def derive_final_key(bb84_key, dh_key):
    # Combinar bits de BB84 en bytes
    bb_bytes = bytes(int(''.join(str(bit) for bit in bb84_key[i : i + 8]), 2) for i in range(0, len(bb84_key), 8))
    # Convertir el entero DH a bytes
    dh_bytes = dh_key.to_bytes((dh_key.bit_length() + 7) // 8, 'big')
    # Derivar usando HKDF con SHA3-256
    hkdf = HKDF(
        algorithm=hashes.SHA3_256(),
        length=32,
        salt=None,
        info=b'hybrid key derivation',
    )
    return hkdf.derive(bb_bytes + dh_bytes)


def hybrid_encrypt(plaintext: str) -> dict:
    # Normalizar la entrada: admite numéricos, alfanuméricos y símbolos; convertir a cadena en minúsculas
    if not isinstance(plaintext, (bytes, bytearray)):
        plaintext = str(plaintext).lower()
    """
    Realiza cifrado híbrido:
    - Simular QKD BB84
    - Intercambio de claves Diffie-Hellman
    - Derivar clave final vía HKDF-SHA3
    - Cifrar usando AES-GCM
    Devuelve un dict con iv, ciphertext y key (cadenas hexadecimales).
    """
    bb84 = simulate_bb84_key()
    dh_key = simulate_diffie_hellman()
    final_key = derive_final_key(bb84, dh_key)
    # Cifrado AES-GCM
    aesgcm = AESGCM(final_key)
    iv = secrets.token_bytes(12)
    ct = aesgcm.encrypt(iv, plaintext.encode(), None)
    return {'iv': iv.hex(), 'ciphertext': ct.hex(), 'key': final_key.hex()}


def hybrid_decrypt(iv_hex: str, ciphertext_hex: str, key_hex: str) -> str:
    """
    Descifrar un mensaje cifrado con hybrid_encrypt.
    Requiere iv, ciphertext y key como cadenas hexadecimales.
    """
    iv = bytes.fromhex(iv_hex)
    ct = bytes.fromhex(ciphertext_hex)
    key = bytes.fromhex(key_hex)
    aesgcm = AESGCM(key)
    pt = aesgcm.decrypt(iv, ct, None)
    return pt.decode()