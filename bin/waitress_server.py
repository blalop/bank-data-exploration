#!/usr/bin/env python

import os
import sys

import waitress


try:
    from accountman.app import server
except ImportError:
    sys.path.append(os.path.abspath('./'))
    from accountman.app import server


if __name__ == '__main__':
    waitress.serve(server)
