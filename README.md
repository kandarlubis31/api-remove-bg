---
title: Api Remove Bg
emoji: 🏃
colorFrom: yellow
colorTo: indigo
sdk: docker
pinned: false
license: mit
---

# api-remove-bg

API penghapus latar belakang gambar. Kirim satu gambar, terima PNG dengan latar transparan.

Dibungkus sebagai layanan HTTP kecil: **FastAPI** sebagai server, **rembg** (model U2-Net) sebagai
mesin pemotong latar, **Pillow** untuk membaca gambar. Tidak ada antrean, tidak ada penyimpanan —
gambar diproses di memori dan langsung dikembalikan.

## Endpoint

| Method | Path | Isi |
| :--- | :--- | :--- |
| `GET` | `/` | Cek status: `{"status": "Backend AI is Running!"}` |
| `POST` | `/remove-bg` | Body `multipart/form-data`, field `file`. Mengembalikan byte PNG. |
| `POST` | `/api/process` | Sama, tetapi mengembalikan `Response` dengan `media_type: image/png`. |

Dua endpoint POST berisi logika yang sama. `/api/process` adalah yang dipakai klien browser karena
header responsnya eksplisit, sehingga hasilnya bisa langsung dipakai sebagai `src` gambar.

## Contoh

```bash
curl -F "file=@foto.jpg" http://localhost:8000/api/process -o hasil.png
```

## Menjalankan lokal

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Model U2-Net diunduh sekali ke `~/.u2net` pada pemakaian pertama, lalu dipakai ulang.

## Docker

```bash
docker build -t api-remove-bg .
docker run -p 7860:7860 api-remove-bg
```

Image memakai `python:3.9`, memasang `libgl1` (dibutuhkan rembg), dan menjalankan
`uvicorn main:app --host 0.0.0.0 --port 7860`.

## Catatan

- `allow_origins=["*"]` masih terbuka untuk semua domain. Batasi ke domain frontend sendiri
  sebelum dipakai di produksi.
- Batas ukuran unggahan ditentukan oleh server di depannya (Hugging Face Spaces / reverse proxy),
  bukan oleh aplikasi ini.

## Lisensi

MIT.
