import csv
import smtplib  # simple mail protocol
from tempfile import NamedTemporaryFile
import shutil

def totalRows(filename: str) -> int:
    with open('data/items.csv', 'r') as csv_file:
        readCSV = csv.reader(csv_file, delimiter=",")
    # csv_file = csv.reader(open(filename, 'r'), delimiter=",")
        next(readCSV)
        row_count = sum(1 for row in readCSV) # * sf: sum is more efficient
    return row_count


def checkIDs(id: int, filename) -> bool:
    with open(filename, 'r') as csv_file:
        readCSV = csv.reader(csv_file, delimiter=",")
        site_data_cols = ["ID","Description","Price","Date"]
        items_cols = ["ID","Description","URL"]
        ids = []
        for row in readCSV:
            if row == site_data_cols or row == items_cols:
                continue
            elif id == int(row[0]):
                return True
        return False


def getIDs(filename: str)-> list:
    with open('data/items.csv', 'r') as csv_file:
        readCSV = csv.reader(csv_file, delimiter=",")
        next(readCSV) # skips header
        ids = [] # return list of IDs
        for row in readCSV:
            ids.append(row[0])
        return ids


def createID(ids: list) -> int:
    # if there is no ID/list is empty
    if not ids:
        return 1
    return int(ids[-1]) + 1


def getRows(ID: int) -> int:
    with open('data/items.csv', 'r') as csv_file:
        readCSV = csv.reader(csv_file, delimiter=",")
        next(readCSV)
        row_number = 1
        for row in readCSV:
            if ID == int(row[0]):
                return row_number
            else:
                row_number += 1
        return row_number


def addURL(url: str):
    print("addURL\n")
    filename = 'data/items.csv'
    ID = createID(getIDs(filename))

    with open(filename, 'a+') as csvfile:
        item_data = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        item_data.writerow([ID, url])
    print("added url to items.csv\n")


def removeURL(ID: int):
    print("removeURL\n")

    found = False
    tempfile1 = NamedTemporaryFile(mode='w', delete=False)
    filename_items = 'data/test_items.csv'
    header_items = ["ID","URL"]
    filename_site = 'data/test_site.csv'
    header_site = ["ID", "Desc", "Price", "Date"]

    with open(filename_items, 'r+') as items, tempfile1:
        print("removing from items")
        reader = csv.reader(items)
        writer = csv.writer(tempfile1, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_ALL)

        next(reader)
        writer.writerow(header_items)

        for row in reader:
            if int(row[0]) != ID:
                found = True
                writer.writerow(row)

    if (not found):
        print("ID not found.")
        return

    shutil.move(tempfile1.name, filename_items)

    tempfile2 = NamedTemporaryFile(mode='w', delete=False)
    with open(filename_site, 'r+') as site, tempfile2:
        print("removing from site")
        reader = csv.reader(site)
        writer = csv.writer(tempfile2, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_ALL)

        next(reader)
        writer.writerow(header_site)

        for row in reader:
            if int(row[0]) != ID:
                writer.writerow(row)
        
    shutil.move(tempfile2.name, filename_site)


def updateIDs(filename: str):
    print("updating IDs\n")
    
    tempfile1 = NamedTemporaryFile(mode='w', delete=False)
    tempfile2 = NamedTemporaryFile(mode='w', delete=False)
    filename_items = 'data/test_items.csv'
    header_items = ["ID","URL"]
    filename_site = 'data/test_site.csv'
    header_site = ["ID", "Desc", "Price", "Date"]

    with open(filename_items, 'r+') as items, tempfile1:
        print("updating items")
        reader = csv.DictReader(items)
        writer = csv.DictWriter(tempfile1, fieldnames=header_items,delimiter=',',
            quotechar='"', quoting=csv.QUOTE_ALL)

        # next(reader)
        writer.writerow({'ID': "ID", 'URL': "URL"})

        id_count = 1
        prev = 0
        for row in reader:
            ID = int(row["ID"])

            if ID != id_count:
                print("if.. ID:", ID)
                row["ID"], row["URL"] = prev+1, row["URL"]
                row = {"ID": row["ID"], "URL": row["URL"]}
                writer.writerow(row)
            else:
                print("else.. ID:", ID)
                row["ID"], row["URL"] = row["ID"], row["URL"]
                row = {"ID": row["ID"], "URL": row["URL"]}
                writer.writerow(row)
            prev = int(row["ID"]) # * store previous value
            id_count += 1
    
    shutil.move(tempfile1.name, filename_items)

    with open(filename_site, 'r+') as site, tempfile2:
        print("updating site")
        reader = csv.DictReader(site)
        writer = csv.DictWriter(tempfile2, fieldnames=header_site,delimiter=',',
            quotechar='"', quoting=csv.QUOTE_ALL)

        # next(reader)
        writer.writerow({'ID': "ID", 'Desc': "Desc", 'Price': "Price", 'Date': "Date"})

        id_count = 1
        prev = 0
        for row in reader:
            ID = int(row["ID"])

            if ID != id_count:
                print("if.. ID:", ID)
                row["ID"], row["Desc"], row["Price"], row["Date"] = prev+1, row["Desc"], row["Price"], row["Date"]
                row = {"ID": row["ID"], "Desc": row["Desc"], "Price":row["Price"], "Date":row["Date"]}
                writer.writerow(row)
            else:
                print("else.. ID:", ID)
                row["ID"], row["Desc"], row["Price"], row["Date"] = row["ID"], row["Desc"], row["Price"], row["Date"]
                row = {"ID": row["ID"], "Desc": row["Desc"], "Price":row["Price"], "Date":row["Date"]}
                writer.writerow(row)
            prev = int(row["ID"]) # * store previous value
            id_count += 1
    
    shutil.move(tempfile2.name, filename_site)


# ! INCOMPLETE
def sendMail(link):
    print("sendMail\n")
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