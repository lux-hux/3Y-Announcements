from bs4 import BeautifulSoup, NavigableString, Tag

import requests

import pandas as pd

url = "https://www.asx.com.au/asx/v2/statistics/todayAnns.do"

result = requests.get(url)

#print(result.text)

Announcemnents = pd.DataFrame(columns=['ASX Code', 'Description', 'Link', 'Time', 'Price Senstiive'])


doc = BeautifulSoup(result.text, "html.parser")

print(doc.prettify())

counter = 0

for a in doc.find_all('a', href=True):
    if 'displayAnnouncement'in a['href']: #and a !=None:
        counter += 1
        print(a['href'], counter)
        Announcemnents.loc[counter,'Link'] = (a['href'])
        Announcemnents.loc[counter, 'Description'] = a.text
        #print(a.text)

counter = 0

for tr in doc.find_all('tr'):
   if tr.find('td') != None:
        counter += 1
        varb = tr.find('td')
        print('ticker: ', varb, counter)
        Announcemnents.loc[counter, 'ASX Code'] = str(varb)
        Announcemnents.loc[counter, 'Time'] = tr.find('span').text
        if 'images/icon-price-sensitive.svg' in str(tr.find('img')):
         Announcemnents.loc[counter, 'Price Senstiive'] = str(tr.find('img'))
         print('price sensitive')

Announcemnents.to_csv('OUTPUT_Announcements+Text.csv')