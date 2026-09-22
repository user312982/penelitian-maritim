import streamlit as st

st.set_page_config(page_title="Tentang - SAR ALKI II", layout="wide")
st.title("Tentang & Metodologi")

st.markdown(
    """
Dashboard ini adalah prototipe bukti konsep (TKT 3) yang mengintegrasikan tiga
tahap riset payung Riset Konektivitas Nusantara untuk segmen ALKI II (Selat
Makassar):

- **TA-1** — pengumpulan dan penyiapan citra satelit Sentinel-1
- **TA-2** — deteksi kapal dengan model YOLOv8 pada citra SAR Sentinel-1
- **TA-4 (dashboard ini)** — menampilkan hasil TA-2 dan layer kepadatan TA-3
  di atas peta interaktif Streamlit + Folium

### Sumber data
- Citra satelit: Copernicus Data Space Ecosystem / ASF Vertex (Sentinel-1 GRD/SLC)
- Basemap peta: OpenStreetMap (default Folium)

### Batasan
Data pada dashboard ini bersifat **near real-time**, bukan real-time/streaming
kontinu. Pembaruan mengikuti ketersediaan citra Sentinel-1 baru, dengan latensi
sekitar 1-24 jam tergantung prioritas area dan revisit 6-12 hari.

### Kontak
Untuk pertanyaan lebih lanjut mengenai riset ini, hubungi tim peneliti melalui
instansi/pembimbing terkait.
"""
)
