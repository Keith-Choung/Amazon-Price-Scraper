import csv

def total_rows(filename: str) -> int:

    with open('items.csv', 'r') as csv_file:
        readCSV = csv.reader(csv_file, delimiter=",")
    # csv_file = csv.reader(open(filename, 'r'), delimiter=",")
        next(readCSV)
        row_count = sum(1 for row in readCSV) # * sf: sum is more efficient
    return row_count

def checkIDs(id: int) -> bool:
    with open('items.csv', 'r') as csv_file:
        readCSV = csv.reader(csv_file, delimiter=",")
        next(readCSV)
        ids = []
        for row in readCSV:
            if id == int(row[0]):
                return True
        return False

def getIDs(filename: str)-> list:
    with open('items.csv', 'r') as csv_file:
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

def get_row(ID: int) -> int:
    with open('items.csv', 'r') as csv_file:
        readCSV = csv.reader(csv_file, delimiter=",")
        next(readCSV)
        row_number = 1
        for row in readCSV:
            if ID == int(row[0]):
                return row_number
            else:
                row_number += 1
        return row_number

