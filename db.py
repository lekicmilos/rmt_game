import mysql.connector
from mysql.connector import errorcode
import configparser


class DB:

    def __init__(self):
        self.cursor = None
        self.cnx = None

    def connect(self):
        # Parametri za povezivanje sa mySQL bazom se citaju iz config.ini fajla
        config_data = configparser.ConfigParser()
        config_data.read("config.ini")
        dbparams = config_data["database"]

        # Povezivanje sa bazom
        try:
            self.cnx = mysql.connector.connect(**dbparams)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        self.cursor = self.cnx.cursor()

    def disconnect(self):
        self.cnx.close()

    # dodaje novi red (korisnika) u tabelu na osnovu user i pass
    # ako vec postoji user, SQL vraca error 
    def addNewUser(self, usr, pas):
        try:
            self.cursor.execute(f"INSERT INTO user VALUES ('{usr}', '{pas}', 0, 0)")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                msg = 'User already exists, please log in!'
            else:
                msg = err
            return msg

        self.cnx.commit()
        return 'success'

    def checkIfExist(self, usr, pas):
        # Uzmi red sa datim username-om
        self.cursor.execute(f"SELECT username, password, active FROM user WHERE username = '{usr}'")
        row = self.cursor.fetchall()

        # Nije nasao korisnika
        if not row:
            return 'Username not found, please register!'
        # Password nije isti
        elif row[0][1] != pas:
            return 'Incorrect password'
        # Korisnik je aktivan (na drugom racunaru)
        elif row[0][2] == 1:
            return 'User already logged in!'
        else:
            return 'success'

    # postavi active flag (1 - aktivan, 0 - neaktivan)
    # pretpostavlja da je user vec unet
    def setActive(self, usr, act=1):
        self.cursor.execute(f"UPDATE user SET active = {act} WHERE username = '{usr}'")
        self.cnx.commit()

    def removeActive(self, usr):
        self.setActive(usr, 0)
