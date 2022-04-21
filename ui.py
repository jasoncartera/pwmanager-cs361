from cgitb import text
from tkinter import Toplevel, ttk, Tk, StringVar, messagebox
from tkinter import *
from manager import PasswordManager
import pyperclip
from functools import partial

class PasswordUI():

    def __init__(self):
        """
        Sets up the UI instance variables
        """
        self.root = Tk()
        self.root.title("Password Manager")
        self.root.geometry('575x575') 
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()
        self.manager = PasswordManager()
        self.service = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.search_var = StringVar()
        self.decrypt_key = StringVar()
        self.encrypt_key = StringVar()

    def main_page(self):
        """
        Creates the main page where the user can interact with the program
        """
        ttk.Label(self.frm, text="Welcome to the password manager!").grid(column=1, row=0, pady=(0,20))

        ttk.Label(self.frm, text="Enter Decryption Key:").grid(column=0, row=1, pady=(0,20))
        ttk.Entry(self.frm, textvariable=self.decrypt_key).grid(column=1, row=1, pady=(0,20))
        ttk.Button(self.frm, text="Decrypt passwords", command=self.decrypt).grid(column=2, row=1, pady=(0,20))


        ttk.Label(self.frm, text="Password search by service").grid(column=0, row=4, pady=(0,20))
        ttk.Entry(self.frm, textvariable=self.search_var).grid(column=1, row=4, pady=(0,20))
        ttk.Button(self.frm, text="Search", command=self.search_pw).grid(column=2, row=4, pady=(0,20))

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
        ttk.Button(self.frm, text="Encrypt passwords", command=self.encrypt).grid(column=2, row=10, pady=(0,20))
        ttk.Label(self.frm, text="Don't forget your encryption key!").grid(column=1, row=11, pady=(0,20))

        ttk.Button(self.frm, text="Quit", command=self.on_closing).grid(column=1, row=12)
    

    def decrypt(self):
        """
        Decrypts the password file when a user enters the correct key
        """
        try:
            key = self.decrypt_key.get().encode()
            self.manager.decrypt(key)
            self.decrypt_key.set('')
            self.manager.set_is_encrypted(False)
        except Exception as e:
            print(e)
            self.invalid_key()

    def encrypt(self):
        key = self.encrypt_key.get().encode()
        self.manager.encrypt(key)
        self.manager.set_is_encrypted(True)

    def add_pw(self):
        if self.manager.get_is_encrypted():
            self.encrypted_warning()
        else:
            service = self.service.get()
            username = self.username.get()
            password = self.password.get()
            if service == '' or username == '' or password == '':
                self.warning("You must enter all of the fields")
            else:
                self.manager.add_password(service, username, password)


    def search_pw(self):
        if self.manager.get_is_encrypted():
            self.encrypted_warning()
        else:
            try:
                service = self.search_var.get()
                data = self.manager.search_password(service)
                PopUpWindow(self.root, data)
            except Exception as e:
                self.warning(repr(e))

    def invalid_key(self):
        messagebox.showwarning("Invalid token", "Decryption key invalid")

    def encrypted_warning(self):
        messagebox.showwarning("Passwords Encrypted", "You must decrypt the passwords first!")

    def warning(self, error):
        messagebox.showwarning("Warning", error)

    def on_closing(self):
        if self.manager.get_is_encrypted():
            self.root.destroy()
        else:
            response = messagebox.askokcancel("Quit", "Passwords are not encrypted are you sure you want to quit?")
            if response:
                self.root.destroy()

    def run(self):
        self.main_page()
        self.root.mainloop()

class PopUpWindow():

    def __init__(self, parent, data):
        self.window = Toplevel(parent)
        self.window.geometry("320x320")
        self.window.title = "Requested password"
        self.accounts = data['accounts']

        i = 0
        while i < len(self.accounts):
            ttk.Label(self.window, text="Username: ").place(x=10, y=10+(60*i))
            ttk.Label(self.window, text=self.accounts[i]['username']).place(x=75, y=10+(60*i))
            ttk.Label(self.window, text="Password: ").place(x=10, y=30+(60*i))
            ttk.Label(self.window, text=self.accounts[i]['pw']).place(x=75, y=30+(60*i))
            ttk.Button(self.window, text="Copy password", command=partial(self.copy, self.accounts[i]['pw'])).place(x=175, y=15+(60*i))
            i += 1

        ttk.Button(self.window, text="Close", command=self.window.destroy).place(relx=0.5, rely=0.8, anchor=CENTER)

    def copy(self, data):
        pyperclip.copy(data)

if __name__ == '__main__':
    ui = PasswordUI()
    ui.run()