import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def action(pin):
    print('Sensor connected')

GPIO.add_event_detect(23,GPIO.RISING)
GPIO.add_event_callback(23,action)

try:
    while True:
        print('Low Gas')
        time.sleep(0.5)
            
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
