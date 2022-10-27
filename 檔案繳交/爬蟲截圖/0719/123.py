from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests , bs4
from bs4 import BeautifulSoup as Soup
import time
import re

import pandas as pd
df1 = pd.DataFrame(columns=["date","reviews"])


#open uml
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")  #開啟瀏覽器
url = "https://ifoodie.tw/restaurant/61dd2292baf6d30524a2ac37-%E9%90%98%E4%BA%88%E5%8E%9F%E5%91%B3%E7%95%B6%E6%AD%B8%E9%B4%A8-%E5%85%AC%E9%A4%A8%E5%BA%97"
driver.get(url)
time.sleep(1)

element = WebDriverWait(driver,10).until(EC.presence_of_element_located(By.CLASS_NAME,'btn-more-checkin-wrapper'))
 
print(type(element))
'''
except:
    print("An exception occurred")
else:
    button = driver.find_element_by_class_name("btn-more-checkin-wrapper")
    button.click()
    time.sleep(3)
'''
   
        
     
      
