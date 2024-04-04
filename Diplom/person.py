import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
import sqlite3


class Person(object):

    @staticmethod
    def parse_date(date):
        return parser.parse(date, dayfirst=True).date()

    @staticmethod
    def string_date(date):
        if date is not None:
            date_splitted = date.split('-')
            year = date_splitted[0]
            month = date_splitted[1].rjust(2, '0')
            day = date_splitted[2].rjust(2, '0')
            return '.'.join([day, month, year])
        else:
            return None

    @staticmethod
    def save_person(name, gender, birth, death):
        connection = sqlite3.connect("persons.db")
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO persons VALUES(?,?,?,?)''',
                       (name, gender, birth, death))
        connection.commit()
        connection.close()

    def __init__(self, full_name, gender, birth_date, death_date=None):
        self.full_name = full_name.lower()
        self.birth_date = birth_date
        self.gender = gender
        self.death_date = death_date
        Person.save_person(self.full_name, self.gender, self.birth_date, self.death_date)

    @staticmethod
    def calculate_age(birth_date, death_date):
        birth = Person.parse_date(birth_date)
        if death_date:
            death = Person.parse_date(death_date)
            return relativedelta(death, birth).years
        else:
            return relativedelta(datetime.date.today(), birth).years

    @classmethod
    def search_person(cls, search_key):
        connection = sqlite3.connect("persons.db")
        cursor = connection.cursor()
        if search_key == '*':
            cursor.execute('''SELECT * FROM persons''')
            search_data = cursor.fetchall()
        else:
            search_key = f'%{search_key}%'
            cursor.execute("""SELECT * FROM persons WHERE full_name LIKE (?)""", (search_key,))
            search_data = cursor.fetchall()
        return search_data

    @staticmethod
    def print_search_result(keyword):
        search_data = Person.search_person(keyword)
        result = []
        for item in search_data:
            result.append(Person.build_search_result_line(item))
        return result

    @staticmethod
    def build_search_result_line(data):
        full_name = data[0].title()
        age_expl = 'років'
        age = Person.calculate_age(data[2], data[3])
        if age % 10 == 1:
            age_expl = 'рік'
        if age % 10 in (2, 3, 4):
            age_expl = 'роки'
        if age % 100 in (11, 12, 13, 14):
            age_expl = 'років'
        age_string = f'{age} {age_expl},'
        gender = f'{data[1]}.'
        birth_expl = 'Народився' if data[1] == 'чоловік' else 'Народилася'
        birth_date = Person.string_date(data[2])
        birth_date_output = f'{birth_expl} {birth_date}.'
        death_date_output = ''
        if data[3]:
            death_date = Person.string_date(data[3])
            death_expl = 'Вмер' if data[1] == 'чоловік' else 'Вмерла'
            death_date_output = f' {death_expl} {death_date}'
        return ' '.join((full_name, age_string, gender, birth_date_output, death_date_output))
