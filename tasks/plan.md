# Implementation Plan: Dashboard Monitoring Maritim SAR ALKI II (TA-4)

## Overview

Bangun prototipe dashboard Streamlit + Folium sesuai [SPEC.md](../SPEC.md), dimulai dari data dummy, lalu logika data (`lib/data.py`), logika peta (`lib/map.py`), baru 4 halaman Streamlit. Tiap layer di-test sebelum halaman UI dibangun di atasnya.

## Architecture Decisions

- Logika dipisah dari presentasi (`lib/` vs `app.py`/`pages/`) supaya bisa di-unit-test tanpa render Streamlit — sesuai Boundaries §7 SPEC.
- Data dummy jadi kontrak skema kolom; ganti ke data real TA-2/TA-3 nanti cukup ubah `lib/data.py`.
- Halaman "Tentang" statis, tidak butuh test otomatis (sesuai SPEC §5.4).

## Task List

### Phase 1: Foundation

- [ ] Task 1: Setup proyek & data dummy
- [ ] Task 2: `lib/data.py` — load & filter data

### Checkpoint: Foundation
- [ ] `pytest` hijau untuk `tests/test_data.py`
- [ ] `data/dummy_detections.csv` terbaca tanpa error

### Phase 2: Core Logic

- [ ] Task 3: `lib/map.py` — builder peta Folium

### Checkpoint: Core Logic
- [ ] `pytest` hijau untuk seluruh `tests/`

### Phase 3: Halaman

- [ ] Task 4: `app.py` — Halaman Peta Utama
- [ ] Task 5: `pages/1_Unggah_Citra.py` — Unggah & Proses Citra
- [ ] Task 6: `pages/2_Detail_Deteksi.py` — Detail Deteksi
- [ ] Task 7: `pages/3_Tentang.py` — Tentang/Metodologi

### Checkpoint: Complete
- [ ] `streamlit run app.py` jalan tanpa error, 4 halaman bisa dinavigasi
- [ ] Semua acceptance criteria §5 SPEC.md terpenuhi

---

## Task 1: Setup proyek & data dummy

**Description:** Siapkan struktur folder, `requirements.txt`, dan data dummy CSV sesuai skema §4 SPEC.md agar task berikutnya punya fondasi untuk load & test.

**Acceptance criteria:**
- [ ] `requirements.txt` berisi streamlit, folium, streamlit-folium, pandas, pytest
- [ ] `data/dummy_detections.csv` ada, kolom: id, lat, lon, waktu_citra, confidence, area — minimal 30 baris, tersebar di ≥3 tanggal dan ≥2 area
- [ ] Folder `lib/`, `pages/`, `tests/` dibuat (boleh kosong/`__init__.py` jika perlu)

**Verification:**
- [ ] `pip install -r requirements.txt` sukses di venv
- [ ] `python -c "import pandas as pd; d=pd.read_csv('data/dummy_detections.csv'); assert len(d)>=30"`

**Dependencies:** None

**Files likely touched:** `requirements.txt`, `data/dummy_detections.csv`

**Estimated scope:** XS

---

## Task 2: `lib/data.py` — load & filter data

**Description:** Fungsi murni untuk load CSV dummy, filter by rentang tanggal, filter by area, dan agregasi jumlah deteksi per periode (dipakai halaman Peta Utama & Detail Deteksi).

**Acceptance criteria:**
- [ ] `load_detections(path) -> pd.DataFrame`
- [ ] `filter_by_date(df, start, end) -> pd.DataFrame`
- [ ] `filter_by_area(df, areas: list[str]) -> pd.DataFrame`
- [ ] `aggregate_by_period(df) -> pd.DataFrame` (jumlah baris per `waktu_citra`)
- [ ] `latest_image_date(df)` mengembalikan tanggal maksimum dari data **tidak terfilter** (untuk badge §5.1)

**Verification:**
- [ ] `pytest tests/test_data.py` — semua hijau, mencakup: load menghasilkan jumlah baris sesuai CSV; filter tanggal mengecilkan hasil dengan benar; filter area hanya menyisakan area yang dipilih; agregasi cocok dengan `groupby` manual

**Dependencies:** Task 1

**Files likely touched:** `lib/data.py`, `tests/test_data.py`

**Estimated scope:** S

---

## Task 3: `lib/map.py` — builder peta Folium

**Description:** Fungsi untuk membangun objek `folium.Map` dari DataFrame deteksi, mendukung mode marker individual, heatmap, dan cluster.

**Acceptance criteria:**
- [ ] `build_map(df, mode: Literal["marker","heatmap","cluster"]) -> folium.Map`
- [ ] Mode `marker`: jumlah `folium.Marker` pada map == jumlah baris df, popup berisi id/koordinat/waktu/confidence
- [ ] Mode `heatmap`: layer `HeatMap` ter-attach ke map
- [ ] Mode `cluster`: `MarkerCluster` ter-attach dengan jumlah child == jumlah baris df
- [ ] Center default map: `lat=-2.5, lon=118.0`, zoom 7

**Verification:**
- [ ] `pytest tests/test_map.py` — hijau, cek jumlah children/layer pada objek Folium sesuai mode dan ukuran df

**Dependencies:** Task 2 (pakai df dari `lib/data.py` sebagai fixture test)

**Files likely touched:** `lib/map.py`, `tests/test_map.py`

**Estimated scope:** S

---

## Task 4: `app.py` — Halaman Peta Utama

**Description:** Landing page Streamlit: render peta dari `lib/map.py`, sidebar filter tanggal/area dari `lib/data.py`, badge citra terbaru.

**Acceptance criteria (dari SPEC §5.1):**
- [ ] Sidebar: `st.date_input` range dan `st.multiselect` area
- [ ] Peta full-width dengan toggle mode (marker/heatmap/cluster) via `st.radio`
- [ ] Badge "Citra terbaru: {tanggal} · near real-time" pakai `latest_image_date` dari data **tidak terfilter**
- [ ] Mengubah filter mengubah jumlah marker/data yang dipetakan

**Verification:**
- [ ] `streamlit run app.py` — manual: filter tanggal/area berfungsi, badge tidak berubah saat filter diubah
- [ ] Tidak ada test otomatis untuk file ini (UI Streamlit), tapi tidak boleh regresi `pytest` yang sudah ada

**Dependencies:** Task 2, Task 3

**Files likely touched:** `app.py`

**Estimated scope:** S

---

## Task 5: `pages/1_Unggah_Citra.py` — Unggah & Proses Citra

**Description:** Halaman unggah file citra dengan progress bar simulasi tahap proses dan preview hasil sebelum publish ke dataset.

**Acceptance criteria (dari SPEC §5.2):**
- [ ] `st.file_uploader` menerima .tif/.png/.jpg
- [ ] Progress bar tahap preprocessing → inferensi → hasil (stub, karena model TA-2 belum terintegrasi — beri catatan jelas di UI bahwa ini simulasi)
- [ ] Preview hasil deteksi (dummy/stub) ditampilkan sebelum publish
- [ ] Tombol publish menambah baris ke dataset yang dibaca `app.py` (append ke CSV atau session state — pilih yang paling sederhana: session state, karena CSV shared-state lintas proses tidak realistis untuk prototipe lokal)

**Verification:**
- [ ] Manual: upload file → progress selesai → preview muncul → publish menambah baris terlihat di halaman Peta Utama (dalam sesi yang sama)

**Dependencies:** Task 2

**Files likely touched:** `pages/1_Unggah_Citra.py`

**Estimated scope:** S

---

## Task 6: `pages/2_Detail_Deteksi.py` — Detail Deteksi

**Description:** Tabel hasil deteksi, grafik jumlah kapal per periode, tombol ekspor CSV.

**Acceptance criteria (dari SPEC §5.3):**
- [ ] `st.dataframe` menampilkan semua baris dataset (id, koordinat, confidence, waktu)
- [ ] `st.bar_chart`/`st.line_chart` dari `aggregate_by_period`
- [ ] `st.download_button` menghasilkan CSV identik dengan dataset yang ditampilkan

**Verification:**
- [ ] Manual: buka halaman, tabel dan grafik konsisten dengan `data/dummy_detections.csv`; download CSV lalu diff dengan data sumber

**Dependencies:** Task 2

**Files likely touched:** `pages/2_Detail_Deteksi.py`

**Estimated scope:** XS

---

## Task 7: `pages/3_Tentang.py` — Tentang/Metodologi

**Description:** Halaman statis: penjelasan pipeline TA-1/2/3, sumber data, batasan near real-time, kontak.

**Acceptance criteria (dari SPEC §5.4):**
- [ ] Konten menjelaskan pipeline TA-1/2/3 (ringkas, dari PRD §1 dan §4)
- [ ] Menyebut sumber data (Copernicus/ASF Vertex) dan basemap (OSM/OpenSeaMap)
- [ ] Menyebut batasan near real-time secara eksplisit (bukan real-time), sesuai PRD §6

**Verification:**
- [ ] Manual: halaman render tanpa error. Tidak perlu test otomatis (konten statis, per SPEC §5.4).

**Dependencies:** None (independen, bisa duluan jika mau, tapi diurutkan terakhir sesuai permintaan)

**Files likely touched:** `pages/3_Tentang.py`

**Estimated scope:** XS

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Model TA-2 belum siap saat Task 5 | Medium | Progress bar & preview di-stub eksplisit, ditandai jelas di UI, mudah diganti nanti |
| Streamlit tidak punya test framework native | Low | Halaman UI diverifikasi manual; logika inti (data, map) full di-unit-test |

## Open Questions

- Publish di Task 5: pakai `st.session_state` (hilang saat restart) vs append ke CSV (persist tapi race condition kalau multi-user). Plan ini pakai session_state untuk kesederhanaan prototipe — beri tahu kalau butuh persist ke file.
