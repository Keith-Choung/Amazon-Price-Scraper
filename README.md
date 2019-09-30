# Amazon Price Checker
This program's goal is to take in an Amazon URL and check that item's price by storing user input and the scraped data in two separate csv files

Please feel free to contribute to this as it is my very first project :)

There is no installation process yet as it is not finished.

Steps to Use:
- launch the GUI by typing "python3 src/mainGUI.py" in the Amazon Price Scraper directory
- Copy & paste a URL into the text box and press "Add"
- Press "Scrape" for the program to scrape for the data
- To remove an item, get the ID of the item and put it in the "Remove:" text box, then press "Remove"
- Press "Refresh" after removing an item to reset the IDs to be contiguous (1, 2, 3, ..)

Requirements:
- Python 3.4+
- Terminal
- Install BeautifulSoup

ToDo List:
- Implement email/text function through SMTP to notify user of updated prices 
- Simplify usage
    - Create UNDO Button
    - Scrape should happen to the URL that was added, instead of scraping the whole file after adding one URL
        - Scrape Most Recents Button

- Need to catch max redirect error and continue looping *DONE
- Remove should be coupled with refresh *DONE
- Near 100% request success with Sessions *DONE
- Allow interactive usage, either through terminal or GUI (Tkinter?) *DONE
- Determine what input removeURL should take *DONE
- Create a rotating User Agent function to prevent scrape blocking *DONE
