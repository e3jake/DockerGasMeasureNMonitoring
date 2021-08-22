import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
time.time()
GPIO.setwarnings(False)

#=========================================================

#1st sensor
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

result_f = ""

#======================================================

def A_sensor_gas(FA, FB):
    global result_f
    if ((FA==0)&(FB==0)):
        result_f = "0"
    elif ((FA==0)&(FB==1)):
        result_f = "700"
    elif ((FA==1)&(FB==0)):
        result_f = "1500"
    elif ((FA==1)&(FB==1)):
        result_f = "2000"
    return result_f

def A_sensor_gas(RA, RB):
    global result_f
    if ((RA==0)&(RB==0)):
        result_f = "0"
    elif ((RA==0)&(RB==1)):
        result_f = "700"
    elif ((RA==1)&(RB==0)):
        result_f = "1500"
    elif ((RA==1)&(RB==1)):
        result_f = "2000"
    return result_f

#==========================================================

try:
    while True:
        print(time.strftime('%y/%m/%d - %H:%M:%S'))
        
        RA = (GPIO.input(23))
        RB = (GPIO.input(24))
        print(A_sensor_gas(RA, RB))
        
        FA = (GPIO.input(27))
        FB = (GPIO.input(22))
        print(A_sensor_gas(FA, FB))
        time.sleep(1.0)
 
except KeyboardInterrupt:
    print("Keyboard Interrupt")
    
except:
    print("Wrong key, Some error")
        
finally:
    print("Clean Up")
    GPIO.cleanup()
