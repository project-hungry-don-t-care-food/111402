from unicodedata import name
import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver
import re
import datetime

import pandas as pd
df1 = pd.DataFrame(columns=["title","date","tel","address","star","link"])
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
        star.append(["餐廳評價"])

   
    print(title)

#open uml
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")  #開啟瀏覽器
url = "https://ifoodie.tw/restaurant/61dd2292baf6d30524a2ac37-%E9%90%98%E4%BA%88%E5%8E%9F%E5%91%B3%E7%95%B6%E6%AD%B8%E9%B4%A8-%E5%85%AC%E9%A4%A8%E5%BA%97"
driver.get(url)
time.sleep(1)

soup = Soup(driver.page_source,"lxml")

#date 
date = datetime.datetime.now()
                               
# tel
telphone = soup.find_all("div",class_="phone-wrapper")

for tel in telphone:
    #tel
    tel = tel.find("a").text
    s2 = pd.Series([name,date,tel,address,star,link],index=["title","date","tel","address","star","link"])
    df1 = df1.append(s2, ignore_index=True)


print("完成")

driver.close()
df1.to_csv("3.csv", encoding="utf-8", index=False)    