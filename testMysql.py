from mysql.connector import connect, Error
import mysql.connector 

from config import *

try:
    with connect(
        host = user_db.get("host"),
        user = user_db.get('user'),
        password = user_db.get('password')
    ) as connection:
        print(connection)
except Error as e:
    print(e)

