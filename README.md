☕ Sistem Rekomendasi Warung Kopi di Malang
Proyek ini adalah sistem rekomendasi berbasis Machine Learning (Content-Based Filtering) yang dirancang untuk membantu mahasiswa, pekerja remote, dan penikmat kopi di Kota Malang menemukan tempat yang paling sesuai dengan kebutuhan spesifik mereka.

Sistem ini tidak hanya merekomendasikan berdasarkan rating bintang, tetapi memahami konteks "Vibe" (suasana) melalui pemrosesan bahasa alami (Natural Language Processing) dari ulasan pengunjung.

🚀 Fitur Utama
Smart Search (NLP): Cari tempat dengan kalimat manusiawi.

Contoh: "Tempat sepi buat skripsi wifi kencang" atau "Cafe aesthetic buat foto instagram".

Analisis Sentimen "Vibe": Menggunakan algoritma TF-IDF dan Cosine Similarity untuk mencocokkan query pengguna dengan ribuan ulasan asli.

Quick Chips: Tombol cepat untuk kategori populer (Nugas, Aesthetic, Nongkrong Santai).

Informasi Lengkap: Menampilkan Nama, Alamat, Rating Google, Cuplikan Review Relevan, dan Link Google Maps.

UI Modern: Antarmuka responsif berbasis Grid yang dibangun dengan Streamlit.

🛠️ Teknologi yang Digunakan
Bahasa Pemrograman: Python 3.10+

Web Framework: Streamlit

Data Processing: Pandas, NumPy

Machine Learning: Scikit-Learn (TF-IDF Vectorizer, Cosine Similarity)

Natural Language Processing (NLP): Sastrawi (Stemming Bahasa Indonesia)

Data Source: Google Maps Reviews (Scraped Data)

📂 Struktur Proyek
📁 OyiKopi/
├── 📁 data_mentah
├──── 📄 List_Kafe_Malang_Lengkap.xlsx # Result Scrapper
├── 📄 app.py                   # Main Application (UI & Logic)
├── 📄 dataset_kafe_final.csv   # Dataset hasil cleaning & preprocessing
├── 📄 requirements.txt         # Daftar library dependency
├── 📄 preprocessing.py         # (Opsional) Script pembersih data mentah
└── 📄 README.md                # Dokumentasi Proyek
└── 📄 scraper.js               # Puppeteer Scrapper Map

💻 Cara Menjalankan Program
Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal:

1. Persiapan Lingkungan
Pastikan Python sudah terinstall. Sangat disarankan menggunakan Virtual Environment.

Bash

# Clone atau download folder ini
# Masuk ke direktori
cd OyiKopi
2. Install Library
Install semua dependensi yang dibutuhkan secara otomatis:

Bash

pip install -r requirements.txt
npm install
3. Jalankan Aplikasi
Ketik perintah berikut di terminal:

Bash

streamlit run app.py
Aplikasi akan otomatis terbuka di browser Anda (biasanya di alamat http://localhost:8501).

🧠 Cara Kerja Model
Input: Pengguna memasukkan kalimat preferensi.

Preprocessing: Sistem membersihkan input (menghapus tanda baca, stopword removal, dan melakukan stemming kata dasar bahasa Indonesia).

Vectorization: Mengubah teks input menjadi vektor angka menggunakan bobot TF-IDF yang telah dilatih dengan data ulasan kafe.

Similarity Check: Menghitung jarak kedekatan (Cosine Similarity) antara vektor input pengguna dengan vektor setiap kafe.

Ranking: Menampilkan kafe dengan skor kemiripan tertinggi.

Dibuat oleh: Tim OYIKOPI UBHINUS MALANG