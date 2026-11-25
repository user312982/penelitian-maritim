import streamlit as st
from streamlit_folium import st_folium

from lib.data import filter_by_area, filter_by_date, latest_image_date, load_all_detections
from lib.map import build_map

df = load_all_detections()

with st.sidebar:
    st.header("Filter", icon=":material/filter_list:")
    min_date, max_date = df["waktu_citra"].min(), df["waktu_citra"].max()
    date_range = st.date_input(
        "Rentang tanggal citra", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )
    all_areas = sorted(df["area"].unique())
    areas = st.pills("Area", all_areas, selection_mode="multi", default=all_areas)

filtered = df
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filter_by_date(filtered, str(date_range[0]), str(date_range[1]))
if areas:
    filtered = filter_by_area(filtered, areas)

with st.container(horizontal=True, vertical_alignment="bottom"):
    st.title("Monitoring kapal Selat Makassar", icon=":material/sailing:")
    st.badge(f"Citra terbaru {latest_image_date(df)}", icon=":material/satellite_alt:", color="blue")

with st.container(horizontal=True):
    st.metric("Kapal terdeteksi", len(filtered), border=True)
    avg_conf = f"{filtered['confidence'].mean():.0%}" if len(filtered) else "–"
    st.metric("Rata-rata confidence", avg_conf, border=True)
    avg_len = f"{filtered['length_m'].mean():.0f} m" if len(filtered) else "–"
    st.metric("Rata-rata panjang kapal", avg_len, border=True)
    st.metric("Area terpantau", filtered["area"].nunique(), border=True)

mode_label = st.segmented_control(
    "Mode tampilan",
    [":material/crop_free: Bounding box", ":material/blur_on: Heatmap", ":material/hub: Cluster"],
    default=":material/crop_free: Bounding box",
    label_visibility="collapsed",
)
mode = {"Heatmap": "heatmap", "Cluster": "cluster"}.get((mode_label or "").split(": ")[-1], "marker")

st_folium(build_map(filtered, mode=mode), width=None, height=620, returned_objects=[])
