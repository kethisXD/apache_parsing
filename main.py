from config import *
from DataBaseMySQL import DataBase

def main():
    database = user_db.get('database')
    host = user_db.get('host')
    user = user_db.get('user')
    password = user_db.get('password')
    
    db = DataBase(database, host, user, password)
    db.SaveData()
    db.ShowData()

if __name__=="__main__":
    main()