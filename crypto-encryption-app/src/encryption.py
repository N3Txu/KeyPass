def encrypt_message(algorithm, message, key):
    # Normalizar entrada: soporta dígitos, caracteres alfanuméricos y símbolos; convertir a minúsculas e incluir espacios
    message = str(message).lower()
    # Normalizar el algoritmo
    alg = algorithm.lower()
    if alg == 'caesar':
        from algorithms.caesar import caesar_encrypt
        # Desplazamiento aleatorio cada vez si no hay clave predefinida
        from random import randint
        shift = randint(1, 25)
        encrypted = caesar_encrypt(message, shift)
        return f"{shift}:{encrypted}"
    elif alg == 'aes':
        from algorithms.aes import aes_encrypt
        return aes_encrypt(message, key)
    elif alg == 'rsa':
        from algorithms.rsa import rsa_encrypt
        public_key, _ = key
        return rsa_encrypt(message, public_key)
    elif alg == 'hybrid':
        from algorithms.hybrid import hybrid_encrypt
        # Usar cadena hex separada por dos puntos: iv:ciphertext:key
        result = hybrid_encrypt(message)
        return f"{result['iv']}:{result['ciphertext']}:{result['key']}"
    else:
        raise ValueError("Unsupported encryption algorithm")

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
        from algorithms.rsa import rsa_generate_keys
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