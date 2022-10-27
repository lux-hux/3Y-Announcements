# ASX-3Y-Announcement-Scraper+Extractor

### Background

The Australian stock exchange requires listed companies to inform the market whenever their directors transact in company shares. Directors buying (selling) shares is a potential buy (sell) signal for investors because directors, as company insiders, presumably have a strong understanding of the company's future profitability. The company must lodge an announcement to the market titled an 'Appendix 3Y  - Change in Director's Interest Notice' through the Australian stock-exchange website within five business days of the transaction. 

### Problem

The information found in ASX announcements, such as the 'Appendix 3Y', are not made readily available to investors in a database. Instead, information on directors' transactions are hidden among many other announcements, in a .pdf format with difficult to extract fields, and each stored at a seperate website link. 

### Solution

A Python script to download the current day's announcement files, extract details of director's transactions, and save a summary workbook.  The script is seperated into two modules: 

**ASX_Announcement_Scraper.py** 
- Downloads today's ASX announcements, found here: https://www.asx.com.au/asx/v2/statistics/todayAnns.do. Uses BeautifulSoup package. 
- Isolates announcements with the title '3Y' or 'Change of Director's Interest Notice', navigates to the announcement's pdf link, and downloads the file. Uses Selenium (geckodriver + Firefox) and PyAutoGui packages.

**Announcement_3Y_PDF_Extractor.py**

- Extracts relevant details from each announcement's .pdf file, including: 'Name of director', 'Number acquired', 'Number disposed', and 'Class' (rights/shares), and saves as an excel file. Uses Tabula package. 

![](example_picture.png)

*Pictured - Left: the output from the Python scripts, an Excel summary of each director's transaction.*
*Right: an example 'Appendix 3Y' announcement.*



### Instructions

- Argument 1: Enter 1 to run ASX scraper or 0 otherwise
- Argument 2: Enter 1 to run PDF extractor or 0 otherwise

```
python3 main.py 1 1
```

### Environment

- Python 3.10.6
- requests==2.28.1
- selenium==4.5.0
- tabula-py==2.5.1
- PyAutoGUI==0.9.53
- pandas==1.5.0
- numpy==1.23.3
- openpyxl==3.0.10
- beautifulsoup4==4.11.1

### To-Do List

- ASX_Announcement_Scraper.py - Currently, on each pdf download's confirmation screen the PYAutoGUI module presses the enter key. Ideally, the enter key should just be sent to the webdriver window rather than the whole system. That way, the script could be run in the background. PyAutoGUI does not currently support sending keys to specific windows on Mac. 
