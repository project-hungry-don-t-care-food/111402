import csv
# 開啟 CSV 檔案
with open('Restaurant data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader = csv.DictReader(csvfile)
    title = []
    link = []
    address = []
    star = []
    for i in reader:
        title.append(i["餐廳名稱"])
        link.append(i["餐廳連結"])
        address.append(i["餐廳地址"])
        star.append(i["餐廳評價"])
   
    print(address)
    print(star)