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
df = pd.DataFrame(columns=["lat"])


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

with open('Restaurant data.csv', 'r',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
    reader = csv.DictReader(csvfile)
    adr = []
    for i in reader:
        adr.append(i["餐廳地址"])

for address in adr:
    distance = get_coordinate(address)
    s = pd.Series([distance],index=["lat"])
    df = df.append(s, ignore_index=True)
    
df.to_csv("lat.csv", encoding="utf-8", index=False)
driver.close()


