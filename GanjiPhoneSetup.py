#coding=GBK
from distutils.core import setup
import py2exe

##options = {"py2exe":
##
##    {"compressed": 1, 
##     "optimize": 2,
##     "ascii": 1,
##     "includes":includes,
##     "bundle_files":  }
##    }
options = {"py2exe":
           {"bundle_files": 1}
           }

data_files = [
    ("", ["test.bmp"
          ])
    ]

setup(
    options = options,      
    zipfile=None,
    console=["GanjiPhone.py"],
    data_files=data_files,
    )
