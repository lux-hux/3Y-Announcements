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
import pdfplumber as plumb


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

Announcemnents['Price Sensitive'] = np.where(Announcemnents['Price Sensitive'].notnull(), '■$■' ,'')

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


Announcemnents_directors.to_csv('OUTPUT_' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-' + 'Announcements_Directors+Text.csv')

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

    time.sleep(2)
    pyauto.press('enter') 

    # Move recently downloaded pdf file into previously created directory

    glob.glob('*.pdf')

    directory = glob.glob('*.pdf')

    for i in directory:

     if i.endswith(".pdf"):

      os.rename(i, link_no + '-' + ticker + ".pdf")

    shutil.move(link_no + '-' + ticker + ".pdf", str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-3Y Announcements')

os.chdir('/Users/' + user + '/Downloads/' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-3Y Announcements')

glob.glob('*.pdf')
directory = glob.glob('*.pdf')

results = pd.DataFrame(columns=['File Name', 'Name of Director', 'Date of last notice', 'Interest', 'Nature of Interest', 'Date of change', 'No. of securities held prior to change', 'Class', 'Number acquired', \
    'Number disposed', 'Value/Consideration', 'No. of securities held after change'])

counter = 0

for p in directory:
    print('PDF file: ', p)
    
    with plumb.open('/Users/' + user + '/Downloads/' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-3Y Announcements/' + p) as pdf:

     counter += 1

     results.loc[counter, 'File Name'] = str(p)

     pages = pdf.pages

     for i,pg in enumerate(pages):

      page = pdf.pages[i]

    #   text = page.extract_text()
    #   table = page.extract_table()

      tables = page.find_tables()

  
      for table_iter in range(0, len(tables)):

          t2_content = tables[table_iter].extract(x_tolerance = 5)

          #print(t2_content)

          for list_iter in t2_content:

                    if list_iter[0] == 'Direct or indirect interest':
                        results.loc[counter, 'Interest'] = str(list_iter[1])

                    if 'Nature of indirect interest' in list_iter[0]:
                        results.loc[counter, 'Nature of Interest'] = str(list_iter[1])

                    if 'Detail of contract' in list_iter[0]:
                        break

                    if 'Date of change' in list_iter[0]:
                        results.loc[counter, 'Date of change'] = str(list_iter[1])

                    if 'No. of securities held prior to change' in list_iter[0]:
                        results.loc[counter, 'No. of securities held prior to change'] = str(list_iter[1])

                    if 'Class' in list_iter[0]:
                        results.loc[counter, 'Class'] = str(list_iter[1])

                    if 'Number acquired' in list_iter[0]:
                        results.loc[counter, 'Number acquired'] = str(list_iter[1])

                    if 'Number disposed' in list_iter[0]:
                        results.loc[counter, 'Number disposed'] = str(list_iter[1])

                    if 'Value/Consideration' in list_iter[0]:
                        results.loc[counter, 'Value/Consideration'] = str(list_iter[1])

                    if 'after change' in list_iter[0]:
                        results.loc[counter, 'No. of securities held after change'] = str(list_iter[1])  

                    if 'Name of Director' in list_iter[0]:
                        results.loc[counter, 'Name of Director'] = str(list_iter[1])

                    if 'Date of last notice' in list_iter[0]:
                        results.loc[counter, 'Date of last notice'] = str(list_iter[1])  

results.to_csv('OUTPUT_announcement_summary.csv')