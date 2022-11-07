from optparse import TitledHelpFormatter
from bs4 import BeautifulSoup
from urllib.request import urlopen
import  bs4
import requests
import matplotlib.pyplot as plt
import os
import pymssql

def conn(): #連接資料庫
    connect = pymssql.connect('(local)', 'sa', 'Food111402', 'Food')
    if connect:
        print("連線成功!")
    return connect
conn = conn()

def to_img(id,title,url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    
    results = soup.find_all("img", {"alt":title})
    print(results)

    image_links = [result.get("src") for result in results[0:1]]
    for index, link in enumerate(image_links):

        if not os.path.exists("images"):
            os.mkdir("images")
        img = requests.get(link)
        print(img)
        with conn.cursor() as cursor:       
            SQL_input = """Insert Into picture (id,img) Values (N'{}',{})""".format(title,img)
            command = SQL_input
            cursor.execute(command)
            conn.commit()
            
        '''
        with open("images\\" +str(id) +"."+ str(title) + ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
              file.write(img.content)  # 寫入圖片的二進位碼
 '''

import csv
# 開啟 CSV 檔案
with open('Restaurant data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader1 = csv.DictReader(csvfile)
    title = []
    link = []
    id = []
    for i in reader1:
        title.append(i["餐廳名稱"])
        link.append(i["餐廳連結"])
        id.append(i["id"])
    print(title)
    print(link)
    print(id)

for index, row in enumerate(title):
    
    print("目前：" + str(index))
    to_img(id[index],title[index],link[index])


    
