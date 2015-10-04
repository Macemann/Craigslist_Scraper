#Program to scrape craigslist and write contents of particular neighborhood searches into a CSV file

# -*- coding: utf-8 -*-

import requests
import csv
from bs4 import BeautifulSoup
import time
from time import strftime
import datetime
import re
import os


#Urls for scraping- one for each DC neighborhood.
CH_url = "https://washingtondc.craigslist.org/search/apa?query=Columbia%20Heights&s=0"
AM_url = "https://washingtondc.craigslist.org/search/apa?query=Adams%20Morgan&s=0"

#Retrieves year, month, day
now = datetime.datetime.now().timetuple()
year_month_day = [now.tm_year, now.tm_mon, now.tm_mday]

def scraper(url):

    #Retrieve and parse url

    r = requests.get(url)

    soup = BeautifulSoup(r.content, "lxml")
    
    #Gets the total count of postings, to be used by the counter
    total_count = soup.find("span", {"class": "totalcount"}).contents[0]

    #Writes desired content (price, neighborhood, etc.) to a list

    price_data = []
    data1 = soup.find_all("span", {"class": "price"})
    for price in data1:
        price_data.append(price.contents[0])

    neighborhood_data = []
    data2 = soup.find_all("span", {"class": "pnr"})
    for neighborhood in data2:
        neighborhood_data.append(neighborhood.contents[1].contents[0])

    size_data = []
    data3 = soup.find_all("span", {"class": "housing"})
    for size in data3:
        size_data.append(size.contents[0])

    date_data = []
    data4 = soup.find_all("span", {"class": "pl"})
    for date in data4:
        date_data.append(date.contents[1].contents[0])

    comment_data = []
    data5 = soup.find_all("span", {"class": "pl"})
    for comment in data5:
        comment_data.append(comment.contents[3].contents[0])

    #There is much content in this subheader. Link data is only the end of the url extension,
    #so this adds the extension to the base craigslist url in order to return the full path.

    link_data = []
    data6 = soup.find_all("span", {"class": "pl"})
    for link in data6:
        baselink = url[:35]
        link = re.sub(r'.*(/doc.*)\.html.*', baselink + r'\1' + r'.html', str(link))
        link_data.append(link)

    #Like above, except this strips away all other content to provide just the ID number

    id_data = []
    data7 = soup.find_all("span", {"class": "pl"})
    for ids in data7:
        ids = re.sub(r'.*data-id="(.*[0-9])\".*', r'\1', str(ids))
        id_data.append(ids)

    data = zip(price_data, neighborhood_data, size_data, date_data, comment_data, link_data, id_data)

    with open(str(year_month_day) + url[53:58] + "_scraper_output.csv", "ab") as output:
        csv_out = csv.writer(output)
        if os.path.exists(str(year_month_day) + url[53:58] + "_scraper_output.csv"):
            pass
        else:
            csv_out.writerow(["Price", "Neighborhood", "Size", "Date Posted", "Comment", "Link", "ID", "Retrieval_Year", "Retrieval_Month", "Retrieval_Day"])
        for row in data:
            csv_out.writerow(map(clean_any, row) + year_month_day)
            
#list_maker creates a list of urls for each page of the query to be used by the scraper
def list_maker(url):
    
    counter = 0
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "lxml")
    
    #Gets the total count of postings, to be used with the counter
    total_count = soup.find("span", {"class": "totalcount"}).contents[0]
    print total_count
    
    page_number = (int(total_count) / 100) + 1
    
    print page_number
    
    #takes base url and creates a list of all pages of the query
    url_list = []
    while counter < (int(total_count)):
        url_page = url + str(counter)
        counter += 100
        url_list.append(url_page)
        
    return url_list
    #print url_list


def clean_str(string):
    return unicode(string).encode('utf-8')


def clean_any(anything):
    return clean_str(anything) if isinstance(anything, basestring) else anything
    
# #    time.sleep(10)

for item in list_maker(AM_url):
    scraper(AM_url)
#    time.sleep(10)