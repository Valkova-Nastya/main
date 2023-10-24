import tkinter as tk
from tkinter import ttk
import sqlite3

# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.tree = ttk.Treeview(self,
                                 columns=('ID', 'name', 'phone', 'email'),
                                 show='headings', height=17)
        self.irefresh = tk.PhotoImage(file='./img/refresh.png')
        self.isearch = tk.PhotoImage(file='./img/search.png')
        self.idel = tk.PhotoImage(file='./img/delete.png')
        self.iupd = tk.PhotoImage(file='./img/update.png')
        self.iadd = tk.PhotoImage(file='./img/add.png')
        self.db = db
        self.init_main()
        self.view_records()

    # создание и работа с главным окном
    def init_main(self):
        # Панель
        toolbar = tk.Frame(bg='slategray', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        # Кнопка "Добавить"
        # PhotoImage - добавленное изображение
        # image - картинка, которая размещена на кнопке
        btn_add = tk.Button(toolbar,
                            image=self.iadd,
                            bg='slategray', bd=0,
                            command=self.open_add)
        btn_add.pack(side=tk.LEFT)
        # "Редактирование"
        btn_upd = tk.Button(toolbar,
                            image=self.iupd,
                            bg='slategray', bd=0,
                            command=self.open_update)
        btn_upd.pack(side=tk.LEFT)
        # "Удаление"
        btn_del = tk.Button(toolbar,
                            image=self.idel,
                            bg='slategray', bd=0,
                            command=self.del_records)
        btn_del.pack(side=tk.LEFT)
        # "Поиск"
        btn_search = tk.Button(toolbar,
                               image=self.isearch,
                               bg='slategray', bd=0,
                               command=self.open_search)
        btn_search.pack(side=tk.LEFT)
        # "Обновление"
        btn_refresh = tk.Button(toolbar,
                                image=self.irefresh,
                                bg='slategray', bd=0,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)
        # Таблица с данными
        # Настройка столбцов
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='Email')
        self.tree.pack()
        # Создание полосы прокрутки
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод добавления в БД
    def record(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    # Редактирование
    def upd_record(self, name, phone, email):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cursor.execute('''
            UPDATE Users SET name = ?, phone = ?, email = ?
            WHERE id = ?
            ''', (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()

    # Удаление
    def del_records(self):
        for i in self.tree.selection():
            self.db.cursor.execute('DELETE FROM Users WHERE id = ?',
                                   (self.tree.set(i, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Поиск
    def search_records(self, name):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cursor.execute('SELECT * FROM Users WHERE name LIKE ? ', ('%' + name + '%',))
        r = self.db.cursor.fetchall()
        for i in r:
            self.tree.insert('', 'end', values=i)

    # Отрисовка данных
    def view_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cursor.execute('SELECT * FROM Users')
        r = self.db.cursor.fetchall()
        for i in r:
            self.tree.insert('', 'end', values=i)

    # Открытие дочерноего окна добавления
    def open_add(self):
        AddFrame()

    # Открытие дочерноего окна редактирования
    def open_update(self):
        UpdateFrame()

    # Открытие дочерноего окна поиска
    def open_search(self):
        SearchFrame()


# Классы дочерних окон
class AddFrame(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.btn_ok = tk.Button(self, text='Добавить')
        self.entry_email = tk.Entry(self)
        self.entry_phone = tk.Entry(self)
        self.entry_name = tk.Entry(self)
        self.view = app
        self.init_child()

    # Метод создания окна добавления
    def init_child(self):
        self.title('Добавление контакта')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        label_name = tk.Label(self, text='ФИО')
        label_phone = tk.Label(self, text='Телефон')
        label_email = tk.Label(self, text='Email')
        label_name.place(x=60, y=50)
        label_phone.place(x=60, y=80)
        label_email.place(x=60, y=110)
        self.entry_name.place(x=220, y=50)
        self.entry_phone.place(x=220, y=80)
        self.entry_email.place(x=220, y=110)
        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=220, y=160)
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.record(self.entry_name.get(),
                                                                   self.entry_phone.get(),
                                                                   self.entry_email.get()))
        self.btn_ok.place(x=290, y=160)


# Класс редактирования
class UpdateFrame(AddFrame):
    def __init__(self):
        super().__init__()
        self.btn_upd = tk.Button(self, text='Сохранить')
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Редактирование контакта')
        self.btn_ok.destroy()
        self.btn_upd.bind('<Button-1>',
                          lambda ev: self.view.upd_record(self.entry_name.get(),
                                                          self.entry_phone.get(),
                                                          self.entry_email.get()))
        self.btn_upd.bind('<Button-1>',
                          lambda ev: self.destroy(),
                          add='+')
        self.btn_upd.place(x=290, y=160)

    # Метод автозаполнения формы
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cursor.execute('SELECT *  FROM Users WHERE id = ?', (id,))
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])


# Класс поиска
class SearchFrame(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.btn_ok = tk.Button(self, text='Найти')
        self.entry_name = tk.Entry(self)
        self.view = app
        self.init_search()

    def init_search(self):
        self.title('Поиск контакта')
        self.geometry('300x100')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=40, y=20)
        self.entry_name.place(x=140, y=20)
        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=130, y=70)
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>',
                         lambda ev: self.destroy(),
                         add='+')
        self.btn_ok.place(x=220, y=70)


# Класс БД
class Db:
    # Инициализация БД
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         phone TEXT,
                         email TEXT
            )''')

    # Метод добавления данных
    def insert_data(self, name, phone, email):
        self.cursor.execute('''
                INSERT INTO Users (name, phone, email)
                VALUES (?, ?, ?)
        ''', (name, phone, email))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Телефонная книга')
    root.geometry('665x450')
    root.resizable(False, False)
    db = Db()
    app = Main(root)
    app.pack()
    root.mainloop()