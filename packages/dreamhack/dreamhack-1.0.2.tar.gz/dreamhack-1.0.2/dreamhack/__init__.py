from .encryption import encryption
from .windows import windows
from .colorcodes import colorcodes # type:ignore
from .zipfiles import zipfiles
from .logging import logging #type:ignore
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