"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.

https://learn.adafruit.com/slamtec-rplidar-on-pi/cpython-on-raspberry-pi
"""

import os
from math import cos, sin, pi, floor
import pygame
from rplidar import RPLidar

# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb0')
pygame.init()
lcd = pygame.display.set_mode((480,320))
print(pygame.display.get_driver())
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = 'COM3'
lidar = RPLidar(None, PORT_NAME)

# used to scale data to fit on the screen
max_distance = 0

#pylint: disable=redefined-outer-name,global-statement
def process_data(data):
    global max_distance
    lcd.fill((0,0,0))
    for angle in range(360):
        distance = data[angle]
        if distance > 0:                  # ignore initially ungathered data points
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (240 + int(x / max_distance * 240), 160 + int(y / max_distance * 160))
            lcd.set_at(point, pygame.Color(255, 255, 255))
            
    pygame.draw.line(lcd,pygame.Color(255,0,0), [240,160],[340,160],2)
    pygame.display.update()


scan_data = [0]*360

try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        print(scan_data)
        process_data(scan_data)

except KeyboardInterrupt:
    print('Stoping.')
finally:
    lidar.stop()
    lidar.disconnect()
