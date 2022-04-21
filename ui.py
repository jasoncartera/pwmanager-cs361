from cgitb import text
from tkinter import Toplevel, ttk, Tk, StringVar, messagebox

from manager import PasswordManager

class PasswordUI():

    def __init__(self):
        """
        Sets up the UI instance variables
        """
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
        """
        Creates the main page where the user can interact with the program
        """
        ttk.Label(self.frm, text="Welcome to the password manager!").grid(column=1, row=0, pady=(0,20))

        ttk.Label(self.frm, text="Enter Decryption Key:").grid(column=0, row=1, pady=(0,20))
        ttk.Entry(self.frm, textvariable=self.decrypt_key).grid(column=1, row=1, pady=(0,20))
        ttk.Button(self.frm, text="Decrypt passwords", command=self.decrypt).grid(column=2, row=1, pady=(0,20))


        ttk.Label(self.frm, text="Search for password").grid(column=0, row=4, pady=(0,20))
        ttk.Entry(self.frm).grid(column=1, row=4, pady=(0,20))
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

        ttk.Button(self.frm, text="Quit", command=self.root.destroy).grid(column=1, row=12)
    

    def decrypt(self):
        """
        Decrypts the password file when a user enters the correct key
        """
        try:
            key = self.decrypt_key.get().encode()
            self.manager.validate_password(key)
            self.manager.set_encrypted(False)
            self.decrypt_key = ''
        except:
            self.invalid_key()
            #self.pop_up()

    def encrypt(self):
        key = self.encrypt_key.get().encode()
        self.manager.encrypt(key)
        self.manager.set_encrypted(True)

    def add_pw(self):
        service = self.service.get()
        username = self.username.get()
        password = self.password.get()
        self.manager.add_password(service, username, password)

    def search_pw(self):
        PopupWindow(self.root)

    def invalid_key(self):
        messagebox.showwarning("Invalid token", "Decryption key invalid")

    def run(self):
        self.main_page()
        self.root.mainloop()

class PopupWindow():

    def __init__(self, parent):
        window = Toplevel(parent)
        window.geometry("200x200")
        window.title = "Requested password"
        message = ttk.Label(window, text="Hello World!")
        button = ttk.Button(window, text="Close", command=window.destroy)

        

if __name__ == '__main__':
    ui = PasswordUI()
    ui.run()