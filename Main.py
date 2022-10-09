
import ASX_Announce_Scraper as ASX_Scraper


url = "https://www.asx.com.au/asx/v2/statistics/todayAnns.do"

scrape = ASX_Scraper.ASX_Announcement_Scrape(url)

df_returned = scrape.find_announcements() 

print(df_returned.head())

df_cleaned = scrape.clean_df(df_returned)

df_dir = scrape.isolate_dir(df_cleaned)

scrape.launch_webdriver()

scrape.scrape_links(df_dir)
