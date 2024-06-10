# -*- coding: utf-8 -*-
# Copyright (C) 2024 Odoo Turkey Community (https://github.com/orgs/Odoo-Turkey-Community/dashboard)
# License Other proprietary. Please see the license file in the Addon folder.

import binascii

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES, PKCS1_v1_5
from Crypto.Random import get_random_bytes

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend


class HybridEncryptor:
    def __init__(self, x509_cert):
        x509_cert = x509.load_pem_x509_certificate(x509_cert, default_backend())

        self.x509_cert = x509_cert
        self.rsa_key = RSA.import_key(x509_cert.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))
        self.rsa_cipher = PKCS1_v1_5.new(self.rsa_key)

    def encrypt(self, message):
        """Encrypt a large message using hybrid encryption."""
        # Generate a random AES key
        aes_key = get_random_bytes(16)  # AES-128
        aes_cipher = AES.new(aes_key, AES.MODE_EAX)

        # Encrypt the message with AES
        ciphertext, tag = aes_cipher.encrypt_and_digest(message)

        # Encrypt the AES key with RSA
        encrypted_aes_key = self.rsa_cipher.encrypt(aes_key)

        # Combine the encrypted AES key, nonce, tag, and ciphertext
        combined_encrypted_message = encrypted_aes_key + aes_cipher.nonce + tag + ciphertext

        return combined_encrypted_message

    def decrypt(self, private_key, combined_encrypted_message):
        """Decrypt a message encrypted using hybrid encryption."""
        # Extract the encrypted AES key, nonce, tag, and ciphertext

        encrypted_aes_key_size = private_key.size_in_bytes()
        encrypted_aes_key = combined_encrypted_message[:encrypted_aes_key_size]
        nonce = combined_encrypted_message[encrypted_aes_key_size:encrypted_aes_key_size + 16]
        tag = combined_encrypted_message[encrypted_aes_key_size + 16:encrypted_aes_key_size + 32]
        ciphertext = combined_encrypted_message[encrypted_aes_key_size + 32:]

        # Decrypt the AES key with RSA
        rsa_cipher = PKCS1_v1_5.new(private_key)
        aes_key = rsa_cipher.decrypt(encrypted_aes_key, None)

        # Decrypt the message with AES
        aes_cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
        message = aes_cipher.decrypt_and_verify(ciphertext, tag)

        return message


class CryptEncrypteMessage:
    def __init__(self, priv, pub, password=None) -> None:
        self.public = RSA.import_key(binascii.unhexlify(pub))
        private_key_pem = binascii.unhexlify(priv)

        if password:
            private_key = load_pem_private_key(private_key_pem, password=password.encode('utf-8'), backend=default_backend())
            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        self.private = RSA.import_key(private_key_pem)

        self.encryptor = HybridEncryptor(binascii.unhexlify(pub))

    def encrypte(self, data) -> bytes:
        cipher = PKCS1_OAEP.new(self.public)
        ciphertext = cipher.encrypt(data.encode('utf-8'))
        return binascii.hexlify(ciphertext)

    def decrypte(self, data) -> bytes:
        cipher = PKCS1_OAEP.new(self.private)
        return cipher.decrypt(binascii.unhexlify(data))

    def long_encrypte(self, data) -> bytes:
        ciphertext = self.encryptor.encrypt(data.encode('utf-8'))
        return binascii.hexlify(ciphertext)

    def long_decrypte(self, data) -> bytes:
        return self.encryptor.decrypt(self.private, binascii.unhexlify(data))
