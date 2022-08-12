import os
import time
import requests
import zipfile
import csv
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

def binance_data_fetch(symbol, interval, save_dir):

    #Connection URL
    BASE_URL = "https://data.binance.vision/?prefix=data/spot/monthly/klines/" + symbol + "/" + interval + "/"

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
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, symbol + "-" + interval)

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
                zip_ref.extractall(save_dir)

            os.remove(filename)

    print(" ")

#Conversion to TSLab format
def csv2tslab(csv_dir, tslab_dir):
    files = [f for f in listdir(csv_dir) if isfile(join(csv_dir, f))]

    for file_name in files:
        data = pd.read_csv(csv_dir + file_name, header=None, usecols=[i for i in range(0,6)])
        data.insert(0, '', 0)
        dt = pd.to_datetime(data.iloc[:,1], unit='ms')

        data.iloc[:,0] = dt.dt.strftime('%m/%d/%Y')
        data.iloc[:,1] = dt.dt.strftime('%H:%M')

        data.to_csv(tslab_dir + file_name, sep=';', header=False, index=False)

#CSV merge
def merge_csv(src_dir, dst_dir, filename):
    files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]

    data_to_merge = []

    for file_name in files:
        data = pd.read_csv(src_dir + file_name, header=None)
        data_to_merge.append(data)
        os.remove(src_dir + file_name)

    merged_data= pd.concat(data_to_merge, axis=0, ignore_index=True)
    merged_data.to_csv(dst_dir + filename[:-4] + '_tmp.csv', sep=';', header=False, index=False)

    temp_filename = dst_dir + filename[:-4] + '_tmp.csv'

    with open(temp_filename, 'r') as infile, open(dst_dir + filename, 'w') as outfile:
        data = infile.read()
        data = data.replace('"', '')
        outfile.write(data)

    os.remove(temp_filename)



