import csv
import pymssql

def conn(): #連接資料庫
    connect = pymssql.connect('(local)', 'sa', 'Food111402', 'food')
    if connect:
        print("連線成功!")
    return connect
conn = conn()

with conn.cursor() as cursor: #先刪除資料表的資料
    command = "DELETE store_info; DBCC CHECKIDENT('store_info', RESEED, 0)"
    cursor.execute(command)
    conn.commit()

# 開啟 CSV 檔案
with open('Data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    rows = csv.reader(csvfile)
    for index, row in enumerate(rows):
        if index == 0:
            continue
        row = [x.strip(' ') for x in row]

        with conn.cursor() as cursor:
            try:
                SQL_input = """INSERT INTO store_info(store_name, create_time, phone_number, address, total_score, business_hour, url, is_appointed_store, is_unknown_store)
                Values(N'{}', CONVERT(DATETIME, '{}', 121), N'{}', N'{}',{},N'{}',N'{}',{},{})""".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                
                command = SQL_input
                cursor.execute(command)
                conn.commit()

                print(True)
                
            except Exception as ex:
                print(ex)
                print(SQL_input)