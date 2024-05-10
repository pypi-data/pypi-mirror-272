from .encryption import encryption
from .windows import windows
from .colorcodes import colorcodes
from .zipfiles import zipfiles
from .logging import logging 
from .networking import networking
from .randoms import randoms
from .downloads import downloads
from .filepaths import filepaths
from .gui import gui
#type:ignore

import os
import sys
import subprocess

def install(package):
  try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
  except Exception as e:
    raise e
  else:
    return package

def install_list_of_packages(package_list):
  for package in package_list:
    install(package)

def random_int_in_range(min, max):
  return randoms.random_number_in_range(min,max)

def list_directory(directory):
  return filepaths.get_all_files_in_directory(directory)