import random
import time

import streamlit as st

st.set_page_config(page_title="Unggah Citra - SAR ALKI II", layout="wide")
st.title("Unggah & Proses Citra SAR")

st.info(
    "Prototipe TKT 3: tahap inferensi model TA-2 disimulasikan (stub). "
    "Saat model TA-2 terintegrasi, bagian ini diganti panggilan model asli."
)

if "extra_detections" not in st.session_state:
    st.session_state.extra_detections = []
if "pending_preview" not in st.session_state:
    st.session_state.pending_preview = None

uploaded = st.file_uploader("Pilih citra SAR", type=["tif", "png", "jpg", "jpeg"])

if uploaded is not None and st.button("Proses citra"):
    progress = st.progress(0, text="Preprocessing...")
    time.sleep(0.3)
    progress.progress(40, text="Inferensi model (stub)...")
    time.sleep(0.3)
    progress.progress(100, text="Selesai")

    st.session_state.pending_preview = {
        "id": f"KPL-UP{random.randint(100, 999)}",
        "lat": round(-2.5 + random.uniform(-0.5, 0.5), 4),
        "lon": round(118.0 + random.uniform(-0.5, 0.5), 4),
        "waktu_citra": time.strftime("%Y-%m-%d"),
        "confidence": round(random.uniform(0.6, 0.95), 2),
        "area": "Makassar-Tengah",
    }

if st.session_state.pending_preview:
    st.subheader("Preview hasil deteksi (sebelum dipublikasikan)")
    st.json(st.session_state.pending_preview)

    if st.button("Publikasikan ke peta utama"):
        st.session_state.extra_detections.append(st.session_state.pending_preview)
        st.session_state.pending_preview = None
        st.success("Hasil deteksi ditambahkan ke Halaman Peta Utama.")
