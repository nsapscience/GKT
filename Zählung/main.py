from ultralytics import YOLO
import cv2


model = YOLO("yolov8n.pt")
cam = cv2.VideoCapture(0)
next_id = 0
carton_box = cv2.rectangle((100, 200), (300, 400), (255, 0, 0), 2)



#Gibt jedem Objekt eine ID, damit man sie über mehrere Frames hinweg verfolgen kann
def give_id():
    global obj_id #Freigeben für andere Funktionen

    next_id += 1 #ID erhöhen, damit jedes Objekt eine neue ID bekommt
    obj_id = next_id





#Zählt die Anzahl der Objekte, die Erkannt wurden
def count():
    print("Hello World")





#Wenn Objekt in den Karton gefallen ist, wird die ID gelöscht und damit wieder freigegeben
#Somit geht der ID-Wert nicht in das unendliche
def forget():
    if obj_id in karton:
        del obj_id




#Verbindet alles miteinander (Threading?)
def main():
    print("Hello World")






if __name__ == "__main__":
    main()