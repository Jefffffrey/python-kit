import unittest
from datetime import datetime
from unittest.mock import patch

from utils.date import *


class TestDate(unittest.TestCase):
    def test_to_date(self):
        date = '2016-05-26'
        date2 = datetime.date(2016, 5, 26)
        self.assertEqual(to_date(date), date2)

    def test_to_date_stamp(self):
        date = '2016-05-26'
        date2 = datetime.date(2016, 5, 26)
        self.assertEqual(date, to_stamp(date2))

    def test_sub(self):
        date = datetime.date
        values = {
            ('2016-05-26', 1): date(2016, 5, 25),
            ('2016-05-26', '2016-05-25'): 1,
            (date(2016, 5, 25), '2016-05-24'): 1,
            ('2016-05-26', 1, 'str'): '2016-05-25',
        }

        for arg, result in values.items():
            res = sub(*arg)
            self.assertEqual(res, result)

    @patch('utils.date.today', autospec=True)
    def test_days_ago(self, mock_today):
        values = {
            ('2016-06-26',): 2,
            ('2016-06-28',): 0
        }
        mock_today.return_value = datetime.date(2016, 6, 28)

        for arg, result in values.items():
            res = days_ago(*arg)
            self.assertEqual(res, result)

    def test_add(self):
        values = {
            ('2016-06-26', 4): datetime.date(2016, 6, 30),
            (datetime.date(2016, 6, 26), 6): datetime.date(2016, 7, 2),
            (datetime.date(2016, 6, 26), 6, 'str'): '2016-07-02'
        }

        for arg, result in values.items():
            res = add(*arg)
            self.assertEqual(res, result)
