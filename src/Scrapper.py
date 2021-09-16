import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import argparse


class Scrapper:
    
    output = ""

    def __init__(self, site, keyword, location):
        self.output = f"{site}.csv"

    def get_search_url():
        """
            Generate url from job and location
            Returns the URL
        """
        raise Exception("You need to implement the method get_search_url for this scrapper")

        


    ## This method will start looping all the possible results
    def start(self):
        """Run the main scrapper routine"""

        records = []
        url     = self.get_search_url(job, location)
        
        while True:
            response    = requests.get(url)
            soup        = BeautifulSoup(response.text, 'html.parser')
            results     = soup.find(id="resultsCol")
            cards       = results.find_all('a', class_='tapItem')
            
            if None in (cards):
                continue
            
            for card in cards:
                record = scp_get_record(card)
                records.append(record)

            try:
                url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
            except AttributeError:
                break
        
        """save the job data"""
        df = pd.DataFrame(records, columns=['JobTitle', 'Company', 'Location', 'PostDate', 'ExtractDate', 'Summary', 'Salary', 'JobUrl'])
        df.to_csv(self.output)