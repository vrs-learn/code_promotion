#
# This program checks if there is a TSO environment already configured :
from env.crypt import *
import sqlite3
from env.logging import *

default_db = "tsoenv.db"

class Database:

    def __init__(self, db=default_db):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS tsoenv (id INTEGER PRIMARY KEY, server VARCHAR NOT NULL, port INTEGER NOT NULL, sec_value NOT NULL CHECK (sec_value IN (0,1)), username TEXT NOT NULL, password VARCHAR NOT NULL, component TEXT NOT NULL CHECK ( component in ('CDP','REPO','RSSO')), s_or_d TEXT NOT NULL)")
        self.conn.commit()
        self.crypt_key=get_key()

    def insert(self,server,port,sec_value,username,password,component,s_or_d):
        self.log_this = Log_Process()
        passw_cr=encrypt_value(password,self.crypt_key)
        try:
            self.cur.execute("INSERT INTO tsoenv VALUES(NULL,?,?,?,?,?,?,?)",(server,port,sec_value,username,passw_cr,component,s_or_d))
            self.conn.commit()
            self.log_this.logger.info("TSO details inserted successfully for "+str(server))
        except sqlite3.IntegrityError as e:
            print("Data Integrity Check failed. " + str(e))
            self.log_this.logger.exception("TSO details insertion failed for "+str(server))
            sys.exit()
        self.cur.execute("SELECT * FROM tsoenv")

    def view(self,component,s_or_d):
        self.log_this = Log_Process()
        self.cur.execute("SELECT * FROM tsoenv where component=? and s_or_d=?",(component,s_or_d))
        rows=self.cur.fetchall()
        if len(rows) > 0:
            rows=rows[0]
            #rows = c.fetchone()
            if len(rows) == 8:
                pass_dcr=decrypt_value(rows[5],self.crypt_key)
                data={'id' : rows[0] , 'server' : rows[1] , 'port' : rows[2] , 'sec_value' : rows[3] , 'username' : rows[4] , 'password' : pass_dcr , 'component' : rows[6] , 's_or_d' : rows[7]}
                return data
            else :
                return {}
                self.log_this.logger.error("inconsistent data for "+str(s_or_d)+" "+str(component))
        else :
            return {}
            self.log_this.logger.info("No data exists for "+str(s_or_d)+" "+str(component))

    def delete(self,id):
        self.cur.execute("DELETE FROM tsoenv where id=?",(id))
        self.conn.commit()

    def delete_all(self):
        self.cur.execute("DELETE FROM tsoenv")
        self.cur.execute("SELECT * FROM tsoenv")
        print(self.cur.fetchall())
        self.conn.commit()

    def __del__(self):
        self.conn.close()


'''
database = Database()
try :
    database.insert("clm-aus-018786",38080,0,"aoadmin","admin123","CDP","source")
except sqlite3.IntegrityError as e:
    print("Data Integrity Check failed. " + str(e))

print("The List of enteries in DB are :")
rows=database.view("CDP","source")
print("http://"+str(rows['server'])+":"+str(rows['port']))
print(len(rows))
'''
