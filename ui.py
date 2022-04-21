from cgitb import text
from tkinter import *
from tkinter import ttk
from manager import PasswordManager

class PasswordUI():

    def __init__(self):
        self.root = Tk()
        self.root.title("Password Manager")
        self.root.geometry('550x550') 
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()
        self.manager = PasswordManager()
        self.service = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.search = StringVar()
        self.decrypt_key = StringVar()
        self.encrypt_key = StringVar()

    def main_page(self):
        ttk.Label(self.frm, text="Welcome to the password manager!").grid(column=1, row=0, pady=(0,20))

        ttk.Label(self.frm, text="Enter Decryption Key:").grid(column=0, row=1, pady=(0,20))
        ttk.Entry(self.frm, textvariable=self.decrypt_key).grid(column=1, row=1, pady=(0,20))
        ttk.Button(self.frm, text="Decrypt passwords", command=self.decrypt).grid(column=2, row=1, pady=(0,20))


        ttk.Label(self.frm, text="Search for password").grid(column=0, row=4, pady=(0,20))
        ttk.Entry(self.frm).grid(column=1, row=4, pady=(0,20))
        ttk.Button(self.frm, text="Submit").grid(column=2, row=4, pady=(0,20))

        ttk.Label(self.frm, text="Add a new password").grid(column=1, row=5)
        ttk.Label(self.frm, text="Service").grid(column=0, row=6)
        ttk.Label(self.frm, text="Username/Email").grid(column=0, row=7)
        ttk.Label(self.frm, text="Password").grid(column=0, row=8)
        ttk.Entry(self.frm, textvariable=self.service).grid(column=1, row=6)
        ttk.Entry(self.frm, textvariable=self.username).grid(column=1, row=7)
        ttk.Entry(self.frm, textvariable=self.password).grid(column=1, row=8)

        ttk.Button(self.frm, text="Add password", command=self.add_pw).grid(column=1, row=9, pady=(0,20))

        ttk.Label(self.frm, text="Enter Encryption Key:").grid(column=0, row=10, pady=(0,20))
        ttk.Entry(self.frm, textvariable=self.encrypt_key).grid(column=1, row=10, pady=(0,20))
        ttk.Button(self.frm, text="Encrypt passwords").grid(column=2, row=10, pady=(0,20))
        ttk.Label(self.frm, text="Don't forget your encryption key!").grid(column=1, row=11, pady=(0,20))

        ttk.Button(self.frm, text="Quit", command=self.root.destroy).grid(column=1, row=12)
    

    def decrypt(self):
        key = self.decrypt_key.get()
        self.manager.validate_password(key)

    def add_pw(self):
        key = self.service.get()

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