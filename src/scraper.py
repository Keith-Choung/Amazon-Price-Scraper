from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from bs4 import BeautifulSoup

import requests
import datetime
import random
import shutil
import time
import csv

# found online | rotates use of user agent to prevent website scraping blockage
class UserAgent:

    UAsourceURL='https://deviceatlas.com/blog/list-of-user-agent-strings#desktop'

    def __init__(self):
        self.newUA = random.choice(self.getUA())
        
    def getUA(self, source=UAsourceURL):
        r = requests.get(source)
        soup = BeautifulSoup(r.content, "html.parser")
        tables = soup.find_all('table')
        return [table.find('td').text for table in tables]


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
            userAgent = UserAgent().newUA
            print(userAgent)
            headers = {"User-Agent" : userAgent}

            # need to take out the quotes in the string
            URL = target[1].replace('\"', '')
            page = requests.get(URL, headers=headers)
        
            # Parse everything for us
            soup = BeautifulSoup(page.content, 'lxml')
            unstripTitle = soup.find("span", {"id": "productTitle"})

            # checks if it got blocked
            if (unstripTitle != None):
                found = True
                new = unstripTitle.get_text()

            # pause to be friendly toward the server :)
            else:
                print("resting...")
                time.sleep(2)
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

        print("GOT DATA")

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
                if (self.ID == int(row[0])):
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

            print("STORED DATA")

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
        print("UPDATED DATA")

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
            print("resting...")
            time.sleep(1)
            continue
        if(ID == total):
            break
        
        print("resting...")
        time.sleep(1)
    
    print("EXIT\n")


if __name__ == '__main__':
    main()