import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver
import re
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
df1 = pd.DataFrame(columns=["title","username","date","star","reviews"])

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
   
    print(title)

#open uml
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")  #開啟瀏覽器
for index, row in enumerate(link):
    print("目前：" + str(index+1))
    url=(row[0:])
    name = title[index]
    print(name)
    print(url)
  
    driver.get(url)
    time.sleep(1)

    for x in range(20):
        try :
            button = driver.find_element_by_class_name("btn-more-checkin-wrapper")
            button.click()
        except:
            print("沒更多的按鈕了")
            break
        time.sleep(1)
    
        
    soup = Soup(driver.page_source,"lxml")                                 
    comment=1

    #評論  
    reviews = soup.find_all("div",class_="comment-content-outer")
    for review in reviews:
        # id
        username = review.find("div",class_="username-outer").text
            
        #date 
        date = review.find("div",class_="date").text
        date_time= re.search(r"(\d{4}/\d{1,2}/\d{1,2})",date).group(0)

        #start
        star = review.find("div",class_="text")
        if star == None: #判斷有沒有餐廳評價
            star = "999"
        else:
            star = float(star.string)
            
        #review
        rev = review.find("div", class_="message").text
        rev = str(rev)

        r = review.find("div",class_="action-outer").text
        r = str(r)
        
        for x in range(len(r)):
            rev = rev.replace(r[x],"")

        
        s2 = pd.Series([name,username,date_time,star,rev],index=["title","username","date","star","reviews"])
        df1 = df1.append(s2, ignore_index=True)
        
        print("完成第"+f"{comment}"+"條")
        comment +=1
        
        #time.sleep(5)
    
    print("結束：" + str(index+1))
    print(" ") #分段落
df1.to_csv("Comment.csv", encoding="utf-8", index=False)

