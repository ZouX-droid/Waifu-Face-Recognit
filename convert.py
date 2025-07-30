from PIL import Image
import os

input_folder = 'Briyan'
output_folder = 'Briyan_RGB'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("[INFO] Mulai konversi ulang semua gambar ke RGB 8bit JPEG...")

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp', '.jfif')):
        input_path = os.path.join(input_folder, filename)
        try:
            with Image.open(input_path) as img:
                print(f"[INFO] {filename} | Mode: {img.mode}")
                img_rgb = img.convert('RGB')
                new_filename = os.path.splitext(filename)[0] + '_RGB.jpg'
                output_path = os.path.join(output_folder, new_filename)
                img_rgb.save(output_path, format='JPEG')
                print(f"[OK] Disimpan ke: {output_path}")
        except Exception as e:
            print(f"[ERROR] Gagal konversi {filename}: {str(e)}")

print("[SELESAI] Semua gambar selesai dikonversi.")
