from zoomto.utils import importlocalFile
import os

try:
    conf = importlocalFile(os.path.join(os.getcwd(), "conf.py"))
except:  # noqa
    conf = object()