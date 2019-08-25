from tempfile import NamedTemporaryFile
from tkinter import *

import csv
import shutil
import importlib
import commands as com
import scraper as scrap

root = Tk() # * creates the blank window

c = com.Commands()

def printMessage():
    print("Wow it works")

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def checkURL():
    print("Checking URL")
    # Some Regex Function

def addURL():
    inputValue=urlEntry.get()
    c.addURL(inputValue)
    print("Added Item")

def removeID():
    inputValue=IDEntry.get()

    # if the input value is an int and the ID is in files -> Remove
    if isInt(inputValue):
        if c.checkIDs(int(inputValue)):
            c.removeItem(int(inputValue))
            print("Removed Item")
    else:
        print("Invalid Input")

# Title
titleLable = Label(root, text="Amazon Price Scraper", bg="grey", fg="white")
titleLable.grid(row=1, column=2)

# URL Entry/Label
urlLabel = Label(root, text="URL:")
urlLabel.grid(row=3, column=1, sticky=E)

urlEntry = Entry(root)
urlEntry.grid(row=3, column=2, sticky=E)

# Add URL | command=lambda -> do this
addButton = Button(root, text="Add", fg="red", command=lambda: addURL())
addButton.grid(row=3, column=3)

# ID Entry/Label
IDLabel = Label(root, text="ID:")
IDLabel.grid(row=4, column=1, sticky=E)

IDEntry = Entry(root)
IDEntry.grid(row=4, column=2, sticky=E)

# Remove ID
removeButton = Button(root, text="Remove", fg="purple", command=lambda: removeID())
removeButton.grid(row=4, column=3)

# Scrape
scrapeButton = Button(root, text="Scrape", fg="orange", command=lambda: scrap.main())
scrapeButton.grid(row=5, column=1)

# Refresh CSV File
refreshButton = Button(root, text="Refresh", fg="green", command=lambda: c.resetIDs())
refreshButton.grid(row=5, column=2)

# Quit
quitButton = Button(root, text="Quit", command=root.quit) 
quitButton.grid(row=5, column=3)

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