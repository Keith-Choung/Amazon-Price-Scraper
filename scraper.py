
# ! ALERT
# * BETTER
# ? QUESTION
# COMMENT

from bs4 import BeautifulSoup
import requests
import smtplib  # simple mail protocol
import time

URL = 'https://www.amazon.com/Dell-LED-Lit-Monitor-Black-S3219D/dp/B07JVQ8M3Q/ref=sr_1_4?keywords=monitor&qid=1562984199&refinements=p_n_size_browse-bin%3A3547808011%7C3547809011&rnid=2633086011&s=pc&sr=1-4'

headers = {
    "User-Agnet": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


def check_price():
    page = requests.get(URL, headers=headers)

    # parse everything for us
    soup = BeautifulSoup(page.content, 'html.parser')

    # print(soup.prettify())

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    # takes out '$' and the cents | still a string
    converted_price = float(price[1:4])

    if (converted_price < 1800):
        send_mail()

    print(title.strip())  # -> prints the title
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


# while(True):
#     check_price()
#     time.sleep(60 * 60 * 5)  # pauses while loop for a day
check_price()
