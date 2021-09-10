import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import argparse

"""Scrapes job postings from indeed, optionally by job and location.
    :param job: job title
    :param location: Where the job is located
    :type job: str
    :type location: str
    :return: all job postings from all page that match the search results. and save the results in CSV
    :rtype: requests object
    :rtype: bs4 object
    :rtype: pandas object
    :rtype: argparse object
    """

def scp_get_url(job=None, location=None):
    """Generate url from job and location"""
    if location and job:
        URL = f"https://www.indeed.com/jobs?q={job}&l={location}"
    elif location and not job:
        URL = f"https://www.indeed.com/trabajo?q=developer&l={location}"
    elif job and not location:
        URL = f"https://www.indeed.com/jobs?q={job}&l="
    elif not job and not location:
        URL = "https://www.indeed.com/jobs?q=&l="

    return URL


def scp_get_record(card):
    """Extract job data from a single record
    :param card: data generated in the function main(job, location)
    :param title_elem: Job title 
    :param company_elem: company Name
    :param location_elem: company Location
    :param post_date: posted date
    :param today: Scrape Date
    :param link_cont_elem: URL to apply to.
    :param sumary: Required skills
    :param salary_tag: Annuall sallary.
    :type card: object
    :type title_elem: str
    :type company_elem: str
    :type location_elem: str
    :type post_date: str
    :type today: str
    :type link_cont_elem: str
    :type sumary: str
    :type salary_tag: str"""

    title_elem = card.find('div', 'slider_container').find('h2', 'jobTitle')
    company_elem = card.find('div', 'slider_container').find('span', class_='companyName')
    location_elem = card.find('div', 'slider_container').find('div', class_='companyLocation')
    post_date = card.find('div', 'slider_container').find('span', 'date')
    today = datetime.today().strftime('%Y-%m-%d')  
    link_cont_elem = card["href"]
    sumary = card.find('div', 'slider_container').find('div', class_='job-snippet')
    salary_tag = card.find('div', 'slider_container').find('span', 'salary-snippet')

    if salary_tag:
        salary = salary_tag.attrs.get('aria-label')
    else:
        salary = ''  


    """Assigns the data obtained to the variables to later be saved"""
    job_title = title_elem.text.strip()
    company = company_elem.text.strip()
    job_location = location_elem.text.strip()
    post_date = post_date.text
    today = today
    summary = sumary.get_text('lu')
    salary = salary
    job_url = "https://www.indeed.com" + link_cont_elem
        
    
    """Extract job data from a single record"""
    record = (job_title, company, job_location, post_date, today, summary, salary, job_url)
    

    """we print the results of the query to the console"""
    print("Vacant: " + job_title)
    print("Company: " + company)
    print("Place: " + job_location)
    print("Posted: " + post_date)
    print("Date: " + today)
    print("Salary: " + salary)
    print("Url: " + job_url)
    print("Description: " + summary)
    print("*"*140)
    print()
    return record


def main(job=None, location=None):
    """Run the main program routine"""
    records = []
    url = scp_get_url(job, location)
    
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find(id="resultsCol")
        cards = results.find_all('a', class_='tapItem')
        
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
    df.to_csv('datos.csv')


# ----------------------------------------------------------------------------
""" -----------USE THE SCRIPT AS A COMMAND-LINE INTERFACE------------------"""
# ----------------------------------------------------------------------------
console = argparse.ArgumentParser(description="Web scraping tool for job search", epilog="Good luck with the search!")
console.add_argument("-job", metavar="'job'", type=str, help="A keyword to look for the desired job")
console.add_argument("-location", metavar="'location'", type=str, help="The location of the job")

args = console.parse_args()
job, location = args.job, args.location


if not job and not  location:
    print()
    print("Enter the data for your search (-job job, -location location)")
    print()
elif job == '' and location == '':
    print()
    print("Enter the data for your search (-job job, -location location)")
    print()
elif job or location:

    main(job, location)
