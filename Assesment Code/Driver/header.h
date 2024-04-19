/*
 Name        : header.h - the header file with five IO controls
 Author      : Nikos Ledakis Engonopoulos
 Version     : 0.1
 Copyright   : :|
 Description : RPi - GPIO Driver 
 */
#ifndef HEADER_H
#define HEADER_H


typedef struct lkm_data {
        unsigned char data[256];
        unsigned long len;
        char type;
} lkm_data;

typedef struct gpio_pin {
        char desc[16];
        unsigned int pin;
        int value;
        int dir;
        char opt;
} gpio_pin;

#define IOCTL_PIIO_READ 0x65
#define IOCTL_PIIO_WRITE 0x66
#define IOCTL_PIIO_GPIO_READ 0x67
#define IOCTL_PIIO_GPIO_WRITE 0x68
#define IOCTL_PIIO_GPIO_SERVO_WRITE 0x69


#define  DEVICE_NAME "piiodev"
#define  CLASS_NAME  "piiocls"

#endif