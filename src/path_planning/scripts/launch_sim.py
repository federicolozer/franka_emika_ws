#!/usr/bin/env python3
# coding=utf-8

import yaml
import rospkg
import os

yaml_path = rospkg.RosPack().get_path("path_planning") + "/config/mode.yaml"

if __name__ == '__main__': 
    with open(yaml_path, 'r') as file:
        yaml = yaml.safe_load(file)

        mode = list(yaml.values())[0]

        msg = f"roslaunch path_planning main.launch mode:={mode}"
        os.system(msg)

    