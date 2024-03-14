from person import Person
import csv


def export_file(path):
    heading_row = ["Прізвище", "Ім'я", "По батькові", "Дата народження", "Дата смерті", "Стать", "Вік"]
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(heading_row)
        for item in Person.PERSONS:
            writer.writerow(item[0:7])
    return 'Файл збережено'


