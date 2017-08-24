from selenium import webdriver
from lxml import html
from functools import total_ordering
import sys

#Home object, with values for room type, property type,  listing name, and price
#compares by price
@total_ordering
class Home(object):
    def __init__(self, roomType, name, price, link): 
        self.roomType = roomType
        self.name = name
        self.price = price
        self.link = link
    def __repr__(self):
        return(self.name + ": " + self.roomType + ", starting at $" + str(self.price) + "\n https://airbnb.com" + self.link)
    def __eq__(self, other):
        return (self.name == other.name)
    def __ne__(self, other):
        return not (self.name == other.name)
    def __lt__(self, other):
        return(self.price < other.price)

#finds all newly added homes on first four pages depending on user location
def findHomesHTML(city, country):
    #launches airbnb webpage
    browser = webdriver.PhantomJS(r'C:\Users\jess2\webscraping\phantomjs.exe')

    for pageCount in range(2):
        url = "https://airbnb.com/s/" + city + "--" + country + "/homes?section_offset=" + str(pageCount)
        browser.get(url)
        innerHTML = browser.execute_script("return document.body.innerHTML")
        tree = html.document_fromstring(innerHTML)

        newHomes = tree.xpath('//div[@class="infoContainer_v72lrv"]//text()')
        links = tree.xpath('//div[@class="container_1xf3sln"]/a/@href')

    return [newHomes, links]

#given HomeHTML, parses list, and returns list of Homes sorted by price
def sortByPrice(homes, links):
    homeCounter = 0
    linkCounter = 0
    listings = []
    #parses list, checking for keywords
    while (homeCounter < len(homes)):
        if(homes[homeCounter] == 'Price'):
            price = int(homes[homeCounter + 1][1:]) #ignores dollar sign
            name = homes[homeCounter + 3]
            roomType = homes[homeCounter + 4]
            newHome = Home(roomType, name, price, links[linkCounter])
            homeCounter += 5
            linkCounter += 1
            listings.append(newHome)
        homeCounter += 1
    return(sorted(listings))

if __name__ == '__main__':
    city = input("City: ")
    country = input("Country: ")
    print("Searching up homes... \n")
    listOfHomes, listOfLinks = findHomesHTML(city, country) 
    print("\n".join(str(home) for home in (sortByPrice(listOfHomes, listOfLinks))))

