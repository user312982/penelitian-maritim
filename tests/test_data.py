import pandas as pd
import pytest

from lib.data import (
    aggregate_by_period,
    filter_by_area,
    filter_by_date,
    latest_image_date,
    load_detections,
)

CSV_PATH = "data/dummy_detections.csv"


def test_load_detections_reads_all_rows():
    df = load_detections(CSV_PATH)
    raw = pd.read_csv(CSV_PATH)
    assert len(df) == len(raw)
    assert set(df.columns) == {"id", "lat", "lon", "waktu_citra", "confidence", "area"}


def test_filter_by_date_narrows_range():
    df = load_detections(CSV_PATH)
    start, end = "2026-09-01", "2026-09-01"
    filtered = filter_by_date(df, start, end)
    assert len(filtered) < len(df)
    assert (filtered["waktu_citra"] == "2026-09-01").all()


def test_filter_by_date_full_range_returns_all():
    df = load_detections(CSV_PATH)
    filtered = filter_by_date(df, "2026-01-01", "2026-12-31")
    assert len(filtered) == len(df)


def test_filter_by_area_keeps_only_selected():
    df = load_detections(CSV_PATH)
    selected = ["Makassar-Utara"]
    filtered = filter_by_area(df, selected)
    assert len(filtered) > 0
    assert set(filtered["area"].unique()) <= set(selected)


def test_filter_by_area_multiple():
    df = load_detections(CSV_PATH)
    selected = ["Makassar-Utara", "Makassar-Selatan"]
    filtered = filter_by_area(df, selected)
    assert set(filtered["area"].unique()) <= set(selected)
    assert len(filtered) < len(df)  # excludes Makassar-Tengah


def test_aggregate_by_period_matches_manual_groupby():
    df = load_detections(CSV_PATH)
    agg = aggregate_by_period(df)
    expected = df.groupby("waktu_citra").size()
    assert agg["count"].sum() == expected.sum()
    assert set(agg["waktu_citra"]) == set(expected.index)


def test_latest_image_date_returns_max_of_full_dataset():
    df = load_detections(CSV_PATH)
    result = latest_image_date(df)
    assert result == df["waktu_citra"].max()

    # even with a filtered (smaller) subset passed elsewhere, latest_image_date
    # should be computed from whatever df it's given — callers pass unfiltered df
    subset = df[df["area"] == "Makassar-Utara"]
    assert latest_image_date(df) >= latest_image_date(subset)
