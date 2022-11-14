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
with open('data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    rows = csv.reader(csvfile)
    for index, row in enumerate(rows):
        if index == 0:
            continue
        row = [x.strip(' ') for x in row]

        with conn.cursor() as cursor:
            try:
                SQL_input = """INSERT INTO 店家資料(店名, 建立時間, 電話, 地址, 總體評分, 網址)
                Values(N'{}', CONVERT(DATETIME, '{}', 121), N'{}', N'{}',{},N'{}')""".format(row[0],row[1],row[2],row[3],row[4],row[5])
                
                command = SQL_input
                cursor.execute(command)
                conn.commit()
                print(True)
                
            except Exception as ex:
                print(ex)

