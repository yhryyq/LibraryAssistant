import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QAction,QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2
import time
import datetime

qtCreatorFile = "user.ui"
qtReminder = "reminder.ui"
qtLogin = "login.ui"
qtadmin = "admin.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
Ui_reminder, QtBaseClass = uic.loadUiType(qtReminder)
Ui_login, QtBaseClass = uic.loadUiType(qtLogin)
Ui_admin, QtBaseClass = uic.loadUiType(qtadmin)

class loginWindow(QMainWindow ):
    def __init__(self, parent=None):
        super(loginWindow, self).__init__(parent)
        self.ui = Ui_login()
        self.ui.setupUi(self)
        self.ui.btnLogin.clicked.connect(self.btnLoginclicked)

    def executeQuery(self, sql_str):
        # sql_str.lstrip('\\')
        # print(sql_str)
        try:
            conn = psycopg2.connect("dbname='LibrarySystem' user='postgres' host='localhost' password='123456'")
        except:
            print("Unable to connect to the database")
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def btnLoginclicked(self):
        windowChange = 0 # 0 not change, 1 user system, 2 admin system
        id = self.ui.idText.document().toPlainText()
        password = self.ui.passwordText.document().toPlainText()
        if(id != "" and password != ""):
            sql_str = "select id from users where id ='"+ id +"';"
            try:
                results = self.executeQuery(sql_str)
                if(results):
                    sql_str1 = "select id from users where id ='"+ id +"' and password = '"+ password +"';"
                    try:
                        results = self.executeQuery(sql_str1)
                        if(results):
                            if self.ui.radioUser.isChecked() == False and self.ui.radioAdmin.isChecked() == False:
                                self.ui.warningLabel.setText("Choose a system")
                            elif self.ui.radioUser.isChecked() == True:
                                windowChange = 1
                            elif self.ui.radioAdmin.isChecked() == True:
                                windowChange = 2
                        else:
                            self.ui.warningLabel.setText("Password error!")
                    except:
                        print("query failed1")
                else:
                    self.ui.warningLabel.setText("ID error!")
            except:
                print("query failed2")
        else:
            self.ui.warningLabel.setText("Finish ID and password")

        if(windowChange == 1):
            self.close()
            windows = userWindow(self)
            windows.show()

        elif(windowChange == 2):
            self.close()
            windows = adminWindow(self)
            windows.show()
            windows.loadBooks()


class reminderWindow(QMainWindow ):
    def __init__(self, parent=None):
        super(reminderWindow, self).__init__(parent)
        self.ui = Ui_reminder()
        self.ui.setupUi(self)
        self.ui.btnSave.clicked.connect(self.btnSaveclicked)

    def btnSaveclicked(self):
        self.close()

class adminWindow(QMainWindow ):
    def __init__(self, parent=None):
        super(adminWindow, self).__init__(parent)
        self.ui = Ui_admin()
        self.ui.setupUi(self)
        self.ui.btnAdd.clicked.connect(self.btnAddclicked)
        self.ui.btnDelete.clicked.connect(self.btnDeleteclicked)

    def executeQuery(self, sql_str):
        # sql_str.lstrip('\\')
        # print(sql_str)
        try:
            conn = psycopg2.connect("dbname='LibrarySystem' user='postgres' host='localhost' password='123456'")
        except:
            print("Unable to connect to the database")
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def btnAddclicked(self):
        title = self.ui.titleText.document().toPlainText()
        authors = self.ui.authorsText.document().toPlainText()
        isbn = self.ui.isbnText.document().toPlainText()
        available = self.ui.availableText.document().toPlainText()
        subjects = self.ui.subjectsText.document().toPlainText()
        notes = self.ui.notesText.document().toPlainText()
        if(authors != "" and title != "" and isbn != ""):
            sql_str = "INSERT INTO book VALUES('" + isbn +"','"+ title + "','"+ authors +"','"+ subjects +"','"+ notes +"',"+ available +");"
            try:
                results = self.executeQuery(sql_str)
                print(results)
            except:
                print("insert")
        else:
            print(0)
        self.loadBooks()

    def btnDeleteclicked(self):
        if (self.ui.bookTable.currentRow() >= 0):
            isbn = self.ui.bookTable.item(self.ui.bookTable.currentRow(), 0).text()
            sql_str = "delete from book where isbn = '" + isbn + "';"
            try:
                results = self.executeQuery(sql_str)
            except:
                print("delete")
        self.loadBooks()



    def loadBooks(self):
        self.ui.bookTable.clearContents()
        sql_str = "select isbn,title,authors,subjects,available,notes from book order by isbn desc"
        try:
            results = self.executeQuery(sql_str)
            if (results):
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.bookTable.horizontalHeader().setStyleSheet(style)
                self.ui.bookTable.setColumnCount(len(results[0]))
                self.ui.bookTable.setRowCount(len(results))
                self.ui.bookTable.setHorizontalHeaderLabels(
                    ['ISBN', 'Title', 'Authors', 'Subjects', 'Available','Notes'])
                self.ui.bookTable.resizeColumnsToContents()
                self.ui.bookTable.setColumnWidth(0, 110)
                self.ui.bookTable.setColumnWidth(1, 220)
                self.ui.bookTable.setColumnWidth(2, 220)
                self.ui.bookTable.setColumnWidth(3, 120)
                self.ui.bookTable.setColumnWidth(4, 80)
                self.ui.bookTable.setColumnWidth(5, 300)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.bookTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            else:
                self.ui.bookTable.clearContents()
        except:
            print("Query failed")


class userWindow(QMainWindow):
    def __init__(self, parent=None):
        super(userWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.btnAdd.clicked.connect(self.btnAddclicked)
        self.ui.btnSearch.clicked.connect(self.btnSearchclicked)
        self.ui.btnBorrow.clicked.connect(self.btnBorrowclicked)
        self.ui.btnReturn.clicked.connect(self.btnReturnclicked)
        self.ui.btnReminder.clicked.connect(self.btnReminderclicked)
        self.ui.tabWidget.currentChanged.connect(self.tabclicked)

    def executeQuery(self, sql_str):
        # sql_str.lstrip('\\')
        # print(sql_str)
        try:
            conn = psycopg2.connect("dbname='LibrarySystem' user='postgres' host='localhost' password='123456'")
        except:
            print("Unable to connect to the database")
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result


    def btnSearchclicked(self):
        self.ui.bookTable.clearContents()
        searchText = self.ui.searchText.document().toPlainText()
        sql_str = "select isbn,title,authors,subjects,available from book where title like '%"+ searchText +"%' order by isbn desc"
        try:
            results = self.executeQuery(sql_str)
            if (results):
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.bookTable.horizontalHeader().setStyleSheet(style)
                self.ui.bookTable.setColumnCount(len(results[0]))
                self.ui.bookTable.setRowCount(len(results))
                self.ui.bookTable.setHorizontalHeaderLabels(
                    ['ISBN','Title', 'Authors','Subjects','Available'])
                self.ui.bookTable.resizeColumnsToContents()
                self.ui.bookTable.setColumnWidth(0, 110)
                self.ui.bookTable.setColumnWidth(1, 220)
                self.ui.bookTable.setColumnWidth(2, 220)
                self.ui.bookTable.setColumnWidth(3, 120)
                self.ui.bookTable.setColumnWidth(4, 80)
                # self.ui.bookTable.setColumnWidth(5, 100)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.bookTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            else:
                self.ui.bookTable.clearContents()
        except:
            print("Query failed")

    def btnBorrowclicked(self):
        if(self.ui.bookTable.currentRow() >= 0):
            isbn = self.ui.bookTable.item(self.ui.bookTable.currentRow(), 0).text()
            userid = "11651156"
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            limittime = 15
            sql_str = "INSERT INTO borrow(isbn,userid,borrowtime,limittime) VALUES('" + isbn +"','"+ userid + "','"+ str(date) +"',"+ str(limittime) +");"
            available = int(self.ui.bookTable.item(self.ui.bookTable.currentRow(), 4).text())
            if (available > 0):
                try:
                        results = self.executeQuery(sql_str)
                except:
                    print("insert")

                sql_str2 = "update book set available = available - 1 where book.isbn = '" + isbn +"'"
                try:
                    results = self.executeQuery(sql_str2)
                except:
                    print("update")

                self.btnSearchclicked()

    def tabclicked(self):
        if(self.ui.tabWidget.currentIndex() == 1):
            self.ui.returnTable.clearContents()
            userid = "11651156"
            sql_str = "select book.isbn,book.title,borrow.borrowtime,(borrow.limittime - extract(day FROM (now() - borrow.borrowtime)))\
             as Remainingtime from book,borrow where book.isbn = borrow.isbn and borrow.userid = '"+ userid +"' order by isbn desc"
            try:
                results = self.executeQuery(sql_str)
                if (results):
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.returnTable.horizontalHeader().setStyleSheet(style)
                    self.ui.returnTable.setColumnCount(len(results[0]))
                    self.ui.returnTable.setRowCount(len(results))
                    self.ui.returnTable.setHorizontalHeaderLabels(
                        ['ISBN', 'Title', 'BorrowTime', 'Remaining Days'])
                    self.ui.returnTable.resizeColumnsToContents()
                    self.ui.returnTable.setColumnWidth(0, 150)
                    self.ui.returnTable.setColumnWidth(1, 280)
                    self.ui.returnTable.setColumnWidth(2, 150)
                    self.ui.returnTable.setColumnWidth(3, 120)
                    # self.ui.returnTable.setColumnWidth(4, 80)
                    # self.ui.returnTable.setColumnWidth(5, 100)
                    currentRowCount = 0
                    for row in results:
                        for colCount in range(0, len(results[0])):
                            self.ui.returnTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
                else:
                    self.ui.returnTable.clearContents()
            except:
                print("Query failed")

    def btnReturnclicked(self):
        if (self.ui.returnTable.currentRow() >= 0):
            isbn = self.ui.returnTable.item(self.ui.returnTable.currentRow(), 0).text()
            userid = "11651156"
            borrowTime = self.ui.returnTable.item(self.ui.returnTable.currentRow(), 2).text()
            sql_str = "delete from borrow where isbn = '"+ isbn +"' and userid ='"+ userid +"' and borrowtime = '"+ borrowTime +"';"
            try:
                results = self.executeQuery(sql_str)
            except:
                print("delete")

            sql_str2 = "update book set available = available + 1 where book.isbn = '" + isbn + "'"
            try:
                results = self.executeQuery(sql_str2)
            except:
                print("update")

        self.tabclicked()

    def btnReminderclicked(self):
        windows = reminderWindow(self)
        windows.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = loginWindow()
    window.show()
    sys.exit(app.exec_())