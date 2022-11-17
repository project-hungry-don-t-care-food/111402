from lib2to3.pgen2 import driver
import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
from selenium import webdriver
import re
import datetime
import warnings
warnings.filterwarnings("ignore")
import csv
from connectdb import conn
import pandas as pd
df = pd.DataFrame(columns=["lat" ,"distance"])
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe") 
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

from math import*
def Distance1(lat1,lng1,lat2,lng2):# 第二種計算方法
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

with open('Restaurant data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader = csv.DictReader(csvfile)
    adr = []
    for i in reader:
        adr.append(i["餐廳地址"])

for address in adr:
    lat = get_coordinate(address) 
    a = lat[0:9]
    b = lat[10:]
    print(a,b)
    Lat_A = 25.05430; Lng_A=121.52221 # ntub
    Lat_B = float(a) ; Lng_B=float(b)  # 北京
    distance = Distance1(Lat_A,Lng_A,Lat_B,Lng_B)
    distance = f'{distance:.3f}km'

    s = pd.Series([lat,distance],index=["lat" ,"distance"])
    df = df.append(s, ignore_index=True)

df.to_csv("lat.csv", encoding="utf-8", index=False)
driver.close()


