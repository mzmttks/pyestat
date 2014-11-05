import pyestat
import unittest

class TestGetData(unittest.TestCase):
    def setUp(self):
        pass

    def test_constructData(self):
        url = pyestat.constructURL("getStatsList", {"surveyYears": "b"})
        self.assertTrue(url[:4] == "http")


    def test_find_date(self):
        # find stats on 2010
        result = pyestat.find(year=2010)

        # find stats on 2010-2014  (error)
        with self.assertRaises(ValueError):
            pyestat.find(year=(2010, 2014))

        # find stats on 2010-12
        result = pyestat.find(year=2010, month=12)

        # find stats from 2010-10 to 2014-10
        result = pyestat.find(year=(2010, 2014), month=10)

        # find stats from 2010-1 to 2014-10
        result = pyestat.find(year=(2010, 2014), month=(1, 10))

        # find stats from 2010-1 to 2010-10
        result = pyestat.find(year=2010, month=(1, 10))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestGetData))
    return suite

if __name__ == '__main__':
    unittest.main()
