from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys, os

import string
import json
import numpy as np
import pandas as pd


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans

class MyWindow(QMainWindow):
    def __init__(self,a,b,c,d,e):
        super(MyWindow,self).__init__()
        self.initUI()
        self.stopword = a
        self.punctuation = b
        self.vectorizer = c
        self.x_train = d
        self.y_train = e

    def button_clicked(self):
        clear = lambda: os.system('clear') 
        clear()

        k = self.inputk.text()
        textsms = self.textsms.toPlainText()

        modelknn = KNeighborsClassifier(n_neighbors=int(k), weights='distance')
        modelknn.fit(self.x_train,self.y_train)

        sms = textsms
        sms = sms.split(",, ")

        nama_label = ["normal", "penipuan", "penawaran"]

        for teks in sms:
            arr_teks = []
            arr_teks.append(teks)
            vektor = self.vectorizer.transform(arr_teks)
            prediksi_label_knn = modelknn.predict(vektor)
            QMessageBox.about(self, "Hasil Klarifikasi","\n " + "Kelompok : "+nama_label[np.int(prediksi_label_knn)]+"\t\n\t")

    def initUI(self):
        self.setGeometry(2000, 200, 600, 300)
        self.setWindowTitle("Klarifikasi SMS")

        self.lsms = QtWidgets.QLabel(self)
        self.lsms.setText("Masukkan SMS : ")
        self.lsms.move(20,30)

        self.textsms = QtWidgets.QTextEdit(self)
        self.textsms.setGeometry(130, 30,200,100)

        self.lk = QtWidgets.QLabel(self)
        self.lk.setText("Masukkan K : ")
        self.lk.move(20,135)

        self.inputk = QtWidgets.QLineEdit(self)
        self.inputk.setGeometry(130, 135, 200,30)

        self.hasil = QtWidgets.QLabel(self)
        self.hasil.setGeometry(370,20,200,50)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Submit")
        self.b1.setGeometry(130, 175,200,25)
        self.b1.clicked.connect(self.button_clicked)


def window():
    app = QApplication(sys.argv)

    data_stopword = json.load(open('stopwords-id.json','r'))
    stopword = set(data_stopword)
    punctuation = set(string.punctuation)

    sms_csv = pd.read_csv('dataset_sms.csv')
    sms_bersih = []
    for index, row in sms_csv.iterrows():
        sms_bersih.append(row["Teks"])

    y_train = []
    for index, row in sms_csv.iterrows():
        y_train.append(row["label"])

    vectorizer = TfidfVectorizer(stop_words=data_stopword)
    x_train = vectorizer.fit_transform(sms_bersih)

    win2 = MyWindow(stopword,punctuation,vectorizer,x_train,y_train)

    win2.show()
    sys.exit(app.exec_())


window()
