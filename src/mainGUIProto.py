import scraper
import csv
from tempfile import NamedTemporaryFile
import shutil
from tkinter import *

class ScrapyButtons:

    def __init__(self, master):
        frame = Frame(master)
        frame.grid()

        titleLable = Label(frame, text="Scra.py", bg="red", fg="white")
        titleLable.grid()

        bottomFrame = Frame()
        bottomFrame.grid(sticky=S)

        # self.printButton = Button(bottomFrame, text="Print Message", command=self.printMessage)
        # self.printButton.grid()
        # * quit breaks the mainloop
        self.quitButton = Button(bottomFrame, text="Quit", command=frame.quit) 
        self.quitButton.grid()

        self.addButton = Button(frame, text="Add", fg="red", command=self.add_URL)
        self.removeButton = Button(frame, text="Remove", fg="purple", )
        self.refreshButton = Button(frame, text="Refresh", bg = "purple", fg="green")

        # * grid them in to display them
        self.addButton.grid(row=1, sticky=E)

        self.urlLabel = Label(master, text="URL:")
        self.urlEntry = Entry(master)
        self.urlLabel.grid(row=3)
        self.urlEntry.grid(row=3, sticky=E)

        self.removeButton.grid()
        self.refreshButton.grid()


    def printMessage(self):
        print("Wow it works")


    def total_rows(self, filename: str) -> int:

        with open('data/items.csv', 'r') as csv_file:
            readCSV = csv.reader(csv_file, delimiter=",")
        # csv_file = csv.reader(open(filename, 'r'), delimiter=",")
            next(readCSV)
            row_count = sum(1 for row in readCSV) # * sf: sum is more efficient
        return row_count


    def checkIDs(self, id: int, filename) -> bool:
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


    def getIDs(self, filename: str)-> list:
        with open('data/items.csv', 'r') as csv_file:
            readCSV = csv.reader(csv_file, delimiter=",")
            next(readCSV) # skips header
            ids = [] # return list of IDs
            for row in readCSV:
                ids.append(row[0])
            return ids


    def createID(self, ids: list) -> int:
        # if there is no ID/list is empty
        if not ids:
            return 1
        return int(ids[-1]) + 1


    def get_row(self, ID: int) -> int:
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


    def add_URL(self, url: str):
        print("add_link\n")

        filename = 'data/items.csv'
        ID = createID(getIDs(filename))

        with open(filename, 'a+') as csvfile:
            item_data = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
            item_data.writerow([ID, url])
        print("added url to items.csv\n")


    def remove_link(self, ID: int):
        print("remove_link\n")

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



    def update_IDs(self, filename: str):
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



root = Tk() # * creates the blank window
canvas = Canvas(root, width=250, height=50)
canvas.grid()
scrapy = ScrapyButtons(root)
root.mainloop()

# def printName():
#     print("Hello my name is Keith")


# titleLable = Label(root, text="Scra.py", bg="red", fg="white")
# titleLable.pack()
# two = Label(root, text="Two", bg="green", fg="black")
# two.pack(fill=X)
# three = Label(root, text="Three", bg="blue", fg="white")
# three.pack(side=LEFT, fill=Y)

# # typable entries
# # urlLabel = Label(root, text="URL:")
# # urlEntry = Entry(root)

# # # * North, East, Sout West for sticky
# # urlLabel.grid(row=0, sticky=E)
# # urlEntry.grid(row=0, column=1)

# # # ? where do we want to put this?
 
# # theLabel.pack() # ! first place you can fit it. DO NOT USE

# topFrame = Frame(root, width=1000, height=1000)
# topFrame.pack()
# bottomFrame = Frame(root)
# bottomFrame.pack(side=BOTTOM)

# # making widgets
# # * created the widgets, does not display yet
# addButton = Button(topFrame, text="Add", fg="red", command=printName)
# removeButton = Button(topFrame, text="Remove", fg="purple")
# refreshButton = Button(bottomFrame, text="Refresh", bg = "purple", fg="green")

# # * pack them in to display them
# addButton.pack(side=LEFT)
# removeButton.pack(side=LEFT)
# refreshButton.pack(side=BOTTOM, fill=X)


# root.mainloop() # * makes sure that the window is constantly displayed