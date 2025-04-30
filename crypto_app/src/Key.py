import os
import json
from .algorithms.rsa import rsa_generate_keys

KEYS_FILE = os.path.join(os.path.dirname(__file__), 'default_keys.json')

def load_default_keys():
    if (os.path.exists(KEYS_FILE)):
        with open(KEYS_FILE, 'r') as f:
            return json.load(f)
    else:
        defaults = {'caesar': 3, 'aes': '00112233445566778899aabbccddeeff'}
        with open(KEYS_FILE, 'w') as f:
            json.dump(defaults, f, indent=4)
        return defaults

default_keys = load_default_keys()

# Almacenar par de claves RSA en memoria para que cifrado/descifrado use las mismas claves
rsa_cached_keys = None

def get_default_key(algorithm):
    alg = algorithm.lower()
    if alg == 'caesar':
        return default_keys.get('caesar')
    elif alg == 'aes':
        return bytes.fromhex(default_keys.get('aes', ''))
    elif alg == 'rsa':
        # Generate or reuse one RSA key pair per session
        global rsa_cached_keys
        if rsa_cached_keys is None:
            rsa_cached_keys = rsa_generate_keys()
        return rsa_cached_keys
    else:
        return None

def format_key(algorithm, key):
    alg = algorithm.lower()
    if alg == 'caesar':
        return str(key)
    elif alg == 'aes':
        return key.hex()
    elif alg == 'rsa':
        return '<RSA key pair generated>'
    else:
        return ''