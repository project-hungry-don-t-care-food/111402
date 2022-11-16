from sqlite3 import Cursor, dbapi2
import pymssql
# 去資料庫取資料 store_info_id 和 url 
def conn(): #連接資料庫
    connect = pymssql.connect('(local)', 'sa', 'Food111402', 'food')
    if connect:
        print("連線成功!")
    return connect
conn = conn()

with conn.cursor() as cursor:
    SQL_output = """SELECT  store_info_id, url FROM store_info"""
       
    command = SQL_output
    cursor.execute(command)
    db = cursor.fetchall()

for index, row in enumerate(db):
    print("目前：" + str(index+1))
    print(row[1])
    
    
                
    