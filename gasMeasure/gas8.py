import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
time.time()
GPIO.setwarnings(False)

#=========================================================

#Front sensor
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Left sensor
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Right sensor
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Back sensor
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#LED OUTPUT
GPIO.setup(5, GPIO.OUT)  #Green
GPIO.setup(6, GPIO.OUT)  #Yellow
GPIO.setup(13, GPIO.OUT) #Red

#Buzzer Output
GPIO.setup(12, GPIO.OUT)

result_f = ""
result_l = ""
result_r = ""
result_b = ""

#======================================================

def front_sensor_gas(FA, FB):
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

def left_sensor_gas(LA, LB):
    global result_l
    if ((LA==0)&(LB==0)):
        result_l = "0"
    elif ((LA==0)&(LB==1)):
        result_l = "700"
    elif ((LA==1)&(LB==0)):
        result_l = "1500"
    elif ((LA==1)&(LB==1)):
        result_l = "2000"
    return result_l

def right_sensor_gas(RA, RB):
    global result_r
    if ((RA==0)&(RB==0)):
        result_r = "0"
    elif ((RA==0)&(RB==1)):
        result_r = "700"
    elif ((RA==1)&(RB==0)):
        result_r = "1500"
    elif ((RA==1)&(RB==1)):
        result_r = "2000"
    return result_r

def back_sensor_gas(BA, BB):
    global result_b
    if ((BA==0)&(BB==0)):
        result_b = "0"
    elif ((BA==0)&(BB==1)):
        result_b = "700"
    elif ((BA==1)&(BB==0)):
        result_b = "1500"
    elif ((BA==1)&(BB==1)):
        result_b = "2000"
    return result_b

#==========================================================

try:
    while True:
        print(time.strftime('%y/%m/%d - %H:%M:%S'))
        
        FA = (GPIO.input(23))
        FB = (GPIO.input(24))
        LA = (GPIO.input(27))
        LB = (GPIO.input(22))
        RA = (GPIO.input(20))
        RB = (GPIO.input(21))
        BA = (GPIO.input(19))
        BB = (GPIO.input(26))
        print(front_sensor_gas(FA, FB)) #front
        print(left_sensor_gas(LA, LB))  #left
        print(right_sensor_gas(RA, RB)) #right
        print(back_sensor_gas(BA, BB))  #back
        print()
        
        if ((GPIO.input(23)==False)&(GPIO.input(24)==False)):
            GPIO.output(5, True)
            GPIO.output(6, False)
            GPIO.output(13, False)     
            GPIO.output(12, False)
            
        elif ((GPIO.input(23)==True)&(GPIO.input(24)==False)):
            GPIO.output(5, False)
            GPIO.output(6, True)
            GPIO.output(13, False)
            GPIO.output(12, False)

        elif ((GPIO.input(23)==True)&(GPIO.input(24)==True)):
            GPIO.output(5, False)
            GPIO.output(6, False)
            GPIO.output(13, True)
            GPIO.output(12, True)
                
        time.sleep(1.0)
 
except KeyboardInterrupt:
    print("Keyboard Interrupt")
    
except:
    print("Wrong key, Some error")
        
finally:
    print("Clean Up")
    GPIO.cleanup()
