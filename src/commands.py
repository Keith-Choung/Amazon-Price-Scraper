from tempfile import NamedTemporaryFile

import scraper as scrap
import importlib
import smtplib 
import shutil
import csv

class Commands:

    def __init__(self):
        pass

    def addURL(self, url: str):
        print("addURL\n")

        filename = 'data/items.csv'
        s = scrap.Files(filename)
        ID = s.createID(s.getIDs())

        with open(filename, 'a+') as csvfile:
            item_data = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
            item_data.writerow([ID, url])
        print("added url to items.csv\n")


    def removeItem(self, ID: int):
        print("removeURL\n")

        found = False
        tempfile1 = NamedTemporaryFile(mode='w', delete=False)
        filename_items = 'data/items.csv'
        header_items = ["ID","URL"]
        filename_site = 'data/site_data.csv'
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

    '''
    resetIDs: resets IDs in files to be contiguous (1, 2, 3 ...)
    '''
    def resetIDs(self):
        print("updating IDs\n")
        
        tempfile1 = NamedTemporaryFile(mode='w', delete=False)
        tempfile2 = NamedTemporaryFile(mode='w', delete=False)
        filename_items = 'data/items.csv'
        header_items = ["ID","URL"]
        filename_site = 'data/site_data.csv'
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
                    print(row["Desc"])
                    row["ID"], row["Desc"], row["Price"], row["Date"] = row["ID"], row["Desc"], row["Price"], row["Date"]
                    row = {"ID": row["ID"], "Desc": row["Desc"], "Price":row["Price"], "Date":row["Date"]}
                    writer.writerow(row)
                prev = int(row["ID"]) # * store previous value
                id_count += 1
        
        shutil.move(tempfile2.name, filename_site)

    '''
    checkIDs: checks if the target ID is in any of the files
    '''
    def checkIDs(self, id: int) -> bool:

        site_data_cols = ["ID","Description","Price","Date"]
        items_cols = ["ID","Description","URL"]

        filename = 'data/items.csv'

        with open(filename, 'r') as CSVFile:
            readCSV = csv.reader(CSVFile, delimiter=",")
            next(readCSV)

            # iterate through rows for target ID
            for row in readCSV:
                if row == site_data_cols or row == items_cols:
                    continue
                elif id == int(row[0]):
                    return True
            return False


    # ! INCOMPLETE
    def sendMail(self, link):
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

# s = scrpr.Files('data/items.csv')
# c = Commands()
# # c.addURL('https://www.amazon.com/Optimum-Nutrition-Standard-Protein-Chocolate/dp/B000QSNYGI/ref=sr_1_1_sspa?crid=1ZT5VOLE03TLN&keywords=protein+powder&qid=1566608841&s=gateway&sprefix=protein+%2Caps%2C210&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEySFFWNDFXTEZVVzhDJmVuY3J5cHRlZElkPUEwODcyOTM0RDREUDlUSzNEUEFRJmVuY3J5cHRlZEFkSWQ9QTAwNDA4OTUxR0xXRjQ2OURPMDZaJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==')
# c.removeItem(4)