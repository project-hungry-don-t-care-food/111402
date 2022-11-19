from cProfile import label
from bs4 import BeautifulSoup
from urllib.request import urlopen
import  bs4
import requests
import matplotlib.pyplot as plt
import os
import datetime
import base64
from PIL import Image
import warnings
import time
warnings.filterwarnings("ignore")
import pymssql

def conn(): #連接資料庫
    connect = pymssql.connect('ntubfood.westus2.cloudapp.azure.com', 'sa', 'ntub_pj123456', 'food')
    if connect:
        print("連線成功!")
    return connect
conn = conn()

with conn.cursor() as cursor: #先刪除資料表的資料
    command = "DELETE store_image; DBCC CHECKIDENT('store_image', RESEED,0)"
    cursor.execute(command)
    conn.commit()

with conn.cursor() as cursor:#取出資料表的資料
    SQL_output = """SELECT store_info_id,store_name, url FROM store_info"""   
    command = SQL_output
    cursor.execute(command)
    db = cursor.fetchall()

def to_img(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    results = soup.find_all("img", {"alt":store_name})
    

    image_links = [result.get("src") for result in results[0:1]]
    is_from_store_owner = 0
    label = 3
    for index , link in enumerate(image_links):
        if not os.path.exists("images"):
            os.mkdir("images")
        img = requests.get(link)

        with open("images\\" + str(store_info_id) + ".png", "wb") as file:  # 開啟資料夾及命名圖片檔
            f = file.write(img.content) 
            im = Image.open("images\\" + str(store_info_id) + ".png")
            (x,y) = im.size #read image size
            x_s = 400 #define standard width
            y_s = 400 #calc height based on standard width
            out = im.resize((x_s,y_s),Image.ANTIALIAS) #resize image with high-quality
            out.save("images\\" + str(store_info_id) + ".png",)
            print(out)
    
        
        with open("images\\" + str(store_info_id) + ".png", "rb") as file:  # 開啟資料夾及命名圖片檔
            r = file.read()
            base64_data = base64.b64encode(r)  # base64編碼
            #print(base64_data)
            base64_data = str(base64_data, 'utf-8')

        with conn.cursor() as cursor:  
            SQL_input = """Insert Into store_image(store_info_id,create_time, image ,label,is_from_store_owner) 
                        Values ({},CONVERT(DATETIME, '{}', 121),'{}','{}',{})""".format(store_info_id,create_time,base64_data,label,is_from_store_owner)
            command = SQL_input
            cursor.execute(command)
            conn.commit()
            
        
#create_time
create_time = datetime.datetime.now().replace(microsecond=0)

for index , row in enumerate(db):
    store_info_id = row[0]
    store_name = row[1]
    
    print("目前：" + str(index+1))
    to_img(row[2])
