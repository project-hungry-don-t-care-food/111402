import csv
import pymssql

def conn(): #連接資料庫
    connect = pymssql.connect('(local)', 'sa', 'Food111402', 'Food')
    if connect:
        print("連線成功!")
    return connect
conn = conn()

with conn.cursor() as cursor: #先刪除restaurant_list的資料
    command = "Delete From review"
    cursor.execute(command)
    conn.commit()

# 開啟 CSV 檔案
with open('Comment.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    rows = csv.reader(csvfile)
    for index, row in enumerate(rows):
        # trim leading and trailing empty spaces
        row = [x.strip(' ') for x in row]
        if "'" in row:
            row= row.replace("'","''")
    
    

    with conn.cursor() as cursor:
        try:
            SQL_input = """Insert Into review (title,uesrid,評論時間,評論評分,評論)
                        Values (N'{}', N'{}', {}, {}, N'{}')""".format(row[0],row[1],row[2],row[3],row[4])
            command = SQL_input
            cursor.execute(command)
            conn.commit()
            
        except Exception as ex:
            print(False)

