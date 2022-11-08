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
    print("總共" + str(rows.line_num))
    # 以迴圈輸出每一列
    title = []
    userid = []
    date= []
    star= []
    rev= []
    for i in rows:
        title.append(i[0])
        userid.append(i[1])
        date.append(i[2])
        star.append(i[3])
        rev.append(i[4])
    print(title)
    print(userid)
    print(date)
    print(star)
    print(rev)

for index, row in enumerate(rows):
    with conn.cursor() as cursor:
        try:
            SQL_input = """Insert Into review (title,uesrid,評論時間,評論評分,評論)
                        Values (N'{}', N'{}', {}, {}, N'{}')""".format(title,userid,date,star,rev)
            command = SQL_input
            cursor.execute(command)
            conn.commit()
            
        except Exception as ex:
            print(False)