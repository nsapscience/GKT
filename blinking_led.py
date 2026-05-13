import Jetson.GPIO as GPIO
import time

led_pin = 19

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)

try:
	while True:
		GPIO.output(led_pin, GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(led_pin, GPIO.LOW)
		time.sleep(0.5)
		
except KeyboardInterrupt:
	print("Exiting gracefully")
	GPIO.cleanup()
