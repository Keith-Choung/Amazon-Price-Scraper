
# ! reinstall macOS b/c it deleted Python 2.7
# ! ALERT
# * FUNCTION
# ? QUESTION
# COMMENT

from bs4 import BeautifulSoup
import requests
import smtplib  # simple mail protocol
import time
import datetime
import csv

URL = 'https://www.amazon.com/Dell-LED-Lit-Monitor-Black-S3219D/dp/B07JVQ8M3Q/ref=sr_1_4?keywords=monitor&qid=1562984199&refinements=p_n_size_browse-bin%3A3547808011%7C3547809011&rnid=2633086011&s=pc&sr=1-4'

headers = {
    "User-Agnet": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


def check_price():
    page = requests.get(URL, headers=headers)

    # parse everything for us
    soup = BeautifulSoup(page.content, 'html.parser')  # ? clarification

    # print(soup.prettify())

    unstripped_title = soup.find(id="productTitle").get_text()
    title = unstripped_title.strip()

    # make short description to store
    title_split = title.split()
    short_desc_split = title_split[0:6]
    short_desc = " ".join(short_desc_split)

    price = soup.find(id="priceblock_ourprice").get_text()
    # takes out '$' and the cents | still a string
    converted_price = float(price[1:4])

    if (converted_price < 300):
        date = datetime.date.today()
        date_str = "{}/{}/{}".format(date.month, date.day, date.year)

        store_data(short_desc, converted_price, date_str)
        # send_mail()

    print(title)  # -> prints the title
    print(converted_price)

# sends email w updated price


def send_mail():
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
        'tchennn@umich.edu',  # to
        msg
    )

    print("email has been sent")

    server.quit()


# * stores data: reads in data and stores it into csv file. checks if data is new and updates
def store_data(Desc, Price, Date):
    # ! newline='' is not working correctly. might be becuase 'encodings' isn't added
    with open('site_data.csv', mode='w+') as csvfile:
        item_data = csv.writer(csvfile, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_ALL)

        # OrigPrice =
        # if (Price < OrigPrice):
        item_data.writerow([Desc, Price, Date])


    # * to keep the program running daily
    # while(True):
    #     check_price()
    #     time.sleep(60 * 60 * 5)  # pauses while loop for a day
check_price()
