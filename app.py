import streamlit as st
from streamlit_folium import st_folium

from lib.data import filter_by_area, filter_by_date, latest_image_date, load_detections
from lib.map import build_map

st.set_page_config(page_title="Peta Utama - SAR ALKI II", layout="wide")

DATA_PATH = "data/dummy_detections.csv"

if "extra_detections" not in st.session_state:
    st.session_state.extra_detections = []

df = load_detections(DATA_PATH)
if st.session_state.extra_detections:
    import pandas as pd

    df = pd.concat([df, pd.DataFrame(st.session_state.extra_detections)], ignore_index=True)

st.title("Dashboard Monitoring Maritim - ALKI II")
st.caption(f"Citra terbaru: {latest_image_date(df)} · near real-time")

st.sidebar.header("Filter")
min_date, max_date = df["waktu_citra"].min(), df["waktu_citra"].max()
date_range = st.sidebar.date_input(
    "Rentang tanggal citra", value=(min_date, max_date), min_value=min_date, max_value=max_date
)
areas = st.sidebar.multiselect("Area sub-segmen", options=sorted(df["area"].unique()), default=sorted(df["area"].unique()))

mode_label = st.radio("Mode tampilan", ["Marker individual", "Heatmap kepadatan", "Cluster"], horizontal=True)
mode = {"Marker individual": "marker", "Heatmap kepadatan": "heatmap", "Cluster": "cluster"}[mode_label]

filtered = df
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filter_by_date(filtered, str(date_range[0]), str(date_range[1]))
if areas:
    filtered = filter_by_area(filtered, areas)

st.write(f"Menampilkan {len(filtered)} deteksi kapal")
fmap = build_map(filtered, mode=mode)
st_folium(fmap, width=None, height=600)
