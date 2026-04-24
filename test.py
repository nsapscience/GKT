import cv2

def carton_box(frame):
    # Box zeichnen (x1, y1, x2, y2, Farbe, Dicke)
    cv2.rectangle(frame, (100, 100), (300, 300), (255, 0, 0), 2)

# Kamera öffnen (0 für die Standardkamera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Fehler: Kamera konnte nicht geöffnet werden")
    exit()

while True:
    # Frame von der Kamera lesen
    ret, frame = cap.read()
    if not ret:
        print("Fehler: Frame konnte nicht gelesen werden")
        break

    # Box zeichnen durch Aufruf der Funktion
    carton_box(frame)

    # Frame anzeigen
    cv2.imshow('Kamera mit Box', frame)

    # Auf 'q' warten, um zu beenden
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Ressourcen freigeben
cap.release()
cv2.destroyAllWindows()