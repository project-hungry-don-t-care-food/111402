from urllib.request import urlopen
import  bs4
from bs4 import BeautifulSoup
import time
import pymssql
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
df = pd.DataFrame(columns=["id","餐廳名稱","餐廳評價","餐廳地址","餐廳連結"])

page =1

def conn(): #連接資料庫
    connect = pymssql.connect('(local)', 'sa', 'Food111402', 'Food')
    if connect:
        print("連線成功!")
    return connect
conn = conn()

with conn.cursor() as cursor: #先刪除restaurant_list的資料
    command = "Delete From restaurant_list"
    cursor.execute(command)
    conn.commit()

while 1:
    if page>=2:
        break
    # 利用增加的數字製作網
    url = "https://ifoodie.tw/explore/%E5%8F%B0%E5%8C%97%E5%B8%82/%E4%B8%AD%E6%AD%A3%E5%8D%80/list?"+  f'page={page}'
    response = urlopen(url)
    html = BeautifulSoup(response, "html.parser")
    no_result = html.find("div", class_ = "no-result-title")
    
    #判斷是否為最後一頁
    if no_result != None:
        if "沒有搜尋結果" in no_result.string: 
            print("最後一頁了")
            break
    
    print("[正在處理]", url)
  
  
    cards = html.find_all("div",class_="restaurant-info")
    for card in cards:
        #編號
        rest_id = card.find("span",class_="index").text
        rest_id = int(float(rest_id))

        # 餐廳名稱
        title = card.find("a", class_="title-text")
        link = "https://ifoodie.tw" + title.get("href")
        title = str(title.string)
        
        
        # 餐廳評價
        stars = card.find("div", class_= "text")
        if stars == None: #判斷有沒有餐廳評價
            stars = "999"
        else:
            stars = float(stars.string)
            
        # 餐廳地址
        address = card.find("div", class_="address-row")
        address = address.string
        
        #存入資料庫
        with conn.cursor() as cursor:
            try:
                if "'" in title:
                    title = title.replace("'","''")
                    link = link.replace("'","''")
                
                SQL_input = """Insert Into restaurant_list (id, 餐廳名稱, 餐廳評價, 餐廳地址, 餐廳連結)
                        Values ({}, N'{}', {}, N'{}', '{}')""".format(rest_id,title,stars,address,link)
                command = SQL_input
                cursor.execute(command)
                conn.commit()
            except Exception as ex:
                print(rest_id)
                print(title)
                print(link)
                print(SQL_input)
                print(ex)
        
        s = pd.Series([rest_id,title, stars, address, link],index=["id","餐廳名稱","餐廳評價","餐廳地址","餐廳連結"])
        df = df.append(s, ignore_index=True)
    print("[" + str(page) + "]完成")
    page = page + 1
    time.sleep(1)
       
df.to_csv("Restaurant data.csv", encoding="utf-8", index=False)