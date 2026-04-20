#import aller Sachen für Objekterkennung
from ultralytics import YOLO
import cv2
import numpy as np

#Import aller Sachen für Esp32
import time
import serial

#Import für Fenster
import tkinter as tk

#Import für Ablauf
from multiprocessing import Process
from threading import Thread

#Übergangsweise
import random

#*Versucht Verbindung zum ESP32 herzustellen
try:
    ser = serial.Serial('COM3', 115200, timeout=3)
    print("Verbindung zu ESP32 hergestellt")
    time.sleep(2) #Wartezeit, damit ESP32 bereit ist
except serial.SerialException:
    print("Fehler: Verbindung zu ESP32 konnte nicht hergestellt werden")






#!WIRD NOCH NICHT AUSGEFÜHRT
model = YOLO("yolov8n.pt")

#Öffnen der Kameras
cameras = [
    cv2.VideoCapture(0),
    cv2.VideoCapture(1),
    cv2.VideoCapture(2),
    cv2.VideoCapture(3),
]

#Übergangsweise
area_mm2 = 0
deviation = 0.0

def art_int(cam):
    global area_mm2
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        results = model(frame)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                #Alles über 0.5% Sicherheit, wird berechnet
                if conf < 0.5:
                    continue
                #Berechnung der Fläche des Fehlers
                width = x2 - x1
                height = y2 - y1
                area_mm2 = width * height * (0.2 ** 2)

        if cv2.waitKey(1) == ord('q'):
            break


try:
    # Alle Kameras parallel in eigenen Threads starten
    import threading
    threads = [threading.Thread(target=art_int, args=(cam,)) for cam in cameras]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

#Wird sicherhaltshalber immer ausgeführt, damit im Hindergrund nichts aktiv ist
finally:
    # Alle Kameras sauber freigeben
    for cam in cameras:
        cam.release()
    cv2.destroyAllWindows()






#Übergangsweise
bad_value = 100 #* 100%

#*Berechnung der Abweichung
def output_deviation():
    #Berechnung der Werte       
    global deviation #Für andere Funktionen veröffentlicht
    #Berechnung der Gesamtabweichung
    while True:
        deviation = min((area_mm2 / bad_value) * 100, 100)
        time.sleep(1)
    #Soll die Werte zur Berechnung von der Kamera und KI bekommen (scratch, color)
        #ideal_value ist immer in 100 gerechnet
            #Bspw.: ideal_color = 100 (%), color = 95 (%)
        #Muss noch KI sagen was Optimum ist






#*Gibt an welchen Status das Programm gerade hat und was gut/schlecht ist für Produkte
def status(msg):
    message = msg + '\n'
    ser.write(message.encode('utf-8'))

    #Könnte aber meiner Meinung nach irgendwo hängen bleiben, Blau für Überprüfen
    #Er überprüft ja dauerhaft...
        #Ihn nur in einer gewissen Zeit überprüfen lassen?
            #zwischen den Zeiten dann calculation() und tranfer()






#*Rückmeldung an ESP32 was gerade passiert und was mit dem Produkt ist (gut, schlecht, unsicher, überprüft)
def transfer():
    r = random.randint(1, 100) #!Muss noch raus
    while True:
        if ser:
            ser.write(str(r).encode()) #!Muss noch geändert werden, mit den Werten die weiteregegeben werden sollen!
        time.sleep(1)







#*Erstellt das Fenster
def window():  
    window = tk.Tk()
    window.title("Objekterkennung")
    window.geometry("400x200")

    error_typ = tk.Label(window, text="") #Fehlerart (falls geht)
    error_typ.pack()

    procent = tk.Label(window, text="") #Prozent Übereinstimmung mit Optimum
    procent.pack()

    p = 50 #Später durch Variable, welche die Übereinstimmigkeit mit perfektem Teil abstimmt (neue funktion zur Berechnung)
    
    def update_text():
        error_typ.config(text=str(p))
        procent.config(text=f"Abweichung: {deviation:.1f}%")
        #Aktualisiert das Fenster alle 200ms
        window.after(200, update_text)

    update_text()
    window.mainloop()






#*Verbindet alle benötigte Funktionen miteinander
def main():
    t_camera = Thread(target=art_int)
    t_transfer = Thread(target=transfer)
    t_deviation = Thread(target=output_deviation)

    t_camera.start()
    t_transfer.start()
    t_deviation.start()


    #*HIER MUSS DANN NOCH ALLES REIN, ES IST NOCH GAR NICHTS FERTIG!




#Aufruf der Funktionen
main()
window()
