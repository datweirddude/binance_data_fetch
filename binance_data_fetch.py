import os
import time
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

SYMBOL = "CTXCUSDT"      #Currency pair to download
INTERVAL = "5m"         #Time interval

#Connection URL
BASE_URL = "https://data.binance.vision/?prefix=data/spot/monthly/klines/" + SYMBOL + "/" + INTERVAL + "/"

#Save directory
SAVE_DIR = "D:/Research/crypto/historical_data/"

#Establish a connection
print("Running headless Chrome...")
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(executable_path = "D:/chromedriver.exe", options = options)

#Send GET
print ("Reading list from " + BASE_URL)
driver.get(BASE_URL)

#Wait until Javascript renders all the links (may require more than 5 seconds)
print("Waiting for download: 5", end="")
print("\r", end="")
for seconds in range(1, 6):
    time.sleep(1)
    print("Waiting for download: " + str(5-seconds), end="")
    print("\r", end="")

#Find all download links in page
links = driver.find_elements(By.PARTIAL_LINK_TEXT, SYMBOL + "-" + INTERVAL)

link_num = int(len(links)/2)
link_cnt = 1;

#Download and unzip all files
for link in links:
    link_text = link.get_attribute("href")
    if link_text[-3:] == "zip":
        ix = link_text.rfind("/")
        filename = link_text[ix+1:]
        print("\r", end="")
        print("Downloading data: " + filename + "(" + str(link_cnt) + " of " + str(link_num) + ")", end="")
        link_cnt += 1
        response = requests.get(link_text)
        open(filename, "wb").write(response.content)

        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(SAVE_DIR + SYMBOL)

        os.remove(filename)




