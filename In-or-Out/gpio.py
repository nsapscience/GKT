import Jetson.GPIO as GPIO

global_initialized = False

PIN_OUT = 11

def init_gpio(pin_out=PIN_OUT):
    global global_initialized, PIN_OUT
    PIN_OUT = pin_out

    GPIO.setmode(GPIO.board)
    GPIO.setup(PIN_OUT, GPIO.OUT, initial=GPIO.LOW)
    global_initialized = True


def set_output_signal(active: bool):
    if not global_initialized:
        init_gpio()
    GPIO.output(PIN_OUT, GPIO.HIGH if active else GPIO.LOW)


def cleanup():
    if global_initialized:
        GPIO.cleanup()


if __name__ == "__main__":
    try:
        init_gpio()
        while True:
            set_output_signal(True)
            set_output_signal(False)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
