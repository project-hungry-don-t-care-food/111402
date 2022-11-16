import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver
import re
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
df1 = pd.DataFrame(columns=["store_info_id","create_time","score","content"])

import pymssql
# 去資料庫取資料 store_info_id 和 url 
def conn(): #連接資料庫
    connect = pymssql.connect('(local)', 'sa', 'Food111402', 'food')
    if connect:
        print("連線成功!")
    return connect
conn = conn()

with conn.cursor() as cursor: #先刪除資料表的資料
    command = "DELETE store_external_comment; DBCC CHECKIDENT('store_external_comment', RESEED, 0)"
    cursor.execute(command)
    conn.commit()

with conn.cursor() as cursor: #取出資料表的資料
    SQL_output = """SELECT store_info_id, url FROM store_info"""   
    command = SQL_output
    cursor.execute(command)
    db = cursor.fetchall()

   
#open uml
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")  #開啟瀏覽器
for index, row in enumerate(db):
    print("目前：" + str(index+1))
    store_info_id = row[0]
    url = row[1]
    
    driver.get(url)
    time.sleep(1)

    for x in range(20):
        try :
            btn1 = driver.find_element("xpath","/html/body/div[1]/div/div/div/div[2]/main/div[2]/div[2]/div[6]/div[3]/div[3]/button")
            btn1.click()
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
            
        #create_time 
        date = review.find("div",class_="date").text
        create_time= re.search(r"(\d{4}/\d{1,2}/\d{1,2})",date).group(0)

        #score
        score = review.find("div",class_="text")
        if score == None: #判斷有沒有餐廳評價
           score = "999"
        else:
            score= float(score.string)
            
        #[content]
        content = review.find("div", class_="message").text
        content = str(content)

        r = review.find("div",class_="action-outer").text
        r = str(r)
        
        for x in range(len(r)):
            content = content.replace(r[x],"")
      
        #存入資料庫
        with conn.cursor() as cursor:
            try:
                SQL_input = """Insert Into store_external_comment(store_info_id, create_time, score, [content])
                             Values({},CONVERT(DATETIME,'{}', 121),{}, N'{}')""".format(store_info_id,create_time,score,content)
                command = SQL_input
                cursor.execute(command)
                conn.commit()
            except Exception as ex:
                print(SQL_input)
                print(ex)
            
        s2 = pd.Series([store_info_id,create_time,score,content],index=["store_info_id","create_time","score","content"])
        df1 = df1.append(s2, ignore_index=True)
        
        print("完成第"+f"{comment}"+"條")
        comment +=1
    
    print("結束：" + str(index+1))
    print(" ") #分段落
df1.to_csv("Comment.csv", encoding="utf-8", index=False)
driver.close() 
