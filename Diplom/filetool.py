from person import Person
import csv


def export_file(path, keyword):
    heading_row = ["ПІБ", "Стать", "Дата народження", "Дата смерті"]
    if path:
        search_data = Person.search_person(keyword)
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(heading_row)
            for item in search_data:
                modified_item = list(item)
                modified_item[0] = modified_item[0].title()
                writer.writerow(modified_item)
        return 'Файл збережено'


def import_file(path):
    if path:
        try:
            with open(path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                data = []
                for row in reader:
                    data.append(row)
                for person in data[1:]:
                    full_name = person[0]
                    birth_date = Person.parse_date(person[2])
                    gender = person[1]
                    death_date = Person.parse_date(person[3]) if person[3] != '' else None
                    Person(full_name, gender, birth_date, death_date)
            return 'Дані імпортовані'
        except Exception:
            return 'Неможливо завантажити'
