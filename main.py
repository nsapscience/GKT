#import aller Sachen für Objekterkennung
from matplotlib.pyplot import box
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
except serial.SerialException:
    print("Fehler: Verbindung zu ESP32 konnte nicht hergestellt werden")

#!WIRD NOCH NICHT AUFGEFUREN
def area():
    x1, y1, x2, y2 = box

    width = x2 - x1
    height = y2 - y1
    
    area_px = width * height
    area_mm2 = area_px * (0.2 ** 2) #!Umrechnungsfaktor von px in mm², muss noch an Kamera angepasst werden












#Übergangsweise
ideal_scratch = 0
ideal_size = 0






#*Berechnung der Abweichung
def output_deviation():
    #Berechnung der Werte
    def calculation(ideal_value, value):
        return abs(value - ideal_value) / ideal_value * 100
        
    global deviation #Für andere Funktionen veröffentlicht
    #Berechnung der Gesamtabweichung
    deviation = (calculation(ideal_scratch, scratch)*0,3 +   #Berechnung Kratzer
                 calculation(ideal_size, size)*0,3      #Berechnung Größe
                # + weitere Berechnungen
                )

    #Soll die Werte zur Berechnung von der Kamera und KI bekommen (scratch, color)
        #ideal_value ist immer in 100 gerechnet
            #Bspw.: ideal_color = 100 (%), color = 95 (%)
        #Muss noch KI sagen was Optimum ist

#*Gibt an welchen Status das Programm gerade hat und was gut/schlecht ist für Produkte
def status():
    print("Hello World!")

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

#*Erstellt das Fenster
def window():  
    window = tk.Tk()
    window.title("Objekterkennung")
    window.geometry("400x200")

    error_typ = tk.Label(window, text="") #Fehlerart (falls geht)
    error_typ.pack()

    procent = tk.label(window, text="") #Prozent Übereinstimmung mit Optimum
    procent.pack()

    p = 50 #Später durch Variable, welche die Übereinstimmigkeit mit perfektem Teil abstimmt (neue funktion zur Berechnung)
    
    def update_text():
        error_typ.config(error_typ=str(p))
        procent.config(procent=f"Abweichung: {deviation:.1f}%")
        #Aktualisiert das Fenster alle 200ms
        window.after(200, update_text)

    update_text()
    window.mainloop()

#*Verbindet alle benötigte Funktionen miteinander
def main():
    producer = Thread(target=transfer)
    consumer = Thread(target=output_deviation)

    producer.start()
    consumer.start()

#Aufruf der Funktionen
main()
window()