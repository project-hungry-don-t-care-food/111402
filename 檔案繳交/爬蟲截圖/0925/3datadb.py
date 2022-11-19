from os import times
from turtle import title
from unicodedata import name
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
import pymssql
import pandas as pd
df1 = pd.DataFrame(columns=["address","distance","latitude_longitude"])

def conn(): #連接資料庫
    connect = pymssql.connect('ntubfood.westus2.cloudapp.azure.com', 'sa', 'ntub_pj123456', 'Food')
    if connect:
        print("連線成功!")
    return connect
conn = conn()

start = time.time()

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

with open('lat and long.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader = csv.DictReader(csvfile)
    title_na = []
    adr = []
    Lat = []
    Long = [] 
    for i in reader:
        title_na.append(i["store_name"])
        adr.append(i["address"])
        Lat.append(i["Latitude"])
        Long.append(i["Longitude"]) 

    for index, row in enumerate(adr):
        store_name = title_na[index]
        address = adr[index]
        Latitude = Lat[index]
        Longitude = Long[index]
        print("目前：" + str(index+1))
        #經緯度
        latitude_longitude = Latitude + "," + Longitude
        print(latitude_longitude)
        log_lng = latitude_longitude.split(',')

        if "'" in store_name:
            store_name = store_name.replace("'","''")
        
        # distance
        lat_b = log_lng[0]
        lng_b = log_lng[1]
        Lat_A_1 = 25.04193 ; Lng_A_1 = 121.52562 # ntub 正門
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
                SQL_update ="UPDATE store_info SET distance=N'" + distance + "',latitude_longitude = '" + latitude_longitude +"' WHERE store_name=N'" + store_name+"'"
                command = SQL_update
                cursor.execute(command)
                conn.commit()
            except Exception as ex:
                print(ex)
                print(SQL_update)

        s2 = pd.Series([address,distance,latitude_longitude],index=["address","distance","latitude_longitude"])
        df1 = df1.append(s2, ignore_index=True)
df1.to_csv("Data_LAT_LONG.csv", encoding="utf-8", index=False)

    
        
 
    
    