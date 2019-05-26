import time
import sys
import json
import socket

class Actuator():
    def __init__(self, relay1=18, relay2=23):
        self.relay1 = relay1
        self.relay2 = relay2
        self.height = 0
        
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay1, GPIO.OUT)
        GPIO.setup(self.relay2, GPIO.OUT)

    def calculate_time(self, distance):
        rate = 0.6
        return distance/rate
    
    def move_to(self, height, other=None):

        current = self.height
        distance = int(height) - current
        print("distance to move" + str(distance))
        if distance > 0: 
            self.elevate(abs(distance), other)
        elif distance < 0:
            self.lower(abs(distance), other)

    def elevate(self, distance, other=None):
        import time
        extend_time = self.calculate_time(distance)
        self.extend()
        if(other != None):
            other.extend()
        
        time.sleep(extend_time)
        

        self.stop()
        if(other != None):
            other.stop()
        self.height += distance

    def lower(self, distance):
        extend_time = self.calculate_time(distance)
        self.retract()
        time.sleep(extend_time)
        self.stop()
        self.height -= distance
    
    def retract(self):
        import RPi.GPIO as GPIO
        GPIO.output(self.relay1, GPIO.HIGH)
        GPIO.output(self.relay2, GPIO.LOW)
        
    def extend(self):
        import RPi.GPIO as GPIO
        GPIO.output(self.relay1, GPIO.LOW)
        GPIO.output(self.relay2, GPIO.HIGH)
        
    def stop(self):
        import RPi.GPIO as GPIO
        GPIO.output(self.relay1, GPIO.LOW)
        GPIO.output(self.relay2, GPIO.LOW)


def control():
    actuator1 = Actuator()
    actuator2 = Actuator(24, 25)
    while(True):
        char = input()
        if(char == 'w'):
            actuator1.extend()
            actuator2.extend()
        elif(char == 'x'):
            actuator1.retract()
            actuator2.retract()
        elif(char == 's'):
            actuator1.stop()
            actuator2.stop()

def distance():
    actuator1 = Actuator()
    actuator2 = Actuator(24, 25)
    while(True):
        print("Enter Distance to Go To: ")
        height = input()
        actuator1.move_to(height, actuator2)

if __name__ == "__main__":
    print("Control mode (c) or distance mode (d)")
    dec = input()
    if dec == 'c':
        control()
    elif dec == 'd':
        distance()
        GPIO.cleanup()

