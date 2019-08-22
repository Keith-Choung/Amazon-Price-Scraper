from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from bs4 import BeautifulSoup

import requests
import datetime
import shutil
import csv

# to be sent to in requests
headers = {
    """
    User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 
    Safari/537.36
    """
    }


'''
getData: takes in an ID and returns data of that ID 
'''
def getData(ID: int) -> (str, str, float, str):
    CSVFile = csv.reader(open('data/items.csv', 'r'), delimiter=",")
    next(CSVFile) # skips header

    i = 0
    target = ""

    for row in CSVFile:
        if(ID == int(row[0])):
            target = row
            break
        else:
            i += 1
            continue

    # need to take out the quotes in the string
    URL = target[1].replace('\"', '')
    page = requests.get(URL, headers=headers)
 
    # Parse everything for us
    soup = BeautifulSoup(page.content, 'lxml')

    # incase scraping first time doesnt work
    if soup.find("span", {"id": "productTitle"}) == None:
        unstripped_title = soup.find("h1", {"id": "title"}).get_text()
    else:
        unstripped_title = soup.find("span", {"id": "productTitle"}).get_text()

    
    # Make short description to store
    title_split = unstripped_title.split()
    short_desc_split = title_split[0:6]
    short_desc = " ".join(short_desc_split)

    # Find price
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[1:4])

    # Get Date
    date = datetime.date.today()
    date_str = "{}/{}/{}".format(date.month, date.day, date.year)

    return unstripped_title, short_desc, converted_price, date_str

'''
totalRows: takes in filename argument and 
           returns the row count of the file
'''
def totalRows(filename: str) -> int:
    with open('data/items.csv', 'r') as CSVFile:
        readCSV = csv.reader(CSVFile, delimiter=",")
        next(readCSV)

        # sof: sum is more efficient
        row_count = sum(1 for row in readCSV)

    return row_count


'''
checkPrice: searches for original price and
            compares it to the new price
'''
def checkPrice(ID: int, newPrice: float) -> int:
    print("checkPrice\n")

    orig = []
    i = 0
    p = 0
    exist = False

    with open('data/site_data.csv', mode='r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)

        # checks for ID
        for row in readCSV:
            if (int(row[0]) == ID):
                exist = True
                orig = row
                storedPrice = float(orig[2])

    # ID doesnt exist
    if not exist:
        print("checkPrice returned: DNE\n")
        return 1

    # ID exists && new price is cheaper
    elif (exist & storedPrice > newPrice):
        print("checkPrice returned: UPDATE\n")
        return 2

    # ID exists but price didn't decrease
    print("checkPrice returned: N/A\n")
    return 3


'''
storeData: reads in data and stores it into csv file. 
'''
def storeData(ID: int, Desc: str, Price: float, Date: str):
    with open('data/site_data.csv', mode='a+') as csvfile:
        item_data = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        item_data.writerow([ID, Desc, Price, Date])

        print("STORED DATA")
    

'''
updateData: updates the ID's to be contiguous (1, 2, 3, ...)
'''
def updateData(ID: int, Desc: str, Price: float, Date: str):
    
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    filename = 'data/site_data.csv'
    header = ["ID", "Desc", "Price", "Date"]
    headerDict = {'ID': "ID", 'Desc': "Description", 'Price': "Price", 'Date': "Date"}

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=header)
        writer = csv.DictWriter(tempfile, fieldnames=header, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_ALL)
        next(reader)

        # add categories to first row of csv file
        writer.writerow(headerDict)
        
        # add in each row | if row ID matches given ID, update with new data
        for row in reader:

            if int(row['ID']) == ID:
                row['Desc'], row['Price'], row['Date'] = Desc, Price, Date

            row = {'ID': row['ID'], 'Desc': row['Desc'], 'Price': row['Price'], 'Date': row['Date']}    
            writer.writerow(row)

    shutil.move(tempfile.name, 'data/site_data.csv')


def main():

    # read in CSV to parse
    CSVFile = csv.reader(open('data/items.csv', 'r'), delimiter=',')
    total = totalRows('data/items.csv')

    # skip categories (first row)
    next(CSVFile)

    for row in CSVFile:

        ID = int(row[0])
        title, short_desc, converted_price, date_str = getData(ID)
        switch_case_value = checkPrice(ID, converted_price)

        # * -> append
        if (switch_case_value == 1):
            storeData(ID, short_desc, converted_price, date_str)
        # * -> update
        elif (switch_case_value == 2): 
            updateData(ID,short_desc,converted_price, date_str)
        # * -> continue
        else:
            continue
        if(ID == total):
            break
    
    print("EXIT\n")


if __name__ == '__main__':
    main()