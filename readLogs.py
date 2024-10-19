import re
import mysql.connector
from config import *
import json
pattern = r'(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\]'

path_log = "/var/log/apache2/access.log.1"

last_line = None

db = mysql.connector.connect(
        host = user_db.get("host"),
        user = user_db.get('user'),
        password = user_db.get('password'),
        database = user_db.get('database')
)
cursor = db.cursor()

sql_delete_table = "DELETE FROM parsing_logs"
cursor.execute(sql_delete_table)

#SaveData
sql_insert = "INSERT INTO parsing_logs (ip, date) VALUES (%s, %s)"
with open(path_log, 'r') as f:
    for line_log in f:
        match = re.search(pattern, line_log)
        if match != None:
            ip = match.group('ip')
            date = match.group('datetime')
            val = (ip, date)
            cursor.execute(sql_insert, val)
            db.commit()

sql_show_table = "select * from parsing_logs"
cursor.execute(sql_show_table)
sql_res = cursor.fetchall()
for line in sql_res:
    print(line)

# sql_show_where_date = "SELECT * FROM parsing_logs WHERE STR_TO_DATE(date, '%d/%b/%Y:%H:%i:%s +0300') BETWEEN STR_TO_DATE('16/Oct/2024:00:00:00 +0300', '%d/%b/%Y:%H:%i:%s +0300') AND STR_TO_DATE('16/Oct/2024:23:59:59 +0300', '%d/%b/%Y:%H:%i:%s +0300');"
# cursor.execute(sql_show_where_date)
# sql_res = cursor.fetchall()
# print("Дата 16 октября")
# for line in sql_res:
#     print(line)


#Save to json
cursor_json = db.cursor(dictionary=True)
sql_show_table = "select * from parsing_logs"
cursor_json.execute(sql_show_table)
rows = cursor_json.fetchall()
json_path = "database.json"
with open(json_path, 'w') as f:
    json.dump(rows, f, indent=4)
    print("файл сохранен в json")
