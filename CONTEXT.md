# api-remove-bg — Project Context

## Ringkasan

Layanan HTTP kecil yang menerima satu gambar dan mengembalikan PNG dengan latar transparan.
Dipakai oleh frontend terpisah (Astro/Vercel) lewat CORS, atau langsung lewat `curl`.

## Arsitektur

- **FastAPI** menangani request; **rembg** (model U2-Net) memotong latar; **Pillow** membaca gambar.
- Seluruh proses terjadi di memori: gambar tidak ditulis ke disk dan tidak disimpan. Ini keputusan
  sadar supaya tidak perlu storage dan tidak ada foto pengguna yang tertinggal di server.
- Model U2-Net diunduh sekali ke `~/.u2net` saat pemakaian pertama, lalu dipakai ulang. Dockerfile
  menyiapkan folder itu agar model tidak diunduh ulang setiap container dibuat.

## Endpoint

| Method | Path | Keterangan |
| :--- | :--- | :--- |
| `GET` | `/` | Cek status |
| `POST` | `/remove-bg` | Field `file`, mengembalikan byte PNG |
| `POST` | `/api/process` | Sama, tetapi lewat `Response(media_type="image/png")` |

Dua endpoint POST berbagi logika yang sama. `/api/process` yang dipakai klien browser karena header
`Content-Type` eksplisit, sehingga hasilnya bisa langsung dipasang sebagai `src` gambar.

## Struktur

```
main.py             Seluruh server (routing + CORS + pemrosesan)
Dockerfile          python:3.9, libgl1, uvicorn di port 7860
requirements.txt    fastapi, uvicorn, python-multipart, rembg[cpu], pillow
```

## Menjalankan

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Docker (port mengikuti CMD di Dockerfile):

```bash
docker build -t api-remove-bg .
docker run -p 7860:7860 api-remove-bg
```

## Jebakan yang diketahui

- `allow_origins=["*"]` masih terbuka. Batasi ke domain frontend sebelum dipakai publik.
- `libgl1` wajib ada di image, kalau tidak rembg gagal saat memuat model.
- Batas ukuran unggahan ditentukan proxy/Hugging Face Spaces, bukan aplikasi ini.
