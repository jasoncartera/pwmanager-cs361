import cryptography
from encrypt import Encryption
import os
from rich.console import Console
import time
import traceback
import logging
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
        self.encrypted = True

    def decrypt(self, key):
        self.__encryption.decrypt(key)

    def encrypt(self, key):
        self.__encryption.encrypt(key)


    def get_passwords(self):
        return self.__passwords

    def is_encrypted(self):
        return self.encrypted

    def set_encrypted(self, bool):
        self.encrypted = bool

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
        self.set_passwords()
        pws = self.get_passwords()
        if pws and pws.get(service):
            pws[service]['accounts'].append({'username': username, 'pw': password})
        else:
            pws[service] = {'accounts': [{'username': username, 'pw': password}]}

        with open(self.__filename, "w") as file:
            json.dump(pws, file, ensure_ascii=False, indent=4)

    def search_password(self):
        files = os.listdir()
        if self.__filename not in files:
            print("You haven't saved any passwords yet!")
            print("1. Enter a new password")
            print("2. Exit program")
            selection = input("Select an option by entering the number: ")

            if selection == "1":
                self.add_password()
            elif selection == "2":
                self.exit()
            else:
                print("Invalid selection..returning to home.")
                time.sleep(1)
                self.main_page()
        else:
            if self.is_encrypted:
                self.validate_password(self.search_password)
            service_search = input("Enter the service (gmail, amazon, ect..): ")
            service = self.get_passwords()[service_search]
            print(f"Accounts avalaible for {service_search}: ")
            for i in range(len(service['accounts'])):
                print(f"Account {i}: ")
                print(f"Account email: {service['accounts'][i]['email']}")
                print(f"Account password: {service['accounts'][i]['pw']}")
                print()
            user_in = input("1) Enter new password, 2) Search new, 3) Return to main: ")
            if user_in == "1":
                self.add_password()
            elif user_in == "2":
                self.search_password()
            elif user_in == "3":
                self.main_page()

    def validate_password(self, key):
        self.decrypt(key)
        self.is_encrypted = False
        self.set_passwords()

        
    def exit(self):
        key = input("Enter an encryption key: ").encode()
        print("Encrypting passwords...")
        self.__passwords = None
        self.encrypt(key)
        print("Encryption complete. Goodbye")
        sys.exit()

    def main_page(self):
        try:
            os.system('cls||clear')

            console.print(
                    "\nThis program manages passwords in an encrypted json file. ", \
                    "If you've saved a password before, you will need to enter a decryption key. ", \
                    "Select an option below to get started.\n", sep='', justify="center"
                )

            print("1. Search for an account")
            print("2. Enter a new password")
            print("3. Exit program")
            print()
            selection = input("Please select an option by entering the number: ")

            if selection == "1":
                self.search_password()
            elif selection == "2":
                self.add_password()
            elif selection == "3":
                self.exit()
            else:
                print("Invalid selection, try again")
                time.sleep(1)
                self.main_page()

        except Exception as e:
            logging.error(traceback.format_exc())

if __name__ == "__main__":

    manager = PasswordManager()
    manager.main_page()





