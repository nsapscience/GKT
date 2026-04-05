import serial
import time
import cv2

ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)

def sende_befehl(befehl):
    ser.write((befehl +"\n").encode())
    print(f'Befehl gesendet: {befehl}')
    
    time.sleep(0.1)

    if ser.in_waiting:
        antwort = ser.readline().decode().strip()

sende_befehl('überprüft')
time.sleep(3)
sende_befehl('gut')
time.sleep(3)
sende_befehl('unbekannt')
time.sleep(3)
sende_befehl('schlecht')
time.sleep(3)

ser.close()