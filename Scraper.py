import requests
import csv
from bs4 import BeautifulSoup

url = "http://washingtondc.craigslist.org/search/apa?s=0"
r = requests.get(url)

soup = BeautifulSoup(r.content, "lxml")
#print soup

price_data = []
data1 = soup.find_all("span", {"class":"price"})
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
    
data = zip(price_data,neighborhood_data,size_data)
#print data

with open("scraper_output.csv","wb") as output:
    csv_out=csv.writer(output)
    csv_out.writerow(["Price","Neighborhood","Size"])
    for row in data:
        csv_out.writerow(row)
