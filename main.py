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

import random


#Versucht Verbindung zum ESP32 herzustellen
try:
    ser = serial.Serial('COM3', 115200, timeout=3)
    print("Verbindung zu ESP32 hergestellt")
except serial.SerialException:
    print("Fehler: Verbindung zu ESP32 konnte nicht hergestellt werden")

def zahl():
    while True:
        r = random.randint(1, 4)
        if r == 1:
            if ser:
                ser.write(b'1')
                print("1")
                time.sleep(1)
        elif r == 2:
            if ser:
                ser.write(b'2')
                print("2")
                time.sleep(1)
        elif r == 3:
            if ser:
                ser.write(b'3')
                print("3")
                time.sleep(1)
        elif r == 4:
            if ser:
                ser.write(b'4')
                print("4")
                time.sleep(1)


def main():
    producer = Thread(target=zahl)

    producer.start()


#Erstellt das Fenster  
window = tk.Tk()
window.title("Objekt Erkennung")
window.geometry("400x200")


#Aufruf der Funktionen
main()
window.mainloop()