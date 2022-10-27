import csv
# 開啟 CSV 檔案
with open('Restaurant data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader = csv.DictReader(csvfile)
    column = [row['餐廳連結'] for row in reader]
    print(column[2])

for index, row in enumerate(column):
    print("目前：" + str(index))
    url=(row[0:])
   
    print(url)
  