import cv2
from ultralytics import YOLO
import time
import threading
import queue

model = YOLO("yolov8n.pt")
cam = cv2.VideoCapture(0)

# Kamera-Auflösung reduzieren für mehr FPS
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_queue = queue.Queue(maxsize=1)  # Nur ein Frame in der Queue, um Speicher zu sparen
result_queue = queue.Queue(maxsize=1)

def inference_worker():
    while True:
        try:
            frame = frame_queue.get(timeout=1)
            if frame is None:  # Signal zum Beenden
                break
            results = model(frame, conf=0.3, imgsz=256, verbose=False)  # verbose=False um Logs zu reduzieren
            annotated_frame = results[0].plot()
            result_queue.put(annotated_frame)
        except queue.Empty:
            continue

def main():
    # Starte Inference-Thread
    inference_thread = threading.Thread(target=inference_worker, daemon=True)
    inference_thread.start()

    frame_count = 0
    prev_time = time.time()
    fps = 0
    annotated_frame = None

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame_count += 1

        # Frame in Queue legen für Inference (nur wenn Queue leer, um nicht zu überladen)
        if frame_queue.empty():
            try:
                frame_queue.put(frame, block=False)
            except queue.Full:
                pass

        # Ergebnis aus Queue holen, falls verfügbar
        try:
            annotated_frame = result_queue.get(block=False)
        except queue.Empty:
            pass

        # Fallback falls noch kein Ergebnis
        if annotated_frame is None:
            annotated_frame = frame

        # FPS berechnen jeden Frame
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # FPS im Bild anzeigen
        cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Kameras", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Thread beenden
    frame_queue.put(None)
    inference_thread.join(timeout=1)

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()