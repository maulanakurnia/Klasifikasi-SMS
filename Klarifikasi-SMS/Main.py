from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys, os

import string
import re
import json
from collections import Counter


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans

import numpy as np
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from tqdm import tqdm


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

        kalimat_tes = textsms
        kalimat_tes = kalimat_tes.split(", ")



        # membersihkan dokumen pengujian
        kalimat_tes_bersih = self.clean_with_loop(kalimat_tes)

        # definisikan nama label
        nama_label = ["normal", "penipuan", "penawaran"]


        # loop untuk prediksi kelompok
        for teks in kalimat_tes_bersih:
            arr_teks = []
            arr_teks.append(teks)
            vektor = self.vectorizer.transform(arr_teks)
            prediksi_label_knn = modelknn.predict(vektor)
            # self.hasil.setText("kelompok: " + nama_label[np.int(prediksi_label_knn)]+ "\n")
            QMessageBox.about(self, "Hasil Klarifikasi", "Kelompok : "+nama_label[np.int(prediksi_label_knn)]+"\n")
            # print(teks, ":\n" + "- kelompok: " + nama_label[np.int(prediksi_label_knn)]+ "\n")



        # print(textsms)
        # print(shost)

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

    def clean(self, doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in self.stopword])
        punc_free = ''.join(ch for ch in stop_free if ch not in self.punctuation)
        stemmer = StemmerFactory().create_stemmer()
        normalized = stemmer.stem(punc_free)
        processed = re.sub(r"\d+","",normalized)
        y = processed.split()
        return y

    def clean_with_loop(self, arr):
        print("Memuat Data")
        hasil = []
        progress = tqdm(arr)
        for item in progress:
            # progress.set_description("Membersihkan dokumen")
            cleaned = self.clean(item)
            cleaned = ' '.join(cleaned)
            hasil.append(cleaned)
        return hasil


def clean(doc,stopword,punctuation):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stopword])
    punc_free = ''.join(ch for ch in stop_free if ch not in punctuation)
    stemmer = StemmerFactory().create_stemmer()
    normalized = stemmer.stem(punc_free)
    processed = re.sub(r"\d+","",normalized)
    y = processed.split()
    return y

def clean_with_loop(arr,b,c):
    print("Memuat Data")
    hasil = []
    progress = tqdm(arr)
    for item in progress:
        # progress.set_description("Membersihkan dokumen")
        cleaned = clean(item,b,c)
        cleaned = ' '.join(cleaned)
        hasil.append(cleaned)
    return hasil



def window():
    app = QApplication(sys.argv)


    data_stopword = json.load(open('stopwords-id.json','r'))
    stopword = set(data_stopword)
    punctuation = set(string.punctuation)

    # ini object
    # win = MyWindow()

    sms_csv = pd.read_csv('dataset_sms.csv')
    sms = []
    for index, row in sms_csv.iterrows():
        sms.append(row["Teks"])

    y_train = []
    for index, row in sms_csv.iterrows():
        y_train.append(row["label"])

    sms_bersih = clean_with_loop(sms,stopword,punctuation)

    vectorizer = TfidfVectorizer(stop_words=data_stopword)
    x_train = vectorizer.fit_transform(sms_bersih)

    win2 = MyWindow(stopword,punctuation,vectorizer,x_train,y_train)




    

    win2.show()
    sys.exit(app.exec_())


window()
