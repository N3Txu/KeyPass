from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Optional
from encryption import encrypt_message
from decryption import decrypt_message

app = FastAPI()

class EncryptRequest(BaseModel):
    message: str
    algorithm: str
    key: Optional[str] = None

class EncryptResponse(BaseModel):
    encrypted_message: str

class DecryptRequest(BaseModel):
    encrypted_message: str
    algorithm: str
    key: Optional[str] = None

class DecryptResponse(BaseModel):
    decrypted_message: str

@app.post('/encrypt', response_model=EncryptResponse)
def encrypt(req: EncryptRequest) -> EncryptResponse:
    message = req.message
    algorithm = req.algorithm
    key = req.key
    # Convierte la clave AES de hexadecimal si se proporciona como cadena
    if algorithm.lower() == 'aes' and key is not None:
        key = bytes.fromhex(key)
    try:
        encrypted_message = encrypt_message(algorithm, message, key)
        if isinstance(encrypted_message, (bytes, bytearray)):
            encrypted_message = encrypted_message.hex()
        return EncryptResponse(encrypted_message=encrypted_message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/decrypt', response_model=DecryptResponse)
def decrypt(req: DecryptRequest) -> DecryptResponse:
    encrypted_message = req.encrypted_message
    algorithm = req.algorithm
    key = req.key
    # Convierte la clave AES y el texto cifrado de hexadecimal
    if algorithm.lower() == 'aes' and key is not None:
        key = bytes.fromhex(key)
        encrypted_message = bytes.fromhex(encrypted_message)
    elif algorithm.lower() == 'rsa':
        encrypted_message = bytes.fromhex(encrypted_message)
    try:
        decrypted_message = decrypt_message(encrypted_message, key, algorithm)
        if isinstance(decrypted_message, (bytes, bytearray)):
            decrypted_message = decrypted_message.decode()
        return DecryptResponse(decrypted_message=decrypted_message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    uvicorn.run("API:app", host="0.0.0.0", port=5000, reload=True)