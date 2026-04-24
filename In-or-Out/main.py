#Import aller benötigte Komponenten
from ultralytics import YOLO
import time
from threading import Thread
import cv2

#Definitionen
cameras = [cv2.VideoCapture(i) for i in range(2)]
model = YOLO("yolov8n.pt")
inside = False

#Eingang von der Maschine bekommen
def input():
  print("Eingang von der Maschine bekommen")


def output():
  print("Ausgang an die Maschine gesendet")




#Hier passiert alles wichtige
def analyse():
  global inside
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
          inside = True
          #Signal weiter das Teil drin
        else: 
          inside = False
          #Signal weiter das Teil nicht drin


def main():
  t_input = Thread(target=input)
  t_analyse = Thread(target=analyse)
  t_output = Thread(target=output)
  
  t_input.start()
  t_analyse.start()
  t_output.start()


#Ausführen der main()-Funktion
if __name__ == "__main__":
  main()