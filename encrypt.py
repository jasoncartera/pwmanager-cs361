from operator import ge
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
import base64
import bcrypt

class Encryption():
    """ 
    Use Bcrypt library for key derivation and Fernet to encrypt the file with the derived key.
    
    """

    def __init__(self, filename):
        """
        Initializes the encryption object for a specific file to be encrypted.

        Attributes:
            filename: string - name of the file to encrypt
            _encrypted: boolean - if the file is encrypted or not 
        """

        self.filename = filename

    def generate_salt(self):
        """
        Generates a random salt to be used in a key derivation function

        Returns: salt value

        """
        salt = bcrypt.gensalt()
        with open ("salt.txt", "wb") as s:
            s.write(salt)
        return salt

    def get_salt(self):
        """
        Gets the derived salt from the last encryption effort saved in the file "salt.key"

        Returns: salt
        """
        with open ("salt.txt", "rb") as salt:
            salt = salt.read()
        return salt


    def create_key(self, pw, salt):
        """
        Creates a key for Fernet encryption using Bcrypt key derivation function
        Source: https://github.com/pyca/bcrypt/
        Returns: key

        """

        key = bcrypt.kdf(
            password=pw,
            salt=salt,
            desired_key_bytes=32,
            rounds=100
        )  
            
        encoded_key = base64.urlsafe_b64encode(key)

        return encoded_key

    def encrypt(self, pw):
        """
        Encryption using Fernet symmetric encryption with the key derived from a user password
        Source: https://cryptography.io/en/3.4.4/fernet.html

        """
        salt = self.generate_salt()
        key = self.create_key(pw, salt)

        fernet = Fernet(key)

        with open(self.filename, 'rb') as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        with open(self.filename, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        
    def decrypt(self, pw):
        """
        Decrypts a file with a user password
        
        """
        salt = self.get_salt()
        key = self.create_key(pw, salt)
        
        fernet = Fernet(key)

        with open(self.filename, 'rb') as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)

        with open(self.filename, 'wb') as dec_file:
            dec_file.write(decrypted)
    