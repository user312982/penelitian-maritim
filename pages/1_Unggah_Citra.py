import random
import time

import streamlit as st

st.set_page_config(page_title="Unggah citra - SAR ALKI II", page_icon=":material/upload_file:", layout="wide")
st.title("Unggah & proses citra SAR", icon=":material/upload_file:")

st.badge(
    "Prototipe TKT 3: inferensi model TA-2 disimulasikan",
    icon=":material/science:",
    color="orange",
)

if "extra_detections" not in st.session_state:
    st.session_state.extra_detections = []
if "pending_preview" not in st.session_state:
    st.session_state.pending_preview = None

uploaded = st.file_uploader("Pilih citra SAR", type=["tif", "png", "jpg", "jpeg"])

if uploaded is not None and st.button("Proses citra", icon=":material/play_arrow:", type="primary"):
    with st.status("Memproses citra...", expanded=True) as status:
        st.write("Preprocessing...")
        time.sleep(0.3)
        st.write("Inferensi model (stub)...")
        time.sleep(0.3)
        status.update(label="Selesai", state="complete")

    st.session_state.pending_preview = {
        "id": f"KPL-UP{random.randint(100, 999)}",
        "lat": round(-2.5 + random.uniform(-0.5, 0.5), 4),
        "lon": round(118.0 + random.uniform(-0.5, 0.5), 4),
        "waktu_citra": time.strftime("%Y-%m-%d"),
        "confidence": round(random.uniform(0.6, 0.95), 2),
        "area": "Makassar-Tengah",
    }

if st.session_state.pending_preview:
    with st.container(border=True):
        st.subheader("Preview hasil deteksi", icon=":material/visibility:")
        st.caption("Belum dipublikasikan ke peta utama")
        st.json(st.session_state.pending_preview)

        if st.button("Publikasikan ke peta utama", icon=":material/publish:", type="primary"):
            st.session_state.extra_detections.append(st.session_state.pending_preview)
            st.session_state.pending_preview = None
            st.toast("Hasil deteksi ditambahkan ke halaman peta utama.", icon=":material/check_circle:")
            st.rerun()
