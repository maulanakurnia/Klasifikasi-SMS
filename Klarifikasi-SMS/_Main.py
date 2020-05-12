import string
import re
import json
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

########### ISI ################

# import file yang berisi kata-kata tidak penting
data_stopword = json.load(open('stopwords-id.json','r'))

# menjadikan array stopword menjadi unordered collection (set())
# agar dapat dilakukan operasi matematis seperti union, intersection, symmetric difference
stopword = set(data_stopword)
punctuation = set(string.punctuation)

# method untuk cleaning dokumen
def clean(doc):
    # menghilangkan kata tidak penting
    stop_free = " ".join([i for i in doc.lower().split() if i not in stopword])
    # menghilangkan tanda baca
    punc_free = ''.join(ch for ch in stop_free if ch not in punctuation)
    # menjadikan ke kata dasar
    stemmer = StemmerFactory().create_stemmer()
    normalized = stemmer.stem(punc_free)
    # menghilangkan angka
    processed = re.sub(r"\d+","",normalized)
    # membuat satu dokumen menjadi array berisi tiap kata
    y = processed.split()
    return y

# method untuk cleaning dokumen berupa array
def clean_with_loop(arr):
    hasil = []
    progress = tqdm(arr)
    for item in progress:
        progress.set_description("Membersihkan dokumen")
        cleaned = clean(item)
        cleaned = ' '.join(cleaned)
        hasil.append(cleaned)
    return hasil

##### CSV ######
# import dataset sms
sms_csv = pd.read_csv('dataset_sms.csv')
print(sms_csv.head())

# mengambil hanya kolom Teks sms dan disimpan di variabel sms (yang siap dibersihkan)
sms = []
for index, row in sms_csv.iterrows():
    sms.append(row["Teks"])
print("Jumlah sms: ", len(sms))

# mengambil hanya kolom label dalam variabel y_train
y_train = []
for index, row in sms_csv.iterrows():
    y_train.append(row["label"])
print("Jumlah label: ", len(y_train))

# membersihkan dokumen sms
sms_bersih = clean_with_loop(sms)

# pembentukan vektor tf-idf untuk pembobotan kata
vectorizer = TfidfVectorizer(stop_words=data_stopword)
x_train = vectorizer.fit_transform(sms_bersih)
print(x_train)

# pengelompokan dokumen dengan knn (k=5)
# penghitungan jarak dengan euclidean distance
# dokumentasi: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html#sklearn.neighbors.KNeighborsClassifier
modelknn = KNeighborsClassifier(n_neighbors=5, weights='distance')
modelknn.fit(x_train,y_train)

kalimat_tes = ["INFO RESMI PT-SHOPEE 2018 Selamat No.Anda meraih hadiah ke-2 Rp.175jt dgn kode PIN b8337h9",
               "Besok tahun baruan dimana bro?",
               "Cari tiket pesawat paling gampang dan hemat, ya pakai Airy App. Tinggal tekan, langsung sampai! Ada kode Mudah50 spesial buat kamu"]

# membersihkan dokumen pengujian
kalimat_tes_bersih = clean_with_loop(kalimat_tes)

# definisikan nama label
nama_label = ["normal", "penipuan", "penawaran"]

# loop untuk prediksi kelompok
for teks in kalimat_tes_bersih:
    arr_teks = []
    arr_teks.append(teks)
    vektor = vectorizer.transform(arr_teks)
    prediksi_label_knn = modelknn.predict(vektor)
    print(teks, ":\n" + "- kelompok: " + nama_label[np.int(prediksi_label_knn)]+ "\n")