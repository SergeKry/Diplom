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

    def test_full_name(self):
        date = datetime.date.today()
        person1 = Person(' Alex', date, 'чоловік')
        person2 = Person(' Alex', date, 'чоловік', second_name=' John')
        person3 = Person(' Alex', date, 'чоловік', second_name=' John', last_name=' ')
        person4 = Person(' Alex', date, 'чоловік', second_name=' John', last_name='')
        self.assertEqual(person1.full_name, 'Alex')
        self.assertEqual(person2.full_name, 'Alex John')
        self.assertEqual(person3.full_name, 'Alex John')
        self.assertEqual(person4.full_name, 'Alex John')

    def test_age(self):
        birth_date = datetime.date(1990, 6,6)
        d_date = datetime.date(2000,6,7)
        person1 = Person('Alex', birth_date, 'чоловік', death_date=d_date)
        self.assertEqual(person1.calculate_age, 10)


if __name__ == '__main__':
    unittest.main()
