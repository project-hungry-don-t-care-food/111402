import email
from lib2to3.pgen2 import driver
from urllib.request import urlopen
# 在你剛剛安裝的 beautifulsoup4 函式庫裡使用 BeautifulSoup 這個解析器
import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re

import pandas as pd
df1 = pd.DataFrame(columns=["date","reviews"])

#open uml
driver = webdriver.Chrome()  #開啟瀏覽器
url = "https://ifoodie.tw/restaurant/59ff52d22756dd6f04e9d377-93%E7%95%AA%E8%8C%84%E7%89%9B%E8%82%89%E9%BA%B5"
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

        rev_text= re.search(r"(.*)",rev).group(0)

        
        s2 = pd.Series([date_time,rev_text],index=["date","review"])
        df1 = df1.append(s2, ignore_index=True)
        
        print("完成第"+f"{comment}"+"條")
        comment +=1
        
        time.sleep(5)
    df1.to_csv("3.csv", encoding="utf-8", index=False)
    
    driver.close()





