import cv2
import mediapipe as mp
import pyautogui

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils  # Untuk menggambar tangan

cap = cv2.VideoCapture(0)  # Buka kamera
cap.set(3, 1200)  # Lebar kamera
cap.set(4, 720)  # Tinggi kamera

prev_x, prev_y = 0, 0  # Simpan posisi tangan sebelumnya

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Balik gambar biar lebih natural
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Ubah ke RGB
    results = hands.process(frame_rgb)  # Deteksi tangan

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )  # Gambar tangan

            wrist = hand_landmarks.landmark[8]

            # Konversi koordinat ke ukuran layar
            h, w, _ = frame.shape
            x, y = int(wrist.x * w), int(wrist.y * h)

            # Jika sudah ada posisi sebelumnya, bandingkan pergerakannya
            if prev_x != 0 and prev_y != 0:
                if x - prev_x > 60:
                    pyautogui.press("right")  # Geser kanan
                    print("Geser ke kanan ➡️")

                elif prev_x - x > 60:
                    pyautogui.press("left")  # Geser kiri
                    print("Geser ke kiri ⬅️")

                elif prev_y - y > 60:
                    pyautogui.press("up")  # Geser atas
                    print("Geser ke atas ⬆️")

                elif y - prev_y > 60:
                    pyautogui.press("down")  # Geser bawah
                    print("Geser ke bawah ⬇️")

            prev_x, prev_y = x, y  # Simpan posisi terakhir

    cv2.imshow("Gesture Control", frame)  # Tampilkan kamera

    if cv2.waitKey(1) & 0xFF == ord("q"):  # Tekan 'q' untuk keluar
        break

cap.release()
cv2.destroyAllWindows()
