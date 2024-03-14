from tkinter import *
from tkinter import ttk
from person import *
from utils import parse_date

root = Tk()
root.title("Person data")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


def startframe():
    startframe = ttk.Frame(root, padding="3 20 3 12")
    startframe.grid(column=0, row=0, sticky="NWES")
    ttk.Button(startframe, text="Почати роботу з порожньою базою", command=add_or_find, width=30).grid(row=1, column=1, sticky=(W, E))
    ttk.Button(startframe, text="Завантажити файл", command=root.destroy).grid(row=2, column=1, sticky='WE')
    ttk.Button(startframe, text="Вийти", command=root.destroy).grid(row=3, column=1)

    for child in startframe.winfo_children():
        child.grid_configure(padx=5, pady=5)


def add_or_find():
    add_or_find_frame = ttk.Frame(root, padding="3 20 3 12")
    add_or_find_frame.grid(column=0, row=0, sticky="NWES")
    ttk.Button(add_or_find_frame, text="Додати персону", command=add_person, width=30).grid(row=1, column=1, sticky="WE")
    ttk.Button(add_or_find_frame, text="Пошук", command=search).grid(row=2, column=1, sticky="WE")
    ttk.Button(add_or_find_frame, text="< Назад", command=startframe).grid(row=3, column=1)

    for child in add_or_find_frame.winfo_children():
        child.grid_configure(padx=5, pady=5)


def add_person():

    def validate_inputs():
        if name.get() == '' or birth_date.get() == '':
            return 'Заповніть обовʼязкові поля'
        try:
            birth = parse_date(birth_date.get())
            if birth > datetime.date.today():
                return 'Дата народження не може бути в майбутньому'
        except Exception as err:
            return 'Неправильна дати народженя: {}'.format(err)
        if death_date.get() != '':
            try:
                death = parse_date(death_date.get())
                if death > datetime.date.today():
                    return 'Дата смерті не може бути в майбутньому'
            except Exception:
                return "Неправильна дата смерті"
        return f'Песрону {name.get()} додано'

    def submit_person():
        validation_result = validate_inputs()
        feedback.set(validation_result)
        if 'додано' in validation_result:
            birth = parse_date(birth_date.get())
            death = parse_date(death_date.get()) if death_date.get() != '' else None
            first_name = name.get()
            sec_name = second_name.get() if second_name.get() != '' else None
            gend = gender.get()
            lst_name = last_name.get() if last_name.get() != '' else None
            print('OK')
            return Person(first_name, birth, gend, sec_name, lst_name, death)

    add_person_frame = ttk.Frame(root, padding="3 5 3 12")
    add_person_frame.grid(column=0, row=0, sticky="NWES")
    title = ttk.Label(add_person_frame, text="Додати персону", font='TkDefaultFont 16 bold')
    title.grid(row=1, column=1, sticky="W", pady=10, padx=3)

    name_label = ttk.Label(add_person_frame, text="Імʼя*")
    name_label.grid(row=2, column=1, sticky="W")
    name = StringVar()
    name_input = ttk.Entry(add_person_frame, textvariable=name, width=20)
    name_input.grid(row=3, column=1, sticky="W")

    second_name_label = ttk.Label(add_person_frame, text="По батькові")
    second_name_label.grid(row=2, column=2, sticky="W")
    second_name = StringVar()
    second_name_input = ttk.Entry(add_person_frame, textvariable=second_name, width=20)
    second_name_input.grid(row=3, column=2, sticky="W")

    last_name_label = ttk.Label(add_person_frame, text="Прізвище")
    last_name_label.grid(row=2, column=3, sticky="W")
    last_name = StringVar()
    last_name_input = ttk.Entry(add_person_frame, textvariable=last_name, width=20)
    last_name_input.grid(row=3, column=3, sticky="W")

    birth_date_label = ttk.Label(add_person_frame, text="Дата народження*")
    birth_date_label.grid(row=4, column=1, sticky="W")
    birth_date = StringVar()
    birth_date_input = ttk.Entry(add_person_frame, textvariable=birth_date, width=20)
    birth_date_input.grid(row=5, column=1, sticky="W")

    birth_date_label = ttk.Label(add_person_frame, text="Дата смерті")
    birth_date_label.grid(row=4, column=2, sticky="W")
    death_date = StringVar()
    death_date_input = ttk.Entry(add_person_frame, textvariable=death_date, width=20)
    death_date_input.grid(row=5, column=2, sticky="W")

    gender = StringVar(value='чоловік')
    male = ttk.Radiobutton(add_person_frame, text="Чоловік", variable=gender, value="чоловік")
    male.grid(row=4, column=3, sticky="W")
    female = ttk.Radiobutton(add_person_frame, text="Жінка", variable=gender, value="жінка")
    female.grid(row=5, column=3, sticky="W")

    submit = ttk.Button(add_person_frame, text="Додати", command=submit_person)
    submit.grid(row=6, column=3, sticky='W', pady=10)

    separator = ttk.Separator(add_person_frame, orient=HORIZONTAL)
    separator.grid(row=7, column=1, sticky='EW', columnspan=3)

    back = ttk.Button(add_person_frame, text="< Назад", command=add_or_find)
    back.grid(row=8, column=1, sticky='W', pady=10)

    save = ttk.Button(add_person_frame, text="Зберегти у файл")
    save.grid(row=8, column=3, sticky='W', pady=10)

    feedback = StringVar()
    feedback_label=ttk.Label(add_person_frame, textvariable=feedback)
    feedback_label.grid(row=6, column=1, sticky='W', pady=10, columnspan=2)

    for item in (name_input,second_name_input, last_name_input):
        item.grid_configure(pady=(2,10))

    for child in add_person_frame.winfo_children():
        child.grid_configure(padx=5)


def search():
    search_frame = ttk.Frame(root, padding="3 5 3 12")
    search_frame.grid(column=0, row=0, sticky="NWES")
    title = ttk.Label(search_frame, text="Пошук", font='TkDefaultFont 16 bold')
    title.grid(row=1, column=1, sticky="W", pady=10, padx=3)

    search_label = ttk.Label(search_frame, text="Введіть ПІБ")
    search_label.grid(row=2, column=1, sticky="W")
    search_key = StringVar()
    search_input = ttk.Entry(search_frame, textvariable=search_key, width=40)
    search_input.grid(row=3, column=1, sticky="W", pady=3)
    search_button = ttk.Button(search_frame, text="Пошук")
    search_button.grid(row=3, column=2, sticky='W', pady=3)
    separator = ttk.Separator(search_frame, orient=HORIZONTAL)
    separator.grid(row=4, column=1, sticky="WE", columnspan=2)

    search_result = StringVar()
    result_label = ttk.Label(search_frame, textvariable=search_result)
    result_label.grid(row=5, column=1, sticky="WE", columnspan=2)

    back = ttk.Button(search_frame, text="< Назад", command=add_or_find)
    back.grid(row=6, column=1, sticky='W', pady=10)

    for child in search_frame.winfo_children():
        child.grid_configure(padx=5)

startframe()
root.mainloop()