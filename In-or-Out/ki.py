#Übungsskript
#----------------------------------------------------------------------------------------------------------------------------------
#Autor: Noel Sappeck
#Datum: 30.04.2026
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

print("Alle Importe abgeschlossen")
time.sleep(1)

#Definitionen
#Kameras initialisieren, anpassbar je nach Anzahl der Kameras
cameras = [cv2.VideoCapture(i) for i in range(1)]
#YOLO-Modell laden, als -.engine Datei, für Schnelligkeit
model = YOLO("yolov8n.engine", device='cuda' if torch.cuda.is_available() else 'cpu') 
#Grundlegend ist ein Teil in der Form, sicherheit das die Maschine nicht einfach wieder losfährt
inside = True 
#Queue für Frames vom Analyse-Thread zum Hauptthread, begrenzte Größe um Speicher zu sparen
frame_queue = Queue(maxsize=20)
stop_analysis = False  # Flagge zum Beenden der Analyse
#globale Variable, die verfolgt, ob die GPIO-Initialisierung bereits erfolgt ist (um Mehrfachinitialisierungen zu vermeiden)
global_initialized_gpio = False
#GPIO-Pins für Signalausgabe an die Maschine
PIN_OUT = 10

print("Alle Definitionen abgeschlossen")
time.sleep(1)

#GPIO initialisieren
def init_gpio():
  global global_initialized_gpio, PIN_OUT
  
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(PIN_OUT, GPIO.OUT, initial=GPIO.LOW)
  global_initialized_gpio = True

  print("init_gpio() abgeschlossen")
  time.sleep(1)

#GPIO aufräumen
def cleanup_gpio():
  if global_initialized_gpio:
    GPIO.cleanup()

    print("cleanup_gpio() abgeschlossen")
    time.sleep(1)

#Konsolenausgabe der KI unterdrücken
@contextmanager 
def suppress_output():
  with open(os.devnull, 'w') as devnull:
    with redirect_stdout(devnull), redirect_stderr(devnull):
      yield

  print("suppress_output() abgeschlossen")
  time.sleep(1)    

#Kameraaufnahmeauflösung einstellen, damit weniger Speicher und CPU verwendet wird
for cam in cameras:
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Kameraauflösung eingestellt")
time.sleep(1)

#Hier passiert alles wichtige
def analyse():
  global inside, stop_analysis
  
  print("Analyse-Thread gestartet")
  time.sleep(1)

  while not stop_analysis:  
    try:
      for idx, cam in enumerate(cameras):
        ret, frame = cam.read()
        
        if not ret:
            continue

        with suppress_output():
          results = model(frame, imgsz=320, conf=0.5, half=torch.cuda.is_available(), verbose=False)
        annotated_frame = results[0].plot()

        # Prüfe, ob irgendein Objekt erkannt wurde
        detected = False
        for result in results:
          boxes = result.boxes
          if len(boxes) > 0:
            for box in boxes:
              conf = box.conf[0]
              if conf > 0.5:
                detected = True

                print(f"Objekt erkannt mit Konfidenz {conf:.2f}")
                time.sleep(1)

                break
            if detected:
              break
        
        inside = detected  # True wenn Teil erkannt, False sonst
        
        # Frame in Queue legen, ohne Blockieren
        try:
          frame_queue.put_nowait(annotated_frame)
        except:
          # Queue voll - Frame überspringen
          pass
    except Exception as e:
      continue

    print("analyse() Schleife abgeschlossen")
    time.sleep(1)

#An Maschine Signal schicken, ob Produkt noch in der Form ist oder nicht
def output():

  print("Output-Thread gestartet")
  time.sleep(1)

  global inside, global_initialized_gpio
  
  if not global_initialized_gpio:
    init_gpio()
  
  while not stop_analysis:
    try:
      if inside == True:
        # Teil noch in der Form - GPIO LOW (kein Signal)
        GPIO.output(PIN_OUT, GPIO.LOW)

        print("Teil erkannt - GPIO LOW")
        time.sleep(1)

      else:
        # Teil nicht mehr in der Form - GPIO HIGH (Signal gesendet)
        GPIO.output(PIN_OUT, GPIO.HIGH)

        print("Teil nicht erkannt - GPIO HIGH")
        time.sleep(1)

    except Exception as e:
      continue

    print("output() Schleife abgeschlossen")
    time.sleep(1)

#Hauptfunktion in der alles zusammengepackt wird 
def main():

  print("Hauptfunktion gestartet")
  time.sleep(1)

  global stop_analysis
  
  t_analyse = Thread(target=analyse)
  t_output = Thread(target=output)
  
  t_output.daemon = True
  
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
    
    try:
      if cv2.waitKey(1) & 0xFF == ord('q'):
        stop_analysis = True
        break
    except:
      # Fehler bei waitKey - ignorieren
      pass
  
  # Aufräumen
  t_analyse.join(timeout=5)
  
  #GPIO aufräumen
  cleanup_gpio()
  
  #Kameras freigeben und Fenster schließen
  for cam in cameras:
    cam.release()
  cv2.destroyAllWindows()
  
  print("Hauptfunktion abgeschlossen - Aufräumen durchgeführt")
  time.sleep(1)

#Aufrufen und Ausführen der main()-Funktion
if __name__ == "__main__":
  main()