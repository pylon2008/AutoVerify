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
           {"bundle_files": 3}
           }

data_files = [
    ("", ["UrlConfig.xls",
          "Config.ini"
##          "C:\WINDOWS\system32\ole32.dll",
##          "C:\WINDOWS\system32\OLEAUT32.dll",
##          "C:\WINDOWS\system32\USER32.dll",
##          "C:\WINDOWS\system32\SHELL32.dll",
##          "C:\WINDOWS\system32\MSWSOCK.dll",
##          "C:\WINDOWS\system32\COMDLG32.dll",
##          "C:\WINDOWS\system32\COMCTL32.dll",
##          "C:\WINDOWS\system32\ADVAPI32.dll",
##          "c:\Python27\lib\site-packages\Pythonwin\mfc90.dll",
##          "C:\WINDOWS\system32\msvcrt.dll",
##          "C:\WINDOWS\system32\WS2_32.dll",
##          "C:\WINDOWS\system32\WINSPOOL.DRV",
##          "C:\WINDOWS\system32\GDI32.dll",
##          "C:\WINDOWS\system32\SHLWAPI.dll",
##          "C:\WINDOWS\system32\RPCRT4.dll",
##          "C:\WINDOWS\system32\VERSION.dll",
##          "C:\WINDOWS\system32\KERNEL32.dll",
##          "C:\WINDOWS\system32\\ntdll.dll"
          ])
    ]

setup(
    options = options,      
##    zipfile=None,
    console=["TaobaoViewer.py"],
    data_files=data_files,
    )
