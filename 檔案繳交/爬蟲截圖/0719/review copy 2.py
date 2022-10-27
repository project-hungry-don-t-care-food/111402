import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver
import re

import pandas as pd
df1 = pd.DataFrame(columns=["date","reviews"])

import csv
# 開啟 CSV 檔案
with open('Restaurant data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader = csv.DictReader(csvfile)
    column = [row['餐廳連結'] for row in reader]

#open uml
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")  #開啟瀏覽器
for index, row in enumerate(column):
    print("目前：" + str(index))
    url=(row[0:])
  
    driver.get(url)
    time.sleep(1)

    for x in range(20):
        button = driver.find_element_by_class_name("btn-more-checkin-wrapper")
        button.click()
        time.sleep(3)

        soup = Soup(driver.page_source,"lxml")                                 
        comment=1

        #評論  
        reviews = soup.find_all("div",class_="comment-content-outer")
        for review in reviews:
                
            #date 
            date = review.find("div",class_="date").text
            date_time= re.search(r"(\d{4}/\d{1,2}/\d{1,2})",date).group(0)
            
            #review
            rev = review.find("div", class_="message").text
            rev = str(rev)

            r = review.find("div",class_="action-outer").text
            r = str(r)
            
            for x in range(len(r)):
                rev = rev.replace(r[x],"")
            
            s2 = pd.Series([date_time,rev],index=["date","reviews"])
            df1 = df1.append(s2, ignore_index=True)
            
            print("完成第"+f"{comment}"+"條")
            comment +=1
            
            time.sleep(5)
        driver.close()
        df1.to_csv("3.csv", encoding="utf-8", index=False)
    print("結束：" + str(index))
