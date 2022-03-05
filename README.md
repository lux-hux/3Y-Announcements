# ASX-Announcements

### Background

Directors of Australian listed companies are required to inform the market whenever they transact in the shares of a company they advise. This is a potential buy signal for investors because directors, as company insiders, presumably have a strong understanding of the company's future profitability. The company must lodge an announcement to the market titled an 'Appendix 3Y  - Change in Director's Interest Notice' through the Australian stock-exchange website within five business days of the transaction. 

### Problem

The information found in ASX announcements, such as 'Appendix 3Y', are not made readily available to investors. Firsly, each announcement is a .pdf file which must be individually navigated to through a website link. Secondly, the .pdf files' formatting makes extracting the relevant details difficult. Thirdly, historical announcements for all companies are not easily accessed. 

### Solution

Python scripts to download all of the current day's announcement files, extract the details, and save as a workbook.  

**ASX_Announce_Scraper.py** 
- Downloads a list of the current day's ASX announcements along with relevant details, found here: https://www.asx.com.au/asx/v2/statistics/todayAnns.do. Uses BeautifulSoup package. 
- Isolates announcements with the title '3Y' or 'Change of Director's Interest Notice', navigates to the announcement's pdf link, and downloads the file. Uses Selenium (geckodriver + Firefox) and PyAutoGui packages.

**3Y_Announce_PDF_Extractor.py**

- Extracts relevant details from each announcement's .pdf file, including: 'Name of director', 'Name acquired', 'Number disposed', and 'Class' (rights/shares), and saves as an excel file. Uses Tabula package. 

![](Example_Mapping.png)

*Picture - Left: output from the Python scripts, a summary of each '3Y' announcement. Right: corresponding fields from .pdf file colour-coded. 


**Environment**





