import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlQuery
from PyQt5.QtWidgets import QApplication, QInputDialog, QDialog, QStatusBar, QTableWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

import addEditCoffeeForm


class Dialog(QDialog, addEditCoffeeForm.Ui_Dialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUI()
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.answer = {}
        for i in range(self.tableWidget.rowCount):
            self.answer[self.tableWidget.item(i, 0).text()] = self.tableWidget.item(i, 1).text()
        self.accept()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.con = sqlite3.connect("coffee.db")
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.change)
        res = self.con.cursor().execute("""SELECT * FROM coffee""").fetchall()
        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "name", "roast", "type", "flavour", "cost", "volume"])
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def add(self):
        dial = Dialog()
        if dial.exec_:
            self.con.cursor().execute("""INSERT INTO coffee VALUES(""" + ", ".join([
                "'" + str(dial.answer[x]) + "'" for x in dial.answer
            ]) + ")")

    def change(self):


    def closeEvent(self, event):
        self.con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())