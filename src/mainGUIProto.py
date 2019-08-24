from tempfile import NamedTemporaryFile
from tkinter import *

import csv
import shutil
import importlib
import commands as com
import scraper as scrap

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

        self.addButton = Button(frame, text="Add", fg="red", command=self.printMessage)
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