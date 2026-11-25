import folium
import pytest
from folium.plugins import HeatMap, MarkerCluster

from lib.data import load_detections
from lib.map import build_map

CSV_PATH = "data/dummy_detections.csv"


@pytest.fixture
def df():
    return load_detections(CSV_PATH)


def _count_children_of_type(fmap, cls):
    return sum(1 for child in fmap._children.values() if isinstance(child, cls))


def test_build_map_default_center_and_zoom(df):
    fmap = build_map(df, mode="marker")
    assert fmap.location == [-2.5, 118.0]
    assert fmap.options["zoom"] == 7


def test_marker_mode_creates_one_bounding_box_per_row(df):
    fmap = build_map(df, mode="marker")
    assert _count_children_of_type(fmap, folium.Rectangle) == len(df)


def test_marker_popup_contains_expected_fields(df):
    fmap = build_map(df, mode="marker")
    boxes = [c for c in fmap._children.values() if isinstance(c, folium.Rectangle)]
    first_row = df.iloc[0]
    popups = [
        child
        for box in boxes
        for child in box._children.values()
        if isinstance(child, folium.Popup)
    ]
    popup_htmls = [p.html.render() for p in popups]
    assert any(str(first_row["id"]) in html for html in popup_htmls)
    assert any(str(first_row["confidence"]) in html for html in popup_htmls)


def test_bounding_box_size_scales_with_ship_length(df):
    """Kotak dalam derajat lat/lon (geografis), jadi kapal lebih panjang harus
    punya bounds lebih lebar - inilah yang membuatnya membesar saat zoom in,
    beda dari ukuran piksel tetap yang selalu sama di semua level zoom."""
    fmap = build_map(df, mode="marker")
    boxes = [c for c in fmap._children.values() if isinstance(c, folium.Rectangle)]

    sorted_df = df.sort_values("length_m")
    smallest_id, largest_id = sorted_df.iloc[0]["id"], sorted_df.iloc[-1]["id"]

    def box_lat_span(box):
        (lat1, _), (lat2, _) = box.locations
        return abs(lat2 - lat1)

    boxes_by_id = {}
    for box in boxes:
        for child in box._children.values():
            if isinstance(child, folium.Popup) and smallest_id in child.html.render():
                boxes_by_id["small"] = box
            if isinstance(child, folium.Popup) and largest_id in child.html.render():
                boxes_by_id["large"] = box

    assert box_lat_span(boxes_by_id["large"]) > box_lat_span(boxes_by_id["small"])


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


def test_default_basemap_is_satellite_imagery(df):
    fmap = build_map(df, mode="marker")
    tile_layers = [c for c in fmap._children.values() if isinstance(c, folium.TileLayer)]
    assert any("arcgisonline.com" in layer.tiles for layer in tile_layers)
