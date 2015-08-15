#tutorial on yellow pages for scraping data
#notes and code relating to the tutorial:
#https://www.youtube.com/watch?v=3xQTJi2tqgk

#inspect element on searched items
#items tagged (div class = "info") gives information we are looking for

#pip install requests --upgrade
#pip install beautifulsoup4 --upgrade

import requests
from bs4 import BeautifulSoup

r = requests.get("URL")
#r.content to see all the downloaded data
soup = beautifulsoup("URL")
#or-- soup = BeautifulSoup(r.content)
soup = BeautifulSoup
print soup.prettify() # cleans up url content
soup.find_all("a") #finds all tags of a, like anchor tags

for link in soup.find_all("a"): #puts all links on new line
	print link.get("href")

for link in soup.find_all("a")
	print link.text #shows text for all links on page

for link in soup.find_all("a"):
	print link.text, link.get("href") #link texts with links

for link in soup.find_all("a"): #gets all links without classes and stuff... just links
	"<a href='%s'>%s</a>" %(link.get("href"), link.text)

--

import requests
from bs4 import BeautifulSoup

url = ""
r = requests.get("")

soup = BeautifulSoup(r.content)

links = soup.find_all("a")

for link in links:
#can tryif "http" in link.get("href"):
		print "<a href='%s'>%s</a>" %(link.get("href"), link.text)

#info is in divclass info

g_data = soup.find_all("div", {"class": "info"})
print g_data #all content 

for item in g_data:
	print item #this is a list
	print item.content #sets of lists
	print item.text

for item in g_data:
	print item.contents[0].text #prints list of contents
	print item.contents[1].text #prints 2nd list (in this case, addresses)

#just subcontents of these lists?
#class called business name, links to listing

for item in g_data:
	print item.contents[0].find_all("a",{"class": "business-name"})#[0].text (for first list element, in this case, company names)
		#finds subclass- business name with link

		#want address?
	print item.contents[1].find_all("p",{"class": "adr"})[0].text #prints addresses

#want phone number?
try:
	print item.contents[1].find_all("li", {"class": "primary"})[0].text
except:
	pass

#try and except this too
	print item.contents[1].find_all("span", {"itemprop": "address"})[0].text
	print item.contents[1].find_all("span", {"itemprop": "addressLocality"})[0].text

#find items in inspect element and manipulate as you see fit

#how to go to next page

def get_data_from_url(url, 10):
