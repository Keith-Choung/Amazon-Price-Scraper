

# ! ALERT
# * FUNCTION
# ? QUESTION
# COMMENT

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import smtplib  # simple mail protocol
import time
import datetime
import csv
import organize
import pprint

# URL = "https://www.amazon.com/Dell-LED-Lit-Monitor-Black-S3219D/dp/B07JVQ8M3Q/ref=sr_1_4?keywords=monitor&qid=1562984199&refinements=p_n_size_browse-bin%3A3547808011%7C3547809011&rnid=2633086011&s=pc&sr=1-4"
       
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

def get_info(ID):
    
    csv_file = csv.reader(open('items.csv', 'r'), delimiter=",")
    next(csv_file) # skips header
    i = 0
    target = ""
    print("ID", ID)
    for row in csv_file:
        # print("row: ", row)
        if(ID == int(row[0])):
            target = row
            # print("Target:\n" , target)
            break
        else:
            i += 1
            continue

    URL = target[2].replace('\"', '')       # need to take out the quotes in the string
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
    price_list = []
    i = 0
    p = 0
    exist = False
    with open('site_data.csv', mode='r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            price = row[2]
            price_list.append(float(price))
            i += 1
            if (int(row[0]) == ID):
                exist = True
    print(price_list)
    print("ID:", ID)
    if not price_list:
        print("1check_price returned: TRUE\n")
        return True, exist
    elif (not exist or new_price < price_list[ID-1]):
        exist = True
        return True, exist
    print("check_price returned: FALSE\n")
    return False, exist


# * stores data: reads in data and stores it into csv file. checks if data is new and updates
def store_data(ID, Desc, Price, Date):
    print("store_data\n")
    # after reading, if the price is new, replace that line
    with open('site_data.csv', mode='a+') as csvfile:
        item_data = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        if organize.checkIDs(ID):
            item_data.writerow([ID, Desc, Price, Date])
        else:
            organize.createID(organize.getIDs('items.csv'))
        print("STORED DATA")
    

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
        # ! get ID to run through checks
        if (check_price(ID, converted_price)):
            store_data(ID, short_desc, converted_price, date_str)
            # print(link)
            # send_mail(ID, short_desc, converted_price, date, link)
        if (ID == total):
            break
    
    print("EXIT\n")

# main()
# print(get_info(1))
# print(check_price(1, 300))
