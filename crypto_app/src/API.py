from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from crypto_app.src.encryption import encrypt_message
from crypto_app.src.decryption import decrypt_message
from crypto_app.src.Key import default_keys, get_default_key
import json
import logging

import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EncryptRequest(BaseModel):
    message: str
    algorithm: str

class EncryptResponse(BaseModel):
    encrypted_message: str

class DecryptRequest(BaseModel):
    encrypted_message: str
    algorithm: str
    

class DecryptResponse(BaseModel):
    decrypted_message: str
    
@app.post("/")
async def root():
    return {"message": "Todo OK desde raíz"}

@app.get("/")
async def root_get():
    return {"message": "Todo OK desde raíz GET"}

def is_hexadecimal(s: str) -> bool:
    try:
        bytes.fromhex(s)
        return True
    except ValueError:
        return False

@app.post('/encrypt', response_model=EncryptResponse)
def encrypt(req: EncryptRequest) -> EncryptResponse:
    message = req.message
    algorithm = req.algorithm
    key = get_default_key(algorithm)  # Use get_default_key for RSA and other algorithms

    logging.info(f"Encrypt request received: message={message}, algorithm={algorithm}, key={key}")

    if algorithm.lower() == 'aes' and key is not None:
        if not is_hexadecimal(key):
            logging.error(f"Invalid hexadecimal key: {key}")
            raise HTTPException(status_code=400, detail="Invalid hexadecimal key")
        key = bytes.fromhex(key)

    try:
        encrypted_message = encrypt_message(algorithm, message, key)
        if isinstance(encrypted_message, dict):
            # Concatenate iv, ciphertext, and key into a single string
            encrypted_message = f"{encrypted_message['iv']} {encrypted_message['ciphertext']} {encrypted_message['key']}"
        elif isinstance(encrypted_message, (bytes, bytearray)):
            encrypted_message = encrypted_message.hex()
        logging.info(f"Encryption successful: {encrypted_message}")
        return EncryptResponse(encrypted_message=encrypted_message)
    except Exception as e:
        logging.error(f"Encryption failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/decrypt', response_model=DecryptResponse)
def decrypt(req: DecryptRequest) -> DecryptResponse:
    encrypted_message = req.encrypted_message
    algorithm = req.algorithm
    key = get_default_key(algorithm)  # Use get_default_key for RSA and other algorithms

    logging.info(f"Decrypt request received: encrypted_message={encrypted_message}, algorithm={algorithm}, key={key}")

    if algorithm.lower() == 'hybrid':
        iv = ciphertext = encrypted_key = None
        # Try space-separated format
        parts = encrypted_message.split()
        if len(parts) == 3:
            iv, ciphertext, encrypted_key = parts
        elif encrypted_message.strip().startswith('{'):
            # Try JSON format
            try:
                data = json.loads(encrypted_message)
                iv = data.get('iv')
                ciphertext = data.get('ciphertext')
                encrypted_key = data.get('key')
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON for hybrid encrypted message: {encrypted_message}")
                raise HTTPException(status_code=400, detail="Invalid JSON format for hybrid encrypted message")
            if not all([iv, ciphertext, encrypted_key]):
                logging.error(f"Missing fields in hybrid JSON: {data}")
                raise HTTPException(status_code=400, detail="Hybrid encrypted message JSON must contain iv, ciphertext, and key")
        else:
            logging.error(f"Invalid hybrid encrypted message format: {encrypted_message}")
            raise HTTPException(status_code=400, detail="Hybrid encrypted message must be space-separated or JSON with iv, ciphertext, and key")
        # Decrypt using decrypt_message which expects colon-delimited input
        new_message = f"{iv}:{ciphertext}:{encrypted_key}"
        decrypted_message = decrypt_message(new_message, key, algorithm)
        if isinstance(decrypted_message, (bytes, bytearray)):
            decrypted_message = decrypted_message.decode()
        logging.info(f"Hybrid decryption successful: {decrypted_message}")
        return DecryptResponse(decrypted_message=decrypted_message)

    if algorithm.lower() == 'aes' and key is not None:
        # Validate and decode AES key
        if not is_hexadecimal(key):
            logging.error(f"Invalid hexadecimal key: {key}")
            raise HTTPException(status_code=400, detail="Invalid hexadecimal key")
        key = bytes.fromhex(key)
        # Decode encrypted_message hex to bytes for AES decryption
        if not is_hexadecimal(encrypted_message):
            logging.error(f"Invalid hexadecimal encrypted message: {encrypted_message}")
            raise HTTPException(status_code=400, detail="Invalid hexadecimal encrypted message")
        encrypted_message = bytes.fromhex(encrypted_message)

    elif algorithm.lower() == 'rsa':
        if not is_hexadecimal(encrypted_message):
            logging.error(f"Invalid hexadecimal encrypted message: {encrypted_message}")
            raise HTTPException(status_code=400, detail="Invalid hexadecimal encrypted message")
        encrypted_message = bytes.fromhex(encrypted_message)

    try:
        decrypted_message = decrypt_message(encrypted_message, key, algorithm)
        if isinstance(decrypted_message, (bytes, bytearray)):
            decrypted_message = decrypted_message.decode()
        logging.info(f"Decryption successful: {decrypted_message}")
        return DecryptResponse(decrypted_message=decrypted_message)
    except Exception as e:
        logging.error(f"Decryption failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    uvicorn.run("API:app", host="0.0.0.0", port=5000, reload=True)