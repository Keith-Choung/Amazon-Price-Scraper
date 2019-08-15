
# ! ALERT
# * FUNCTION
# ? QUESTION
# COMMENT

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import smtplib  # simple mail protocol
import datetime
import csv
import organize
from tempfile import NamedTemporaryFile
import shutil

       
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

def get_info(ID):
    csv_file = csv.reader(open('items.csv', 'r'), delimiter=",")
    next(csv_file) # skips header
    i = 0
    target = ""
    # print("ID", ID)
    for row in csv_file:
        # print("row: ", row)
        if(ID == int(row[0])):
            target = row
            # print("Target:\n" , target)
            break
        else:
            i += 1
            continue

    URL = target[1].replace('\"', '')       # need to take out the quotes in the string
    page = requests.get(URL, headers=headers)
 
    # parse everything for us
    # ! 'lxml' is better parser. amazon's html is messy?
    soup = BeautifulSoup(page.content, 'lxml')
    #! need to specify tags AND attributes for bs4 to find()

    if soup.find("span", {"id": "productTitle"}) == None:
        unstripped_title = soup.find("h1", {"id": "title"}).get_text()
    else:
        unstripped_title = soup.find("span", {"id": "productTitle"}).get_text()

    
    # make short description to store
    title_split = unstripped_title.split()
    short_desc_split = title_split[0:6]
    short_desc = " ".join(short_desc_split)

    price = soup.find(id="priceblock_ourprice").get_text()
    # takes out '$' and the cents | still a string
    converted_price = float(price[1:4])

    date = datetime.date.today()
    date_str = "{}/{}/{}".format(date.month, date.day, date.year)

    return unstripped_title, short_desc, converted_price, date_str

# * check_price: takes in origPrice and index and compares with new price w that index's value
def check_price(ID, new_price):
    print("check_price\n")
    orig = []
    i = 0
    p = 0
    exist = False
    with open('site_data.csv', mode='r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            if (int(row[0]) == ID):
                exist = True
                orig = row
    print("ID:", ID)
    if not exist:
        print("check_price returned: DNE\n")
        return 1
    elif (exist and float(orig[2]) > new_price):
        print("check_price returned: UPDATE\n")
        return 2
    print("check_price returned: N/A\n")
    return 3

# * stores data: reads in data and stores it into csv file. checks if data is new and updates
def store_data(ID, Desc, Price, Date):
    print("store_data\n")

    # append
    with open('site_data.csv', mode='a+') as csvfile:
        item_data = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        item_data.writerow([ID, Desc, Price, Date])
            # if the ID is not found, create a new one and append
            # new_ID = organize.createID(organize.getIDs('items.csv'))
            # item_data.writerow([new_ID, Desc, Price, Date])
        
        print("STORED DATA")
    
def update_data(ID, Desc, Price, Date):
    print("update_data\n")

    tempfile = NamedTemporaryFile(mode='w', delete=False)
    filename = 'site_data.csv'
    header = ["ID", "Desc", "Price", "Date"]

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=header)
        writer = csv.DictWriter(tempfile, fieldnames=header, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_ALL)
            
        next(reader)

        # * print the header
        writer.writerow({'ID': "ID", 'Desc': "Description", 'Price': "Price", 'Date': "Date"})
        for row in reader:
            if int(row['ID']) == ID:
                # print("updating row:", row[ID])
                row['Desc'], row['Price'], row['Date'] = Desc, Price, Date
            row = {'ID': row['ID'], 'Desc': row['Desc'], 'Price': row['Price'], 'Date': row['Date']}
            writer.writerow(row)

    shutil.move(tempfile.name, 'site_data.csv')
    

def send_mail(link):
    print("send_mail\n")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()  # command sent by email when identifying btwn the 2
    server.starttls()
    server.ehlo()

    server.login('keithchoung@gmail.com', 'kfcwxiosfwykkzhb')

    subject = "price fell down!"
    body = "check the amazon link: {}".format(link)

    msg = "Subject: {}\n\n{}".format(
        subject, body)  # ? why does it need two '\n'

    server.sendmail(
        'keithchoung@gmail.com',  # from
        'kjchoung@ucdavis.edu',  # to
        msg
    )

    print("email has been sent")

    server.quit()

def main():
    csv_file = csv.reader(open('items.csv', 'r'), delimiter=',')
    total = organize.total_rows('items.csv')
    next(csv_file)
    for row in csv_file:

        ID = int(row[0])
        title, short_desc, converted_price, date_str = get_info(ID)
        switch_case_value = check_price(ID, converted_price)

        if (switch_case_value == 1): # * -> append
            store_data(ID, short_desc, converted_price, date_str)
        elif (switch_case_value == 2): # * -> update
            update_data(ID,short_desc,converted_price, date_str)
        else: # * -> continue
            continue
        if(ID == total):
            break
    
    print("EXIT\n")

main()
