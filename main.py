import sqlite3

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets, uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
con = sqlite3.connect("coffee0.db")
curs = con.cursor()
result = curs.execute('CREATE TABLE IF NOT EXISTS coffees(ID INTEGER, '
                      'sort TEXT, '
                      'degree_of_roasting TEXT, '
                      'ground__or__in_grains TEXT, '
                      'taste_description TEXT, '
                      'value INTEGER, '
                      'packing_volume INTEGER)').fetchall()
con.commit()
con.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.show()
        db = QSqlDatabase.addDatabase('QSQLITE')

        # 2. Вызовите setDatabaseName(), чтобы установить имя базы данных, которое будет использоваться.
        #    Вам нужно только написать путь, а имя файла заканчивается на .db
        #   (если база данных уже существует, используйте базу данных; если она не существует,
        #    будет создана новая);
        db.setDatabaseName('coffee0.db')  # !!! ваша db

        # 3. Вызовите метод open(), чтобы открыть базу данных.
        #    Если открытие прошло успешно, оно вернет True, а в случае неудачи - False.
        db.open()

        # Создайте модель QSqlTableModel и вызовите setTable(),
        # чтобы выбрать таблицу данных для обработки.
        self.model = QSqlTableModel(self)
        self.model.setTable('coffees')  # !!! тавлица в db

        # вызовите метод select(), чтобы выбрать все данные в таблице, и соответствующее
        # представление также отобразит все данные;
        self.model.select()
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    exit(app.exec())
