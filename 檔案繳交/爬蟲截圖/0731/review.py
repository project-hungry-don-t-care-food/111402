import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver
import re

import pandas as pd
df1 = pd.DataFrame(columns=["username","date","star","reviews"])

#open uml
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")  #開啟瀏覽器
url = "https://ifoodie.tw/restaurant/61dd2292baf6d30524a2ac37-%E9%90%98%E4%BA%88%E5%8E%9F%E5%91%B3%E7%95%B6%E6%AD%B8%E9%B4%A8-%E5%85%AC%E9%A4%A8%E5%BA%97"
driver.get(url)
time.sleep(1)

button = driver.find_element_by_class_name("btn-more-checkin-wrapper")
for x in range(20):
    
    button.click()
    time.sleep(3)
    
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
        
        s2 = pd.Series([username,date_time,star,rev],index=["username","date","star","reviews"])
        df1 = df1.append(s2, ignore_index=True)
        
        print("完成第"+f"{comment}"+"條")
        comment +=1
        time.sleep(3)
        
    driver.close()
    df1.to_csv("3.csv", encoding="utf-8", index=False)    