import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver
import re
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
df1 = pd.DataFrame(columns=["opentime"])

import csv
# 開啟 CSV 檔案
with open('Restaurant data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader = csv.DictReader(csvfile)
    title = []
    link = []
    for i in reader:
        title.append(i["餐廳名稱"])
        link.append(i["餐廳連結"])

#open uml
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")  #開啟瀏覽器
for index, row in enumerate(link):
    print("目前：" + str(index+1))
    url=(row[0:])
    name = title[index]
  
    driver.get(url)
    time.sleep(1)
    
    business_hour = ""

    try :
        button = driver.find_element("xpath", "/html/body/div[1]/div/div/div/div[2]/main/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/button")
        button.click()
    except:
        print("沒按鈕了")
        break
    time.sleep(1)
       
    soup = Soup(driver.page_source,"lxml")                                 
    #營業時間 
    opentimes = soup.find_all("div",class_="jss76 jss116 jss119 jss124 jss125")
    for index, opentime in enumerate(opentimes):
        #opentime
        opentime = opentime.find("div",class_="weekday-hours").text
        #print(index, opentime)

        timelist = opentime.split(" ")
        if timelist[1] == "休息":
            continue
            
        print(timelist)
        
        # 處理星期數
        if timelist[0] == "星期一":
            weekday = "1:"
        if timelist[0] == "星期二":
            weekday = "2:"
        if timelist[0] == "星期三":
            weekday = "3:"
        if timelist[0] == "星期四":
            weekday = "4:"
        if timelist[0] == "星期五":
            weekday = "5:"
        if timelist[0] == "星期六":
            weekday = "6:"
        if timelist[0] == "星期日":
            weekday = "7:"
        business_hour += weekday
        
        # 處理每天的時間
        for i in range(1, len(timelist)):
            #print(timelist[i])
            if i == 2:
                business_hour += "," + weekday
            business_hour += timelist[i][0:2] + timelist[i][3:5] + timelist[i][6:8] + timelist[i][9:11]

        # 如果是最後一天就不加逗號
        if index == len(opentimes) - 1:
            pass
        else:
            business_hour += ","
        
    s2 = pd.Series([business_hour],index=["opentime"])
    df1 = df1.append(s2, ignore_index=True)
    print(business_hour)
print("結束："+str(index+1))

df1.to_csv("time.csv", encoding="utf-8", index=False)
driver.close() 