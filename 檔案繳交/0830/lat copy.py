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

# 開啟 CSV 檔案

with conn.cursor() as cursor:
    try:
        SQL_input = """INSERT INTO store_info(store_name, create_time, phone_number,distance)Values(N"123456","201210","25151","25.046386,121.51074")"""
        command = SQL_input
        cursor.execute(command)
        conn.commit()
        print(True)
                    
    except Exception as ex:
        print(ex)
        print(SQL_input)



