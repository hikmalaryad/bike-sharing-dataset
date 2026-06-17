# 🚲 Bike Sharing Data Analysis Dashboard

## 🌐 Dashboard Deployment

Dashboard dapat diakses melalui:

**https://hikmalaryad-bike-sharing-dataset.streamlit.app/**

---

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis pola penggunaan sepeda menggunakan **Bike Sharing Dataset (2011–2012)**.

Analisis dilakukan untuk memahami:

* Pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda
* Pola musiman penggunaan sepeda
* Tren penyewaan dari waktu ke waktu

Hasil analisis divisualisasikan dalam bentuk **dashboard interaktif menggunakan Streamlit**.

---

## 👤 Informasi

* **Nama:** Hikmal Arya Dwitama
* **Email:** [cdcc200d6y1003@student.devacademy.id](mailto:cdcc200d6y1003@student.devacademy.id)
* **ID Dicoding:** CDCC200D6Y1003

---

## 📊 Pertanyaan Bisnis

1. Bagaimana hubungan suhu terhadap jumlah penyewaan sepeda?
2. Bagaimana pengaruh kelembaban terhadap jumlah penyewaan?
3. Bagaimana tren penyewaan dari waktu ke waktu?
4. Bagaimana perbedaan penyewaan pada hari kerja vs libur?
5. Bagaimana perbedaan penyewaan berdasarkan musim?

---

## 🎯 Tujuan Analisis

* Mengidentifikasi pola penggunaan sepeda
* Menganalisis pengaruh cuaca terhadap penyewaan
* Mengetahui musim dengan permintaan tertinggi dan terendah
* Menganalisis tren penyewaan dari waktu ke waktu

---

## 🛠️ Tools & Library

* Python
* Pandas
* Matplotlib
* Seaborn
* Streamlit

---

## 📁 Struktur Direktori

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   └── day.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
├── url.txt
```

---

## 🚀 Panduan Menjalankan Aplikasi

### 1. Clone Repository

```bash
git clone https://github.com/hikmalaryad/bike-sharing-dataset.git
cd bike-sharing-dataset
```

### 2. Setup Virtual Environment

#### (a) Menggunakan Anaconda

```bash
conda create --name bike-ds python=3.9
conda activate bike-ds
pip install -r requirements.txt
```

#### (b) Menggunakan venv

```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Menjalankan Dashboard

```bash
python -m streamlit run dashboard/dashboard.py
```

Aplikasi akan berjalan di:

```text
http://localhost:8501
```

---

## 📌 Insight

* Suhu memiliki hubungan positif terhadap jumlah penyewaan sepeda
* Kelembaban memiliki pengaruh negatif namun relatif lemah
* Penyewaan meningkat pada musim tertentu (Summer & Fall)
* Tidak terdapat perbedaan signifikan antara hari kerja dan hari libur

---

## ✨ Author

Hikmal Arya Dwitama
