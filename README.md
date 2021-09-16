# Web Scraper Tool for Jobs

This is a scrapper that takes care of scanning job websites and downloading jobs found on the differnt portals.


| Arguments |                                                       |
| --------- | ----------------------------------------------------- |
| -keworkd  | One or more words (in quotes) to query the jobs from  |
| -site     | One of the following: [indeed, monster, linkedin, etc |
| -location | City name, country name or "online" or "remote"       |



## Architecture

There is a main scrape.py that is the entry point for the entire application, then inside the `./src/sites` folder you can find the scraping details for each site.