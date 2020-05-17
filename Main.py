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

class KlasifikasiSMS(QMainWindow):
    def __init__(self,a,b,c,d,e):
        super(KlasifikasiSMS,self).__init__()
        self.initUI()
        self.stopword = a
        self.tandaBaca = b
        self.vectorizer = c
        self.x_train = d
        self.y_train = e

    def button_clicked(self):
        clear = lambda: os.system('clear') 
        clear()

        k = self.inputk.text()
        textsms = self.textsms.toPlainText()

        kkn = KNeighborsClassifier(n_neighbors=int(k), weights='distance')
        kkn.fit(self.x_train,self.y_train)

        sms = textsms
        sms = sms.split(",, ")

        nama_label = ["normal", "penipuan", "penawaran"]

        for teks in sms:
            arr_teks = []
            arr_teks.append(teks)
            vektor = self.vectorizer.transform(arr_teks)
            prediksi_label_knn = kkn.predict(vektor)
            QMessageBox.about(self, "Hasil Klasifikasi","\n " + "Kelompok : "+nama_label[np.int(prediksi_label_knn)]+"\t\n\t")

    def initUI(self):
        self.setGeometry(2000, 200, 380, 240)
        self.setWindowTitle("Klasifikasi SMS")

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
        self.b1.setText("Klasifikasi")
        self.b1.setGeometry(130, 175,200,25)
        self.b1.clicked.connect(self.button_clicked)


def window():
    app = QApplication(sys.argv)

    data_stopword = json.load(open('stopwords-id.json','r'))
    stopword = set(data_stopword)
    tandaBaca = set(string.punctuation)

    sms_csv = pd.read_csv('dataset_sms.csv')
    dataset = []
    for index, row in sms_csv.iterrows():
        dataset.append(row["Teks"])

    y_train = []
    for index, row in sms_csv.iterrows():
        y_train.append(row["label"])

    vectorizer = TfidfVectorizer(stop_words=data_stopword)
    x_train = vectorizer.fit_transform(dataset)

    ksms = KlasifikasiSMS(stopword,tandaBaca,vectorizer,x_train,y_train)
    ksms.show()
    sys.exit(app.exec_())

window()
