import streamlit as st

GLASS_CSS = """
<style>
[data-testid="stMetric"], .st-key-status_bar {
    backdrop-filter: blur(16px) saturate(160%);
    -webkit-backdrop-filter: blur(16px) saturate(160%);
    background: color-mix(in srgb, var(--secondary-background-color) 55%, transparent);
    border: 1px solid color-mix(in srgb, var(--border-color) 60%, transparent) !important;
    border-radius: 14px;
}
.st-key-status_bar {
    padding: 0.75rem 1rem;
    align-items: center;
}
</style>
"""


def inject_glass_style() -> None:
    st.html(GLASS_CSS)
