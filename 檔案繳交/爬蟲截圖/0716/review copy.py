from numpy import number
import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver
import re

import pandas as pd
df1 = pd.DataFrame(columns=["date","reviews"])


# open csv
infile=open('Restaurant data.csv','r',encoding='utf-8')
outfile=open('out2.csv','w',encoding='utf-8')

data=infile.readlines()

outdate=[]
for d in data:
    d=d.strip().split(',')
    num=str(d[0])
    name=str(d[1])
    link=str(d[4])
    outdate.append(f'{num},{name},{link}\n')

outdate[-1]=outdate[-1].strip()
print(outdate)

#open uml
z=1
driver = webdriver.Chrome()  #開啟瀏覽器
for num,link in data:
    for z in num:
        url = f'{link}'
        driver.get(url)
        z+=1
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


outfile.writelines(outdate)

infile.close()
outfile.close()