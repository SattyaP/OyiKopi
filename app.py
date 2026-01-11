import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import base64
import requests
import time

st.set_page_config(
    page_title="Malang Coffee Finder (OyiKopi)",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Global Style */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #FAFAFA; /* Warna background global */
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 40px 20px 20px 20px;
        background: linear-gradient(135deg, #FFF8F0 0%, #FFFFFF 100%); /* Gradasi background */
        border-radius: 20px;
        margin-bottom: 30px;
        border: 1px solid #F0E6DD;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #4b3621, #A0522D); /* Gradasi Teks */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 20px;
    }

    .cafe-card {
        background: white;
        border-radius: 16px;
        border: 1px solid #eee;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        overflow: hidden;

        display: flex;
        flex-direction: column;
        min-height: 520px;
    }

    .cafe-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
        border-color: #d4a373;
    }

    .cafe-img-container {
        width: 100%;
        height: 180px;
        object-fit: contain !important;
        flex-shrink: 0; /* penting */
    }

    .card-content {
        padding: 20px;

        display: flex;
        flex-direction: column;
        flex: 1; /* WAJIB */
    }

    .cafe-name {
        font-size: 1.25rem;
        font-weight: 700;
        margin: 8px 0 4px 0;
        line-height: 1.4;
        color: #333 !important;
    }

    .cafe-meta {
        font-size: 0.85rem;
        color: #636E72; /* Warna Meta */
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    .match-badge {
        background-color: #E8F5E9; /* Hijau Muda */
        color: #2E7D32; /* Hijau Tua */
        padding: 4px 12px;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 8px;
    }

    .review-box {
        background-color: #FFF8F0;
        border-radius: 8px;
        padding: 12px;
        font-size: 0.85rem;
        color: #5D4037;
        font-style: italic;
        margin-bottom: 16px;
        border: 1px dashed #D7CCC8;
    }

    .highlight {
        background-color: #FFECB3;
        color: #5D4037;
        padding: 0 4px;
        border-radius: 4px;
        font-weight: 600;
    }


    .btn-maps {
        margin-top: auto; 
        display: block;
        width: 100%;
        text-align: center;
        background-color: #2D3436; /* Tombol Gelap */
        color: white !important;
        text-decoration: none;
        padding: 10px 0;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: background 0.2s;
    }
    
    .btn-maps:hover {
        background-color: #000;
    }

    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Styling Suggestion Buttons */
    .stButton button {
        border-radius: 50px !important;
        border: 1px solid #ddd !important;
        background-color: white !important;
        color: #555 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s;
    }
    .stButton button:hover {
        border-color: #4b3621 !important;
        color: #4b3621 !important;
        background-color: #FFF8F0 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def get_image_base64(url):
    placeholder_img = "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=800&q=80"
    
    if not url or pd.isna(url) or "http" not in str(url):
        return placeholder_img

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        time.sleep(0.1) 
        
        response = requests.get(url, headers=headers, timeout=3)
        
        if response.status_code == 200:
            img_b64 = base64.b64encode(response.content).decode()
            return f"data:image/jpeg;base64,{img_b64}"
        else:
            return placeholder_img
    except:
        return placeholder_img
    
@st.cache_resource
def load_data():
    try:
        df = pd.read_csv("dataset_kafe_final.csv")
        df = df.fillna('')
        
        if 'Link Gambar' not in df.columns:
            placeholders = [
                "https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=800&q=80", 
                "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=800&q=80", 
                "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=800&q=80", 
                "https://images.unsplash.com/photo-1525610553991-2bede1a236e2?auto=format&fit=crop&w=800&q=80", 
                "https://images.unsplash.com/photo-1453614512568-c4024d13c247?auto=format&fit=crop&w=800&q=80"  
            ]
            df['Link Gambar'] = [placeholders[i % len(placeholders)] for i in range(len(df))]

        tfidf = TfidfVectorizer(max_features=5000)
        tfidf_matrix = tfidf.fit_transform(df['tags_model'])
        
        return df, tfidf, tfidf_matrix
    except FileNotFoundError:
        return None, None, None

df, tfidf, tfidf_matrix = load_data()
stemmer = StemmerFactory().create_stemmer()

def clean_query(text):
    return stemmer.stem(re.sub(r"[^a-zA-Z0-9\s]", "", text.lower()))

def get_smart_recommendations(query, top_n=6):
    clean_q = clean_query(query)
    query_vec = tfidf.transform([clean_q])
    
    similarity_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    max_score = similarity_scores.max()
    if max_score > 0.05: 
        final_scores = (similarity_scores / max_score) * 0.99
    else:
        final_scores = similarity_scores

    top_indices = final_scores.argsort()[-top_n:][::-1]
    results = df.iloc[top_indices].copy()
    results['final_score'] = final_scores[top_indices]
    
    return results[results['final_score'] > 0.1]

def highlight_text(full_text, query):
    query_words = query.lower().split()
    clean_text = re.sub(r'Fasilitas:.*?Kata Mereka:', '', full_text, flags=re.IGNORECASE)
    sentences = re.split(r'[.!]', clean_text)
    
    matched_sentences = []
    for sentence in sentences:
        if len(sentence) < 15: continue
        if any(q in sentence.lower() for q in query_words if len(q) > 3):
            for q in query_words:
                if len(q) > 3:
                    pattern = re.compile(re.escape(q), re.IGNORECASE)
                    sentence = pattern.sub(f'<span class="highlight">{q}</span>', sentence)
            matched_sentences.append(sentence.strip())
            if len(matched_sentences) >= 1: break 
            
    if matched_sentences:
        return f'"{matched_sentences[0]}..."'
    else:
        return f'"{clean_text[:160]}..."'

def set_query(query_text):
    st.session_state.search_query = query_text

st.markdown("""
<div class="hero-container">
    <div style="display:flex;justify-content:center;margin-bottom:12px;">
        <div style="width:88px;height:88px;background:linear-gradient(135deg,#6b4f3a,#d29b5a);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(0,0,0,0.12);">
            <span style="font-size:42px;line-height:1;">☕</span>
        </div>
    </div>
    <div class="main-title">Malang Coffee Finder (OyiKopi)</div>
    <div class="subtitle">Temukan vibe ngopi terbaikmu dalam hitungan detik.</div>
</div>
""", unsafe_allow_html=True)

col_space_1, col_center, col_space_2 = st.columns([1, 2, 1])

with col_center:
    user_query = st.text_input(
        "Search", 
        value=st.session_state.search_query,
        label_visibility="collapsed", 
        placeholder="Ketik suasana... (contoh: sepi buat skripsi)"
    )
    
    if st.button("🔍 Cari Sekarang", use_container_width=True, type="primary"):
        pass 

    st.write("") 

    st.caption("✨ Atau coba kata kunci populer:")
    s1, s2, s3 = st.columns(3)
    
    with s1:
        if st.button("💻 WFC & Nugas", use_container_width=True):
            set_query("cafe tenang sepi wifi kencang colokan banyak buat nugas")
            st.rerun()
            
    with s2:
        if st.button("📸 Aesthetic & Hits", use_container_width=True):
            set_query("cafe aesthetic instagramable bagus buat foto view bagus")
            st.rerun()
            
    with s3:
        if st.button("☕ Santai & Murah", use_container_width=True):
            set_query("tempat nongkrong santai kopi murah enak nyaman")
            st.rerun()

st.divider()

final_query = user_query if user_query else st.session_state.search_query

if final_query:
    if not final_query.strip():
        st.warning("⚠️ Ketik sesuatu dulu dong...")
    else:
        results = get_smart_recommendations(final_query)
        
        if results.empty:
            st.error(f"❌ Tidak menemukan kafe yang cocok untuk '{final_query}'. Coba kata lain ya!")
        else:
            st.markdown(f"<h5>🎉 Menemukan {len(results)} kafe untukmu:</h5><br>", unsafe_allow_html=True)
            
            cols = st.columns(3)
            
            for idx, (index, row) in enumerate(results.iterrows()):
                col_idx = idx % 3
                
                with cols[col_idx]:
                    score_pct = int(row['final_score'] * 100)
                    snippet = highlight_text(row['tags_readable'], final_query)
                    maps_url = row['Link Maps'] if row['Link Maps'] else "#"
                    final_img_src = get_image_base64(row['Link Gambar'])
                    
                    alamat = row['Alamat'] if row['Alamat'] else "Alamat tidak tersedia, silahkan click tombol Maps."
                    
                    st.markdown(f"""
                    <div class="cafe-card">
                        <img src="{final_img_src}" class="cafe-img-container">
                        <div class="card-content">
                            <div>
                                <span class="match-badge">⚡ {score_pct}% Match</span>
                                <h3 class="cafe-name">{row['Nama Kafe']}</h3>
                                <div class="cafe-meta">
                                    <span>📍</span> <span>{alamat}</span>
                                </div>
                                <div class="cafe-meta">
                                    <span>⭐</span> {row['Rating']} / 5.0 di Google
                                </div>
                                <div class="review-box">{snippet}</div>
                            </div>
                            <a href="{maps_url}" target="_blank" class="btn-maps">
                                🗺️ Buka di Google Maps
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("") 
                    st.write("") 
else:
    st.markdown("""
    <div style="text-align: center; color: #aaa; margin-top: 50px;">
        <h3>👈 Mulai cari dengan mengetik di atas<br>atau pilih tombol saran cepat.</h3>
    </div>
    """, unsafe_allow_html=True)