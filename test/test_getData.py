import pyestat
import unittest
import pprint

pp = pprint.PrettyPrinter(indent=2)


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

    def checkKeys(self, obj, keys):
        for k in keys:
            self.assertTrue(k in obj.keys())

    def test_xml2dataList(self):
        obj = pyestat.xml2obj("".join(open("test/statsList.xml")))
        self.checkKeys(obj["result"], ["status", "error_msg", "date"])
        self.checkKeys(obj["parameter"], ["lang"])
        self.assertIsInstance(obj["datalist_inf"], list)
        [self.checkKeys(l, ["stat_name", "gov_org", "statistics_name", "title",
                            "cycle", "survey_date", "open_date", "small_area"])
         for l in obj["datalist_inf"]]

    def test_xml2dataMeta(self):
        obj = pyestat.xml2obj("".join(open("test/metaInfo.xml")))
        self.checkKeys(obj["result"], ["status", "error_msg", "date"])
        self.checkKeys(obj["parameter"], ["lang"])
        self.checkKeys(obj["metadata_inf"], ["table_inf", "class_inf"])

    def test_xml2dataData(self):
        obj = pyestat.xml2obj("".join(open("test/statsData.xml")))
        self.checkKeys(obj["result"], ["status", "error_msg", "date"])
        self.checkKeys(obj["parameter"], ["lang"])


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestGetData))
    return suite

if __name__ == '__main__':
    unittest.main()
