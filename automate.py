#!/usr/bin/python
import json, sys, getopt, itertools, re, os, subprocess, pathlib

def permuteConfig(config):
    settingNames = []
    settingLists = []
    for setting in config:
        settingNames.append(setting)
        values = []
        for value in config[setting]:
            values.append(value)
            if (setting == "filename"):
                path = os.path.dirname(value)
                pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        settingLists.append(values)
    configurations = list(itertools.product(*settingLists))
    print(str(len(configurations)) + " configuration(s) were created.")
    return (settingNames, configurations)

def subSettingValue(name, value, pbrtFile):
    return re.sub(r'(?P<before>' + str(name) + r'" *?[\["]{1,2})(.*?)(?P<after>[\]"]{1,2})', r'\g<before>' + str(value) + r'\g<after>', pbrtFile)

def render(pbrt, args):
    tempFile = re.sub(r'\.pbrt$', r'_temp.pbrt', args[-1])
    assert tempFile != args[-1]
    with open(tempFile, "w+") as pbrtFile:
        pbrtFile.write(pbrt)
    subprocess.call(["./pbrt"] + args[:-1] + [tempFile])
    os.remove(tempFile)


with open(sys.argv[-1], "r") as pbrtFile:
    pbrt = pbrtFile.read()

with open("automate.config", "r") as configFile:
    renderGroups = json.loads(configFile.read())

for renderGroup in renderGroups:
    settingNames, configurations = permuteConfig(renderGroup)
    for config in configurations:
        currentFile = pbrt
        for setting, value in zip(settingNames, config):
            currentFile = subSettingValue(setting, value, currentFile)
        render(currentFile, sys.argv[1:])
