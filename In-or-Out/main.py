#Import aller benötigte Komponenten
from ultralytics import YOLO
import time
from Thread import threading

#Eingang von der Maschine bekommen



#Definitionen
cameras = [cv2.VideoCapture(i) for i in range(2)]
model = YOLO("yolov8n.pt")


#Hier passiert alles wichtige
def analyse():
  print("hello world")


def main():
  t_analyse = threading.Thread(target=analyse)
  
  t_analyse.start()

main() #Führt die main()-Funktion aus
