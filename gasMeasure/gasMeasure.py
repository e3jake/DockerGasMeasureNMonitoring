#!/usr/bin/python

import time
import random
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
time.time()
GPIO.setwarnings(False)

#=========================================================

#1st sensor
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#2nd sensor
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

result_f = ""
result_r = ""

#======================================================

def front_sensors(FA, FB):
    global result_f
    if ((FA==0)&(FB==0)):
        #result_f = "0"
        result_f = random.randrange(0,10)
    elif ((FA==0)&(FB==1)):
        #result_f = "700"
        result_f = random,randrange(700,720)
    elif ((FA==1)&(FB==0)):
        #result_f = "1500"
        result_f = random,randrange(1500,1700)
    elif ((FA==1)&(FB==1)):
        #result_f = "2000"
        result_f = random,randrange(2000,2200)
    return result_f

def rear_sensors(RA, RB):
    global result_r
    if ((RA==0)&(RB==0)):
        result_r = random.randrange(0,10)
    elif ((RA==0)&(RB==1)):
        result_r = random,randrange(700,720)
    elif ((RA==1)&(RB==0)):
        result_r = random,randrange(1500,1650)
    elif ((RA==1)&(RB==1)):
        result_r = random,randrange(2000,2200)
    return result_r

def db_update(default_m, front_m, rear_m):
    os.system("default : ", default_m)
    #/curl -X POST 'http://127.0.0.1:8086/write?db=gasdb&u=gasadmin&p=gasadmin' --data-binary "gasdb,host=drone default_m=$d_m
    #/gasdb,host=drone front_m=$random_f
    #/gasdb,host=drone rear_m=$random_r"
    return true 

#==========================================================

try:
    while True:
        
        #print(time.strftime('%y/%m/%d - %H:%M:%S'))

        FA = (GPIO.input(27))
        FB = (GPIO.input(22))
        RA = (GPIO.input(23))
        RB = (GPIO.input(24))

	default_m=700
	front_m=front_sensors(FA, FB)
	rear_m=rear_sensors(RA, RB)

	db_update(default_m, front_m, rear_m)

	#print(front_m, rear_m)
        #print(front_sensors(FA, FB), rear_sensors(RA, RB))
        #print(front_sensors(FA, FB))
        #print(rear_sensors(RA, RB))

        time.sleep(1.0)
 
except KeyboardInterrupt:
    print("Keyboard Interrupt")
    
except:
    print("Wrong key, Some error")
        
finally:
    print("Clean Up")
    GPIO.cleanup()
