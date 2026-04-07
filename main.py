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
def output_deviation():
    #Berechnung der Werte
    def calculation(ideal_value, value):
        return abs(value - ideal_value) / ideal_value * 100
        
    global deviation #Für andere Funktionen veröffentlicht
    #Berechnung der Gesamtabweichung
    deviation = (calculation(ideal_color, color)*0,X + #Berechnung Farbe
                 calculation(ideal_scratch, scratch)*0,X #Berechnung Kratzer
                # + weitere Berechnungen
                )
    #Muss noch 0,X anpassen!!!
    #Soll die Werte zur Berechnugn von der Kamera und KI bekommen
    
#Gibt an welchen Status das Programm gerade hat und was gut/schlecht ist für Produkte
def status():
    print("Hello World!")

#Rückmeldung an ESP32 was gerade passiert und was mit dem Produkt ist (gut, schlecht, unsicher, überprüft)
def transfer():
    while True:
        if ser:
            ser.write(str(r).encode())
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
        procent.config(procent=f"Abweichung: {deviation:.1f}%")
        #Aktualisiert das Fenster alle 200ms
        window.after(200, update_text)

    update_text()
    window.mainloop()

#Verbindet alle benötigte Funktionen miteinander
def main():
    producer = Thread(target=transfer)
    consumer = Thread(target=output_deviation)

    producer.start()
    consumer.start()

#Aufruf der Funktionen
main()
window()
