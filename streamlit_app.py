import streamlit as st
import pandas as pd
import joblib

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Phishing Detector AI", page_icon="🛡️")

# 2. Load Model & Fitur
@st.cache_resource
def load_model():
    model = joblib.load('phishing_model.pkl')
    features = joblib.load('model_features.pkl')
    return model, features

model, features = load_model()

# 3. Antarmuka Pengguna (UI)
st.title("🛡️ Phishing Website Detector")
st.markdown("""
Aplikasi ini memprediksi apakah sebuah website berbahaya (Phishing) atau aman berdasarkan parameter teknis URL.
""")

st.subheader("Input Parameter Website")
st.info("Catatan: Gunakan -1 untuk Phishing, 0 untuk Suspicious, dan 1 untuk Legitimate.")

# Membuat form input otomatis berdasarkan nama fitur yang ada di model_features.pkl
input_data = {}
cols = st.columns(3) # Bagi input menjadi 3 kolom agar rapi

for i, feat in enumerate(features):
    with cols[i % 3]:
        val = st.number_input(f"{feat}", min_value=-1, max_value=1, value=1, step=1)
        input_data[feat] = val

# 4. Tombol Prediksi
if st.button("Analisis Website Sekarang", type="primary"):
    # Ubah input menjadi DataFrame
    df_input = pd.DataFrame([input_data])
    
    # Lakukan Prediksi
    prediction = model.predict(df_input)[0]
    probability = model.predict_proba(df_input)[0]

    st.divider()
    
    if prediction == 1:
        st.success(f"### HASIL: WEBSITE AMAN (LEGITIMATE)")
        st.write(f"Tingkat Keyakinan: {probability[1]*100:.2f}%")
    else:
        st.error(f"### HASIL: TERDETEKSI PHISHING!")
        st.write(f"Tingkat Keyakinan: {probability[0]*100:.2f}%")