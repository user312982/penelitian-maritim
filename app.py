import streamlit as st

from lib.style import inject_glass_style

st.set_page_config(page_title="Monitoring Maritim ALKI II", page_icon=":material/sailing:", layout="wide")
inject_glass_style()

if "extra_detections" not in st.session_state:
    st.session_state.extra_detections = []
if "pending_preview" not in st.session_state:
    st.session_state.pending_preview = None

st.navigation(
    [
        st.Page("app_pages/peta.py", title="Peta", icon=":material/map:", default=True),
        st.Page("app_pages/detail.py", title="Detail deteksi", icon=":material/table_chart:"),
        st.Page("app_pages/unggah.py", title="Unggah citra", icon=":material/upload_file:"),
    ],
    position="top",
).run()
