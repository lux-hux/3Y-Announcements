# Import packages

import tabula
import getpass
import glob
import pandas as pd
import os 
import openpyxl
from datetime import date
import time

# Set current working directory 

user = getpass.getuser()

# Change to folder where current announcements are stored 

announcements_directory  = '2022-3-7-3Y Announcements'

os.chdir('/Users/' + user + '/Downloads/' + announcements_directory)

# Create dataframe for storing results 

announcement_extract_df = pd.DataFrame(columns=['File Name'])

glob.glob('*.pdf')
directory = glob.glob('*.pdf')

counter = 0

for p in directory:

    print('Extracting PDF for file titled: ', p)

    tabula.convert_into('/Users/' + user + '/Downloads/' + announcements_directory + '/' + p, p + ".csv", output_format="csv", pages='all')

    announcement_df = pd.read_csv(p + ".csv", names=['0','1','2','3','4', '5', '6']) 

    row_iter = announcement_df.shape[0]

    column_iter = announcement_df.shape[1]

    for l in range(row_iter - 1):

        for y in range(-1,3):

                        if 'Name of Director' in str(announcement_df.iloc[l, y]):

                            counter += 1

                            announcement_extract_df.loc[counter, 'File Name'] = str(p)

                            for t in range (1,column_iter - 1):

                                if str(announcement_df.iloc[l, y + t]) == "":

                                 continue 

                                else: 

                                 announcement_extract_df.loc[counter, 'Name of director'] = str(announcement_df.iloc[l, y + t])

                                 break

                        if 'Number acquired' in str(announcement_df.iloc[l, y]):

                            for t in range (1,column_iter - 1):

                                if str(announcement_df.iloc[l, y + t]) == "nan":

                                 continue 

                                else: 

                                 announcement_extract_df.loc[counter, 'Number acquired'] = str(announcement_df.iloc[l, y + t])

                                 print(str(announcement_df.iloc[l, y + t]))

                                 break

                        if 'Number disposed' in str(announcement_df.iloc[l, y]):

                            for t in range (1,column_iter - 1):



                                if str(announcement_df.iloc[l, y + t]) == "nan":



                                 continue 

                                else: 

                                 announcement_extract_df.loc[counter, 'Number disposed'] = str(announcement_df.iloc[l, y + t])

                                 print(str(announcement_df.iloc[l, y + t]))

                                 break

                        if str(announcement_df.iloc[l, y]) == 'Class': 

                            for t in range (1,column_iter - y):

                                if str(announcement_df.iloc[l, y + t]) == "nan":

                                 continue 

                                else: 

                                 announcement_extract_df.loc[counter, 'Class'] = str(announcement_df.iloc[l, y + t])

                                 print(str(announcement_df.iloc[l, y + t]))

                                 break


rights_search = ['Rights', 'rights']

rights_search_sep = '|'.join(rights_search)

shares_search = ['Shares', 'shares']

shares_search_sep = '|'.join(shares_search)

announcement_extract_df['Rights - Class'] = announcement_extract_df['Class'].str.contains(rights_search_sep)

announcement_extract_df['Shares - Class'] = announcement_extract_df['Class'].str.contains(shares_search_sep)

announcement_extract_df['Shares - Disposed'] = announcement_extract_df['Number acquired'].str.contains(shares_search_sep)

announcement_extract_df['Shares - Acquired'] = announcement_extract_df['Number disposed'].str.contains(shares_search_sep)

announcement_extract_df['Rights - Disposed'] = announcement_extract_df['Number acquired'].str.contains(rights_search_sep)

announcement_extract_df['Rights - Acquired'] = announcement_extract_df['Number disposed'].str.contains(rights_search_sep)

today = date.today()

announcement_extract_df.to_excel('OUTPUT_' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-' + 'announcement_extract.xlsx')
