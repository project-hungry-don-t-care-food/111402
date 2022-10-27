from os import remove
from urllib.request import urlopen
import requests , bs4
from bs4 import BeautifulSoup
import time
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
df1 = pd.DataFrame(columns=["date","reviews"])

url="https://ifoodie.tw/restaurant/559d04e1c03a103ee86c3419-%E7%93%A6%E5%B4%8E%E7%87%92%E7%83%A4%E7%81%AB%E9%8D%8B-%E5%85%AC%E9%A4%A8%E5%BA%97"
response1= urlopen(url)
html1 = BeautifulSoup(response1, "html.parser")
comment = 1  

#評論  
reviews = html1.find_all("div",class_="comment-content-outer")
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
    

    time.sleep(1)

df1.to_csv("2.csv", encoding="utf-8", index=False)


