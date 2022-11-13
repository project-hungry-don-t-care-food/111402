import csv
import pymssql

def conn(): #連接資料庫
    connect = pymssql.connect('(local)', 'sa', 'Food111402', 'Food')
    if connect:
        print("連線成功!")
    return connect
conn = conn()

with conn.cursor() as cursor: #先刪除資料表的資料
    command = "Delete From 店家資料"
    cursor.execute(command)
    conn.commit()

# 開啟 CSV 檔案

with conn.cursor() as cursor:
    try:
        SQL_input = """INSERT INTO 店家資料(店名, 建立時間, 電話)
        Values(N'城中市場老牌牛肉拉麵大王', '2022-08-17 23:33:28', N'0223815604')"""
        command = SQL_input
        cursor.execute(command)
        conn.commit()
        print(True)
                
    except Exception as ex:
        print(ex)
        print(False)

