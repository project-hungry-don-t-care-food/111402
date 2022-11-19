from os import times
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

start = time.time()

def get_coordinate(addr):
    driver.get("http://www.map.com.tw/")
    search = driver.find_element_by_id("searchWord")
    time.sleep(1)
    search.clear()
    time.sleep(5)
    search.send_keys(addr)
    driver.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click() 
    time.sleep(5)
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
    s = s*earth_radius*1000
    if s < 0:  
        return -s  
    else:  
        return s

with conn.cursor() as cursor: #先刪除資料表的資料
    command = "DELETE store_info; DBCC CHECKIDENT('store_info', RESEED, 0)"
    cursor.execute(command)
    conn.commit()

with open('Data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader = csv.DictReader(csvfile)
    title = []
    cre_time = []
    number = []
    adr = []
    score = []
    hour = []
    link = []
    appointed_str = []
    unknown_str = []
    for i in reader:
        title.append(i["store_name"])
        cre_time.append(i["create_time"])
        number.append(i["phone_number"])
        adr.append(i["address"])
        score.append(i["total_score"])
        hour.append(i["business_hour"])
        link.append(i["url"])
        appointed_str.append(i["is_appointed_store"])
        unknown_str.append(i["is_unknown_store"])

  
#open uml
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")  #開啟瀏覽器

for index, address in enumerate(adr):
    print("目前：" + str(index+1))
    store_name = title[index]
    create_time = cre_time[index]
    phone_number = number[index]
    address = adr[index]
    total_score = score[index]
    business_hour = hour[index]
    url = link[index]
    is_appointed_store=appointed_str[index]
    is_unknown_store=unknown_str[index]
#經緯度
    latitude_longitude = get_coordinate(address)
    log_lng = latitude_longitude.split(',')
    #25.04193588943503, 121.52562935866969
    #25.043097445288065, 121.52484239141924
    
    # distance
    lat_b = log_lng[0]
    lng_b = log_lng[1]
    Lat_A_1 = 25.04193; Lng_A_1 = 121.52562 # ntub 正門
    Lat_A_2 = 25.04309 ; Lng_A_2 = 121.52484 # ntub 後門
    Lat_A_3 = 25.04275; Lng_A_3 = 121.52612 # ntub 側門
    Lat_B = float(lat_b) ; Lng_B=float(lng_b)  # 地點

    dis1 = Distance1(Lat_A_1,Lng_A_1,Lat_B,Lng_B)
    dis2 = Distance1(Lat_A_2,Lng_A_2,Lat_B,Lng_B)
    dis3 = Distance1(Lat_A_3,Lng_A_3,Lat_B,Lng_B)
    distance = f'正門:{dis1:.0f}公尺,後門:{dis2:.0f}公尺,側門:{dis3:.0f}公尺'
    print(distance)
    with conn.cursor() as cursor:
        try:
            SQL_input = """INSERT INTO store_info(store_name, create_time, phone_number, address, total_score, business_hour, distance,latitude_longitude,url, is_appointed_store, is_unknown_store)
                Values(N'{}', CONVERT(DATETIME, '{}', 121), N'{}', N'{}',{},N'{}',N'{}',N'{}',N'{}',{},{})""".format(store_name,create_time,phone_number,address,total_score,business_hour,distance,latitude_longitude,url,is_appointed_store,is_unknown_store)
            command = SQL_input
            cursor.execute(command)
            conn.commit()
        except Exception as ex:
            print(ex)
            print(SQL_input)
    
driver.close() 
    
    