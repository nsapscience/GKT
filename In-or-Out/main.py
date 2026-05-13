#Hauptskript
#----------------------------------------------------------------------------------------------------------------------------------
#Autor: Noel Sappeck
#Datum: 28.04.2026
#GitHub: "https://github.com/nsapscience/GKT/tree/main/In-or-Out"

#Ziel ist es eine Künstliche Intelligenz zur Objekterkennung, wie YOLO, in den Maschinenprozess zu implementieren, 
#welches der Maschine ein Signal gibt ob ein Produkt sich noch in der Form befindet, oder vollständig entfernt wurde.
#---------------------------------------------------------------------------------------------------------------------------------

#Import aller benötigte Komponenten
#KI
from ultralytics import YOLO
#Für Parallelität
from threading import Thread
from queue import Queue
#Jetson Orin Nano Super
import Jetson.GPIO as GPIO
#Der Rest
import cv2
import torch
import os
import time
#Für Konsole
from contextlib import redirect_stderr, redirect_stdout, contextmanager

#Definitionen
#Kameras initialisieren, anpassbar je nach Anzahl der Kameras
cameras = []
for i in range(1):
  cam = cv2.VideoCapture(i)
  cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
  cameras.append(cam)  
#YOLO-Modell laden, als -.engine Datei, für Schnelligkeit
model = YOLO("yolov8n.engine")
#Grundlegend ist ein Teil in der Form, sicherheit das die Maschine nicht einfach wieder losfährt
inside = False
#Queue für Frames vom Analyse-Thread zum Hauptthread, kleine Größe für niedrige Latenz
frame_queue = Queue(maxsize=2)
stop_analysis = False  # Flagge zum Beenden der Analyse
#globale Variable, die verfolgt, ob die GPIO-Initialisierung bereits erfolgt ist (um Mehrfachinitialisierungen zu vermeiden)
global_initialized_gpio = False
#GPIO-Pins für Signalausgabe an die Maschine
GPIO_MODE = GPIO.BOARD
PIN_OUT = 19
LED_ACTIVE_HIGH = False  # Setze auf False, wenn LED aktiv low verdrahtet ist

#GPIO initialisieren
def init_gpio():
  global global_initialized_gpio, PIN_OUT, GPIO_MODE
  
  GPIO.setmode(GPIO_MODE)
  GPIO.setup(PIN_OUT, GPIO.OUT, initial=GPIO.LOW)
  global_initialized_gpio = True

#GPIO aufräumen
def cleanup_gpio():
  if global_initialized_gpio:
    GPIO.cleanup()

#Konsolenausgabe der KI unterdrücken
@contextmanager 
def suppress_output():
  with open(os.devnull, 'w') as devnull:
    with redirect_stdout(devnull), redirect_stderr(devnull):
      yield

#Kameraaufnahmeauflösung einstellen, damit weniger Speicher und CPU verwendet wird
for cam in cameras:
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#Hier passiert alles wichtige
def analyse():
  global inside, stop_analysis
  
  while not stop_analysis: 
    try:
      for idx, cam in enumerate(cameras):
        ret, frame = cam.read()
        
        if not ret:
            continue

        try:
          with suppress_output():
            results = model(frame, imgsz=640, conf=0.5, half=torch.cuda.is_available(), verbose=False)
          
          if results is None or len(results) == 0:
            continue
            
          annotated_frame = results[0].plot()
          
          if annotated_frame is None:
            continue

          # Prüfe, ob irgendein Objekt erkannt wurde
          detected = False
          for result in results:
            boxes = result.boxes
            if len(boxes) > 0:
              for box in boxes:
                conf = box.conf[0]
                if conf > 0.5:
                  detected = True
                  break
              if detected:
                break
          
          inside = detected
          
          # Frame in Queue legen - überschreibe alte wenn voll
          try:
            frame_queue.put_nowait(annotated_frame)
          except:
            try:
              frame_queue.get_nowait()
              frame_queue.put_nowait(annotated_frame)
            except:
              pass
          
        except:
          pass
          
    except:
      pass

#An Maschine Signal schicken, ob Produkt noch in der Form ist oder nicht
def output():
  global inside, global_initialized_gpio
  
  if not global_initialized_gpio:
    init_gpio()
    # LED vor Start auf aus setzen
    if LED_ACTIVE_HIGH:
      GPIO.output(PIN_OUT, GPIO.LOW)
    else:
      GPIO.output(PIN_OUT, GPIO.HIGH)
  
  while not stop_analysis:
    time.sleep(0.1)
    try:
      if inside:
        # Objekt erkannt - LED an
        GPIO.output(PIN_OUT, GPIO.HIGH if LED_ACTIVE_HIGH else GPIO.LOW)
      else:
        # Kein Objekt erkannt - LED aus
        GPIO.output(PIN_OUT, GPIO.LOW if LED_ACTIVE_HIGH else GPIO.HIGH)
    except Exception:
      pass

#Hauptfunktion in der alles zusammengepackt wird 
def main():
  global stop_analysis
  
  t_analyse = Thread(target=analyse)
  t_output = Thread(target=output)
  
  t_output.daemon = True
  
  t_analyse.start()
  t_output.start()
  
  # Fenster im Hauptthread anzeigen
  fps_time = time.time()
  fps_count = 0
  
  while not stop_analysis:
    try:
      frame = frame_queue.get(timeout=0.5)
      cv2.imshow('YOLOv8 Detection', frame)
      fps_count += 1
      
      # FPS anzeigen alle 30 Frames
      if fps_count % 30 == 0:
        elapsed = time.time() - fps_time
        fps = 30 / elapsed
        fps_time = time.time()
        fps_count = 0
    except:
      pass
    
    # Wichtig: waitKey muss nach imshow aufgerufen werden
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
      stop_analysis = True
      break
  
  # Aufräumen
  t_analyse.join(timeout=5)
  
  #GPIO aufräumen
  cleanup_gpio()
  
  #Kameras freigeben und Fenster schließen
  for cam in cameras:
    cam.release()
  cv2.destroyAllWindows()

#Aufrufen und Ausführen der main()-Funktion
if __name__ == "__main__":
  main()
