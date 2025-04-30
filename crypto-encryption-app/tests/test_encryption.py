import unittest
class TestEncryption(unittest.TestCase):

    def test_caesar_encryption(self):
        from src.algorithms.caesar import caesar_encrypt, caesar_decrypt
        message = "HELLO"
        key = 3
        encrypted = caesar_encrypt(message, key)
        decrypted = caesar_decrypt(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_aes_encryption(self):
        from src.algorithms.aes import aes_encrypt, aes_decrypt
        message = "HELLO"
        key = b'Sixteen byte key'  # AES requires a 16-byte key
        encrypted = aes_encrypt(message.encode(), key)
        decrypted = aes_decrypt(encrypted, key)
        self.assertEqual(decrypted.decode(), message)

    def test_rsa_encryption(self):
        from src.algorithms.rsa import rsa_generate_keys, rsa_encrypt, rsa_decrypt
        message = "HELLO"
        public_key, private_key = rsa_generate_keys()
        encrypted = rsa_encrypt(message, public_key)
        decrypted = rsa_decrypt(encrypted, private_key)
        self.assertEqual(decrypted, message)

class TestAlgorithmRoundtripAndRandomness(unittest.TestCase):
    def setUp(self):
        self.message = "HelloWorld"

    def test_caesar_nondeterministic(self):
        from src.encryption import encrypt_message
        from src.decryption import decrypt_message
        key = 3
        c1 = encrypt_message('caesar', self.message, key)
        c2 = encrypt_message('caesar', self.message, key)
        # Cada cifrado debe variar
        self.assertNotEqual(c1, c2)
        # Validar que ambos descifran correctamente
        p1 = decrypt_message(c1, key, 'caesar')
        self.assertEqual(p1, self.message)
        p2 = decrypt_message(c2, key, 'caesar')
        self.assertEqual(p2, self.message)

    def test_aes_nondeterministic(self):
        from src.algorithms.aes import generate_key, aes_encrypt, aes_decrypt
        key = generate_key()
        c1 = aes_encrypt(self.message, key)
        p1 = aes_decrypt(c1, key).decode()
        self.assertEqual(p1, self.message)
        c2 = aes_encrypt(self.message, key)
        self.assertNotEqual(c1, c2)

    def test_rsa_nondeterministic(self):
        from src.algorithms.rsa import rsa_generate_keys, rsa_encrypt, rsa_decrypt
        public_key, private_key = rsa_generate_keys()
        c1 = rsa_encrypt(self.message, public_key)
        p1 = rsa_decrypt(c1, private_key)
        self.assertEqual(p1, self.message)
        c2 = rsa_encrypt(self.message, public_key)
        self.assertNotEqual(c1, c2)

    def test_hybrid_nondeterministic(self):
        from src.algorithms.hybrid import hybrid_encrypt, hybrid_decrypt
        data1 = hybrid_encrypt(self.message)
        p1 = hybrid_decrypt(data1['iv'], data1['ciphertext'], data1['key'])
        self.assertEqual(p1, self.message)
        data2 = hybrid_encrypt(self.message)
        # Either IV or ciphertext should differ
        self.assertTrue(data1['iv'] != data2['iv'] or data1['ciphertext'] != data2['ciphertext'])

if __name__ == '__main__':
    unittest.main()