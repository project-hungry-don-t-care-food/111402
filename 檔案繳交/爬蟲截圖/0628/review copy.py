from lib2to3.pgen2 import driver
from urllib.request import urlopen
# 在你剛剛安裝的 beautifulsoup4 函式庫裡使用 BeautifulSoup 這個解析器
import requests , bs4
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re

import pandas as pd
df1 = pd.DataFrame(columns=["user","date","reviews"])

#open uml
driver = webdriver.Chrome()  #開啟瀏覽器
driver.get("https://ifoodie.tw/restaurant/559dac4fc03a103ee86c9908-%E9%9B%AA%E7%8E%8B%E5%86%B0%E6%B7%87%E6%B7%8B")
time.sleep(1)

    
button = driver.find_element_by_class_name("span")
button.send_keys("載入更多動態")
button.click()

time.sleep(1)
                                                                    

"""   
reviews = html1.find_all("div",class_="comment-content-outer")
for review in reviews:
        
    #date 
    date = review.find("div",class_="date").text
    
    
    #review
    re = review.find("div", class_="jsx-" and "message").text

    #more review
    more_re= html1.find("div", class_ = "btn-more-checkin-wrapper").text
   
    if "載入更多動態" in more_re:
        print("還有")
    else:
        break
    
    s1 = pd.Series([user,date,re],index=["user","date","reviews"])
    df1 = df1.append(s1, ignore_index=True)
    
    print("完成第"+f"{comment}"+"條")
    comment +=1

    time.sleep(30)
df1.to_csv("2.csv", encoding="utf-8", index=False)

"""
