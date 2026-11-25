import random
import time

import streamlit as st

st.title("Unggah citra SAR", icon=":material/upload_file:")
st.caption("Unggah citra Sentinel-1, proses deteksi kapal, lalu tampilkan hasilnya di peta.")

uploaded = st.file_uploader("Pilih citra SAR", type=["tif", "png", "jpg", "jpeg"])

if uploaded is not None and st.button("Proses citra", icon=":material/play_arrow:", type="primary"):
    with st.status("Memproses citra...", expanded=True) as status:
        st.write("Preprocessing...")
        time.sleep(0.3)
        st.write("Deteksi kapal...")
        time.sleep(0.3)
        status.update(label="Selesai", state="complete")

    length_m = round(random.uniform(20, 250), 1)
    st.session_state.pending_preview = {
        "id": f"KPL-UP{random.randint(100, 999)}",
        "lat": round(-2.5 + random.uniform(-0.5, 0.5), 4),
        "lon": round(118.0 + random.uniform(-0.5, 0.5), 4),
        "waktu_citra": time.strftime("%Y-%m-%d"),
        "confidence": round(random.uniform(0.6, 0.95), 2),
        "area": "Makassar-Tengah",
        "length_m": length_m,
        "width_m": round(length_m * random.uniform(0.12, 0.18), 1),
    }

if st.session_state.pending_preview:
    with st.container(border=True):
        st.subheader("Preview hasil deteksi", icon=":material/visibility:")
        st.caption("Belum dipublikasikan ke peta utama")
        p = st.session_state.pending_preview
        with st.container(horizontal=True):
            st.metric("ID kapal", p["id"], border=True)
            st.metric("Koordinat", f"{p['lat']}, {p['lon']}", border=True)
            st.metric("Ukuran", f"{p['length_m']:.0f} × {p['width_m']:.0f} m", border=True)
            st.metric("Confidence", f"{p['confidence']:.0%}", border=True)

        if st.button("Publikasikan ke peta utama", icon=":material/publish:", type="primary"):
            st.session_state.extra_detections.append(st.session_state.pending_preview)
            st.session_state.pending_preview = None
            st.toast("Hasil deteksi ditambahkan ke halaman peta utama.", icon=":material/check_circle:")
            st.rerun()
