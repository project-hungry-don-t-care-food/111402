from optparse import TitledHelpFormatter
from bs4 import BeautifulSoup
from urllib.request import urlopen
import  bs4
import requests
import matplotlib.pyplot as plt
import os
def to_img(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    
    results = soup.find_all("img", {"class":title})
    print(results)

    image_links = [result.get("src") for result in results[0:1]]
    for index, link in enumerate(image_links):

        if not os.path.exists("images"):
            os.mkdir("images")
        img = requests.get(link)
        
        with open("images\\" +str(index) +  ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
              file.write(img.content)  # 寫入圖片的二進位碼

import csv
# 開啟 CSV 檔案
with open('Restaurant data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader1 = csv.DictReader(csvfile)
    for i in reader1:
        
        print(title)
        print(link)

for index, row in enumerate(title):
    
    print("目前：" + str(index))
    to_img(os.link)


    
