#!/usr/bin/python
import json

with open("../../../pbrt-scenes/extender/extenderL.pbrt", "r") as pbrtFile:
    pbrt = pbrtFile.read()

with open("render.config", "r") as configFile:
    configs = json.loads(configFile.read())

for config in configs:
    for setting in config:
        print (setting)

#from subprocess import call
#call(["ls", "-l"])
