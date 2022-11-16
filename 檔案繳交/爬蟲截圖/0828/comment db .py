import csv
import pymssql

def conn(): #連接資料庫
    connect = pymssql.connect('(local)', 'sa', 'Food111402', 'food')
    if connect:
        print("連線成功!")
    return connect
conn = conn()

#先刪除資料表的資料
with conn.cursor() as cursor: 
    command = "DELETE store_external_comment; DBCC CHECKIDENT('store_external_comment', RESEED, 0)"
    cursor.execute(command)
    conn.commit()

# 開啟 CSV 檔案
with open('3Comment.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    rows = csv.reader(csvfile)
    #columns = next(rows)

    for index, row in enumerate(rows):
        # trim leading and trailing empty spaces
        row = [x.strip(' ') for x in row]
    
        with conn.cursor() as cursor:
            try:
                SQL_input = """Insert Into store_external_comment(store_info_id,create_time,score,[content])
                             Values ( {},CONVERT(DATETIME, '{}', 121), {}, N'{}')""".format(row[0],row[1],row[2],row[3])
                command = SQL_input
                cursor.execute(command)
                conn.commit()
                print(True)
                
            except Exception as ex:
                print(False)
                print(ex)

