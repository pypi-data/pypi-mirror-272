import os
import sys

# Get the directory of the current file (__init__.py)
current_dir = os.path.dirname(__file__)

# Add the directory to sys.path if it's not already included
if current_dir not in sys.path:
    sys.path.append(current_dir)

from .g2o import *