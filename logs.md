8/11/2019
- starting logs on 8/11 for the sake of remembering and seeing development/growth in code
- created tests using unittest library and test inputs to expedite and broaden testing
- creating new python file with different functions to organize.
    - for now, it's organize.py, until i figure out how to name these files as well as test_input.txt which might need to change file format?
- sf -> stackoverflow: shows where I got useful information from stackoverflow

- Today I Learned:
    - using "with open(filename)..." automatically closes files when outside of scope. 

8/12/2019
- bs4 wasn't parsing correctly again.
    - everytime I add something to the program, it returns an error that the parser found a None type when searching for id="productTitle"
- trying to find a way to "update" prices if they are changed, but there are three conditions for check_price: add, don't add and update, but cannot just return boolean.
    - trying to remember what to do in ECS 34 for conditional returns/returning cases or something like that

- Today I learned:
    - you have to specify the tag AND the attribute for bs4's find() function.

8/13/2019
- was testing and found that when I ran the test file in terminal, it would also run the scraper.py. Thinking it is because unittest looks for the "main()" function and finds it in both scraper.py and test.py. Should change main in the test.py to "test()".


- Today I learned:
    - there are no switch cases in python (surprisingly) but you can return a dictionary based on value.

8/14/2019
- implementing switch cases via dictionaries in python
- realized I can't return dictionaries either so I just used conditional returns

- Today I learned:
    - you can update a csv row by inputting it with column:value pairs in a dictionary
    - to PROPERLY update a csv file, you create a tempfile and then move it to that file's destination destination... but does it keep the name?