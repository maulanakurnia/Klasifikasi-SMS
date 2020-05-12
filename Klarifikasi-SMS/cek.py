import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication
from PyQt5.QtCore import QTimer, Qt
import json, string, re
from collections import Counter

# sklearn - machine learning library
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans

# numpy - scientific computing library
import numpy as np

# pandas - python data analysis library
import pandas as pd

# sastrawi - stemming library (bahasa indonesia)
# !pip install Sastrawi
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# tqdm - progress bar library
from tqdm import tqdm

class BacaData(QWidget):

    switch_window = QtCore.pyqtSignal(str)
    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Memuat Data')

        self.bar = QProgressBar(self)
        self.bar.setGeometry(80, 20, 200, 25)
        self.bar.setValue(0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimer)
        self.timer.start(100)

        # import file yang berisi kata-kata tidak penting
        data_stopword = json.load(open('stopwords-id.json','r'))
        # menjadikan array stopword menjadi unordered collection (set())
        # agar dapat dilakukan operasi matematis seperti union, intersection, symmetric difference
        self.stopword = set(data_stopword)
        self.punctuation = set(string.punctuation)

        # method untuk cleaning dokumen
    def clean(self, doc):
        # menghilangkan kata tidak penting
        self.stop_free = " ".join([i for i in doc.lower().split() if i not in self.stopword])
        # menghilangkan tanda baca
        self.punc_free = ''.join(ch for ch in self.stop_free if ch not in self.punctuation)
        # menjadikan ke kata dasar
        self.stemmer = StemmerFactory().create_stemmer()
        self.normalized = self.temmer.stem(self.punc_free)
        # menghilangkan angka
        self.processed = re.sub(r"\d+","",self.normalized)
        # membuat satu dokumen menjadi array berisi tiap kata
        y = self.processed.split()
        return y


    def handleTimer(self, arr):
        self.hasil = []
        self.value = self.bar.value(tqdm(arr))
        for item in self.value:
            self.cleaned = BacaData.clean(self, item)
            self.cleaned = ' '.join(self.cleaned)
            self.hasil.append(self.cleaned)
        return self.hasil
        
        if value < 100:
            value = value + 1
            self.bar.setValue(value)
        else:
            self.timer.stop()



    def pindah(self):
        self.switch_window.emit(self.line_edit.text())

    

class MainWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Main Window')

        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.line_edit)

        self.button = QtWidgets.QPushButton('Switch Window')
        self.button.clicked.connect(self.switch)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def switch(self):
        self.switch_window.emit(self.line_edit.text())


class WindowTwo(QtWidgets.QWidget):

    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Window Two')

        layout = QtWidgets.QGridLayout()

        self.label = QtWidgets.QLabel(text)
        layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton('Close')
        self.button.clicked.connect(self.close)

        layout.addWidget(self.button)

        self.setLayout(layout)


class Login(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Membaca Data')

        layout = QtWidgets.QGridLayout()

        self.button = QtWidgets.QPushButton('Login')
        self.button.clicked.connect(self.login)

        layout.addWidget(self.button)

        self.setLayout(layout)

    def login(self):
        self.switch_window.emit()


class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = BacaData()
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self):
        self.window = MainWindow()
        self.window.switch_window.connect(self.show_window_two)
        self.login.close()
        self.window.show()

    def show_window_two(self, text):
        self.window_two = WindowTwo(text)
        self.window.close()
        self.window_two.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())




if __name__ == '__main__':
    main()