# Skript zum regelmäßigen Aufnehmen von Bildern für das Training der KI
# Nimmt Bilder in regelmäßigen Abständen auf und speichert sie im Dataset-Ordner

import cv2
import time
import os
from datetime import datetime

# Verzeichnis zum Speichern der Bilder (bereits erstellter Ordner)
SAVE_DIR = "dataset"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Kamera initialisieren (einfach mit OpenCV)
def init_camera(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Fehler: Kamera {camera_index} konnte nicht geöffnet werden.")
        return None
    return cap

# Hauptfunktion
def main():
    # Eine Kamera initialisieren (für zwei Kameras später erweitern)
    cameras = [init_camera(0)]
    if cameras[0] is None:
        return

    print("Skript gestartet. Bilder werden regelmäßig aufgenommen...")

    try:
        image_counter = 0
        while True:
            # Warte 5 Sekunden bis zum nächsten Bild
            time.sleep(5)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            for i, cap in enumerate(cameras):
                if cap is not None:
                    # Buffer leeren, um aktuelle Frames zu bekommen
                    for _ in range(10):
                        cap.read()
                    
                    ret, frame = cap.read()
                    if ret:
                        filename = f"{SAVE_DIR}/image_{image_counter:06d}_{timestamp}.jpg"
                        cv2.imwrite(filename, frame)
                        print(f"Bild gespeichert: {filename}")
                        image_counter += 1
                    else:
                        print(f"Fehler beim Lesen von Kamera {i}")

    except KeyboardInterrupt:
        print("Skript beendet.")

    finally:
        # Aufräumen
        for cap in cameras:
            if cap is not None:
                cap.release()

if __name__ == "__main__":
    main()