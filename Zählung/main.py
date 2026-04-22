import cv2
from ultralytics import YOLO
from collections import defaultdict


MODEL_PATH = "yolov8n.pt"  # vortrainiertes YOLOv8 Modell (n = nano, schnell)
VIDEO_SOURCE = 0           # 0 = Webcam, oder Pfad zu Videodatei z.B. "video.mp4"
CONF_THRESHOLD = 0.5       # Mindest-Konfidenz für Erkennung


try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"Fehler beim Laden des Modells: {e}")
    exit(1)


cap = cv2.VideoCapture(VIDEO_SOURCE)
if not cap.isOpened():
    print("Fehler: Konnte Videoquelle nicht öffnen.")
    exit(1)


total_counts = defaultdict(int)

print("Drücke 'q' zum Beenden.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO-Inferenz
    results = model(frame, conf=CONF_THRESHOLD)

    # Ergebnisse verarbeiten
    for result in results:
        boxes = result.boxes
        names = model.names

        for box in boxes:
            cls_id = int(box.cls[0])
            label = names[cls_id]
            total_counts[label] += 1

            # Bounding Box zeichnen
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}",
                        (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 1)

    # Zähleranzeige
    y_offset = 20
    for label, count in total_counts.items():
        cv2.putText(frame, f"{label}: {count}",
                    (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255, 255, 255), 2)
        y_offset += 20

    cv2.imshow("YOLO Objektzählung", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
