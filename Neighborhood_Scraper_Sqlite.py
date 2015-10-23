#Program to scrape craigslist and write contents of DC neighborhood searches into a sqlite database
# -*- coding: utf_8 -*-

import requests
import csv
from bs4 import BeautifulSoup
import time
from time import strftime
import datetime
import re
import os
import sqlite3 as lite
import sys
import json

#Urls for scraping- one for each DC neighborhood.
neighborhoods = {
"CH_url" : "https://washingtondc.craigslist.org/search/apa?query=Columbia%20Heights&s=0",
"AM_url" : "https://washingtondc.craigslist.org/search/apa?query=Adams%20Morgan&s=0"
}

#Retrieves neighborhood names and urls as a dictionary from json file
def json_reader(jsondata):

    with open('neighborhoods.json') as json_data:
        d = json.load(json_data)

    neighborhoods = []
    for item in d:
        for items in item['aliases']:
            neighborhoods.append(items)
    for item in d:
        neighborhoods.append(item['desc'])
    
    neighborhood_urls = []
    for item in neighborhoods:
        item = re.sub(r" ","%20",str(item))
        item = re.sub(r"(.*)","https://washingtondc.craigslist.org/search/apa?query="+r"\1"+"&s=0",str(item))
        neighborhood_urls.append(item)

    neighborhood_dic = dict(zip(neighborhoods, neighborhood_urls))

    return neighborhood_dic



con = lite.connect('canimakeit.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS Info")

#Retrieves year, month, day
now = datetime.datetime.now().timetuple()
year_month_day = [str(now.tm_year), str(now.tm_mon), str(now.tm_mday)] ##added str to each value

def scraper(url):

    #Retrieve and parse url

    r = requests.get(url)

    soup = BeautifulSoup(r.content, "lxml")
    
    #Gets the total count of postings, to be used by the counter
    #total_count = soup.find("span", {"class": "totalcount"}).contents[0]

    #Writes desired content (price, neighborhood, etc.) to a list

    price_data = []
    data1 = soup.find_all("span", {"class": "price"})
    for price in data1:
        price_data.append(price.contents[0])

    neighborhood_data = []
    data2 = soup.find_all("div", {"class": "querybox"})
    for neighborhood in data2:
        neighborhood = neighborhood.contents[3]
        neighborhood = re.sub(r'.*value="(.*)".*', r'\1', str(neighborhood))
        neighborhood_data.append(neighborhood)         
    
    br_data = []
    sqft_data = []
    data3 = soup.find_all("span", {"class": "housing"})
    for size in data3:
        size = size.contents[0]
        if "br" in size:
            size_br = re.sub(r'.*\D([\d]*)br.*', r'\1', str(size))
            br_data.append(size_br)
        else:
            br_data.append("NA")
        if "ft" in size:
            size_ft = re.sub(r'.*\D([\d]*)ft.*', r'\1', str(size))
            sqft_data.append(size_ft)
        else:
            sqft_data.append("NA")

    date_data = []
    data4 = soup.find_all("span", {"class": "pl"})
    for date in data4:
        date_data.append(date.contents[1].contents[0])

    comment_data = []
    data5 = soup.find_all("span", {"class": "pl"})
    for comment in data5:
        comment = comment.contents[3].contents[0]     
        comments = comment.encode('ascii', 'ignore').decode('ascii') #removes non-ascii characters from scraper. Makes life easy.
        comment_data.append(comments)

    #There is much content in this subheader. Link data is only the end of the url extension,
    #so this adds the extension to the base craigslist url in order to return the full path.

    link_data = []
    data6 = soup.find_all("span", {"class": "pl"})
    for link in data6:
        baselink = url[:35]
        link = re.sub(r'.*([\d]{10}).*', baselink + r'/doc/apa/'+ r'\1' + r'.html', str(link))
        link_data.append(link)

    #Like above, except this strips away all other content to provide just the ID number

    id_data = []
    data7 = soup.find_all("span", {"class": "pl"})
    for ids in data7:
        ids = re.sub(r'.*data-id="(.*[0-9])\".*', r'\1', str(ids))
        id_data.append(ids)

    data = zip(price_data, br_data, sqft_data, date_data, comment_data, link_data, id_data)

    #assembles data and writes it to the database
    for row in data:
        info = (neighborhood_data + map(clean_any, row) + year_month_day)
          
        with con:
            cur.execute("CREATE TABLE IF NOT EXISTS Info(Neighborhood TEXT, Price INT, BR INT, Sqft INT, Date TEXT, Comment TEXT, Link TEXT, ID TEXT, Year TEXT, Month TEXT, Day TEXT)")
            cur.executemany("INSERT INTO Info VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [info])

#list_maker creates a list of urls for each page of the query to be used by the scraper
def list_maker(url):
    
    counter = 0
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "lxml")
    
    #Gets the total count of postings, to be used with the counter
    total_count = soup.find("span", {"class": "totalcount"}).contents[0]
    
    page_number = (int(total_count) / 100) + 1
    
    #takes base url and creates a list of all pages of the query
    url_list = []
    while counter < (int(total_count)):
        url_page = url[:-1] + str(counter)
        counter += 100
        url_list.append(url_page)
        
    return url_list
    #print url_list
            
            
def clean_str(string):
    return unicode(string).encode('utf-8')


def clean_any(anything):
    return clean_str(anything) if isinstance(anything, basestring) else anything

#iterates through each neighborhood in dictionary, retrieves its url and generates list of all urls for that neighborhood, scraping each one as it goes.
def scraper_helper(urls):
    for neighborhood in urls:
        for item in list_maker(urls[neighborhood]):
            scraper(item)
#            time.sleep(10)
        
        
scraper_helper(json_reader(neighborhoods))
