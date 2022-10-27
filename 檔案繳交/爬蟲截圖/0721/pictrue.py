from urllib.request import urlopen
import  bs4
from bs4 import BeautifulSoup
import time
import pymssql
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
df = pd.DataFrame(columns=["餐廳連結"])

page =1

while 1:
    if page>=3:
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
        #存入資料庫
        try:
            if "'" in title:
                title = title.replace("'","''")
                link = link.replace("'","''")
                
                
        except Exception as ex:
            print(ex)
            
        
        s = pd.Series([link],index=["餐廳連結"])
        df = df.append(s, ignore_index=True)
    print("[" + str(page) + "]完成")
    page = page + 1
    time.sleep(1)
       
df.to_csv("Restaurant data.csv", encoding="utf-8", index=False)