
# ! ALERT
# * FUNCTION
# ? QUESTION
# COMMENT

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import datetime
import csv
from tempfile import NamedTemporaryFile
import shutil


headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

def getInfo(ID):
    csv_file = csv.reader(open('data/items.csv', 'r'), delimiter=",")
    next(csv_file) # skips header
    i = 0
    target = ""

    for row in csv_file:
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

    #! Need to specify tags AND attributes for bs4 to find()
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


def totalRows(filename: str) -> int:
    with open('data/items.csv', 'r') as csv_file:
        readCSV = csv.reader(csv_file, delimiter=",")
    # csv_file = csv.reader(open(filename, 'r'), delimiter=",")
        next(readCSV)
        row_count = sum(1 for row in readCSV) # * sf: sum is more efficient
    return row_count


# * checkPrice: takes in origPrice and index and compares with new price w that index's value
def checkPrice(ID, new_price):
    print("checkPrice\n")
    orig = []
    i = 0
    p = 0
    exist = False
    with open('data/site_data.csv', mode='r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            if (int(row[0]) == ID):
                exist = True
                orig = row
    print("ID:", ID)
    if not exist:
        print("checkPrice returned: DNE\n")
        return 1
    elif (exist and float(orig[2]) > new_price):
        print("checkPrice returned: UPDATE\n")
        return 2
    print("checkPrice returned: N/A\n")
    return 3


# * storeData: reads in data and stores it into csv file. checks if data is new and updates
def storeData(ID, Desc, Price, Date):
    with open('data/site_data.csv', mode='a+') as csvfile:
        item_data = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        item_data.writerow([ID, Desc, Price, Date])
        print("STORED DATA")
    

# * updateData: updates the ID's to be continuous (1, 2, 3, ...)
def updateData(ID, Desc, Price, Date):
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    filename = 'data/site_data.csv'
    header = ["ID", "Desc", "Price", "Date"]

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=header)
        writer = csv.DictWriter(tempfile, fieldnames=header, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_ALL)
        next(reader)

        # print the header
        writer.writerow({'ID': "ID", 'Desc': "Description", 'Price': "Price", 'Date': "Date"})
        
        for row in reader:
            if int(row['ID']) == ID:
                # print("updating row:", row[ID])
                row['Desc'], row['Price'], row['Date'] = Desc, Price, Date
            row = {'ID': row['ID'], 'Desc': row['Desc'], 'Price': row['Price'], 'Date': row['Date']}
            writer.writerow(row)

    shutil.move(tempfile.name, 'data/site_data.csv')


def main():
    csv_file = csv.reader(open('data/items.csv', 'r'), delimiter=',')
    total = totalRows('data/items.csv')
    next(csv_file)
    for row in csv_file:

        ID = int(row[0])
        title, short_desc, converted_price, date_str = getInfo(ID)
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