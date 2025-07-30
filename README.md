
# 🚗 License Plate OCR with LMStudio (Visual Language Model)

Program ini digunakan untuk melakukan **Optical Character Recognition (OCR)** pada gambar plat nomor kendaraan menggunakan **Visual Language Model (VLM)** berbasis **LLava + LMStudio API**. Output dari proses ini adalah prediksi teks plat nomor dari gambar dan evaluasi menggunakan **Character Error Rate (CER)**.

---

## 📁 Struktur Folder

```
project-folder/
│
├── test/                  # Folder berisi gambar plat nomor
│   ├── B1234XYZ.jpg
│   ├── D5678ABC.png
│
├── data.csv               # Ground truth: nama file gambar dan label plat nomor
├── ocr_plate_vlm.py       # File utama (script Python OCR)
├── ocr_results.csv        # Output hasil prediksi dan evaluasi
└── README.md              # File dokumentasi ini
```

---

## 📦 Requirements

- Python 3.8+
- Paket Python:
  - `requests`
  - `Pillow`
  - `python-Levenshtein`


## 🧠 Model yang Digunakan

- Model: `llava-v1.5-7b-llamafile`
- Server: [LMStudio](https://lmstudio.ai/) harus berjalan di `http://localhost:1234`
- Prompt:  
  > "Only return the license plate number shown in this image. No explanation, no description, no extra text. Just the plate number in uppercase."

---

## 📄 Format File `data.csv`

File CSV berisi ground truth label dengan format seperti:

```csv
image,data
B1234XYZ.jpg,B1234XYZ
D5678ABC.jpg,D5678ABC
```

- **image**: nama file gambar di folder `test/`
- **data**: label plat nomor yang benar

---

## ▶️ Cara Menjalankan

1. Jalankan LMStudio dan aktifkan model `llava-v1.5-7b-llamafile`
2. Letakkan gambar di folder `test/`
3. Pastikan `data.csv` sesuai format
4. Jalankan program:

```bash
python ocr_plate_vlm.py
```

---

## 📊 Output

File `ocr_results.csv` akan berisi hasil seperti:

| image        | ground_truth | prediction | CER_score |
|--------------|--------------|------------|-----------|
| B1234XYZ.jpg | B1234XYZ     | B1234XYZ   | 0.0       |
| D5678ABC.png | D5678ABC     | D5678ADC   | 0.1429    |

- **CER (Character Error Rate)** menunjukkan akurasi prediksi
  - 0.0 = prediksi sempurna
  - Semakin besar, semakin banyak error karakter

---

## ⚠️ Catatan Penting

- Pastikan model di LMStudio **aktif dan berjalan**.
- Ukuran gambar harus wajar (tidak terlalu besar) agar proses encoding base64 tidak gagal.
- Gambar harus jelas dan tidak blur agar VLM dapat mengenali plat dengan baik.

---
