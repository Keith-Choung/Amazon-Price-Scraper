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

    def setUp(self):
        ml = """
        <h1 id="title" class="a-size-large a-spacing-none">
            <span id="productTitle" class="a-size-large">
            "
                
                    
                    
                

                
                    
                    
            Dell S Series Led-Lit Monitor 32" Black (S3219D), QHD 2560 X 1440, 60Hz, 99% sRGB, 16: 9, AMD FreeSync, 2 x 5W Speakers, 2 x HDMI 1.4, DP 1.2, USB 3.0
                    
                

                
                    
                    
                
            "
            </span>
            <span id="titleEDPPlaceHolder"></span>
        </h1>"""
        self.soup = BeautifulSoup(ml, "lxml")

    def test_bs4(self):
        matching = self.soup.find("span", {"id":"productTitle"})
        
if __name__ == '__main__': 
    unittest.main() 
    