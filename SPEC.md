# SPEC — Dashboard Monitoring Maritim SAR ALKI II (TA-4)

Diturunkan dari [PRD.md](PRD.md). Scope: prototipe TKT 3, Streamlit + Folium (brief resmi pembimbing). §8 PRD (React/FastAPI/Docker) adalah opsi roadmap Tahun 2 — di luar scope dokumen ini.

## 1. Objective

Dashboard web yang menyatukan hasil deteksi kapal (TA-2, YOLOv8 pada Sentinel-1) dan layer kepadatan kapal (TA-3) ke satu peta interaktif untuk segmen ALKI II (Selat Makassar), dioperasikan pengguna non-teknis (operator Bakamla/TNI AL/Polairud, dosen penguji, peneliti).

Karena data real TA-2/TA-3 mungkin belum siap, dashboard dibangun dulu dengan **data dummy** (CSV lokal) dengan skema yang sama seperti nanti output TA-2/TA-3, integrasi tinggal ganti sumber data.

## 2. Tech Stack

- Python 3.10+
- Streamlit (multipage via folder `pages/`)
- Folium + `streamlit-folium` (peta interaktif)
- pandas (data deteksi/kepadatan)
- pytest (test)

Tidak ada: FastAPI, Docker, PostgreSQL, React — itu §8 PRD, roadmap Tahun 2.

## 3. Struktur Proyek

```
tugas-akhir/
├── app.py                      # Halaman Peta Utama (landing, §5.1)
├── pages/
│   ├── 1_Unggah_Citra.py       # §5.2
│   ├── 2_Detail_Deteksi.py     # §5.3
│   └── 3_Tentang.py            # §5.4
├── lib/
│   ├── data.py                 # load/filter data deteksi & kepadatan (dummy atau real)
│   └── map.py                  # builder peta Folium (marker, heatmap, cluster)
├── data/
│   └── dummy_detections.csv    # data dummy: id, lat, lon, waktu_citra, confidence, area
├── tests/
│   ├── test_data.py
│   └── test_map.py
├── requirements.txt
└── SPEC.md
```

## 4. Skema Data Dummy

`data/dummy_detections.csv` kolom:

| kolom | tipe | contoh |
| --- | --- | --- |
| id | str | KPL-001 |
| lat | float | -2.5489 |
| lon | float | 118.0149 |
| waktu_citra | date (ISO) | 2026-09-15 |
| confidence | float 0-1 | 0.87 |
| area | str (sub-segmen ALKI II) | Makassar-Utara |

Minimal 30 baris dummy tersebar di beberapa tanggal & area agar filter dan heatmap terlihat bermakna.

## 5. Halaman & Acceptance Criteria

### 5.1 Peta Utama (`app.py`)
- Peta Folium full-width, center default Selat Makassar (`lat=-2.5, lon=118.0`, zoom 7)
- Marker per kapal, popup berisi: id, koordinat, waktu_citra, confidence
- Toggle layer: Marker individual / Heatmap / Cluster (via `folium.LayerControl` atau radio Streamlit)
- Sidebar filter: rentang tanggal (`st.date_input` range), area (`st.multiselect`)
- Badge: "Citra terbaru: {tanggal max} · near real-time"

**AC:** memuat CSV dummy → render peta dengan jumlah marker == jumlah baris setelah filter; ubah filter tanggal/area mengubah jumlah marker yang tampil; badge menampilkan tanggal max dari data yang termuat (bukan data terfilter).

### 5.2 Unggah & Proses Citra (`pages/1_Unggah_Citra.py`)
- Form unggah file citra (`st.file_uploader`, terima .tif/.png/.jpg untuk prototipe)
- Progress bar simulasi tahap: preprocessing → inferensi → hasil (karena model TA-2 tidak di-retrain di sini, boleh mock/stub jika model belum terintegrasi)
- Preview bounding box hasil sebelum "dipublikasikan" (tambah ke data deteksi yang dipakai halaman peta)

**AC:** upload file valid → progress bar mencapai selesai → preview menampilkan hasil (dummy/stub jika model belum ada) → tombol publish menambah baris ke dataset yang dibaca `app.py`.

### 5.3 Detail Deteksi (`pages/2_Detail_Deteksi.py`)
- Tabel hasil deteksi (`st.dataframe`): id, koordinat, confidence, waktu
- Grafik ringkas jumlah kapal per periode (`st.bar_chart` atau `st.line_chart`, agregasi per tanggal)
- Tombol ekspor CSV (`st.download_button`)

**AC:** tabel menampilkan semua baris dataset; grafik agregasi jumlah baris per `waktu_citra` cocok dengan `groupby` manual; download button menghasilkan CSV dengan isi identik ke dataset yang ditampilkan.

### 5.4 Tentang / Metodologi (`pages/3_Tentang.py`)
- Konten statis: penjelasan pipeline TA-1/2/3, sumber data, batasan near real-time, kontak
- Tidak ada logika, tidak perlu test otomatis (konten statis)

## 6. Testing Strategy

Mengikuti §6 PRD, tapi level unit/fungsi (bukan UI end-to-end, karena TKT 3 & non-teknis dijadwalkan manual/black-box terpisah oleh peneliti):

- `tests/test_data.py`: fungsi `lib/data.py` — load CSV, filter by tanggal, filter by area, agregasi per periode → assert dengan pytest
- `tests/test_map.py`: fungsi `lib/map.py` — builder peta menghasilkan jumlah marker sesuai input, layer heatmap/cluster ter-attach ke objek Folium

Black-box ECP dan SUS (§6 PRD) adalah pengujian manual terpisah di luar scope kode ini — tidak diautomasi.

## 7. Boundaries

**Selalu:**
- Pertahankan pemisahan `lib/data.py` (logika data) dari halaman Streamlit (presentasi) — supaya bisa di-test tanpa render UI
- Skema kolom dummy dipakai sebagai kontrak; kalau nanti ganti ke data real TA-2/TA-3, hanya `lib/data.py` yang berubah

**Tanya dulu sebelum:**
- Menambah dependency baru di luar requirements.txt (§3 di atas)
- Mengubah skema kolom data dummy setelah beberapa halaman dibangun di atasnya

**Jangan pernah:**
- Menambahkan FastAPI/Docker/PostgreSQL/React atau infra §8 PRD ke scope ini — itu roadmap Tahun 2, perlu konfirmasi pembimbing dulu
- Retraining atau mengubah model deteksi (ranah TA-2, out-of-scope PRD §3)
- Membangun autentikasi/login (out-of-scope TKT 3 per PRD §5.4)
