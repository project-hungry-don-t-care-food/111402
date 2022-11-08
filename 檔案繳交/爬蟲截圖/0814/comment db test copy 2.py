import pymssql
import csv

conn = pymssql.connect('(local)', 'sa', 'Food111402', 'Food')
cursor = conn.cursor()

script = "Insert Into review (title,uesrid,評論時間,評論評分,評論)"

def updateValue(row):
    newRow = []
    for value in row:
        newValue = value.replace("'", "''")
        newRow.append(newValue)
    return newRow


with open('Comment.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    rows = csv.reader(csvfile)
    # row = 一整列 data (type: list)
    for index, row in enumerate(rows):
        # trim leading and trailing empty spaces
        row = [x.strip(' ') for x in row]
        # replace ' to ''
        row = updateValue(row)
        print(row)

        #row = "Values ('value1', 'value2', 'value3', 'value4','value5')".format(row[0], row[1],row[2],row[3],row[4])
        
        # get insert script
        finalScript = script + row

        # Insert script
        try:
            cursor.execute(finalScript)
            conn.commit()
            print("Inserted Count: ", index + 1)
        except:
            conn.rollback()
            print("Script failed")


print("Conn closed")
conn.close()