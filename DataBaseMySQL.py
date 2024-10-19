import mysql.connector
import json
import re 
from pathlib import Path
from config import *
from datetime import datetime

class DataBase():
    def __init__(self, database, host, user, password):
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="Pull",
                pool_size= 5,
                host = host,
                user = user,
                password = password,
                database = database
                )
        except mysql.connector.Error as err:
            raise ConnectionError(f"Ошибка в подключении базе данных {err}")
        self.connection_status = True
        self.path_log_list = self.get_paths_log()

    def is_connected(self):
        return 1 if self.connection_status else 0

    def get_paths_log(self):
        path_log_list = []
        for path_log in path_log_config:
            if Path(path_log).is_file():
                path_log_list.append(path_log)

        return path_log_list

    def get_connection(self):
        try:
            connection = self.pool.get_connection()
            return connection
        except mysql.connector.Error as err:
            raise f"Ошибка получения соединения из пула: {err}"

        
    def SaveData(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql_insert = "INSERT INTO parsing_logs (ip, date) VALUES (%s, %s)"
            pattern = pattern_config
            for path_log in self.path_log_list:
                with open(path_log) as log_file:
                    for row_log in log_file:
                        match = re.search(pattern, row_log)
                        if match != None:
                            ip = match.group('ip')
                            date = match.group('datetime')
                            val = (ip, date)
                            cursor.execute(sql_insert, val)
                            connection.commit()

        except mysql.connector.pooling.PoolError as e:
            print("Пул соединения исчерпан")
        except mysql.connector.Error as err:
            print(f"ошибка при выполнения запроса SaveData {err}")
        finally:
            connection.close()
            cursor.close()

    def ShowData(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql_select = "SELECT * FROM parsing_logs;"
            cursor.execute(sql_select)
            sql_res = cursor.fetchall()
            return sql_res
            # for line in sql_res:
            #     print(line)
        except mysql.connector.pooling.PoolError as e:
            print("Пул соединения исчерпан")
        except mysql.connector.Error as err:
            print(f"ошибка при выполнения запроса SaveData {err}")
        finally:
            connection.close()
            cursor.close()

    def DeleteData(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql_delete = "DELETE FROM parsing_logs"
            cursor.execute(sql_delete)
            connection.commit()
        except mysql.connector.pooling.PoolError as e:
            print("Пул соединения исчерпан")
        except mysql.connector.Error as err:
            print(f"ошибка при выполнения запроса SaveData {err}")
        finally:
            connection.close()
            cursor.close()
    
    
    def Format_date(self, date_str):
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        fomatted_date = date_obj.strftime("%d/%b/%Y")
        return fomatted_date
        
        


    def SelectBetween(self, start_date, end_date):
        start_date = self.Format_date(start_date)
        end_date = self.Format_date(end_date)
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql_select = f"SELECT * FROM parsing_logs WHERE STR_TO_DATE(date, '%d/%b/%Y:%H:%i:%s +0300') BETWEEN STR_TO_DATE('{start_date}:00:00:00 +0300', '%d/%b/%Y:%H:%i:%s +0300') AND STR_TO_DATE('{end_date}:23:59:59 +0300', '%d/%b/%Y:%H:%i:%s +0300');"
            cursor.execute(sql_select)
            sql_string = cursor.fetchall()
            for row in sql_string:
                print(row)

        except mysql.connector.pooling.PoolError as e:
            print("Пул соединения исчерпан")
        except mysql.connector.Error as err:
            print(f"ошибка при выполнения запроса SaveData {err}")
        finally:
            connection.close()
            cursor.close()        

    def SaveToJSON(self):
        connection = self.get_connection()
        cursor_json = connection.cursor(dictionary=True)
        sql_show_table = "select * from parsing_logs"
        cursor_json.execute(sql_show_table)
        rows = cursor_json.fetchall()
        json_path = "database.json"
        with open(json_path, 'w') as f:
            json.dump(rows, f, indent=4)
            print("файл сохранен в json")