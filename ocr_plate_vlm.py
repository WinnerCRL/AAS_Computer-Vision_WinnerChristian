import os
import csv
import base64
import re
import requests
from Levenshtein import distance as levenshtein_distance
from PIL import Image

# === Konfigurasi ===
TEST_FOLDER = "test"
RESULT_CSV = "ocr_results.csv"
PROMPT = "Only return the license plate number shown in this image. No explanation, no description, no extra text. Just the plate number in uppercase."
LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"  # pastikan sesuai

# === Encode image jadi base64 untuk dikirim ke LMStudio ===
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# === Kirim ke LMStudio ===
def send_to_lmstudio(image_path):
    image_base64 = encode_image(image_path)
    payload = {
        "model": "llava-v1.5-7b-llamafile",  # pastikan model aktif
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }
        ],
        "temperature": 0.2,
        "max_tokens": 60  # dinaikkan agar tidak terlalu pendek
    }

    try:
        response = requests.post(LMSTUDIO_API_URL, json=payload)
        result = response.json()

        # Validasi response
        if "choices" not in result or not result["choices"]:
            print(f"[ERROR] Response tidak valid:\n{result}")
            return ""

        raw_output = result["choices"][0]["message"]["content"]
        return raw_output

    except Exception as e:
        print(f"[ERROR] LMStudio API failed: {e}")
        return ""

# === Ekstrak hasil jadi plate number bersih ===
def extract_plate_number(text):
    matches = re.findall(r'[A-Z0-9-]+', text.upper())
    plate = ''.join(matches)
    return plate[:10] if plate else ""

# === Hitung Character Error Rate (CER) ===
def calculate_cer(ground_truth, prediction):
    S_D_I = levenshtein_distance(ground_truth, prediction)
    N = len(ground_truth)
    return round(S_D_I / N, 4) if N > 0 else 1.0

# === Fungsi utama ===
def main():
    print("[INFO] Mulai proses OCR menggunakan LMStudio...")

    # Baca data ground truth dari data.csv
    csv_path = "data.csv"
    if not os.path.exists(csv_path):
        print(f"[ERROR] File CSV '{csv_path}' tidak ditemukan.")
        return

    gt_df = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            gt_df[row['image']] = row['data'].upper()

    image_files = sorted([
        f for f in os.listdir(TEST_FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png")) and f in gt_df
    ])

    if not image_files:
        print("[WARNING] Tidak ada gambar yang cocok dengan CSV di folder test/")
        return

    results = []

    for image_file in image_files:
        image_path = os.path.join(TEST_FOLDER, image_file)
        print(f"[PROCESSING] {image_file}")
        
        raw_response = send_to_lmstudio(image_path)
        prediction = extract_plate_number(raw_response)

        ground_truth = gt_df[image_file]
        cer = calculate_cer(ground_truth, prediction)

        print(f"[PREDICTION] {prediction} (GT: {ground_truth}, CER: {cer})")

        results.append([image_file, ground_truth, prediction, cer])

    # Simpan hasil ke CSV
    with open(RESULT_CSV, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["image", "ground_truth", "prediction", "CER_score"])
        writer.writerows(results)

    print(f"[DONE] Hasil disimpan di: {RESULT_CSV}")

if __name__ == "__main__":
    main()