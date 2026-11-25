import pandas as pd


def load_detections(path: str) -> pd.DataFrame:
    return pd.read_csv(path, dtype={"waktu_citra": str})


def filter_by_date(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    return df[(df["waktu_citra"] >= start) & (df["waktu_citra"] <= end)]


def filter_by_area(df: pd.DataFrame, areas: list[str]) -> pd.DataFrame:
    return df[df["area"].isin(areas)]


def aggregate_by_period(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("waktu_citra")
        .size()
        .reset_index(name="count")
        .sort_values("waktu_citra")
        .reset_index(drop=True)
    )


def latest_image_date(df: pd.DataFrame) -> str:
    return df["waktu_citra"].max()


DATA_PATH = "data/dummy_detections.csv"


def load_all_detections() -> pd.DataFrame:
    """Data dummy + deteksi yang dipublikasikan dari halaman unggah (session state)."""
    import streamlit as st

    df = load_detections(DATA_PATH)
    extra = st.session_state.get("extra_detections")
    return pd.concat([df, pd.DataFrame(extra)], ignore_index=True) if extra else df
