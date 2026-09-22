import folium
import pandas as pd
from folium.plugins import HeatMap, MarkerCluster

DEFAULT_CENTER = [-2.5, 118.0]
DEFAULT_ZOOM = 7
DEFAULT_TILES = "OpenStreetMap"

CARTO_ATTR = "&copy; <a href='https://carto.com/attributions'>CARTO</a>"


def carto_tiles(theme_type: str, api_key: str | None) -> tuple[str, str | None]:
    """Basemap URL for CartoDB (needs an API key), falling back to OpenStreetMap."""
    if not api_key:
        return DEFAULT_TILES, None
    style = "dark_all" if theme_type == "dark" else "light_all"
    url = f"https://{{s}}.basemaps.cartocdn.com/{style}/{{z}}/{{x}}/{{y}}{{r}}.png?api_key={api_key}"
    return url, CARTO_ATTR


def _popup_html(row: pd.Series) -> str:
    return (
        f"<b>{row['id']}</b><br>"
        f"Koordinat: {row['lat']}, {row['lon']}<br>"
        f"Waktu citra: {row['waktu_citra']}<br>"
        f"Confidence: {row['confidence']}"
    )


def _add_markers(fmap_or_group, df: pd.DataFrame) -> None:
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(_popup_html(row)),
        ).add_to(fmap_or_group)


def build_map(
    df: pd.DataFrame, mode: str, tiles: str = DEFAULT_TILES, attr: str | None = None
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
