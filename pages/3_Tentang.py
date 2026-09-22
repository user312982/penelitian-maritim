import streamlit as st

st.set_page_config(page_title="Tentang - SAR ALKI II", page_icon=":material/info:", layout="wide")
st.title("Tentang & metodologi", icon=":material/info:")

st.write(
    "Dashboard ini adalah prototipe bukti konsep (TKT 3) yang mengintegrasikan tiga "
    "tahap riset payung Riset Konektivitas Nusantara untuk segmen ALKI II (Selat Makassar)."
)

with st.container(border=True):
    st.subheader("Pipeline riset", icon=":material/route:")
    st.markdown(
        """
- **TA-1** — pengumpulan dan penyiapan citra satelit Sentinel-1
- **TA-2** — deteksi kapal dengan model YOLOv8 pada citra SAR Sentinel-1
- **TA-4 (dashboard ini)** — menampilkan hasil TA-2 dan layer kepadatan TA-3
  di atas peta interaktif Streamlit + Folium
"""
    )

with st.container(horizontal=True):
    with st.container(border=True):
        st.subheader("Sumber data", icon=":material/satellite_alt:")
        st.markdown(
            "- Citra satelit: Copernicus Data Space Ecosystem / ASF Vertex "
            "(Sentinel-1 GRD/SLC)\n- Basemap peta: OpenStreetMap (default Folium)"
        )

    with st.container(border=True):
        st.subheader("Batasan", icon=":material/schedule:")
        st.markdown(
            "Data bersifat **near real-time**, bukan real-time/streaming kontinu. "
            "Pembaruan mengikuti ketersediaan citra Sentinel-1 baru, dengan latensi "
            "sekitar 1-24 jam tergantung prioritas area dan revisit 6-12 hari."
        )

st.caption("Untuk pertanyaan lebih lanjut, hubungi tim peneliti melalui instansi/pembimbing terkait.")
