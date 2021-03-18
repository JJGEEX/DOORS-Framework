#!/usr/bin/env python3

#pip install flux_led
#reference https://github.com/Danielhiversen/flux_led

from parse import *
import os
from flux_led import WifiLedBulb, BulbScanner
from itertools import cycle #for example purposes
import time #for example purposes

def command_handler(sentence):
    scanner = BulbScanner()
    coms, classify = commands()
    msg = ""
    function = None

    print("scanner scan: ", end="")
    print(scanner.scan(timeout = 4))
    #specific ID/MAC of bulb
    #my_light = scanner.getBulbInfoByID("D8F15BA2EE72")

    #if my_light:
    #    print("success!")
    #    bulb = WifiLedBulb(my_light["ipaddr"])
    #else:
    #    msg = "flux lightbulb not detected!"
    #    return msg, function
    bulb = None
    
    for i in coms[0]: #lightbulb color changer
        res = parse(i, sentence)
        if res:
            msg, function = colorChanger(bulb, res[0])
    return msg, function

def commands():
    coms = [
            [
                "turn the flux lightbulb color to {}",
                "set the flux bulb color to {}"
            ],
            ["turn the flux lightbulb off"],
            ["turn the flux lightbulb on"],
        ]
    
    classify = [
            "parse",
            "cosine",
            "cosine"
        ]
    return coms, classify

def colorChanger(bulb, color):
    msg = ""
    function = None
    colors = {
            "red" : (255,0,0),
            "orange" : (255,125,0),
            "yellow" : (255, 255, 0),
            "springgreen" : (125,255,0),
            "green" : (0,255,0),
            "turquoise" : (0,255,125),
            "cyan" : (0, 255, 255),
            "ocean" : (0,125,255),
            "blue" : (0,0,255),
            "violet" : (125, 0, 255),
            "magenta" : (255, 0, 255),
            "raspberry" : (255, 0, 125)
            }
    try:
        r,g,b = colors[color]
    except:
        msg = color+" is not a supported color for flux lightbulb"
        return msg, function
    #bulb.refreshState()

    # set to color and wait
    # (use non-persistent mode to help preserve flash)
    #bulb.setRgb(*color, persist=False)
    msg = "going to change flux bulb color to "+color
    function = None

    return msg, function

#code was ripped from https://github.com/beville/flux_led/blob/master/crossfade_example.py
def crossFadeChanger(bulb, color1, color2):

    r1,g1,b1 = color1
    r2,g2,b2 = color2
    
    steps = 100
    for i in range(1,steps+1):
            r = r1 - int(i * float(r1 - r2)/steps)
            g = g1 - int(i * float(g1 - g2)/steps)
            b = b1 - int(i * float(b1 - b2)/steps)
            # (use non-persistent mode to help preserve flash)
            bulb.setRgb(r,g,b, persist=False)

def crossFade(bulb):
    color_time = 5

    red = (255,0,0)
    orange = (255,125,0)
    yellow = (255, 255, 0)
    springgreen = (125,255,0)
    green = (0,255,0)
    turquoise = (0,255,125)
    cyan = (0, 255, 255)
    ocean = (0,125,255)
    blue = (0,0,255)
    violet = (125, 0, 255)
    magenta = (255, 0, 255)
    raspberry = (255, 0, 125)
    colorwheel = [red, orange, yellow, springgreen, green, turquoise,
                             cyan, ocean, blue, violet, magenta, raspberry]

    # use cycle() to treat the list in a circular fashion
    colorpool = cycle(colorwheel)

    # get the first color before the loop
    color = next(colorpool)

    while True:

            bulb.refreshState()

            # set to color and wait
            # (use non-persistent mode to help preserve flash)
            bulb.setRgb(*color, persist=False)
            time.sleep(color_time)

            #fade from color to next color
            next_color = next(colorpool)
            crossFade(bulb, color, next_color)

            # ready for next loop
            color = next_color


# code was ripped from https://github.com/beville/flux_led/blob/master/crossfade_example.py
def main():
    print("flux main does nothing")
        
if __name__ == "__main__":
    main()