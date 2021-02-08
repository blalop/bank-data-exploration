#!/usr/bin/env python

import os
import sys


try:
    from accountman.app import app
except ImportError:
    sys.path.append(os.path.abspath('./'))
    from accountman.app import app


if __name__ == '__main__':
    app.run_server(use_reloader=False)
