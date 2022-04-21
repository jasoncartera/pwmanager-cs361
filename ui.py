from tkinter import *
from tkinter import ttk
import json 
from cryptography.fernet import InvalidToken

class PasswordUI():

    def __init__(self):
        self.root = Tk()
        self.root.title("Password Manager")
        self.root.geometry('600x600') 
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()

    def main_page(self):
        ttk.Label(self.frm, text="Welcome to the password manager!").grid(column=1, row=0)
        ttk.Button(self.frm, text="Decrypt passwords").grid(column=1, row=1)


        ttk.Label(self.frm, text="Search for password").grid(column=0, row=4)
        search_pw = ttk.Entry(self.frm).grid(column=1, row=4)
        submit_add = ttk.Button(self.frm, text="Submit").grid(column=2, row=4)
        ttk.Label(self.frm, text="Add a new password").grid(column=1, row=5)
        ttk.Label(self.frm, text="Service").grid(column=0, row=6)
        ttk.Label(self.frm, text="Username/Email").grid(column=0, row=7)
        ttk.Label(self.frm, text="Password").grid(column=0, row=8)
        service = ttk.Entry(self.frm).grid(column=1, row=6)
        username = ttk.Entry(self.frm).grid(column=1, row=7)
        password = ttk.Entry(self.frm).grid(column=1, row=8)
        ttk.Button(self.frm, text="Encrypt passwords").grid(column=1, row=9)
        ttk.Button(self.frm, text="Quit", command=self.root.destroy).grid(column=1, row=10)

    def add_pw(self):
        add_frm = ttk.Frame(self.root, padding=10)
        add_frm.grid()
        ttk.Label(add_frm, text="Service").grid(column=0, row=0)

    def start_main(self):
        self.main_page()
        self.root.mainloop()

class EncryptionUI():

    def __init__(self):
        self.root = Tk()
        self.root.title("Password Manager")
        self.root.geometry('300x300')
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()

    def decrypt(self):
        ttk.Label(self.frm, text="Entery the decryption key").grid(column=0, row=0)
        ttk.Entry()

if __name__ == '__main__':
    ui = PasswordUI()
    ui.start_main()