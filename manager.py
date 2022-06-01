from encrypt import Encryption
import os
from rich.console import Console
import sys
import json 

console = Console(width=100)

class PasswordManager:
    """
    Password manager manages the encryption, decryption, and user interactions to manager password 
    in an encrypted file.

    """
    def __init__(self):
        """
        Initializes the PasswordManager

        Attributes:
            __dir: current working directory
            __filename: filename of encrypted passwords
            __encryption: encryption class for the session - handles all encryption
            __passwords: passwords extracted after decryption
        """
        self.__dir = dir_path = os.path.dirname(os.path.realpath(__file__))
        self.__filename = "pw.json"
        self.__encryption = Encryption(self.__filename)
        self.__passwords = None
        self.__is_encrypted = None
        self.set_is_encrypted()
    
    def set_is_encrypted(self, bool=None):
        """
        Sets the status of encryption to True or False
        """
        if bool == None:
            files = os.listdir()
            if 'salt.txt' in files:
                self.__is_encrypted = True
            else:
                self.__is_encrypted = False
        else:
            self.__is_encrypted = bool

    def get_is_encrypted(self):
        """
        Returns status of encryption: boolean
        """
        return self.__is_encrypted

    def decrypt(self, key):
        """
        Decrypts the password file
        """
        self.__encryption.decrypt(key)

    def encrypt(self, key):
        """
        Encrypts the password file
        """
        self.__encryption.encrypt(key)
        self.__passwords = None

    def get_passwords(self):
        """
        Returns the dictionary representation of all passwords in the file
        """
        return self.__passwords

    def set_passwords(self):
        """
        Extracts decrypted passwords from a json file and loads them into the __passwords property.
        Requires that the file exists and is already decrypted
        """
        files = os.listdir()
        if self.__filename in files:
            with open("pw.json", "rb") as file:
                passwords = json.load(file)
        
            self.__passwords = passwords
        else:
            self.__passwords = dict()

        return self.__passwords

    def add_password(self, service, username, password):
        """
        Adds a password to the decrypted password file.
        """
        self.set_passwords()
        pws = self.get_passwords()
        if pws and pws.get(service):
            pws[service]['accounts'].append({'username': username, 'pw': password})
        else:
            pws[service] = {'accounts': [{'username': username, 'pw': password}]}

        with open(self.__filename, "w") as file:
            json.dump(pws, file, ensure_ascii=False, indent=4)

    def delete_password(self, service, username):
        """
        Deletes a password from the password file
        """
        self.set_passwords()
        pws = self.get_passwords()
        if len(pws[service]['accounts']) == 1:
            del pws[service]
        else:
            for account in pws[service]['accounts']:
                if account['username'] == username:
                    pws[service]['accounts'].remove(account)

        with open(self.__filename, "w") as file:
            json.dump(pws, file, ensure_ascii=False, indent=4)

        if pws.get(service):
            return pws[service]
        else:
            return

    def search_password(self, service):
        """
        Searchs for a given password in the decrypted password file
        """
        files = os.listdir()
        self.set_passwords()
        if self.__filename in files:
            result = self.get_passwords()[service]
        return result
        
    def exit(self, key):
        self.__passwords = None
        self.encrypt(key)
        sys.exit()
