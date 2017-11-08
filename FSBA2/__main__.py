#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.dirname(__file__))

from utils import *



if __name__ == '__main__':
    info(__package__)
    GUI("FSBA", login=True)
