#!/usr/bin/env python3
# install modules if it fails:
# pip install sense_energy
# pip install nanoleafapi
# pip install playsound

import json
from sense_energy import Senseable
import time
from nanoleafapi import Nanoleaf, NanoleafDigitalTwin

with open("config.json", "r") as f:
    config = json.load(f)

print("Loading sense module...")
sense = Senseable()
creds = config["credentials"]
sense.authenticate(creds["username"], creds["password"])

print("Connecting to Nanoleaf...")
nl = Nanoleaf("0.0.0.0") #This is where you change your IP to match your own Nanoleaf Canvas/Hexagon Lights
twin = NanoleafDigitalTwin(nl)

# Set baseline colors for Digital Twin
panels = [18062, 110, 44071, 30877, 64842, 54394, 48856]
twin.set_color(panels[0], (200, 255, 200))
twin.set_color(panels[1], (255, 255, 160))
twin.set_color(panels[2], (255, 255, 160))
twin.set_color(panels[3], (255, 240, 216))
twin.set_color(panels[4], (255, 240, 240))
twin.set_color(panels[5], (255, 240, 240))
twin.set_color(panels[6], (204, 229, 255))  # light blue tesla top panel
twin.sync()

def panelupdate(ogwatts):
    if ogwatts < 1000:
        ogwatts = 1001
    watts = (ogwatts - 1000) / 1000
    decimals = (watts - int(watts)) * 1000
    if int(watts) == 0:
        twin.set_color(
            panels[0],
            ((int(200 - (0.2 * decimals))), 255, (200 - (int(0.2 * decimals)))),
        )  # green bottom panel
        twin.set_color(panels[1], (255, 255, 160))
        twin.set_color(panels[2], (255, 255, 160))
        twin.set_color(panels[3], (255, 240, 216))
        twin.set_color(panels[4], (255, 240, 240))
        twin.set_color(panels[5], (255, 240, 240))
    if int(watts) == 1:
        twin.set_color(panels[0], (0, 255, 0))  # set panel 1 green
        twin.set_color(
            panels[1], (255, 255, (160 - (int(0.16 * decimals))))
        )  # panel left yellow
        twin.set_color(
            panels[2], (255, 255, (160 - (int(0.16 * decimals))))
        )  # panel right yellow
        twin.set_color(panels[3], (255, 240, 216))
        twin.set_color(panels[4], (255, 240, 240))
        twin.set_color(panels[5], (255, 240, 240))
    if int(watts) == 2:
        twin.set_color(panels[0], (0, 255, 0))  # set panel 1 green
        twin.set_color(panels[1], (255, 255, 0))  # set panel 2 yellow
        twin.set_color(panels[2], (255, 255, 0))  # set panel 3 yellow
        # set panel full orange twin.set_color(panels[3],(255,140,0)) or 255,240,216
        twin.set_color(
            panels[3],
            (255, (int(240 - (0.1 * decimals))), (216 - (int(0.216 * decimals)))),
        )  # orange
        twin.set_color(panels[4], (255, 240, 240))
        twin.set_color(panels[5], (255, 240, 240))
    if int(watts) == 3:
        twin.set_color(panels[0], (0, 255, 0))  # set panel 1 green
        twin.set_color(panels[1], (255, 255, 0))  # set panel 2 yellow
        twin.set_color(panels[2], (255, 255, 0))  # set panel 3 yellow
        twin.set_color(panels[3], (255, 140, 0))  # set panel 4 orange
        twin.set_color(
            panels[4],
            (255, (int(240 - (0.24 * decimals))), (240 - (int(0.24 * decimals)))),
        )  # red
        twin.set_color(
            panels[5],
            (255, (int(240 - (0.24 * decimals))), (240 - (int(0.24 * decimals)))),
        )  # red
    if int(watts) > 3:
        twin.set_color(panels[0], (0, 255, 0))  # set panel 1 green
        twin.set_color(panels[1], (255, 255, 0))  # set panel 2 yellow
        twin.set_color(panels[2], (255, 255, 0))  # set panel 3 yellow
        twin.set_color(panels[3], (255, 140, 0))  # set panel 4 orange
        twin.set_color(panels[4], (255, 0, 0))  # red
        twin.set_color(panels[5], (255, 0, 0))  # red
    twin.sync()

def loop():
    active = 0
    oldactive = 0
    devices = ["1", "2"]
    twin.set_color(panels[0], (200, 255, 200))
    twin.set_color(panels[1], (255, 255, 160))
    twin.set_color(panels[2], (255, 255, 160))
    twin.set_color(panels[3], (255, 240, 216))
    twin.set_color(panels[4], (255, 240, 240))
    twin.set_color(panels[5], (255, 240, 240))
    twin.set_color(panels[6], (204, 229, 255))  # light blue tesla top panel
    while True:
        try:
            sense.update_realtime()
            oldactive = int(active)
            active = int(sense.active_power)
            #active = int(input("What do you want me to display?")) #uncomment to manually provide values
            devices = sense.active_devices
            for device in devices:
                print("Active Devices: " + device)
        except:
            print("Error connecting to Sense... Trying again in 1 minute")
        logActive(active, oldactive)
        # Updates every 60 seconds because the API updates every minute
        time.sleep(60)

def logActive(active, oldactive):
    diff = active - oldactive
    # active = input("Enter Watts in numerical format: ")
    panelupdate(active)
    curr_time = time.strftime("%H:%M:%S", time.localtime())
    print(curr_time, " Active Power Usage:", active, "W", "(", diff, "W", ")")

if __name__ == "__main__":  # Program entrance
    print("Sense Energy Project is starting...")
    print("Ctrl-C to quit at any time")
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end
        print("Exiting Sense Energy Project")
