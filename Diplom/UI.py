from tkinter import *
from tkinter import ttk, filedialog, messagebox
from person import *
from filetool import export_file, import_file
import sqlite3

root = Tk()
root.title("Person data")
root.geometry("800x300")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(2, weight=1)
root.columnconfigure(2, weight=1)

frame = ttk.Frame(root, padding="3 20 3 12")
frame.grid(column=1, row=1, sticky="NWES")

connection = sqlite3.connect("persons.db")
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS persons 
            (full_name TEXT, gender TEXT, birth_date TEXT, death_date TEXT)''')
connection.commit()
connection.close()


def clear_widgets():
    for widget in frame.winfo_children():
        widget.destroy()


def start():
    def load_file():
        file_path = filedialog.askopenfilename(defaultextension='csv', filetypes=[('CSV', '*.csv')])
        msg = import_file(file_path)
        if msg:
            messagebox.showinfo(message=msg)
            add_or_find()

    clear_widgets()
    start_button = ttk.Button(frame, text="Почати роботу", command=add_or_find, width=35)
    start_button.grid(row=1, column=2, sticky='WE', pady=5)
    ttk.Button(frame, text="Завантажити файл", command=load_file).grid(row=2, column=2, sticky='WE', pady=5)
    exit_button = ttk.Button(frame, text="Вийти", command=root.destroy)
    exit_button.grid(row=3, column=2, sticky='NS', pady=(15, 5))
    for child in frame.winfo_children():
        child.grid_configure(padx=5)


def add_or_find():
    clear_widgets()
    ttk.Button(frame, text="Додати персону", command=add_person, width=35).grid(row=1, column=1, sticky="WE", pady=5)
    ttk.Button(frame, text="Пошук", command=search).grid(row=2, column=1, sticky="WE", pady=5)
    ttk.Button(frame, text="< Назад", command=start).grid(row=3, column=1, pady=(15, 5))

    for child in frame.winfo_children():
        child.grid_configure(padx=5)


def add_person():

    def validate_inputs():
        if name.get() == '' or birth_date.get() == '':
            return 'Заповніть обовʼязкові поля'
        try:
            birth = Person.parse_date(birth_date.get())
            if birth > datetime.date.today():
                return 'Дата народження не може бути в майбутньому'
        except Exception as err:
            return 'Неправильна дата народженя: {}'.format(err)
        if death_date.get() != '':
            try:
                death = Person.parse_date(death_date.get())
                if death > datetime.date.today():
                    return 'Дата смерті не може бути в майбутньому'
                if death < birth:
                    return 'Дата смерті не може буди пізніше народження'
            except Exception:
                return "Неправильна дата смерті"
        return f'Персону {name.get()} додано'

    def get_full_name(last_name, first_name, second_name):
        full_name = ''
        for item in (last_name, first_name, second_name):
            if item is not None:
                full_name += f' {item}'
        return full_name.strip()

    def submit_person(event=None):
        validation_result = validate_inputs()
        feedback.set(validation_result)
        if 'додано' in validation_result:
            birth = Person.parse_date(birth_date.get())
            death = Person.parse_date(death_date.get()) if death_date.get() != '' else None
            first_name = name.get()
            sec_name = second_name.get() if second_name.get() != '' else None
            gend = gender.get()
            lst_name = last_name.get() if last_name.get() != '' else None
            full_name = get_full_name(lst_name, first_name, sec_name)
            for variable in (name, second_name, last_name, birth_date, death_date):
                variable.set('')
            name_input.focus()
            return Person(full_name, gend, birth, death)

    clear_widgets()
    title = ttk.Label(frame, text="Додати персону", font='TkDefaultFont 16 bold')
    title.grid(row=1, column=1, sticky="W", pady=10, padx=3)

    name_label = ttk.Label(frame, text="Імʼя*")
    name_label.grid(row=2, column=1, sticky="W")
    name = StringVar()
    name_input = ttk.Entry(frame, textvariable=name, width=25)
    name_input.grid(row=3, column=1, sticky="W")
    name_input.focus()

    second_name_label = ttk.Label(frame, text="По батькові")
    second_name_label.grid(row=2, column=2, sticky="W")
    second_name = StringVar()
    second_name_input = ttk.Entry(frame, textvariable=second_name, width=25)
    second_name_input.grid(row=3, column=2, sticky="W")

    last_name_label = ttk.Label(frame, text="Прізвище")
    last_name_label.grid(row=2, column=3, sticky="W")
    last_name = StringVar()
    last_name_input = ttk.Entry(frame, textvariable=last_name, width=25)
    last_name_input.grid(row=3, column=3, sticky="W")

    birth_date_label = ttk.Label(frame, text="Дата народження*")
    birth_date_label.grid(row=4, column=1, sticky="W")
    birth_date = StringVar()
    birth_date_input = ttk.Entry(frame, textvariable=birth_date, width=25)
    birth_date_input.grid(row=5, column=1, sticky="W")

    birth_date_label = ttk.Label(frame, text="Дата смерті")
    birth_date_label.grid(row=4, column=2, sticky="W")
    death_date = StringVar()
    death_date_input = ttk.Entry(frame, textvariable=death_date, width=25)
    death_date_input.grid(row=5, column=2, sticky="W")

    gender = StringVar(value='чоловік')
    male = ttk.Radiobutton(frame, text="Чоловік", variable=gender, value="чоловік")
    male.grid(row=4, column=3, sticky="W")
    female = ttk.Radiobutton(frame, text="Жінка", variable=gender, value="жінка")
    female.grid(row=5, column=3, sticky="W")

    submit = ttk.Button(frame, text="Додати", command=submit_person, width=25)
    submit.grid(row=6, column=3, sticky='E', pady=10)
    root.bind("<Return>", submit_person)

    separator = ttk.Separator(frame, orient=HORIZONTAL)
    separator.grid(row=7, column=1, sticky='EW', columnspan=3)

    back = ttk.Button(frame, text="< Назад", command=add_or_find)
    back.grid(row=8, column=1, sticky='WS', pady=10)

    feedback = StringVar()
    feedback_label = ttk.Label(frame, textvariable=feedback)
    feedback_label.grid(row=6, column=1, sticky='W', pady=10, columnspan=2)

    for item in (name_input, second_name_input, last_name_input):
        item.grid_configure(pady=(2, 10))

    for child in frame.winfo_children():
        child.grid_configure(padx=5)


def search():

    def search_result(event=None):
        keyword = search_key.get()
        result = Person.print_search_result(keyword)
        result_list = []
        for item in result:
            result_list.append(item)
        search_output.set(result_list)

    def save_file():
        keyword = search_key.get()
        file_path = filedialog.asksaveasfilename(defaultextension='csv', filetypes=[('CSV', '*.csv')])
        msg = export_file(file_path, keyword)
        if msg:
            messagebox.showinfo(message=msg)

    clear_widgets()
    title = ttk.Label(frame, text="Пошук", font='TkDefaultFont 16 bold')
    title.grid(row=1, column=1, sticky="W", pady=10, padx=3)

    search_label = ttk.Label(frame, text="Введіть ПІБ")
    search_label.grid(row=2, column=1, sticky="W")
    search_key = StringVar()
    search_input = ttk.Entry(frame, textvariable=search_key, width=60)
    search_input.grid(row=3, column=1, sticky="W", pady=3)
    search_input.focus()
    search_button = ttk.Button(frame, text="Пошук", command=search_result)
    search_button.grid(row=3, column=2, sticky='WE', pady=3)
    root.bind('<Return>', search_result)

    result_area = Frame(frame, width=400, height=125)
    result_area.grid(row=5, column=1, sticky='WE', columnspan=2)
    result_area.grid_propagate(True)

    search_output = StringVar(value=[])
    listbox = Listbox(result_area, listvariable=search_output, height=6, width=77)
    listbox.grid(column=1, row=1, sticky="NWES")
    scroll = ttk.Scrollbar(result_area, orient=VERTICAL, command=listbox.yview)
    scroll.grid(column=2, row=1, sticky="NES")
    listbox['yscrollcommand'] = scroll.set

    back_button_area = Frame(frame)
    back_button_area.grid(row=6, column=1, sticky='WE')
    back = ttk.Button(back_button_area, text="< Назад", command=add_or_find)
    back.grid(row=1, column=1, sticky='W', pady=10)

    save_button_area = Frame(frame)
    save_button_area.grid(row=6, column=2, sticky='WE')
    save = ttk.Button(save_button_area, text="Зберегти у файл", command=save_file)
    save.grid(row=1, column=1, sticky='E', pady=10)

    for child in frame.winfo_children():
        child.grid_configure(padx=5)


if __name__ == "__main__":
    start()
    root.mainloop()
