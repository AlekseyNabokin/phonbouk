import tkinter as tk
from tkinter import ttk
import sqlite3

# Класс Main
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

# Главное окно
    def init_main(self):
        toolbar = tk.Frame(bg='beige', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_add_dialog = tk.Button(toolbar, text='Добавить контакт', command=self.add_dialog, bg='beige',
                                    bd=0, compound=tk.TOP)
        btn_add_dialog.pack(side=tk.LEFT)

        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='beige', bd=0,
                                    compound=tk.TOP, command=self.edit_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        btn_delete_dialog = tk.Button(toolbar, text='Удалить контакт', bg='beige', bd=0,
                                      compound=tk.TOP, command=self.delete_records)
        btn_delete_dialog.pack(side=tk.LEFT)

        btn_search = tk.Button(toolbar, text='Поиск', bg='beige', bd=0,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        btn_refresh = tk.Button(toolbar, text='Обновить', bg='beige', bd=0,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'fio', 'category', 'phone', 'birthday'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('fio', width=165, anchor=tk.CENTER)
        self.tree.column('category', width=150, anchor=tk.CENTER)
        self.tree.column('phone', width=100, anchor=tk.CENTER)
        self.tree.column('birthday', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('fio', text='ФИО')
        self.tree.heading('category', text='Категория')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('birthday', text='Дата рождения')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

# Добавление данных
    def records(self, fio, category, phone, birthday):
        self.db.insert_data(fio, category, phone, birthday)
        self.view_records()

# Обновление данных
    def update_record(self, fio, category, phone, birthday):
        self.db.c.execute('''UPDATE phonebook SET fio=?, category=?, phone=?, birthday=? WHERE ID=?''',
                          (fio, category, phone, birthday, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

# Вывод данных
    def view_records(self):
        self.db.c.execute('''SELECT * FROM phonebook''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

# Удаление данных
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM phonebook WHERE id=? ''', (self.tree.set(selection_item, '#1'),))
            self.db.conn.commit()
            self.view_records()

# Поиск данных
    def search_records(self, fio):
        fio = ('%' + fio + '%',)
        self.db.c.execute('''SELECT * FROM phonebook WHERE fio LIKE ?''', fio)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

# Открытие дочернего окна
    def add_dialog(self):
        Child()

    def edit_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()

# Дочернее окно
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить контакт')
        self.geometry('400x300+400+300')
        self.resizable(False, False)

        label_fio = tk.Label(self, text='ФИО')
        label_fio.place(x=50, y=50)

        label_select = tk.Label(self, text='Категория')
        label_select.place(x=50, y=80)

        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=50, y=110)

        label_birthday = tk.Label(self, text='Дата рождения:')
        label_birthday.place(x=50, y=150)

        self.entry_fio = ttk.Entry(self)
        self.entry_fio.place(x=200, y=50)

        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u' ', 'Семья', 'Друзья', 'Работа'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        self.entry_birthday = ttk.Entry(self)
        self.entry_birthday.place(x=200, y=150)

        def popup():
            self.title("Информация")
            label = tk.Label(self, text="Контакт добавлен")
            label.pack(padx=20, pady=20)

        self.btn_ok = ttk.Button(self, text='Добавить', command=popup)
        self.btn_ok.place(x=220, y=200)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_fio.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_phone.get(),
                                                                       self.entry_birthday.get()
                                                                       ))
        
        self.grab_set()
        self.focus_set()

# Класс обновления унаследованный от дочернего окна
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать контакт')
        def popup():
            self.title("Информация об редактировании")
            label = tk.Label(self, text="Контакт отредактирован")
            label.pack(padx=20, pady=20)
        btn_edit = ttk.Button(self, text='Редактировать', command=popup)
        btn_edit.place(x=205, y=205)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_fio.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_phone.get(),
                                                                          self.entry_birthday.get()
                                                                          ))
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM phonebook WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_fio.insert(0, row[1])
        self.combobox.insert(0, row[2])
        self.entry_phone.insert(0, row[3])
        self.entry_birthday.insert(0, row[4])

# Поиск по наименованию
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

# Создание базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('phonebook.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS phonebook (id integer primary key, fio text, 
            category text, phone text, birthday text) ''')
        self.conn.commit()

    def insert_data(self, fio, category, phone, birthday):
        self.c.execute('''INSERT INTO phonebook (fio, category, phone, birthday) VALUES (?, ?, ?, ?) ''',
                       (fio, category, phone, birthday))
        self.conn.commit()

# Основной код для запуска
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Телефонная книга")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()
