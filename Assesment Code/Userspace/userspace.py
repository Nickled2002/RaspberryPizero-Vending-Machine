 
# Name        : userspace.py
# Author      : Nikos Ledakis Engonopoulos
# Version     : 2023/v0.1
# Copyright   : copyright
# Description : userspace to communicate between driver and mqtt

import os
import time
import sys
import fcntl
import ctypes
#servo control change later
#from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
#mqtt
import paho.mqtt.client as paho

#class gpio_pin:
#    def __init__(self):
#        self.pin = 0
#        self.desc = "" 
#        self.value = 0
#        self.opt = ""
        
class gpio_pin(ctypes.Structure):
    _fields_ = [("desc", ctypes.c_char * 16),
                ("pin", ctypes.c_uint),
                ("value", ctypes.c_int),
                ("opt", ctypes.c_char),
                ("dir", ctypes.c_int)]

    def __init__(self):
        self.desc = b""
        self.pin = 0
        self.value = 0
        self.opt = b'E'
        self.dir = 0


#class lkm_data:
#    def __init__(self):
#        self.data = [0] * 256
#        self.len = 0
#        self.type = ""

class lkm_data(ctypes.Structure):
    _fields_ = [("data", ctypes.c_char * 256),
                ("len", ctypes.c_ulong),
                ("type", ctypes.c_char)]

    def __init__(self):
        self.data = b""
        self.len = 0
        self.type = b'E'

IOCTL_PIIO_READ = 0x65
IOCTL_PIIO_WRITE = 0x66
IOCTL_PIIO_GPIO_READ = 0x67
IOCTL_PIIO_GPIO_WRITE = 0x68
IOCTL_PIIO_GPIO_SERVO_WRITE = 0x69


DEVICE_NAME = "piiodev"
CLASS_NAME = "piiocls"

def write_to_driver_more(fd,s):
    ret = 0
    lkmdata = lkm_data()
    lkmdata.data = s
    lkmdata.len = 32
    lkmdata.type = b'w'
    ret = fcntl.ioctl(fd, IOCTL_PIIO_WRITE, lkmdata)
    if ret < 0:
        print("Function failed:{}".format(ret))
        exit(-1)
def write_to_driver(fd):
    ret = 0
    lkmdata = lkm_data()
    lkmdata.data = b"This is from user application"
    lkmdata.len = 32
    lkmdata.type = b'w'
    ret = fcntl.ioctl(fd, IOCTL_PIIO_WRITE, lkmdata)
    if ret < 0:
        print("Function failed:{}".format(ret))
        exit(-1)

def read_from_driver(fd):
    ret = 0
    lkmdata = lkm_data()
    lkmdata.data = b""
    ret = fcntl.ioctl(fd, IOCTL_PIIO_READ, lkmdata)
    if ret < 0:
        print("Function failed:{}".format(ret))
        exit(-1)
    print("Message from driver: {}".format(lkmdata.data))

def on_message_func(client,userdata,message):
    arg = str(message.payload.decode("utf-8","ignore"))
    args = arg.split()
    print("User App")
    fd = 0
    ret = 0
    DEVICE_NAME = "//dev//piiodev"
    msg = "Message passed by ioctl\n"
    fd = os.open(DEVICE_NAME, os.O_RDWR)
    if fd < 0:
        print("Can't open device file: {}".format(DEVICE_NAME))
        exit(-1)
    if len(args) > 0:
        if args[0] == "help":
           print("yes")
           print(args[1])
        if args[0] == "readmsg":
            read_from_driver(fd)
        if args[0] == "writemsg":
            if len (args) > 1:
                s = bytes(args[1], 'utf-8')
                write_to_driver_more(fd,s)
            else:
                write_to_driver(fd)
        if args[0] == "readpin":
            apin = gpio_pin()
            apin.desc = b"Details"
            apin.pin = int(args[1])
            ret = fcntl.ioctl(fd, IOCTL_PIIO_GPIO_READ, apin)
            print("READ:Requested pin:{} - val:{} - desc:{}".format(apin.pin, apin.value, apin.desc))
        if args[0] == "writepin":
            apin = gpio_pin()
            apin.pin = int(args[1])
            apin.value = int(args[2])
            ret = fcntl.ioctl(fd, IOCTL_PIIO_GPIO_WRITE, apin)
            print("WRITE:Requested pin:{} - val:{} - desc:{}".format(apin.pin, apin.value, apin.desc))
        if args[0] == "dispence":
            apin = gpio_pin()
            apin.pin = int(args[1])
            apin.value = 1
            ret = fcntl.ioctl(fd, IOCTL_PIIO_GPIO_WRITE, apin)
            for _ in range(5):
                bpin = gpio_pin()
                bpin.pin = 17
                bpin.value = 1
                ret = fcntl.ioctl(fd, IOCTL_PIIO_GPIO_WRITE, bpin)
                sleep(1)
                bpin.value = 0
                ret = fcntl.ioctl(fd, IOCTL_PIIO_GPIO_WRITE, bpin)
                cpin = gpio_pin()
                cpin.pin = 15
                cpin.value = 1
                ret = fcntl.ioctl(fd, IOCTL_PIIO_GPIO_WRITE, cpin)
                sleep(1)
                cpin.value = 0
                ret = fcntl.ioctl(fd, IOCTL_PIIO_GPIO_WRITE, cpin)
            apin = gpio_pin()
            apin.pin = int(args[1])
            apin.value = 0
            ret = fcntl.ioctl(fd, IOCTL_PIIO_GPIO_WRITE, apin)

            print("Food Dispenced on box:{}".format(apin.pin))
            #apin.value = int(sys.argv[3])
            #apin.dir =  int(sys.argv[4])
            #ret = fcntl.ioctl(fd, IOCTL_PIIO_GPIO_WRITE, apin)
            #print("WRITE:Requested pin:{} - val:{} - desc:{} - dir:{}".format(apin.pin, apin.value, apin.desc, apin.dir))
            #servo ctlr change to driver
            #factory = PiGPIOFactory()
            #servo = Servo(apin.pin, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
            #servo = Servo(apin.pin, pin_factory=factory)
            #servo.mid()
            #sleep(5)
            #servo.min()
            #sleep(10)
            #sleep(2)
            #servo.mid()
            #servo.max()
            #sleep(2)
            #print("Product Dispence")
        if args[0] == "toggle":
            apin = gpio_pin()
            apin.desc = b"desc"
            apin.pin = int(args[1])
            apin.value = int(args[2])
            times = int(args[3])
            delay = int(args[4])
            if times >= 30 or times <= 0:
                times = 10
            if delay >= 100000 * 10 or delay <= 0:
                delay = 100000
            for _ in range(times):
                print("TOGGLE:Requesting pin:{} - val:{} - desc:{}".format(apin.pin, apin.value, apin.desc))
                ret = fcntl.ioctl(fd, IOCTL_PIIO_GPIO_WRITE, apin)
                apin.value = not apin.value
                time.sleep(delay / 1000000)
    print("Exit 0")
    os.close(fd)
    #exit(0)

if __name__ == "__main__":
    broker="44.203.96.38"
    client = paho.Client("CMP408-userspace2")
    client.username_pw_set(username="Cmp408",password="raspberry")
    client.on_message=on_message_func
    client.connect(broker)
    client.subscribe("instructions")
    client.loop_forever()

