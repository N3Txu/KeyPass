from .algorithms.rsa import rsa_encrypt, rsa_generate_keys
from .algorithms.caesar import caesar_encrypt
from .algorithms.aes import aes_encrypt
from .algorithms.hybrid import hybrid_encrypt
import secrets
            
def encrypt_message(algorithm, message, key):
    """
    Cifra un mensaje usando el algoritmo y la llave especificados.
    Algoritmos soportados: 'caesar', 'aes', 'rsa', 'hybrid'.
    Argumentos:
        algorithm (str): nombre del cifrado.
        message (str o bytes): texto plano a cifrar.
        key: llave del cifrado: int para Caesar, bytes para AES, (pub, priv) para RSA, None para híbrido.
    Retorna:
        str: cadena de salida cifrada o campos hexadecimales para híbrido.
    Lanza:
        ValueError: en caso de error de validación o cifrado.
    """
    validate_key(algorithm, key)
    alg = algorithm.lower()
    try:
        if alg == 'caesar':
            # Generar desplazamiento aleatorio entre 1 y 25
            shift = secrets.randbelow(25) + 1
            cipher_text = caesar_encrypt(message, shift)
            # Incluir el desplazamiento en el resultado para descifrado
            return f"{shift}:{cipher_text}"
        elif alg == 'aes':

            # AES-GCM: key validated above
            return aes_encrypt(message, key)
        elif alg == 'rsa':
            # RSA: asymmetric encryption pads internally
            public_key, _ = key
            return rsa_encrypt(message, public_key)
        elif alg == 'hybrid':
            # Hybrid: returns JSON dict with salt, iv, ciphertext
            return hybrid_encrypt(message)
        else:
            raise ValueError(f"Unsupported encryption algorithm: {algorithm}")
    except Exception as e:
        raise ValueError(f"Encryption failed for {algorithm}: {e}")

def validate_key(algorithm, key):
    # Validar clave según el algoritmo (sin distinción de mayúsculas)
    alg = algorithm.lower()
    if alg == 'caesar':
        if not isinstance(key, int):
            raise ValueError("Key for Caesar cipher must be an integer")
    elif alg == 'aes':
        if not isinstance(key, bytes) or len(key) not in [16, 24, 32]:
            raise ValueError("Key for AES must be a byte string of length 16, 24, or 32")
    elif alg == 'rsa':
        if not isinstance(key, tuple) or len(key) != 2:
            raise ValueError("Key for RSA must be a tuple of (public_key, private_key)")
    elif alg == 'hybrid':
        return  # no key needed for Hybrid
    else:
        raise ValueError("Unsupported encryption algorithm")

def main():
    # CLI para probar cifrado
    algorithm = input("Select algorithm (caesar, aes, rsa, hybrid): ")
    message = input("Enter message to encrypt: ")
    # Parse key based on algorithm
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
    # Validate and encrypt
    validate_key(algorithm, key)
    ciphertext = encrypt_message(algorithm, message, key)
    print("Encrypted output:", ciphertext)

if __name__ == "__main__":
    main()