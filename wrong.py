import requests
import csv
import re
from bs4 import BeautifulSoup

# url = "http://washingtondc.craigslist.org/search/apa?s=0"
# r = requests.get(url)

# soup = BeautifulSoup(r.content, "lxml")
# # print soup

# price_data = []
# data1 = soup.find_all("span", {"class": "price"})
# for price in data1:
#     price_data.append(price.contents[0])

# neighborhood_data = []
# data2 = soup.find_all("span", {"class": "pnr"})
# for neighborhood in data2:
#     neighborhood_data.append(neighborhood.contents[1].contents[0])


# size_data = []
# data3 = soup.find_all("span", {"class": "housing"})
# for size in data3:
#     size_data.append(size.contents[0])

# data = zip(price_data, neighborhood_data, size_data)
# # print data

# with open("scraper_output.csv", "wb") as output:
#     csv_out = csv.writer(output)
#     csv_out.writerow(["Price", "Neighborhood", "Size"])
#     for row in data:
#         csv_out.writerow(row)

def clean_row(dirty_row):
    stripped_row = [data.strip() for data in dirty_row]
    price_data, neighborhood_data, size_data = stripped_row

    neighborhood_data = re.sub(r'\((.+?)\)', r'\1', neighborhood_data)
    size_data = re.sub(r'.*?([0-9])+br\s*-\s*([0-9]*).+', r'\1, \2', size_data)

    return neighborhood_data


def clean(dirty_rows):
    # clean_rows = [clean(row) row for row in dirty_rows]
    clean_rows = []
    for row in dirty_rows:
        clean_rows.append(clean_row(row))
    return clean_rows

dirty = []

with open("scraper_output.csv", "rb") as f:
    reader = csv.reader(f)
    for row in reader:
        dirty.append(row)
print clean(dirty)
