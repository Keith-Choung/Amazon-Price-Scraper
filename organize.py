import csv
from tempfile import NamedTemporaryFile
import shutil

def total_rows(filename: str) -> int:

    with open('items.csv', 'r') as csv_file:
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


def add_link(link: str):
    print("add_link\n")

    # ? check if link is valid?
    # ! or else will crash program.

    filename = 'items.csv'
    ID = createID(getIDs(filename))

    with open(filename, 'a+') as csvfile:
        item_data = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        
        item_data.writerow([ID, link])
    print("added link to items.csv\n")

def remove_link(ID: int):
    print("remove_link\n")

    tempfile = NamedTemporaryFile
    filename_items = 'items.csv'
    filename_site = 'site_data.csv'

    with open(filename_items, 'r') as items, tempfile:
        reader = csv.reader(filename_items)
        writer = csv.writer(tempfile, delimiter=',',
        quotechar='"', quoting=csv.QUOTE_ALL)

        next(reader)

        for row in reader:
            if int(row[0]) != ID:
                writer.writerow(row)
        
    shutil.move(tempfile.name, filename_items)


# add_link("https://www.amazon.com/Kodiak-Canvas-Flex-Bow-Deluxe-8-Person/dp/B001NZWQ1C/ref=sxin_2_osp20-bc4034b6_cov?ascsubtag=bc4034b6-8da9-4a1c-89a9-40f92ed4dcf3&creativeASIN=B001NZWQ1C&cv_ct_id=amzn1.osp.bc4034b6-8da9-4a1c-89a9-40f92ed4dcf3&cv_ct_pg=search&cv_ct_wn=osp-search&keywords=tent&linkCode=oas&pd_rd_i=B001NZWQ1C&pd_rd_r=cf5e6cc5-3250-4f56-a8cb-62195d8ab181&pd_rd_w=c3a2L&pd_rd_wg=i8fMf&pf_rd_p=43ba9e17-96f5-4491-b054-e546013f7dc4&pf_rd_r=BQ3ZK0ZX5XBBWS9YR2TN&qid=1565832053&s=electronics&tag=bestcont06-20")
# remove_link(5)