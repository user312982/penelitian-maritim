import pandas as pd
import streamlit as st

from lib.data import aggregate_by_period, load_detections

st.set_page_config(page_title="Detail Deteksi - SAR ALKI II", layout="wide")
st.title("Detail Deteksi Kapal")

DATA_PATH = "data/dummy_detections.csv"

df = load_detections(DATA_PATH)
if st.session_state.get("extra_detections"):
    df = pd.concat([df, pd.DataFrame(st.session_state.extra_detections)], ignore_index=True)

st.subheader("Tabel hasil deteksi")
st.dataframe(df[["id", "lat", "lon", "confidence", "waktu_citra"]], use_container_width=True)

st.subheader("Jumlah kapal terdeteksi per periode")
agg = aggregate_by_period(df)
st.bar_chart(agg.set_index("waktu_citra")["count"])

st.download_button(
    "Ekspor data (CSV)",
    data=df.to_csv(index=False),
    file_name="deteksi_kapal.csv",
    mime="text/csv",
)
