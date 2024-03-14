import datetime
from dateutil.relativedelta import relativedelta
from utils import print_date


class Person(object):
    PERSONS = []

    def __init__(self, first_name, birth_date, gender, second_name=None, last_name=None, death_date=None):
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.second_name = second_name
        self.last_name = last_name
        self.death_date = death_date
        Person.PERSONS.append((self.last_name, self.first_name, self.second_name, print_date(self.birth_date), print_date(self.death_date), self.gender, self.age))

    @property
    def age(self):
        today = datetime.date.today()
        return relativedelta(today, self.birth_date).years

    @classmethod
    def get_persons(cls, search_key):
        result = []
        for item in Person.PERSONS:
            full_name = item[0] + item[1] + item[2]
            if search_key in full_name:
                death_text = {f'{'Вмерла' if item[4] is 'жінка' else 'Вмер'} {item[4]}'} if item[4] is not None else None
                birth_text =


