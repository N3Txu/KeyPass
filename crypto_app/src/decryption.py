from .algorithms.caesar import caesar_decrypt
from .algorithms.aes import aes_decrypt
from .algorithms.rsa import rsa_decrypt, rsa_generate_keys
from .algorithms.hybrid import hybrid_decrypt


def decrypt_message(encrypted_message, key, algorithm):
    alg = algorithm.lower()
    # Manejar César con desplazamiento embebido
    if alg == "caesar":
        if isinstance(encrypted_message, str) and ':' in encrypted_message:
            shift_str, cipher_text = encrypted_message.split(':', 1)
            shift = int(shift_str)
            return caesar_decrypt(cipher_text, shift)
        else:
            return caesar_decrypt(encrypted_message, key)
    elif alg == "aes":
        validate_key(alg, key)
        return aes_decrypt(encrypted_message, key)
    elif alg == "rsa":
        validate_key(alg, key)
        # La clave es una tupla (pública, privada)
        _, private_key = key
        return rsa_decrypt(encrypted_message, private_key)
    elif alg == 'hybrid':
        # Esperar hex separada por dos puntos: iv:ciphertext:key
        iv_hex, ct_hex, key_hex = encrypted_message.split(':', 2)
        return hybrid_decrypt(iv_hex, ct_hex, key_hex)
    else:
        raise ValueError("Unsupported algorithm selected.")

def validate_key(algorithm, key):
    alg = algorithm.lower()
    if alg == "aes":
        if not isinstance(key, bytes) or len(key) not in [16, 24, 32]:
            raise ValueError("Key for AES must be a byte string of length 16, 24, or 32")
    elif alg == "rsa":
        if not isinstance(key, tuple) or len(key) != 2:
            raise ValueError("Key for RSA must be a tuple of (public_key, private_key)")
    # Caesar y Hybrid no requieren validación externa de la clave aquí
    elif alg not in ("caesar", "hybrid"):
        raise ValueError("Unsupported decryption algorithm")

def main():
    # CLI para probar descifrado
    algorithm = input("Select algorithm (caesar, aes, rsa, hybrid): ")
    encrypted_message = input("Enter message to decrypt: ")
    # Analizar clave según el algoritmo
    if algorithm.lower() == 'caesar':
        key = int(input("Enter integer key: "))
    elif algorithm.lower() == 'aes':
        key = input("Enter key (string): ").encode()
    elif algorithm.lower() == 'rsa':
        public_key, private_key = rsa_generate_keys()
        print("Generated RSA key pair.")
        key = (public_key, private_key)
    else:
        key = None
    # Validar y descifrar
    validate_key(algorithm, key)
    plaintext = decrypt_message(encrypted_message, key, algorithm)
    print("Decrypted output:", plaintext)

if __name__ == "__main__":
    main()