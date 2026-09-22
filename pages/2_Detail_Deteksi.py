import pandas as pd
import streamlit as st

from lib.data import aggregate_by_period, load_detections

st.set_page_config(page_title="Detail deteksi - SAR ALKI II", page_icon=":material/table_chart:", layout="wide")
st.title("Detail deteksi kapal", icon=":material/table_chart:")

DATA_PATH = "data/dummy_detections.csv"

df = load_detections(DATA_PATH)
if st.session_state.get("extra_detections"):
    df = pd.concat([df, pd.DataFrame(st.session_state.extra_detections)], ignore_index=True)

with st.container(horizontal=True):
    st.metric("Total deteksi", len(df), border=True)
    st.metric("Rata-rata confidence", f"{df['confidence'].mean():.2f}", border=True)
    st.metric("Area terpantau", df["area"].nunique(), border=True)

with st.container(border=True):
    st.subheader("Tabel hasil deteksi", icon=":material/list_alt:")
    st.dataframe(df[["id", "lat", "lon", "confidence", "waktu_citra"]], width="stretch")

with st.container(border=True):
    st.subheader("Jumlah kapal terdeteksi per periode", icon=":material/bar_chart:")
    agg = aggregate_by_period(df)
    st.bar_chart(agg.set_index("waktu_citra")["count"])

st.download_button(
    "Ekspor data (CSV)",
    icon=":material/download:",
    data=df.to_csv(index=False),
    file_name="deteksi_kapal.csv",
    mime="text/csv",
)
