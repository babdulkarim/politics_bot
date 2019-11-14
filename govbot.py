# importing required modules
import csv
import sys
import os

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup as BS



VISITED_LINKS = set()
OUTPUT = []
INPUT_URL = sys.argv[1]
KEYWORD = sys.argv[2]
LIMIT = int(sys.argv[3])
LINKS = []
IMAGE_FORMATS = ('.png', '.gif', '.gifv', '.jpg', '.jpeg')
LEVELS = 0

def get_links(url):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url)
    data = response.text
    soup = BS(data, 'lxml')

    # find all the texts that match the keyword
    for text in soup.find_all('p'):
        sentence = str(text.string).split()
        if KEYWORD in (word.lower() for word in sentence):
            OUTPUT.append(sentence)

    # find all links on the page
    for link in soup.find_all('a'):
        link_url = link.get('href')

        if link_url is not None:

            # ignore images
            if link_url.endswith(IMAGE_FORMATS): return

            # normal url
            if link_url.startswith('http'):
                tmp_link = link_url

            # subdomain url
            elif link_url.startswith('/'):
                tmp_link = "".join((INPUT_URL, link_url[1:]))

            # subdomain but different format
            else:
                tmp_link = "".join((INPUT_URL, link_url))

            # limit subdomains fetched
            if len(LEVELS) > LIMIT: return
            else:
                if ('gov' in tmp_link and tmp_link not in VISITED_LINKS):
                    LINKS.append(tmp_link)
                    VISITED_LINKS.add(tmp_link)

    LEVELS += 1

    return


def get_all_links(url):
    curr_links = get_links(url)
    if curr_links is None: return
    else:
        for link in curr_links:
            get_all_links(link)


def write_to_file(data):
    # write all data to csv file
    with open('scraped_text.csv', mode='w') as gov_file:
        gov_scraper = csv.writer(gov_file, delimiter='\n',
                                lineterminator=os.linesep, quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        if data is not None:
            for chunk in data:
                if len(chunk) > 1:
                    gov_scraper.writerow([" ".join(chunk)])
                else:
                    gov_scraper.writerow(chunk)


def write_to_links(data):
    # write all data to csv file
    with open('scraped_links.csv', mode='w') as link_file:
        link_scraper = csv.writer(link_file, delimiter='\n',
                                lineterminator=os.linesep, quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)

        if data is not None:
            link_scraper.writerow(data)


def main():
    get_all_links(INPUT_URL)
    # write all the links stored in LINKS list to csv
    write_to_links(LINKS)
    # write all the data stored in OUTPUT list to csv
    write_to_file(OUTPUT)

if __name__=="__main__":
    main()
