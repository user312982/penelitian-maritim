import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from lib.data import filter_by_area, filter_by_date, latest_image_date, load_detections
from lib.map import build_map, carto_tiles
from lib.style import inject_glass_style

st.set_page_config(page_title="Peta utama - SAR ALKI II", page_icon=":material/map:", layout="wide")
inject_glass_style()

DATA_PATH = "data/dummy_detections.csv"

if "extra_detections" not in st.session_state:
    st.session_state.extra_detections = []

df = load_detections(DATA_PATH)
if st.session_state.extra_detections:
    df = pd.concat([df, pd.DataFrame(st.session_state.extra_detections)], ignore_index=True)

st.title("Dashboard monitoring maritim - ALKI II", icon=":material/map:")

with st.container(horizontal=True, key="status_bar"):
    st.badge(f"Citra terbaru: {latest_image_date(df)}", icon=":material/satellite_alt:", color="blue")
    st.caption("near real-time, bukan streaming langsung")

with st.sidebar:
    st.header("Filter", icon=":material/filter_list:")
    min_date, max_date = df["waktu_citra"].min(), df["waktu_citra"].max()
    date_range = st.date_input(
        "Rentang tanggal citra", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )
    areas = st.multiselect(
        "Area sub-segmen", options=sorted(df["area"].unique()), default=sorted(df["area"].unique())
    )

mode_label = st.segmented_control(
    "Mode tampilan",
    ["Marker individual", "Heatmap kepadatan", "Cluster"],
    default="Marker individual",
)
mode = {"Marker individual": "marker", "Heatmap kepadatan": "heatmap", "Cluster": "cluster"}.get(
    mode_label, "marker"
)

filtered = df
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filter_by_date(filtered, str(date_range[0]), str(date_range[1]))
if areas:
    filtered = filter_by_area(filtered, areas)

st.caption(f"Menampilkan {len(filtered)} deteksi kapal")
tiles, attr = carto_tiles(st.context.theme.type, st.secrets.get("CARTO_API_KEY"))
fmap = build_map(filtered, mode=mode, tiles=tiles, attr=attr)
st_folium(fmap, width=None, height=600)
