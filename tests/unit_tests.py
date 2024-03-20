import unittest
from Diplom.person import *


class TestPerson(unittest.TestCase):
    def test_parse_date(self):
        result = datetime.date(2011, 11, 11)
        self.assertEqual(Person.parse_date('11.11.2011'), result)
        self.assertEqual(Person.parse_date('11 11 2011'), result)
        self.assertEqual(Person.parse_date('11/11/2011'), result)
        self.assertEqual(Person.parse_date('11-11-2011'), result)

    def test_string_date(self):
        date1 = datetime.date(1990, 1, 1)
        self.assertEqual(Person.string_date(date1), '01.01.1990')
        date2 = datetime.date(1990, 11, 11)
        self.assertEqual(Person.string_date(date2), '11.11.1990')
        self.assertEqual(Person.string_date(None), None)


if __name__ == '__main__':
    unittest.main()