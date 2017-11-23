#!/usr/bin/env python3
from __magic import *

if __name__ == '__main__':
    info("Package: %r", __package__)
    GUI("FSBA v2.0", login=True, tab_dict=config_dict('config.ini'))
