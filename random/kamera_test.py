import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cam = cv2.VideoCapture(0)

frame_count = 0
annotated_frame = None

while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame_count += 1

    # nur jedes 2. Frame berechnen
    if frame_count % 2 == 0:
        results = model(frame, conf=0.5, imgsz=320)
        annotated_frame = results[0].plot()
    else:
        # letztes Ergebnis weiterverwenden
        pass
    
    # fallback falls noch nichts da ist
    if annotated_frame is None:
        annotated_frame = frame

    cv2.imshow("Kameras", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()