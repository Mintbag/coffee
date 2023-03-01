import sqlite3

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets, uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from untitled import Ui_MainWindow
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


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee0.db')
        db.open()
        self.model = QSqlTableModel(self)
        self.model.setTable('coffees')
        self.model.select()
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.run_2)

    def run(self):
        self.secWin = SecondWindow()
        self.secWin.show()
        self.hide()

    def run_2(self):
        self.cell_value = self.tableView.model().index(self.tableView.currentIndex().row(), 0).data()
        with sqlite3.connect('coffee0.db') as db:
            curs = db.cursor()
            try:
                curs.execute('DELETE FROM coffees WHERE ID=?', (self.cell_value,))
            except sqlite3.IntegrityError:
                pass
        self.mainWin = MyWidget()
        self.mainWin.show()
        self.hide()


class SecondWindow(QMainWindow):
    def __init__(self, values=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.show()
        self.pushButton.clicked.connect(self.run)
        self.pushButton_3.clicked.connect(self.run_3)
        if values:
            self.lineEdit.setText(values[0])
            self.lineEdit_2.setText(values[1])
            self.lineEdit_3.setText(values[2])
            self.lineEdit_4.setText(values[3])
            self.lineEdit_5.setText(values[4])
            self.lineEdit_6.setText(values[5])
            self.lineEdit_7.setText(values[6])

    def run(self):
        name = self.lineEdit.text()
        a = self.lineEdit_2.text()
        b = self.lineEdit_3.text()
        c = self.lineEdit_4.text()
        d = self.lineEdit_5.text()
        e = self.lineEdit_6.text()
        f = self.lineEdit_7.text()
        if name != '' and a != '' and b != '' and c != '' and d != '' and e != '' and f != '':
            with sqlite3.connect('coffee0.db') as db:
                curs = db.cursor()
                try:
                    curs.execute(f"INSERT INTO coffees VALUES({name}, '{a}', '{b}', '{c}', '{d}', {e}, '{f}')")
                except sqlite3.IntegrityError:
                    pass
                db.commit()
            self.label_8.setText('')
        else:
            self.label_8.setText('Введите все данные!')
        self.secWin = SecondWindow()
        self.secWin.show()
        self.hide()

    # def run_2(self):
    #     name = self.lineEdit.text()
    #     a = self.lineEdit_2.text()
    #     b = self.lineEdit_3.text()
    #     c = self.lineEdit_4.text()
    #     d = self.lineEdit_5.text()
    #     e = self.lineEdit_6.text()
    #     f = self.lineEdit_7.text()
    #     if name != '' and a != '' and b != '' and c != '' and d != '' and e != '' and f != '':
    #         with sqlite3.connect('coffee0.db') as db:
    #             curs = db.cursor()
    #             try:
    #                 curs.execute(f"UPDATE coffees SET ID={name}, sort={a}, degree_of_roasting={b},"
    #                              f" ground__or__in_grains={c}, taste_description={d},"
    #                              f"value={e}, packing_volume={f}")
    #             except sqlite3.IntegrityError:
    #                 pass
    #             db.commit()
    #         self.label_8.setText('')
    #     else:
    #         self.label_8.setText('Введите все данные!')

    def run_3(self):
        self.mainWin = MyWidget()
        self.mainWin.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    exit(app.exec())
