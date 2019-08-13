import organize
import scraper
import unittest
from bs4 import BeautifulSoup

class simple_test_cases(unittest.TestCase):

    def test(self):         
        self.assertTrue(True)

    def test_total_rows(self):
        filename = 'items.csv'
        self.assertEqual(organize.total_rows(filename), 3)

    def test_get_row(self):
        self.assertEqual(organize.get_row(1), 1)
        self.assertEqual(organize.get_row(2), 2)   
        self.assertEqual(organize.get_row(3), 3)

    def test_checkIDs(self):
        self.assertTrue(organize.checkIDs(3))
        self.assertFalse(organize.checkIDs(4))

    def test_getID(self):
        filename = 'items.csv'
        self.assertEqual(organize.getIDs(filename), ['1','2','3'])

    def test_createID(self):
        ids0 = []
        ids1 = [1]
        ids2 = [1, 2, 3, 4, 5, 6]

        self.assertEqual(organize.createID(ids0), 1)
        self.assertEqual(organize.createID(ids1), 2)
        self.assertEqual(organize.createID(ids2), 7)

    # def setUp(self):
    #     ml = """
    #     <a id="x">1</a>
    #     <A id="a">2</a>
    #     <b id="b">3</a>
    #     <b href="foo" id="x">4</a>
    #     <ac width=100>4</ac>"""
    #     self.soup = BeautifulSoup(ml)

    # def test_bs4(self):
    #     matching = self.soup('a')
    #     self.assertEqual(len(matching), 1)
    #     self.assertEqual(matching[0].name, 'a')
    #     self.assertEqual(matching, self.soup.findAll('a'))
        
if __name__ == '__main__': 
    unittest.main() 
    