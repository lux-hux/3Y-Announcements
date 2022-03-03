from bs4 import BeautifulSoup
import requests
import re 
import pandas as pd
import numpy as np
import os
from datetime import date

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

print(Announcemnents.head())

today = date.today()

Announcemnents.to_csv('OUTPUT_' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-' + 'Announcements+Text.csv')

Announcemnents_directors = Announcemnents[Announcemnents["Description"].str.contains("Change of Director's Interest Notice|Appendix 3Y")]

Announcemnents_directors.to_csv('OUTPUT_' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-' + 'Announcements_Directors+Text.csv')