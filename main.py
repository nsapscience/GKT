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

#Versucht Verbindung zum ESP32 herzustellen
try:
    ser = serial.Serial('COM3', 115200, timeout=3)
    print("Verbindung zu ESP32 hergestellt")
except serial.SerialException:
    print("Fehler: Verbindung zu ESP32 konnte nicht hergestellt werden")

#Erstellt Zahl
def zufall():
    while True: 
        global r
        r = random.randint(1, 4)
        time.sleep(3)

#Gibt Zahl an ESP32 weiter
def weitergabe():
    while True:
        if ser:
            ser.write(str(r).encode())
            print("Gesendete Zahl: ", r)
        time.sleep(3)

#Erstellt das Fenster
def window():  
    window = tk.Tk()
    window.title("Objekt Erkennung")
    window.geometry("400x200")

    error_typ = tk.Label(window, text="") #Fehlerart (falls geht)
    error_typ.pack()

    procent = tk.label(window, text="") #Prozent Übereinstimmung mit Optimum
    procent.pack()

    p = 50 #Später durch Variable, welche die Übereinstimmigkeit mit perfektem Teil abstimmt (neue funktion zur Berechnung)
    
    def update_text():
        error_typ.config(error_typ=str(r))
        procent.config(procent=str(p) + "%")
        window.after(200, update_text)

    update_text()
    window.mainloop()


#Verbindet alle benötigte Funktionen miteinander
def main():
    producer = Thread(target=weitergabe)
    consumer = Thread(target=zahl)

    producer.start()
    consumer.start()

#Aufruf der Funktionen
main()
window()
