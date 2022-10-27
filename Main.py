import ASX_Announcement_Scraper as ASX_Scraper_module

import Announcement_3Y_PDF_Extractor as PDF_Extractor_module

from datetime import date

import argparse

def main():

    parser = argparse.ArgumentParser(description='Run ASX Announcement scraper and/or Announcement 3Y PDF extraction')

    parser.add_argument('ASX_scrape', help='Enter 1 to run ASX scraper or 0 otherwise')

    parser.add_argument('PDF_extract', help='Enter 1 to run PDF extractor or 0 otherwise')

    args = parser.parse_args()

    today = date.today()

    directory_name = str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-3Y Announcements'

    url = "https://www.asx.com.au/asx/v2/statistics/todayAnns.do"

    print(args.ASX_scrape)

    print(args.PDF_extract)

    if int(args.ASX_scrape) == 1: 

        scrape = ASX_Scraper_module.ASX_Announcement_Scrape(url, directory_name)

        df_returned = scrape.find_announcements()

        print(df_returned.head())

        df_cleaned = scrape.clean_df(df_returned)

        df_dir = scrape.isolate_dir(df_cleaned)

        scrape.launch_webdriver()

        scrape.scrape_links(df_dir)

    if int(args.PDF_extract) == 1:
        extractor = PDF_Extractor_module.Announcement_3Y_PDF_Extractor(directory_name)
        extractor.scrape_pdfs()

if __name__ == "__main__":
    main()
