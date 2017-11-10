#!/usr/bin/env python3

import sys
import os
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cur_dir)

from utils import *

if __name__ == '__main__':
    info(__package__)
    GUI("FSBA v2.0", login=True, tab_dict=config_dict(cur_dir + '/config.ini'))
