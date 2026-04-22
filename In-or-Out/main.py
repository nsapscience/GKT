#Import aller benötigte Komponenten
from ultralytics import YOLO
import time
from threading import Thread
import cv2

#Eingang von der Maschine bekommen
def input():
  print("Eingang von der Maschine bekommen")


def output():
  print("Ausgang an die Maschine gesendet")

#Definitionen
cameras = [cv2.VideoCapture(i) for i in range(2)]
model = YOLO("yolov8n.pt")


#Hier passiert alles wichtige
def analyse():
  for idx, cam in enumerate(cameras):
    ret, frame = cam.read()

    if not ret:
        break

    results = model(frame)

    for result in results:
      boxes = result.boxes
      for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        conf = box.conf[0]
        cls = box.cls[0]

        if conf > 0.5:
          print("Teil ist drin")
          #Signal weiter das Teil drin
        else: 
          print("Teil ist nicht drin")
          #Signal weiter das Teil nicht drin


def main():
  t_input = Thread(target=input)
  t_analyse = Thread(target=analyse)
  t_output = Thread(target=output)
  
  t_input.start()
  t_analyse.start()
  t_output.start()

main() #Führt die main()-Funktion aus
