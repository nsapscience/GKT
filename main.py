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

#Berechnung der Abweichung
def deviation():
    global deviation #Für andere Funktionen veröffentlicht
    deviation = (calculation_color(ideal_color, color)*0,X + #Berechnung Farbe
                 calculation_scratch(ideal_scratch, scratch)*0,X #Berechnung Kratzer
                ... #weitere Berechnungen
                )
    def calculation():

#Rückmeldung an ESP32 was gerade passiert und was mit dem Produkt ist (gut, schlecht, unsicher, überprüft)
def transfer():
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
    producer = Thread(target=transfer)
    consumer = Thread(target=deviation)

    producer.start()
    consumer.start()

#Aufruf der Funktionen
main()
window()
