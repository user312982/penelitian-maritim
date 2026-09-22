import math

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

METERS_PER_DEGREE_LAT = 111_320


def _meters_to_degrees(meters: float, lat: float) -> tuple[float, float]:
    """(delta_lat, delta_lon) for a given size in meters at this latitude."""
    delta_lat = meters / METERS_PER_DEGREE_LAT
    delta_lon = meters / (METERS_PER_DEGREE_LAT * math.cos(math.radians(lat)))
    return delta_lat, delta_lon


def _popup_html(row: pd.Series) -> str:
    return (
        f"<b>{row['id']}</b><br>"
        f"Koordinat: {row['lat']}, {row['lon']}<br>"
        f"Waktu citra: {row['waktu_citra']}<br>"
        f"Confidence: {row['confidence']}<br>"
        f"Ukuran (dummy): {row['length_m']:.0f}m x {row['width_m']:.0f}m"
    )


def _add_bounding_boxes(fmap: folium.Map, df: pd.DataFrame) -> None:
    """Kotak merah dalam koordinat geografis nyata (meter), bukan piksel layar
    tetap - jadi membesar/mengecil mengikuti ukuran kapal saat zoom, seperti
    anotasi bounding box di paper deteksi objek."""
    for _, row in df.iterrows():
        half_lat, _ = _meters_to_degrees(row["length_m"] / 2, row["lat"])
        _, half_lon = _meters_to_degrees(row["width_m"] / 2, row["lat"])
        bounds = [
            [row["lat"] - half_lat, row["lon"] - half_lon],
            [row["lat"] + half_lat, row["lon"] + half_lon],
        ]
        folium.Rectangle(
            bounds=bounds,
            color="#ef4444",
            weight=2,
            fill=False,
            popup=folium.Popup(_popup_html(row)),
            tooltip=f"{row['id']} · {row['confidence']:.2f}",
        ).add_to(fmap)


def _add_point_markers(fmap_or_group, df: pd.DataFrame) -> None:
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=5,
            color="#ef4444",
            fill=True,
            fill_opacity=0.9,
            popup=folium.Popup(_popup_html(row)),
        ).add_to(fmap_or_group)


def build_map(
    df: pd.DataFrame, mode: str, tiles: str = SATELLITE_TILES, attr: str | None = SATELLITE_ATTR
) -> folium.Map:
    fmap = folium.Map(location=DEFAULT_CENTER, zoom_start=DEFAULT_ZOOM, tiles=tiles, attr=attr)

    if mode == "marker":
        _add_bounding_boxes(fmap, df)
    elif mode == "heatmap":
        HeatMap(df[["lat", "lon"]].values.tolist()).add_to(fmap)
    elif mode == "cluster":
        cluster = MarkerCluster()
        _add_point_markers(cluster, df)
        cluster.add_to(fmap)
    else:
        raise ValueError(f"Unknown map mode: {mode}")

    return fmap
