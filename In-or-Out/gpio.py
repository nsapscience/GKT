import Jeston.GPIO as GPIO
import time

GPIO.setmode(GPIO.board)

PIN_OUT = 11 
PIN_IN = 7

GPIO.setup(PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_OUT, GPIO.OUT, initial=GPIO.LOW)


try: 
    while True:
        kontakt = GPIO.input(PIN_IN)

        if kontakt == GPIO.LOW:
            GPIO.output(PIN_OUT, GPIO.HIGH)
            print("Kontakt: Geschlossen -> Ausgang: An")
        else:
            GPIO.output(PIN_OUT, GPIO.LOW)
            print("Kontakt: Offen -> Ausgang: Aus")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Beendet.")

finally:
    GPIO.cleanup()