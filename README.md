# ☕ Sistem Rekomendasi Warung Kopi di Malang

Proyek ini merupakan **sistem rekomendasi berbasis Machine Learning (Content-Based Filtering)** yang dirancang untuk membantu **mahasiswa, pekerja remote, dan penikmat kopi** di Kota Malang menemukan warung kopi yang paling sesuai dengan **kebutuhan dan preferensi spesifik** mereka.

Berbeda dari sistem rekomendasi konvensional yang hanya mengandalkan **rating bintang**, sistem ini memahami **“vibe” atau suasana tempat** melalui **Natural Language Processing (NLP)** pada ulasan asli pengunjung Google Maps.

---

## 🚀 Fitur Utama

### 🔍 Smart Search (NLP-Based)
Pencarian menggunakan **kalimat alami seperti manusia**.

Contoh:
- `Tempat sepi buat skripsi wifi kencang`
- `Cafe aesthetic buat foto instagram`

### 🧠 Analisis Vibe Berbasis Review
- Menggunakan **TF-IDF Vectorizer** dan **Cosine Similarity**
- Mencocokkan preferensi pengguna dengan **ribuan ulasan asli**

### ⚡ Quick Chips
Tombol cepat untuk kategori populer:
- 💻 Nugas / WFC
- 📸 Aesthetic
- ☕ Nongkrong Santai

### 📍 Informasi Lengkap
Setiap rekomendasi menampilkan:
- Nama Kafe
- Alamat
- Rating Google
- Cuplikan Review Relevan
- Link Google Maps

### 🎨 UI Modern & Responsif
- Dibangun dengan **Streamlit**
- Layout berbasis **Grid Card**
- Tampilan konsisten di desktop dan mobile

---

## 🛠️ Teknologi yang Digunakan

| Kategori | Teknologi |
|--------|----------|
| Bahasa Pemrograman | Python 3.10+ |
| Web Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-Learn (TF-IDF, Cosine Similarity) |
| NLP Bahasa Indonesia | Sastrawi (Stemming) |
| Data Source | Google Maps Reviews (Scraped Data) |
| Web Scraping | Puppeteer (Node.js) |

---

## 📂 Struktur Proyek

```text
📁 OyiKopi/
├── 📁 data_mentah/
│   └── 📄 List_Kafe_Malang_Lengkap.xlsx   # Data hasil scraping Google Maps
├── 📄 app.py                             # Aplikasi utama (UI & Logic)
├── 📄 dataset_kafe_final.csv             # Dataset hasil preprocessing
├── 📄 preprocessing.py                   # Script preprocessing data (opsional)
├── 📄 scraper.js                         # Puppeteer Google Maps Scraper
├── 📄 requirements.txt                   # Dependency Python
├── 📄 package.json                       # Dependency Node.js (Scraper)
└── 📄 README.md                          # Dokumentasi proyek
```

## 💻 Cara Menjalankan Program

### 1️⃣ Persiapan Lingkungan

Pastikan **Python 3.10+** dan **Node.js** sudah terinstall di sistem Anda.  
Sangat disarankan menggunakan **Virtual Environment** untuk menjaga isolasi dependensi.

```bash
# Masuk ke direktori proyek
cd OyiKopi
2️⃣ Install Dependency
Python

Install seluruh library Python yang dibutuhkan:

pip install -r requirements.txt

Node.js (Scraper)

Install dependency untuk Puppeteer scraper:

npm install

3️⃣ Jalankan Aplikasi

Jalankan aplikasi Streamlit dengan perintah berikut:

streamlit run app.py


Aplikasi akan terbuka otomatis di browser pada alamat:

http://localhost:8501
```

## 🧠 Cara Kerja Model Rekomendasi

### 1. Input
Pengguna memasukkan **kalimat preferensi bebas (free text)**.

**Contoh:**
- `tempat sepi buat skripsi`
- `cafe aesthetic buat foto`

---

### 2. Preprocessing
Tahapan pembersihan teks meliputi:
- Case folding (mengubah teks menjadi huruf kecil)
- Menghapus simbol dan tanda baca
- Stemming Bahasa Indonesia menggunakan **Sastrawi**

---

### 3. Vectorization
Teks yang telah diproses diubah menjadi vektor numerik menggunakan:
- **TF-IDF (Term Frequency – Inverse Document Frequency)**

---

### 4. Similarity Measurement
Menghitung tingkat kemiripan antara:
- Query pengguna
- Data ulasan kafe  

Menggunakan metode **Cosine Similarity**.

---

### 5. Ranking
Kafe diurutkan berdasarkan:
- Skor kemiripan tertinggi  

Hasil terbaik ditampilkan sebagai **rekomendasi utama**.

---

## 👨‍💻 Tim Pengembang

**Tim OYIKOPI**  
Universitas Bhinus Malang

