import scraper

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/Users/keithchoung/Desktop/CS/WebScraper/src')


import cmd

intro = "Welcome to your WebScraper!\nType -help to list all of the commands you can use :)"

cmd.cmdloop(intro)
