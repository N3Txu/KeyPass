from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def generate_key():
    return os.urandom(16)  # Tamaño de clave AES: 16 bytes (128 bits)

def aes_encrypt(data, key):
    # Normalizar entrada: soporta numérico, alfanumérico, símbolos; convertir a cadena en minúsculas si no es bytes
    if not isinstance(data, (bytes, bytearray)):
        data = str(data).lower()
    if isinstance(data, str):
        data_bytes = data.encode()
    else:
        data_bytes = data
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted = cipher.encrypt(pad(data_bytes, AES.block_size))
    return iv + encrypted  # Prepend IV para uso en descifrado

def aes_decrypt(cipher_text, key):
    iv = cipher_text[:16]  # Extraer IV del comienzo
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = unpad(cipher.decrypt(cipher_text[16:]), AES.block_size)
    return decrypted_bytes  # Devolver bytes sin formato para decodificación por el llamador
