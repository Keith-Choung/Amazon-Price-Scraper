from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from bs4 import BeautifulSoup
from lxml.html import fromstring
from itertools import cycle

import traceback
import requests
import datetime
import random
import shutil
import time
import csv

# found online | rotates use of user agent to prevent website scraping blockage
class Anon:

    UAsourceURL='https://deviceatlas.com/blog/list-of-user-agent-strings#desktop'

    def __init__(self):
        self.newUA = random.choice(self.getUA())
        
    def getUA(self, source=UAsourceURL):
        r = requests.get(source)
        soup = BeautifulSoup(r.content, "html.parser")
        tables = soup.find_all('table')
        return [table.find('td').text for table in tables]

    def getProxies(self):
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:10]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        return proxies

    def chooseProxy(self):
        proxies = self.getProxies()
        url = 'https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests'
        proxyList = list(proxies)

        proxy = random.choice(proxyList)

        return proxy

class Scraper:

    def __init__(self, ID):
        self.ID = ID

    def getData(self) -> (str, float, str):
        CSVFile = csv.reader(open('data/items.csv', 'r'), delimiter=",")
        next(CSVFile) # skips header

        i = 0
        target = ""
        found = False

        for row in CSVFile:
            if(self.ID == int(row[0])):
                target = row
                break
            else:
                i += 1
                continue

        # incase scraping first time doesnt work
        while not found:
            # get a User Agent
            userAgent = Anon().newUA
            # proxy = Anon().chooseProxy
            headers = {"User-Agent" : userAgent}

            # need to take out the quotes in the string
            URL = target[1].replace('\"', '')

            # Create a Session to store cookies
            sess = requests.Session()
            sess.headers = headers
            try:
                page = sess.get(URL)
            except:
                print("Request failure.\n")
                continue

            # Parse everything for us
            soup = BeautifulSoup(page.content, 'lxml')
            unstripTitle = soup.find("span", {"id": "productTitle"})

            # checks if it got blocked
            if (unstripTitle != None):
                found = True
                new = unstripTitle.get_text()

            # pause to be friendly toward the server :)
            else:
                print("resting...\n")
                time.sleep(5)
                continue

        # Make short description to store
        titleSplit = new.split()[0:6]
        shortDesc = " ".join(titleSplit)

        # Find price
        price = soup.find(id="priceblock_ourprice").get_text()
        convPrice = float(price[1:4])

        # Get Date
        date = datetime.date.today()
        dateStr = "{}/{}/{}".format(date.month, date.day, date.year)

        print("GOT DATA\n")

        return shortDesc, convPrice, dateStr

    '''
    checkPrice: searches for original price and
                compares it to the new price
    '''
    def checkPrice(self, newPrice: float) -> int:
        orig = []
        exist = False

        with open('data/site_data.csv', mode='r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)

            # checks for ID
            for row in readCSV:

                # If row is None
                if not row:
                    break

                
                elif (self.ID == int(row[0])):
                    exist = True
                    orig = row
                    storedPrice = float(orig[2])

        # ID doesnt exist
        if not exist:
            print("checkPrice returned: DNE\n")
            return 1

        # ID exists && new price is cheaper
        elif (exist and storedPrice > newPrice):
            print("checkPrice returned: UPDATE\n")
            return 2

        # ID exists but price didn't decrease
        print("checkPrice returned: N/A\n")
        return 3


class DataHandler:

    # updateData() class variables
    storageFilename = 'data/site_data.csv'
    header = ["ID", "Desc", "Price", "Date"]
    headerDict = {'ID': "ID", 'Desc': "Desc", 'Price': "Price", 'Date': "Date"}
    
    # storeData() class variables
    inputFilename = 'data/items.csv'

    def __init__(self, ID, Desc, Price, Date):
        self.ID = ID
        self.Desc = Desc
        self.Price = Price
        self.Date = Date

    '''
    storeData: reads in data and stores it into csv file. 
    '''
    def storeData(self):
        with open(self.storageFilename, mode='a+') as csvfile:
            item_data = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
            item_data.writerow([self.ID, self.Desc, self.Price, self.Date])

            print("STORED DATA\n")

    '''
    updateData: updates the row that had a price decrease
    '''
    def updateData(self):

        tempfile = NamedTemporaryFile(mode='w', delete=False)

        with open(self.storageFilename, 'r') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=self.header)
            writer = csv.DictWriter(tempfile, fieldnames=self.header, delimiter=',',
                quotechar='"', quoting=csv.QUOTE_ALL)
            next(reader)

            # add categories to first row of csv file
            writer.writerow(self.headerDict)

            # add in each row | if row ID matches given ID, update with new data
            for row in reader:

                if int(row['ID']) == self.ID:
                    row['Desc'], row['Price'], row['Date'] = self.Desc, self.Price, self.Date

                row = {'ID': row['ID'], 'Desc': row['Desc'], 'Price': row['Price'], 'Date': row['Date']}    
                writer.writerow(row)

        shutil.move(tempfile.name, 'data/site_data.csv')
        print("UPDATED DATA\n")

class Files:

    def __init__(self, filename:str):
        self.filename = filename
    
    '''
    totalRows: takes in filename argument and 
            returns the row count of the file
    '''
    def totalRows(self) -> int:

        with open(self.filename, 'r') as CSVFile:
            readCSV = csv.reader(CSVFile, delimiter=",")
            next(readCSV)

            # sof: sum is more efficient
            self.rowCount = sum(1 for row in readCSV)

        return self.rowCount

    '''
    getIDs: gets the list of IDs in file
    '''
    def getIDs(self)-> list:
        with open(self.filename, 'r') as CSVFile:
            readCSV = csv.reader(CSVFile, delimiter=",")
            next(readCSV) # skips header
            ids = [] # return list of IDs
            for row in readCSV:
                ids.append(row[0])
            return ids

    '''
    createIDs: makes an ID for the newly added item
    '''
    def createID(self, IDs: list) -> int:
        # if there is no ID/list is empty
        if not IDs:
            return 1
        return int(IDs[-1]) + 1

    '''
    getRows: gets the row number of the ID
    '''
    def getRows(self, ID: int) -> int:
        with open(self.filename, 'r') as CSVFile:
            readCSV = csv.reader(CSVFile, delimiter=",")
            next(readCSV)
            row_number = 1
            for row in readCSV:
                if ID == int(row[0]):
                    return row_number
                else:
                    row_number += 1
            return row_number

    '''
    changeFile: changes path of file
    '''
    @classmethod
    def changeFile(cls, newFile: str):
        cls.filename = newFile

def main():

    # read in CSV to parse
    CSVFile = csv.reader(open('data/items.csv', 'r'), delimiter=',')
    total = Files('data/items.csv').totalRows()

    # skip categories (first row)
    next(CSVFile)

    for row in CSVFile:

        ID = int(row[0])
        Scrap = Scraper(ID)
        shortDesc, convPrice, dateStr = Scrap.getData()

        print(shortDesc, convPrice, dateStr)
        print("")

        switch_case_value = Scrap.checkPrice(convPrice)

        Data = DataHandler(ID, shortDesc, convPrice, dateStr)

        # * -> append
        if (switch_case_value == 1):
            Data.storeData()
        # * -> update
        elif (switch_case_value == 2): 
            Data.updateData()
        # * -> continue
        else:
            print("resting...\n")
            time.sleep(1)
            continue
        if(ID == total):
            break
        
        print("resting...\n")
        time.sleep(1)
    
    print("EXIT\n")


if __name__ == '__main__':
    main()

# a = Anon()
# print(a.getProxies())
# print(a.chooseProxy())
# url = "https://www.amazon.com/AmazonBasics-Dual-Port-USB-Wall-Charger/dp/B0773BHCVD/ref=sxts_srecs_srch_pb_sims?crid=QPRW9LDLRACJ&keywords=amazonbasics&pd_rd_i=B0773BHCVD&pd_rd_r=845be779-af66-44f4-b9f8-7df92aa514aa&pd_rd_w=6SFEX&pd_rd_wg=UT6KL&pf_rd_p=c9185cf0-afb7-43e4-87cf-1b328fd08c73&pf_rd_r=89BCV51E6XM1S4P8VQJB&qid=1566766683&s=electronics&sprefix=amazon%2Celectronics%2C299"

# s = requests.Session()
# s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
# r = s.get(url)
# print(r)