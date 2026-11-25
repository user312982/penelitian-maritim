import streamlit as st

from lib.data import aggregate_by_period, load_all_detections

df = load_all_detections()

with st.container(horizontal=True, vertical_alignment="bottom"):
    st.title("Detail deteksi kapal", icon=":material/table_chart:")
    st.download_button(
        "Ekspor CSV",
        icon=":material/download:",
        data=df.to_csv(index=False),
        file_name="deteksi_kapal.csv",
        mime="text/csv",
    )

with st.container(horizontal=True):
    st.metric("Total deteksi", len(df), border=True)
    st.metric("Rata-rata confidence", f"{df['confidence'].mean():.0%}", border=True)
    st.metric("Rata-rata panjang kapal", f"{df['length_m'].mean():.0f} m", border=True)
    st.metric("Area terpantau", df["area"].nunique(), border=True)

with st.container(horizontal=True):
    with st.container(border=True):
        st.subheader("Deteksi per tanggal citra", icon=":material/bar_chart:")
        agg = aggregate_by_period(df)
        st.bar_chart(agg, x="waktu_citra", y="count", x_label="", y_label="Kapal", height=280)
    with st.container(border=True):
        st.subheader("Deteksi per area", icon=":material/location_on:")
        per_area = df.groupby("area").size().reset_index(name="count")
        st.bar_chart(per_area, x="area", y="count", x_label="", y_label="Kapal", height=280, horizontal=True)

with st.container(border=True):
    st.subheader("Tabel hasil deteksi", icon=":material/list_alt:")
    st.dataframe(
        df[["id", "waktu_citra", "area", "lat", "lon", "length_m", "width_m", "confidence"]],
        hide_index=True,
        column_config={
            "id": "ID",
            "waktu_citra": "Tanggal citra",
            "area": "Area",
            "lat": st.column_config.NumberColumn("Lintang", format="%.4f"),
            "lon": st.column_config.NumberColumn("Bujur", format="%.4f"),
            "length_m": st.column_config.NumberColumn("Panjang", format="%.0f m"),
            "width_m": st.column_config.NumberColumn("Lebar", format="%.0f m"),
            "confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=1, format="percent"),
        },
    )
