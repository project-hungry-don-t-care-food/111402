from bs4 import BeautifulSoup
from urllib.request import urlopen
import  bs4
import requests
import matplotlib.pyplot as plt
import os
import datetime
from connectdb import conn
import warnings
import time
warnings.filterwarnings("ignore")

with conn.cursor() as cursor: #先刪除資料表的資料
    command = "DELETE store_image; DBCC CHECKIDENT('store_image', RESEED, 0)"
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
    for index , link in enumerate(image_links):
        if not os.path.exists("images"):
            os.mkdir("images")
        img = requests.get(link)

        with open("images\\" + str(store_info_id) + ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
            f=file.write(img.content)  # 寫入圖片的二進位碼
        
        with conn.cursor() as cursor:       
            SQL_input = """Insert Into store_image(store_info_id,create_time, image ,is_from_store_owner) 
                        Values ({},CONVERT(DATETIME, '{}', 121),'{}',{})""".format(store_info_id,create_time,f,is_from_store_owner)
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
