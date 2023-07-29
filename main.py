import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
import sys
from PyQt6.QtGui import QAction
import sqlite3



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("ADD Student", self)
        add_student_action.triggered.connect(self.insert)
        add_help_action = QAction("Help", self)
        about_action = QAction("About", self)

        file_menu_item.addAction(add_student_action)
        file_menu_item.addAction(add_help_action)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id","Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()
    
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

class InsertDialog(QDialog):
    def __init__(self, ):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        self.course_name = QComboBox()
        courses = ["biology", "math","physics", "astronomy"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.add_student)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name,course,mobile) VALUES (?,?,?)",(name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        age_calculater.load_data()

app = QApplication(sys.argv)
age_calculater = MainWindow()
age_calculater.show()
age_calculater.load_data()
sys.exit(app.exec())