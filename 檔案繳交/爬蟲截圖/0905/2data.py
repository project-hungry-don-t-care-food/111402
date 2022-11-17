from faulthandler import disable
import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver
import re
import datetime
import warnings
warnings.filterwarnings("ignore")
import csv
from math import*
from connectdb import conn
import pandas as pd
df1 = pd.DataFrame(columns=["store_name","create_time","phone_number","address","total_score",
        "business_hour","distance","latitude_longitude","url","is_appointed_store","is_unknown_store"])

def get_coordinate(addr):
    driver.get("http://www.map.com.tw/")
    search = driver.find_element_by_id("searchWord")
    search.clear()
    time.sleep(3)
    search.send_keys(addr)
    driver.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click() 
    time.sleep(3)
    iframe = driver.find_elements_by_class_name("winfoIframe")[0]
    driver.switch_to.frame(iframe)
    coor_btn = driver.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
    coor_btn.click()
    coor = driver.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr[2]/td")

    coor = coor.text.strip().split(" ")
    lat = coor[-1].split("：")[-1]
    log = coor[0].split("：")[-1]
    conb = lat + "," +log
    return conb

def Distance1(lat1,lng1,lat2,lng2):# 計算
    radlat1 = radians(lat1)  
    radlat2 = radians(lat2)  
    a = radlat1-radlat2  
    b = radians(lng1)-radians(lng2)  
    s = 2*asin(sqrt(pow(sin(a/2),2)+cos(radlat1)*cos(radlat2)*pow(sin(b/2),2)))  
    earth_radius = 6378.137  
    s = s*earth_radius  
    if s < 0:  
        return -s  
    else:  
        return s

with conn.cursor() as cursor: #先刪除資料表的資料
    command = "DELETE store_info; DBCC CHECKIDENT('store_info', RESEED, 0)"
    cursor.execute(command)
    conn.commit()

# 開啟 CSV 檔案
with open('Restaurant data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader = csv.DictReader(csvfile)
    title = []
    link = []
    adr = []
    star = []
    for i in reader:
        title.append(i["餐廳名稱"])
        link.append(i["餐廳連結"])
        adr.append(i["餐廳地址"])
        star.append(i["餐廳評價"])
  
#open uml
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")  #開啟瀏覽器
for index, row in enumerate(link):
    print("目前：" + str(index+1))
    url=(row[0:])
    store_name = title[index]
    address = adr[index]
    url = link[index]
    total_score = star[index]
    is_appointed_store=0
    is_unknown_store=0

    driver.get(url)
    time.sleep(1)

    soup = Soup(driver.page_source,"lxml")
    try :
        btn1 = driver.find_element_by_class_name("phone-wrapper")
    except:
        print("沒有電話")
        phone_number = "999"

    #create_time
    create_time = datetime.datetime.now().replace(microsecond=0)
                                
    # phone_number
    telphone = soup.find_all("div",class_="phone-wrapper")
    for telnum in telphone:
        phone_number = telnum.find("a").text
    
    print("結束：" + str(index+1))
    print(" ") #分段落
    #business_hour
    business_hour = ""

    try :
        btn2 = driver.find_element("xpath", "/html/body/div[1]/div/div/div/div[2]/main/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/button")
        btn2.click()
    except:
        print("沒有營業時間的按鈕")

    time.sleep(1)

    soup = Soup(driver.page_source,"lxml")                         
    #營業時間 
    opentimes = soup.find_all("div",class_="jss76 jss116 jss119 jss124 jss125")
    for index, opentime in enumerate(opentimes):
        #opentime
        opentime = opentime.find("div",class_="weekday-hours").text
    
        timelist = opentime.split(" ")
        if timelist[1] == "休息":
            continue
        
        # 處理星期數
        if timelist[0] == "星期一":
            weekday = "1:"
        if timelist[0] == "星期二":
            weekday = "2:"
        if timelist[0] == "星期三":
            weekday = "3:"
        if timelist[0] == "星期四":
            weekday = "4:"
        if timelist[0] == "星期五":
            weekday = "5:"
        if timelist[0] == "星期六":
            weekday = "6:"
        if timelist[0] == "星期日":
            weekday = "7:"
        business_hour += weekday
        
        # 處理每天的時間
        for i in range(1, len(timelist)):
            if i >= 2:
                business_hour += "," + weekday

            if timelist[i]=="24小時營業":
                business_hour += '00002359'
            else:
                business_hour += timelist[i][0:2] + timelist[i][3:5] + timelist[i][6:8] + timelist[i][9:11]

        # 如果是最後一天就不加逗號
        if index == len(opentimes) - 1:
            pass
        else:
            business_hour += ","
    #經緯度
    latitude_longitude = get_coordinate(address)

    # distance
    lat_b = latitude_longitude[0:9]
    lng_b = latitude_longitude[10:]
    Lat_A = 25.05430; Lng_A=121.52221 # ntub
    Lat_B = float(lat_b) ; Lng_B=float(lng_b)  # 地點
    distance = Distance1(Lat_A,Lng_A,Lat_B,Lng_B)
    distance = f'{distance:.3f}km'
    
    with conn.cursor() as cursor:
        try:
            SQL_input = """INSERT INTO store_info(store_name, create_time, phone_number, address, total_score, business_hour, distance,latitude_longitude,url, is_appointed_store, is_unknown_store)
                Values(N'{}', CONVERT(DATETIME, '{}', 121), N'{}', N'{}',{},N'{}',N'{}',N'{}',N'{}',{},{})""".format(store_name,create_time,phone_number,address,total_score,business_hour,distance,latitude_longitude,url,is_appointed_store,is_unknown_store)
            command = SQL_input
            cursor.execute(command)
            conn.commit()
            print(True)
                
        except Exception as ex:
            print(ex)
            print(SQL_input)
    
    s2 = pd.Series([store_name,create_time,phone_number,address,total_score,business_hour,distance,latitude_longitude,url,is_appointed_store,is_unknown_store],
        index=["store_name","create_time","phone_number","address","total_score","business_hour",
            "distance","latitude_longitude","url","is_appointed_store","is_unknown_store"])
    df1 = df1.append(s2, ignore_index=True)
    
df1.to_csv("Data.csv", encoding="utf-8", index=False)
driver.close() 
  
