from bs4 import BeautifulSoup
import requests
import re 
import pandas as pd
import numpy as np
import os
from datetime import date
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pyautogui as pyauto  
import shutil
import glob
import getpass
import pygetwindow as gw


# Change directory to where the script is located

class ASX_Announcement_Scrape():
    def __init__(self, url, directory_name):
        self.url = url
        self.announcements_df = pd.DataFrame(columns=['ASX Code', 'Description', 'Link', 'Time', 'Price Sensitive'])
        self.announcements_dir_df = pd.DataFrame(columns=['ASX Code', 'Description', 'Link', 'Time', 'Price Sensitive'])
        self.today = date.today()
        self.driver = None
        self.user = getpass.getuser()
        self.full_path = os.path.realpath(__file__) 
        self.file_path =os.path.dirname(self.full_path)
        self.pdf_folder = str(directory_name)
        os.chdir(self.file_path)


    def find_announcements(self):
            
        result = requests.get(self.url)

        doc = BeautifulSoup(result.text, "html.parser")

        # Uncomment to see the HTML cleaned by BeautifulSoup: 
        #print(doc.prettify())
        # LINK & DESCRIPTION COLUMNS -  Iterate through all instances of 'href' nested within 'a' tag and save the results to the 'Announcements' dataframe:
        counter = 0

        for a in doc.find_all('a', href=True):
            if 'displayAnnouncement'in a['href']: 
                counter += 1
                #print(a['href'], counter)
                self.announcements_df.loc[counter,'Link'] = (a['href'])
                self.announcements_df.loc[counter, 'Description'] = a.text
                #print(a.text)

        # ASX CODE, TIME, AND PRICE SENSITIVE COLUMNS - Iterate through all instances 'td' nested in 'tr' tags and save the results to the 'Announcements' dataframe:

        counter = 0

        for tr in doc.find_all('tr'):
            if tr.find('td') != None:
                counter += 1
                varb = tr.find('td')
                #print('ticker: ', varb, counter)
                self.announcements_df.loc[counter, 'ASX Code'] = str(varb)
                self.announcements_df.loc[counter, 'Time'] = tr.find('span').text
                if 'images/icon-price-sensitive.svg' in str(tr.find('img')):
                    self.announcements_df.loc[counter, 'Price Sensitive'] = str(tr.find('img'))
        return self.announcements_df


    def clean_df(self, data_frame = None):

        announcements_df = pd.DataFrame()

        if data_frame is None:
            announcements_df = self.announcements_df
            
        else:
            announcements_df = data_frame 
            print("Cleaning input data frame")

        announcements_df['ASX Code'] = announcements_df['ASX Code'].str.replace('<td>', '')

        announcements_df['ASX Code'] = announcements_df['ASX Code'].str.replace('</td>', '')
        
        announcements_df['Price Sensitive'] = np.where(announcements_df['Price Sensitive'].notnull(), '■$■' ,'')

        announcements_df['Description'] = announcements_df['Description'].astype('string')

        # Could learn some regex to better clean this, such as removing 'KB' after the new lines

        announcements_df['Description'] = announcements_df['Description'].str.replace(r'page.*', '', regex=True)

        announcements_df.to_csv('OUTPUT_' + str(self.today.year) + '-' + str(self.today.month) + '-' + str(self.today.day) + '-' + 'Announcements+Text.csv')

        self.announcements_df = announcements_df
        
        return announcements_df


    def isolate_dir(self, data_frame = None):

        # Isolate announcements concerning 'Change of Director's Interest' also known as '3Y' and save in new dataframe 

        announcements_dir_df = pd.DataFrame()

        if data_frame is None:
            announcements_df_dir = self.announcements_df 
        else:
            announcements_df_dir = data_frame 
            print("Isolating input data frame")

        announcements_dir_df = self.announcements_df[self.announcements_df["Description"].str.contains("Change of Director's Interest Notice|Appendix 3Y")]

        announcements_dir_df = announcements_dir_df.reset_index(drop=True)
        
        announcements_dir_df.to_csv('OUTPUT_' + str(self.today.year) + '-' + str(self.today.month) + '-' + str(self.today.day) + '-' + 'Announcements_ALL.csv')

        self.announcements_dir_df = announcements_dir_df

        return announcements_dir_df

    def launch_webdriver(self):
        self.driver = webdriver.Firefox(executable_path=self.file_path + '/geckodriver')
 
    def scrape_links(self, data_frame = None):

        announcements = pd.DataFrame()

        if data_frame is None:
            announcements = self.announcements_dir_df
        else:
            announcements = data_frame
            print("scraping input data frame")         

        try:
            os.mkdir('/Users/' + self.user + '/Downloads/' + str(self.today.year) + '-' + str(self.today.month) + '-' + str(self.today.day) + '-3Y Announcements')
        except OSError as error:
            print(error)    

        os.chdir('/Users/' + self.user + '/Downloads')

        # Iterate through 3Y announcements

        print(announcements.index)

        for link in announcements.index[0:]:

        # For each announcement, save the ASX code to variable 

            ticker = str(announcements.loc[link, 'ASX Code'])
            link_no = str(link)

        # Navigate to the announcement's url 
            self.driver.get('https://www.asx.com.au/' + announcements.loc[link, 'Link'])

        # The first visit to an announcement pdf has a terms and conditions page where the form must be first accepted before accessing

            if link == 0: 

                print('First download of the session')

                element = self.driver.find_element(By.XPATH, "/html/body/div/form/input[2]")

                element.click()

        # Check if download button present before continuing 

            while not EC.presence_of_element_located((By.XPATH, '//*[@id="download"]')):

                time.sleep(0.5)
                print("Waiting for prescence of download button")

            element2 = self.driver.find_element(By.XPATH,'//*[@id="download"]')
            element2.click()

        # Pyauto (Pyautogui) does not send keys specifically to the window

        # To-do - identify specific window to send keys to so that code can run in background

            time.sleep(1)

            pyauto.press('enter') 

            time.sleep(0.5)

        # Check if downloaded file is present before continuing 

            end_time = time.time() + 10 

            while not glob.glob("*.pdf"):

                print("Waiting for file to finish downloading before continuing")

                time.sleep(1)

                if time.time() > end_time:

                    print("File not found within time")

                    exit()

        # Rename downloaded file

            directory = glob.glob('*.pdf')

            for i in directory:

                if i.endswith(".pdf"):

                    os.rename(i, link_no + '-' + ticker + ".pdf")

        # Move the announcement pdf to the directory created earlier
        
            shutil.move(link_no + '-' + ticker + ".pdf", str(self.today.year) + '-' + str(self.today.month) + '-' + str(self.today.day) + '-3Y Announcements')      






