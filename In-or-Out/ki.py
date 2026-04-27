#Import aller benötigte Komponenten
from ultralytics import YOLO
import os
import time
from contextlib import redirect_stderr, redirect_stdout, contextmanager
from threading import Thread
from queue import Queue
import cv2
import torch

#Definitionen
cameras = [cv2.VideoCapture(i) for i in range(1)] #2 Kameras öffnen
model = YOLO("yolov8n.pt", device='cuda' if torch.cuda.is_available() else 'cpu')  #KI öffnen, GPU bevorzugen wenn verfügbar
inside = True #Grundlegend ist ein Teil in der Form, sicherheit das die Maschine nicht einfach wieder losfährt
frame_queue = Queue(maxsize=10)  # Queue für Frames vom Analyse-Thread zum Hauptthread, begrenzte Größe um Speicher zu sparen
stop_analysis = False  # Flagge zum Beenden der Analyse

@contextmanager #*Dadurch ist die Konsole nicht voll mit Informationen
def suppress_output():
  with open(os.devnull, 'w') as devnull:
    with redirect_stdout(devnull), redirect_stderr(devnull):
      yield

#Kamera-Auflösung
for cam in cameras:
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#Von Maschine Signal bekommen
def input(): #!Input wenn nicht sogar weglassen, weil läuft Script und Kameras laufen ja eh die ganze Zeit im Hintergrunds
  pass

#An Maschine Signal schicken
def output():
  pass

#Hier passiert alles wichtige
def analyse():
  global inside, stop_analysis
  
  while not stop_analysis:  
    for idx, cam in enumerate(cameras):
      ret, frame = cam.read()
      
      if not ret:
          continue

      with suppress_output():
        results = model(frame, imgsz=416, conf=0.5, verbose=False)
      annotated_frame = results[0].plot()

      for result in results:
        boxes = result.boxes
        for box in boxes:
          x1, y1, x2, y2 = box.xyxy[0]
          conf = box.conf[0]
          cls = box.cls[0]

          if conf > 0.5:
            inside = True
            #Signal weiter das Teil drin
          else: 
            inside = False
            #Signal weiter das Teil nicht drin
      
      # Frame in Queue für Hauptthread legen
      frame_queue.put(annotated_frame)

#Hauptfunktion in der alles zusammengepackt wird 
def main():
  global stop_analysis
  
  t_input = Thread(target=input)
  t_analyse = Thread(target=analyse)
  t_output = Thread(target=output)
  
  t_input.daemon = True
  t_output.daemon = True
  
  t_input.start()
  t_analyse.start()
  t_output.start()
  
  # Fenster im Hauptthread anzeigen
  while True:
    try:
      # Frame aus Queue ohne Timeout holen
      frame = frame_queue.get_nowait()
      cv2.imshow('YOLOv8 Detection', frame)
    except:
      # Queue ist leer - weitermachen ohne warten
      pass
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
      stop_analysis = True
      break
  
  # Aufräumen
  t_analyse.join(timeout=5)
  
  for cam in cameras:
    cam.release()
  cv2.destroyAllWindows()

#*Aufrufen und Ausführen der main()-Funktion
if __name__ == "__main__":
  main()