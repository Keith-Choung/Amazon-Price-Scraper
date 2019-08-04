

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

# URL = "https://www.amazon.com/Dell-LED-Lit-Monitor-Black-S3219D/dp/B07JVQ8M3Q/ref=sr_1_4?keywords=monitor&qid=1562984199&refinements=p_n_size_browse-bin%3A3547808011%7C3547809011&rnid=2633086011&s=pc&sr=1-4"
       
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

def get_info(index):
    
    csv_file = csv.reader(open('items.csv', 'r'), delimiter=",")
    i = 0
    target = ""
    for row in csv_file:
        if(index == i):
            target = row
            print("Target:\n" , target)
            break
        else:
            i += 1
            continue

    URL = target[1].replace('\"', '')       # need to take out the quotes in the string
    page = requests.get(URL, headers=headers)

    # parse everything for us
    soup = BeautifulSoup(page.content, 'lxml')  # ! 'lxml' is better parser. amazon's html is messy?

    unstripped_title = soup.find(id="productTitle").get_text()
    title = unstripped_title.strip()

    # make short description to store
    title_split = title.split()
    short_desc_split = title_split[0:6]
    short_desc = " ".join(short_desc_split)

    price = soup.find(id="priceblock_ourprice").get_text()
    # takes out '$' and the cents | still a string
    converted_price = float(price[1:4])

    date = datetime.date.today()
    date_str = "{}/{}/{}".format(date.month, date.day, date.year)

    print(title)  # -> prints the title
    print(converted_price)

    return title, short_desc, converted_price, date_str

# * check_price: takes in origPrice and index and compares with new price w that index's value
def check_price(desc, new_price):
    print("check_price\n")
    price_list = []
    i = 0
    p = 0
    with open('site_data.csv', mode='r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            price = row[1]
            price_list.append(float(price))
            i += 1
            if (row[0] == desc):
                p == i  # ? the one time row[0] == desc, p will take that value, once maybe...
    print("price_list[p]:", price_list[p])
    if (new_price < price_list[p]):
        print("check_price returned: TRUE\n")
        return True
    print("check_price returned: FALSE\n")
    return False


# * stores data: reads in data and stores it into csv file. checks if data is new and updates
def store_data(Desc, Price, Date):
    print("store_data\n")
    # after reading, if the price is new, replace that line
    with open('site_data.csv', mode='w+') as csvfile:
        item_data = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        print("went thru open")
        item_data.writerow([Desc, Price, Date])


def send_mail():
    print("send_mail\n")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()  # command sent by email when identifying btwn the 2
    server.starttls()
    server.ehlo()

    server.login('keithchoung@gmail.com', 'kfcwxiosfwykkzhb')

    subject = "price fell down!"
    body = "check the amazon link: https://www.amazon.com/Dell-LED-Lit-Monitor-Black-S3219D/dp/B07JVQ8M3Q/ref=sr_1_4?keywords=monitor&qid=1562984199&refinements=p_n_size_browse-bin%3A3547808011%7C3547809011&rnid=2633086011&s=pc&sr=1-4"

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
    index = 1
    # get_info(index)
    title, short_desc, converted_price, date_str = get_info(index)
    print("\n")
    print("Title: {}\nshort_desc: {}\nconverted_price: {}\ndate_str: {}\n".format(title, short_desc, converted_price, date_str))
    if (check_price(short_desc, converted_price)):
        store_data(short_desc, converted_price, date_str)
        # send_mail()


# get_info(1)

main()



# * to keep the program running daily
# while(True):
#     check_price()
#     time.sleep(60 * 60 * 5)  # pauses while loop for a day
# main()