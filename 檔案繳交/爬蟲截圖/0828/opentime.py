from os import times
import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver

import pandas as pd
df1 = pd.DataFrame(columns=["opentime"])

#open uml
driver = webdriver.Edge("msedgedriver.exe")  #開啟瀏覽器
url = "https://ifoodie.tw/restaurant/559d4bc0c03a103ee86c5eb1-%E5%8D%81%E4%BA%8C%E5%BB%9A-(%E5%96%9C%E4%BE%86%E7%99%BB%E5%A4%A7%E9%A3%AF%E5%BA%97)"
driver.get(url)
business_hour = ""

button = driver.find_element("xpath", "/html/body/div[1]/div/div/div/div[2]/main/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/button")
button.click()

soup = Soup(driver.page_source,"lxml")                                 

#營業時間 
opentimes = soup.find_all("div",class_="jss76 jss116 jss119 jss124 jss125")
for index, opentime in enumerate(opentimes):
    #date
    opentime = opentime.find("div",class_="weekday-hours").text
    print(index, opentime)

    timelist = opentime.split(" ")
    print(timelist)
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
        print(timelist[i])
        
        if i >= 2:
            business_hour += "," + weekday
        business_hour += timelist[i][0:2] + timelist[i][3:5] + timelist[i][6:8] + timelist[i][9:11]

    # 如果是最後一天就不加逗號
    if index == len(opentimes) - 1:
        pass
    else:
        business_hour += ","
        
print(business_hour)
driver.close()