import face_recognition
import cv2
import os
import numpy as np

# === Step 1: Muat encoding dari 1 gambar terbaik ===
face_folder = 'Briyan'
print(f"[INFO] Memuat wajah kamu dari folder: {face_folder}")

known_face_encoding = None
for filename in os.listdir(face_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(face_folder, filename)
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encoding = encodings[0]
                print(f"[OK] Wajah digunakan dari: {filename}")
                break
            else:
                print(f"[WARNING] Tidak ada wajah di {filename}")
        except Exception as e:
            print(f"[ERROR] Gagal baca {filename}: {e}")

if known_face_encoding is None:
    print("[FATAL] Tidak ada wajah berhasil dimuat. Program berhenti.")
    exit()

# === Step 2: Mulai Kamera ===
video_capture = cv2.VideoCapture(0)
print("[INFO] Kamera aktif. Tekan 'q' untuk keluar.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        distance = face_recognition.face_distance([known_face_encoding], face_encoding)[0]
        score = round((1 - distance) * 100, 2)
        print(f"[DEBUG] Distance: {distance:.4f} | Score: {score:.2f}%")

        threshold = 0.60
        if distance < threshold:
            name = f"Briyan ({score}%)"
            color = (0, 255, 0)
        else:
            name = "Tidak Dikenal"
            color = (0, 0, 255)

        # Gambar kotak dan teks (font diperbesar)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom + 5), (right, bottom + 35), color, cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom + 28),
                    cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)

    cv2.imshow('Pengenalan Wajah Briyan', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
print("[INFO] Program selesai.")
