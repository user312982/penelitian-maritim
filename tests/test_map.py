import folium
import pytest
from folium.plugins import HeatMap, MarkerCluster

from lib.data import load_detections
from lib.map import build_map, carto_tiles

CSV_PATH = "data/dummy_detections.csv"


def test_carto_tiles_without_key_falls_back_to_osm():
    tiles, attr = carto_tiles("light", None)
    assert tiles == "OpenStreetMap"
    assert attr is None


def test_carto_tiles_with_key_picks_style_by_theme():
    light_tiles, light_attr = carto_tiles("light", "mykey")
    dark_tiles, dark_attr = carto_tiles("dark", "mykey")
    assert "light_all" in light_tiles
    assert "dark_all" in dark_tiles
    assert "api_key=mykey" in light_tiles
    assert light_attr and dark_attr


@pytest.fixture
def df():
    return load_detections(CSV_PATH)


def _count_children_of_type(fmap, cls):
    return sum(1 for child in fmap._children.values() if isinstance(child, cls))


def test_build_map_default_center_and_zoom(df):
    fmap = build_map(df, mode="marker")
    assert fmap.location == [-2.5, 118.0]
    assert fmap.options["zoom"] == 7


def test_marker_mode_creates_one_marker_per_row(df):
    fmap = build_map(df, mode="marker")
    assert _count_children_of_type(fmap, folium.Marker) == len(df)


def test_marker_popup_contains_expected_fields(df):
    fmap = build_map(df, mode="marker")
    markers = [c for c in fmap._children.values() if isinstance(c, folium.Marker)]
    first_row = df.iloc[0]
    popups = [
        child
        for m in markers
        for child in m._children.values()
        if isinstance(child, folium.Popup)
    ]
    popup_htmls = [p.html.render() for p in popups]
    assert any(str(first_row["id"]) in html for html in popup_htmls)
    assert any(str(first_row["confidence"]) in html for html in popup_htmls)


def test_heatmap_mode_attaches_heatmap_layer(df):
    fmap = build_map(df, mode="heatmap")
    assert _count_children_of_type(fmap, HeatMap) == 1


def test_cluster_mode_attaches_cluster_with_all_points(df):
    fmap = build_map(df, mode="cluster")
    clusters = [c for c in fmap._children.values() if isinstance(c, MarkerCluster)]
    assert len(clusters) == 1
    cluster = clusters[0]
    marker_count = sum(1 for c in cluster._children.values() if isinstance(c, folium.Marker))
    assert marker_count == len(df)


def test_invalid_mode_raises():
    with pytest.raises(ValueError):
        build_map(load_detections(CSV_PATH), mode="bogus")
