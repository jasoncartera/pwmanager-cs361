from tkinter import Toplevel, ttk, Tk, StringVar, messagebox
from tkinter import *
from manager import PasswordManager
import pyperclip
from functools import partial
import requests

class PasswordUI():

    def __init__(self):
        """
        Sets up the UI instance variables
        """
        self.root = Tk()
        self.root.title("Password Manager")
        self.root.geometry('700x700') 
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
        self.pw_len = IntVar()
        self.pw_len.set(10)

    def main_page(self):
        """
        Creates the main page where the user can interact with the program
        """
        ttk.Label(self.frm, text="Welcome to the password manager!").grid(column=1, row=0, pady=(0,20))

        ttk.Label(self.frm, text="Enter Decryption Key:").grid(column=0, row=1, pady=(0,20))
        ttk.Entry(self.frm, textvariable=self.decrypt_key).grid(column=1, row=1, pady=(0,20))
        ttk.Button(self.frm, text="Decrypt passwords", command=self.decrypt).grid(column=2, row=1, pady=(0,20))


        ttk.Label(self.frm, text="Password search by service").grid(column=0, row=4, pady=(0,10))
        ttk.Entry(self.frm, textvariable=self.search_var).grid(column=1, row=4, pady=(0,10))
        ttk.Button(self.frm, text="Search", command=self.search_pw).grid(column=2, row=4, pady=(0,10))
        ttk.Button(self.frm, text="List all services", command=self.list_services).grid(column=1, row=5, pady=(0,20))

        ttk.Label(self.frm, text="Add a new password").grid(column=1, row=6)
        ttk.Label(self.frm, text="Service").grid(column=0, row=7)
        ttk.Label(self.frm, text="Username/Email").grid(column=0, row=8)
        ttk.Label(self.frm, text="Password").grid(column=0, row=9)
        ttk.Entry(self.frm, textvariable=self.service).grid(column=1, row=7)
        ttk.Entry(self.frm, textvariable=self.username).grid(column=1, row=8)
        ttk.Entry(self.frm, textvariable=self.password).grid(column=1, row=9)
        ttk.Button(self.frm, text="Generate Password", command=self.generate_pw).grid(column=2, row=9)
        ttk.Spinbox(self.frm, from_=10, to=64, wrap=True, width=2, textvariable=self.pw_len).grid(column=3, row=9)
        ttk.Button(self.frm, text="Add password", command=self.add_pw).grid(column=1, row=10, pady=(0,20))

        ttk.Label(self.frm, text="Enter Encryption Key:").grid(column=0, row=11, pady=(0,20))
        ttk.Entry(self.frm, textvariable=self.encrypt_key).grid(column=1, row=11, pady=(0,20))
        ttk.Button(self.frm, text="Encrypt passwords", command=self.encrypt).grid(column=2, row=11, pady=(0,20))
        ttk.Label(self.frm, text="Don't forget your encryption key!").grid(column=1, row=12, pady=(0,20))

        ttk.Button(self.frm, text="Quit", command=self.on_closing).grid(column=1, row=13)
    

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
        """
        Encrypts the password file with a given key
        """
        key = self.encrypt_key.get().encode()
        self.manager.encrypt(key)
        self.manager.set_is_encrypted(True)

    def add_pw(self):
        """
        Adds a password to the decrypted password file
        """
        if self.manager.get_is_encrypted():
            self.encrypted_warning()
        else:
            service = self.service.get()
            username = self.username.get()
            password = self.password.get()
            if service == '' or username == '' or password == '':
                self.warning("You must enter all of the fields")
            else:
                confirm = self.confirm_pw((service, username, password))
                if confirm:
                    self.manager.add_password(service, username, password)
                    self.password.set('')
                    self.service.set('')
                    self.username.set('')


    def search_pw(self):
        """
        Searches for passwords in the password file by service
        """
        if self.manager.get_is_encrypted():
            self.encrypted_warning()
        else:
            try:
                service = self.search_var.get()
                data = self.manager.search_password(service)
                PasswordSearchPopUp(self.root, data, service, self.manager)
            except Exception as e:
                self.warning(repr(e))

    def generate_pw(self):
        """
        Requests my teammates microservice from https://pw-gen-cs361.herokuapp.com/ 
        and returns a randomly generated password of a given length

        retuns: string
        """
        length = self.pw_len.get()
        pw_url = f"https://pw-gen-cs361.herokuapp.com/{length}"
        pw = requests.get(pw_url).json()
        self.password.set(pw['pw'])

    def list_services(self):
        """
        Generates a popup that lists all avalaible services with a password
        """
        if self.manager.get_is_encrypted():
            self.encrypted_warning()
        else:
            self.manager.set_passwords()
            data = self.manager.get_passwords()
            ServiceListPopUp(self.root, data)

    def invalid_key(self):
        messagebox.showwarning("Invalid token", "Decryption key invalid")

    def encrypted_warning(self):
        messagebox.showwarning("Passwords Encrypted", "You must decrypt the passwords first!")

    def warning(self, error):
        messagebox.showwarning("Warning", error)

    def confirm_pw(self, data):
        if self.manager.get_is_encrypted():
            self.root.destroy()
        else:
            response = messagebox.askokcancel("Confirm Password", f"\nConfirm Service: {data[0]}\n Username: {data[1]}\n Password: {data[2]}")
            if response:
                return response

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

class ServiceListPopUp():

    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        self.window = Toplevel(self.parent)
        self.window.geometry("450x450")

        i = 1
        for key in self.data.keys():
            ttk.Label(self.window, text=key+": ").grid(row=i, column=1)
            j = 2
            for account in self.data[key]['accounts']:
                ttk.Label(self.window, text=account['username']).grid(row=i, column=j)
                j += 1
            i += 1

class PasswordSearchPopUp():

    def __init__(self, parent, data, service, manager):
        self.parent = parent
        self.window = Toplevel(self.parent)
        self.window.geometry("450x450")
        self.data = data
        self.accounts = self.data['accounts']
        self.service = service
        self.manager = manager

        i = 0
        while i < len(self.accounts):
            ttk.Label(self.window, text="Username: ").place(x=10, y=10+(75*i))
            ttk.Label(self.window, text=self.accounts[i]['username']).place(x=80, y=10+(75*i))
            ttk.Label(self.window, text="Password: ").place(x=10, y=30+(75*i))
            ttk.Label(self.window, text=self.accounts[i]['pw']).place(x=80, y=30+(75*i))
            ttk.Button(self.window, text="Copy password", command=partial(self.copy, self.accounts[i]['pw'])).place(x=10, y=50+(75*i))
            ttk.Button(self.window, text="Delete password", command=partial(self.delete, service, self.accounts[i]['username'])).place(x=150, y=50+(75*i))
            i += 1

        ttk.Button(self.window, text="Close", command=self.window.destroy).place(relx=0.5, rely=0.8, anchor=CENTER)

    def copy(self, data):
        pyperclip.copy(data)

    def delete(self, service, username):
        self.data = self.manager.delete_password(service, username)
        if self.data:
            self.refresh()
        else:
            self.window.destroy()

    def refresh(self):
        self.window.destroy()
        self.__init__(self.parent, self.data, self.service, self.manager)

if __name__ == '__main__':
    ui = PasswordUI()
    ui.run()