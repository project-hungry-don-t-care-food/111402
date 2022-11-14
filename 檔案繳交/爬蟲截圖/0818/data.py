from asyncio.windows_events import NULL
from unicodedata import mirrored
import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver
import re
import datetime
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
df1 = pd.DataFrame(columns=["title","date","tel","address","star","link"])

import csv
# 開啟 CSV 檔案
with open('Restaurant data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader = csv.DictReader(csvfile)
    title = []
    link = []
    adr = []
    star = []
    for i in reader:
        title.append(i["餐廳名稱"])
        link.append(i["餐廳連結"])
        adr.append(i["餐廳地址"])
        star.append(i["餐廳評價"])
  

#open uml
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")  #開啟瀏覽器
for index, row in enumerate(link):
    print("目前：" + str(index+1))
    url=(row[0:])
    name = title[index]
    address = adr[index]
    alink = link[index]
    stars = star[index]

    
    driver.get(url)
    time.sleep(1)

    soup = Soup(driver.page_source,"lxml")

    #date 
    date = datetime.datetime.now().replace(microsecond=0)
                                
    # tel
    telphone = soup.find_all("div",class_="phone-wrapper")

    for tel in telphone:
        #tel
        tel = tel.find("a").text
           
        
        
        s2 = pd.Series([name,date,tel,address,stars,alink],index=["title","date","tel","address","star","link"])
        df1 = df1.append(s2, ignore_index=True)

    print("結束：" + str(index+1))
    print(" ") #分段落
df1.to_csv("data.csv", encoding="utf-8", index=False)  
  
