#Skript zum Aufnehmen der Bilder für das Training der KI# Skript zum Aufnehmen von Bildern mit Kameras bei GPIO-Signal auf Jetson Orin Nano
# Unterstützt anfangs eine Kamera, erweiterbar auf zwei Kameras

import cv2
import Jetson.GPIO as GPIO
import time
import os
from datetime import datetime

# GPIO Pin für das Signal (anpassen je nach Hardware)
SIGNAL_PIN = 18

# Verzeichnis zum Speichern der Bilder
SAVE_DIR = "captured_images" #in "..." kommt der Pfad zum Ordner
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Kamera initialisieren (für Jetson mit GStreamer)
def init_camera(camera_index=0):
    gst_pipeline = (
        f"nvarguscamerasrc sensor-id={camera_index} ! "
        "video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)30/1 ! "
        "nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! "
        "videoconvert ! video/x-raw, format=(string)BGR ! appsink"
    )
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
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

    print("Skript gestartet. Warte auf Signal...")

    try:
        while True:
            # Auf Signal warten
            if GPIO.input(SIGNAL_PIN):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                for i, cap in enumerate(cameras):
                    if cap is not None:
                        ret, frame = cap.read()
                        if ret:
                            filename = f"{SAVE_DIR}/camera_{i}_{timestamp}.jpg"
                            cv2.imwrite(filename, frame)
                            print(f"Bild gespeichert: {filename}")
                        else:
                            print(f"Fehler beim Lesen von Kamera {i}")
                
                # Kurze Pause, um Mehrfachauslösungen zu vermeiden
                time.sleep(1)
            
            time.sleep(0.1)  # Polling-Intervall
    
    except KeyboardInterrupt:
        print("Skript beendet.")
    
    finally:
        # Aufräumen
        for cap in cameras:
            if cap is not None:
                cap.release()
        GPIO.cleanup()

if __name__ == "__main__":
    main()