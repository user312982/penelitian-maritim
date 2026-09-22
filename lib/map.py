import folium
import pandas as pd
from folium.plugins import HeatMap, MarkerCluster

DEFAULT_CENTER = [-2.5, 118.0]
DEFAULT_ZOOM = 7

# Citra satelit optik gratis, tanpa API key. Bukan citra radar SAR asli
# (tidak ada basemap tile SAR publik global) - ini cuma basemap visual
# yang lebih enak dilihat dibanding peta garis OpenStreetMap.
SATELLITE_TILES = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/"
    "World_Imagery/MapServer/tile/{z}/{y}/{x}"
)
SATELLITE_ATTR = (
    "Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics, "
    "and the GIS User Community"
)

# Kotak "penanda deteksi" ala anotasi model deteksi objek (bounding box merah
# + label) di paper YOLO, bukan pin peta biasa. Ukuran tetap dalam piksel
# layar karena data dummy tidak punya lebar/panjang kapal asli.
BOX_SIZE_PX = 34


def _popup_html(row: pd.Series) -> str:
    return (
        f"<b>{row['id']}</b><br>"
        f"Koordinat: {row['lat']}, {row['lon']}<br>"
        f"Waktu citra: {row['waktu_citra']}<br>"
        f"Confidence: {row['confidence']}"
    )


def _detection_box_icon(row: pd.Series) -> folium.DivIcon:
    half = BOX_SIZE_PX / 2
    html = f"""
        <div style="width:{BOX_SIZE_PX}px;height:{BOX_SIZE_PX}px;position:relative;">
          <div style="position:absolute;inset:0;border:2px solid #ef4444;
                      border-radius:3px;box-shadow:0 0 0 1px rgba(0,0,0,0.35);"></div>
          <span style="position:absolute;top:-16px;left:0;white-space:nowrap;
                       background:#ef4444;color:white;font-size:9px;font-weight:600;
                       padding:0 3px;border-radius:2px;line-height:1.3;">
            {row['id']} &middot; {row['confidence']:.2f}
          </span>
        </div>
    """
    return folium.DivIcon(html=html, icon_size=(BOX_SIZE_PX, BOX_SIZE_PX), icon_anchor=(half, half))


def _add_markers(fmap_or_group, df: pd.DataFrame) -> None:
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(_popup_html(row)),
            icon=_detection_box_icon(row),
        ).add_to(fmap_or_group)


def build_map(
    df: pd.DataFrame, mode: str, tiles: str = SATELLITE_TILES, attr: str | None = SATELLITE_ATTR
) -> folium.Map:
    fmap = folium.Map(location=DEFAULT_CENTER, zoom_start=DEFAULT_ZOOM, tiles=tiles, attr=attr)

    if mode == "marker":
        _add_markers(fmap, df)
    elif mode == "heatmap":
        HeatMap(df[["lat", "lon"]].values.tolist()).add_to(fmap)
    elif mode == "cluster":
        cluster = MarkerCluster()
        _add_markers(cluster, df)
        cluster.add_to(fmap)
    else:
        raise ValueError(f"Unknown map mode: {mode}")

    return fmap
