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
        # self.bar.setValue(100)

        self.timer = QTimer()
        self.timer.timeout.connect(self.clean_with_loop)
        self.timer.start(100)

        # import file yang berisi kata-kata tidak penting
        data_stopword = json.load(open('stopwords-id.json','r'))
        # menjadikan array stopword menjadi unordered collection (set())
        # agar dapat dilakukan operasi matematis seperti union, intersection, symmetric difference
        self.stopword = set(data_stopword)
        self.punctuation = set(string.punctuation)


        sms_csv = pd.read_csv('dataset_sms.csv')
        # print(sms_csv.head())

        # mengambil hanya kolom Teks sms dan disimpan di variabel sms (yang siap dibersihkan)
        self.sms = []
        for index, row in sms_csv.iterrows():
            self.sms.append(row["Teks"])
        # print("Jumlah sms: ", len(self.sms))

        # mengambil hanya kolom label dalam variabel y_train
        y_train = []
        for index, row in sms_csv.iterrows():
            y_train.append(row["label"])
        # print("Jumlah label: ", len(y_train))

        # membersihkan dokumen sms
        sms_bersih = self.clean_with_loop(self.sms)    

        # pembentukan vektor tf-idf untuk pembobotan kata
        vectorizer = TfidfVectorizer(stop_words=data_stopword)
        x_train = vectorizer.fit_transform(self.sms_bersih)
        print(x_train)

        # method untuk cleaning dokumen
    def clean(self, doc):
        # menghilangkan kata tidak penting
        self.stop_free = " ".join([i for i in doc.lower().split() if i not in self.stopword])
        # menghilangkan tanda baca
        self.punc_free = ''.join(ch for ch in self.stop_free if ch not in self.punctuation)
        # menjadikan ke kata dasar
        self.stemmer = StemmerFactory().create_stemmer()
        self.normalized = self.stemmer.stem(self.punc_free)
        # menghilangkan angka
        self.processed = re.sub(r"\d+","",self.normalized)
        # membuat satu dokumen menjadi array berisi tiap kata
        y = self.processed.split()
        return y

    def pindah(self):
        self.switch_window.emit(self.line_edit.text())

    def clean_with_loop(self, sms):
        hasil = []
        value = self.bar.setValue(len(sms))
        # progress = tqdm(sms)
        # masalah pada di item dan value, yang seharusnya
        # value diganti dengan progress
        for item in value:
            cleaned = self.clean(item)
            cleaned = ' '.join(cleaned)
            hasil.append(cleaned)
        return hasil
        
        if value < 100:
            print(1)
            value = value + 1
            self.bar.setValue(value)
        else:
            self.timer.stop()





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

    def show_progress(self):
        self.baca = BacaData()
        self.baca.switch_window.connect(self.show_main)
        self.baca.show()

    def show_main(self):
        self.window = MainWindow()
        self.window.switch_window.connect(self.show_window_two)
        self.baca.close()
        self.window.show()

    def show_window_two(self, text):
        self.window_two = WindowTwo(text)
        self.window.close()
        self.window_two.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_progress()
    sys.exit(app.exec_())




if __name__ == '__main__':
    main()