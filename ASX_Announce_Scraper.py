from bs4 import BeautifulSoup
import requests
import re 
import pandas as pd
import numpy as np
import os
from datetime import date
import time
from selenium import webdriver
import pyautogui as pyauto  
import shutil
import glob
import getpass


# Change directory to where the script is located

full_path = os.path.realpath(__file__)
file_path = os.path.dirname(full_path)

os.chdir(file_path)

# Dataframe to save scraped results:

Announcemnents = pd.DataFrame(columns=['ASX Code', 'Description', 'Link', 'Time', 'Price Sensitive'])

# Announcements page: 

url = "https://www.asx.com.au/asx/v2/statistics/todayAnns.do"

result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")

# Uncomment to see the HTML cleaned by BeautifulSoup: 
#print(doc.prettify())

# LINK & DESCRIPTION COLUMNS -  Iterate through all instances of 'href' nested within 'a' tag and save the results to the 'Announcements' dataframe:

counter = 0

for a in doc.find_all('a', href=True):
    if 'displayAnnouncement'in a['href']: 
        counter += 1
        #print(a['href'], counter)
        Announcemnents.loc[counter,'Link'] = (a['href'])
        Announcemnents.loc[counter, 'Description'] = a.text
        #print(a.text)

# ASX CODE, TIME, AND PRICE SENSITIVE COLUMNS - Iterate through all instances 'td' nested in 'tr' tags and save the results to the 'Announcements' dataframe:

counter = 0

for tr in doc.find_all('tr'):
   if tr.find('td') != None:
        counter += 1
        varb = tr.find('td')
        #print('ticker: ', varb, counter)
        Announcemnents.loc[counter, 'ASX Code'] = str(varb)
        Announcemnents.loc[counter, 'Time'] = tr.find('span').text
        if 'images/icon-price-sensitive.svg' in str(tr.find('img')):
         Announcemnents.loc[counter, 'Price Sensitive'] = str(tr.find('img'))
         #print('price sensitive')


# Clean dataframe 

Announcemnents['ASX Code'] = Announcemnents['ASX Code'].str.replace('<td>', '')

Announcemnents['ASX Code'] = Announcemnents['ASX Code'].str.replace('</td>', '')

Announcemnents['Price Sensitive'] = np.where(Announcemnents['Price Sensitive'].notnull(), '???$???' ,'')

Announcemnents['Description'] = Announcemnents['Description'].astype('string')

# Could learn some regex to better clean this, such as removing 'KB' after the new lines

Announcemnents['Description'] = Announcemnents['Description'].str.replace(r'page.*', '', regex=True)

# Save results dataframe to a .csv file: 

#print(Announcemnents.head())

today = date.today()

Announcemnents.to_csv('OUTPUT_' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-' + 'Announcements+Text.csv')

# Isolate announcements concerning 'Change of Director's Interest' also known as '3Y' and save in new dataframe 

Announcemnents_directors = Announcemnents[Announcemnents["Description"].str.contains("Change of Director's Interest Notice|Appendix 3Y")]

Announcemnents_directors = Announcemnents_directors.reset_index(drop=True)


Announcemnents_directors.to_csv('OUTPUT_' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-' + 'Announcements_ALL.csv')

# Create new directory in donwloads folder to save the downloaded pdf's in

user = getpass.getuser()
try:
    os.mkdir('/Users/' + user + '/Downloads/' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-3Y Announcements')
except OSError as error:
    print(error)    

os.chdir('/Users/' + user + '/Downloads')

# Selenium's geckodriver saved alongside script in 'file_path'

driver = webdriver.Firefox(executable_path=file_path + '/geckodriver')

# Iterate through 3Y announcements

for link in Announcemnents_directors.index[0:]:
    
    # For each announcement, save the ASX code to variable 

    ticker = str(Announcemnents_directors.loc[link, 'ASX Code'])
    link_no = str(link)
    
    # Navigate to the announcement's url 
    driver.get('https://www.asx.com.au/' + Announcemnents_directors.loc[link, 'Link'])

    # The first visit to an announcement pdf has a terms and conditions page where the form must be first accepted before accessing

    if link == 0: 
        print('First download of the session')

        element = driver.find_element_by_xpath("/html/body/div/form/input[2]")

        element.click()

     # Click browser's download button
    element2 = driver.find_element_by_xpath('//*[@id="download"]')

    element2.click()

    # Wait two seconds in order to allow download pop-up to appear or for the previous download to complete before clicking enter 
    # May need additional wait time if download speed is slower. ** Alternate code would check whether file had completed downloading
    # before continuing. 

    time.sleep(1)

    pyauto.press('enter') 

    time.sleep(2)

    # Move recently downloaded pdf file into previously created directory

    glob.glob('*.pdf')

    directory = glob.glob('*.pdf')

    for i in directory:

     if i.endswith(".pdf"):

      os.rename(i, link_no + '-' + ticker + ".pdf")

      # Move the announcement pdf to the directory created earlier 

    shutil.move(link_no + '-' + ticker + ".pdf", str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-3Y Announcements')
