def caesar_encrypt(message, shift):
    # Normalize input: support numbers, alphanumeric, symbols; convert to string and lowercase
    message = str(message).lower()
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            # letters shifted in lowercase
            shift_base = ord('a')
            encrypted_message += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        elif char.isdigit():
            # shift digits modulo 10
            encrypted_message += chr((ord(char) - ord('0') + shift) % 10 + ord('0'))
        else:
            encrypted_message += char
    return encrypted_message

def caesar_decrypt(encrypted_message, shift):
    # reuse encrypt with negative shift; input normalization occurs there
    return caesar_encrypt(encrypted_message, -shift)

def main():
    message = input("Enter the message to encrypt: ")
    shift = int(input("Enter the shift value (1-25): "))
    encrypted = caesar_encrypt(message, shift)
    print(f"Encrypted message: {encrypted}")

    decrypted = caesar_decrypt(encrypted, shift)
    print(f"Decrypted message: {decrypted}")

if __name__ == "__main__":
    main()