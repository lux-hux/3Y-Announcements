from bs4 import BeautifulSoup
import requests
import re 
import pandas as pd
import numpy as np
from datetime import date
import time
import pyautogui as pyauto  


import os

full_path = os.path.realpath(__file__)
file_path = os.path.dirname(full_path)

os.chdir(file_path)

# Dataframe to save scraped results:


# Announcements page: 

url = 'https://www.asx.com.au/asx/statistics/displayAnnouncement.do?display=pdf&idsId=02495247' 


# import webdriver
from selenium import webdriver
  
# create webdriver object
driver = webdriver.Firefox(executable_path=file_path + '/geckodriver')
  
# get geeksforgeeks.org
driver.get('https://www.asx.com.au/asx/statistics/displayAnnouncement.do?display=pdf&idsId=02495247')


#time.sleep(6)




  
# get element 
#element = driver.find_element_by_link_text("Courses")
  
# click the element
#element.click()

print('sleep.....')

element = driver.find_element_by_xpath("/html/body/div/form/input[2]")



#time.sleep(3)

print('sleep.....')
# elements = driver.find_elements_by_id("link")


element.click()

download_dir = file_path  # for linux/*nix, download_dir="/usr/Public"

#time.sleep(1)

element2 = driver.find_element_by_xpath('//*[@id="download"]')

element2.click()

time.sleep(1)

pyauto.press('enter') 