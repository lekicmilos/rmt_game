from tkinter import *  
from db import DB

class MainScreen:
    def __init__(self):
        self.dataBase = DB()
        self.logged_user = ''
        self.game_running = False
    
    def run(self):
        # Povezi se sa bazom 
        self.dataBase.connect()
        # Pokreni tkinter
        self.root=Tk()

        self.main_screen('RMT Game')
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.root.mainloop()


    def on_exit(self):
        # Ukoliko korisnik zatvori prozor pre pokretanja igre, ugasi prozor
        if not self.game_running:
            self.root.destroy()

        # Skidanje active flaga za ulogovanog korisnika
        self.dataBase.removeActive(self.logged_user)

        # disconnect od baze
        self.dataBase.disconnect()


    def start_client(self):
        if self.logged_user and not self.game_running:
            self.game_running = True
            
            # Gasenje main prozora
            self.root.destroy()
        


    def main_screen(self, title):
        self.root.title(title)
        self.root.geometry('500x300')

        # Naslov
        lbl1=Label(self.root, text='Welcome to PONG', width=20, font=("Arial", 25))
        lbl1.pack(pady=(0, 20))

        # Play/Status 
        self.btn_play=Button(self.root, text='Log in to play!', width=16, font=("Arial", 18), fg='red', bg='white', 
            command=self.start_client)
        self.btn_play.pack(ipadx =20, ipady=20, pady=(20, 30))
        
        # Login dugme
        btn_login=Button(self.root, text='Log In', height='1', width='15', font='bold', 
            command=self.login_dialog)
        btn_login.pack(ipadx =20, ipady=20, padx=20, pady=20, side=LEFT)

        # Register dugme
        btn_reg=Button(self.root, text='Register', height='1', width='15', font='bold', 
            command=self.register_dialog)
        btn_reg.pack(ipadx =20, ipady=20, padx=20, pady=20, side=RIGHT)

    
    def register_dialog(self):
        register_window = Toplevel(self.root)
        register_window.title('Register New User')
        register_window.geometry('320x280')

        # labele i textboxevi
        fields = {}

        fields['username_label'] = Label(register_window, text='Username:', font=("Arial", 12))
        fields['username'] = Entry(register_window, font=("Arial", 12))

        fields['password_label'] = Label(register_window, text='Password:', font=("Arial", 12))
        fields['password'] = Entry(register_window, show="*", font=("Arial", 12))

        fields['rpassword_label'] = Label(register_window, text='Repeat Password:', font=("Arial", 12))
        fields['rpassword'] = Entry(register_window, show="*", font=("Arial", 12))

        # pozicioniranje
        for field in fields.values():
            field.pack(anchor="w", padx=10, pady=5, fill=X)

        # poruka o uspesnosti
        lbl_msg = Label(register_window, text='', font=("Arial", 12))    

        # dugme koje poziva register_user()
        btn = Button(register_window, text='Register', width=10, font=("Arial", 12), 
            command=lambda: self.register_user(fields['username'].get(), fields['password'].get(), fields['rpassword'].get(), lbl_msg))
        btn.pack(padx=10, pady=5)
        lbl_msg.pack(padx=10, pady=5)

    # callback pri registraciji u register prozoru
    def register_user(self, usr, pas, pas2, lbl_msg):
        # provera da li su user i pass korektno uneti
        if usr=='' or pas=='':
            lbl_msg.config(text='Username or password cannot be empty', fg='red')
        elif pas != pas2:
            lbl_msg.config(text='Passwords not matching!', fg='red')
        else:
            # dodavanje korisnika u bazu ili prikaz greske
            msg = self.dataBase.addNewUser(usr, pas)
            if msg != 'success':
                lbl_msg.config(text=msg, fg='red')            
            else:
                lbl_msg.config(text='Register successful!', fg='green')



    def login_dialog(self):
        login_window = Toplevel(self.root)
        login_window.title('Log In Existing User')
        login_window.geometry('320x220')

        # Labele i textboxevi
        fields = {}

        fields['username_label'] = Label(login_window, text='Username:', font=("Arial", 12))
        fields['username'] = Entry(login_window, font=("Arial", 12))

        fields['password_label'] = Label(login_window, text='Password:', font=("Arial", 12))
        fields['password'] = Entry(login_window, show="*", font=("Arial", 12))

        # pozicioniranje
        for field in fields.values():
            field.pack(anchor="w", padx=10, pady=5, fill=X)

        # Poruka o uspesnosti se daje kao labela
        lbl_msg = Label(login_window, text='', font=("Arial", 12))

        # login dugme koje poziva login_user()
        btn = Button(login_window, text='Log In', width=10, font=("Arial", 12), 
            command=lambda: self.login_user(fields['username'].get(), fields['password'].get(), lbl_msg))
        btn.pack(padx=10, pady=5)
        lbl_msg.pack(padx=10, pady=5)

    # Callback na login korisnika iz login prozora
    def login_user(self, usr, pas, lbl_msg):
        if usr=='' or pas=='':
            lbl_msg.config(text='Username or password cannot be empty', fg='red')
        else:
            msg = self.dataBase.checkIfExist(usr, pas)
            if msg != 'success':
                lbl_msg.config(text=msg, fg='red')
            else:            
                # Ako je login uspesan, skini active trenutnom useru i stavi active novom
                self.dataBase.removeActive(self.logged_user)
                lbl_msg.config(text='Login successful!', fg='green')
                # menja status
                self.logged_user = usr
                self.btn_play.config(text='Play as ' + self.logged_user, fg='green')
                self.dataBase.setActive(usr)