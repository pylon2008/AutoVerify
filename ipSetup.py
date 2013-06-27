#coding=GBK
from distutils.core import setup
import py2exe

options = {"py2exe":
           {"bundle_files": 1}
           }

data_files = [
    ("", ["Config.ini"
          ])
    ]

setup(
    options = options,      
    zipfile=None,
    console=["NetManager.py"],
    data_files=data_files,
    )
