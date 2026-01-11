import pandas as pd
import json
import re
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

print("⏳ Menyiapkan engine NLP...")
factory_stop = StopWordRemoverFactory()
stopword_remover = factory_stop.create_stop_word_remover()
factory_stem = StemmerFactory()
stemmer = factory_stem.create_stemmer()

custom_stopwords = ['yg', 'gak', 'nya', 'kalo', 'sih', 'aja', 'banget', 'bgt', 'dr', 'utk', 'tp', 'ga', 'dan', 'di', 'yang']

def clean_for_machine(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = stopword_remover.remove(text)
    words = text.split()
    words = [w for w in words if w not in custom_stopwords]
    text = " ".join(words)
    text = stemmer.stem(text) 
    return text

def clean_for_human(json_str):
    try:
        data_list = json.loads(json_str)
        top_reviews = [item['Ulasan'] for item in data_list if 'Ulasan' in item][:5]
        return " ... ".join(top_reviews)
    except:
        return ""

def clean_address(text):
    if not isinstance(text, str): return ""
    text = re.split(r'(Buka|Tutup)', text)[0]
    text = re.sub(r'[^\w\s,.]', '', text)
    return text.strip()


nama_file_input = "List_Kafe_Malang_Lengkap.xlsx" 
print(f"📂 Membaca {nama_file_input}...")

try:
    if nama_file_input.endswith('.xlsx'):
        df = pd.read_excel(nama_file_input)
    else:
        df = pd.read_csv(nama_file_input)
except FileNotFoundError:
    print("❌ File tidak ditemukan!")
    exit()

print("-" * 40)
print("🔍 MENGANALISIS DUPLIKAT...")

duplikat = df[df.duplicated(subset=['Nama Kafe', 'Alamat'], keep=False)]

if not duplikat.empty:
    print(f"⚠️ Ditemukan {len(duplikat)} data yang terindikasi ganda (Nama & Alamat sama persis).")
    print("   Contoh yang akan dihapus:")
    print(duplikat[['Nama Kafe', 'Alamat']].head(5)) 
    
    df.drop_duplicates(subset=['Nama Kafe', 'Alamat'], keep='first', inplace=True)
    print("✅ Duplikat identik telah dihapus.")
else:
    print("✅ Tidak ditemukan data duplikat identik (Aman).")
    
print(f"📊 Total Data Akhir: {len(df)} kafe")
print("-" * 40)


print("🚀 Mulai pembersihan teks...")

clean_contents_machine = []
clean_contents_human = []
clean_addresses = []

for index, row in df.iterrows():
    clean_addresses.append(clean_address(row['Alamat']))

    raw_json = row['Ulasan']
    keywords = str(row['Keywords']) if 'Keywords' in df.columns and not pd.isna(row['Keywords']) else ""

    human_text = clean_for_human(raw_json)
    
    if keywords:
        text_display = f"Fasilitas: {keywords}. Kata Mereka: {human_text}"
    else:
        text_display = human_text
        
    clean_contents_human.append(text_display)
    clean_contents_machine.append(clean_for_machine(human_text + " " + keywords))

    if (index + 1) % 10 == 0:
        print(f"   Processed {index + 1}...")

df_final = pd.DataFrame({
    'Nama Kafe': df['Nama Kafe'],
    'Alamat': clean_addresses,
    'Rating': df['Rating'],
    'Link Maps': df['Link Maps'],
    'tags_model': clean_contents_machine,
    'tags_readable': clean_contents_human
})

if 'Link Gambar' in df.columns:
    df_final['Link Gambar'] = df['Link Gambar']

output_file = "dataset_kafe_final.csv"
df_final.to_csv(output_file, index=False)

print("="*40)
print(f"✅ Data bersih tersimpan di: {output_file}")