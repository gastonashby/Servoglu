# Build with `python setup.py build_exe`
from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\iferrer\\AppData\\Local\\Continuum\\\Anaconda3\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\iferrer\\AppData\\Local\\Continuum\\\Anaconda3\\tcl\\tcl8.6"
import shutil
from glob import glob
# Remove the build folder
shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)
import sys

includes = ['PyQt5.QtCore', 'PyQt5.QtGui', 'sip', 'pyqtgraph.graphicsItems',
            'numpy', 'atexit', 'matplotlib.tri.triangulation']
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',"cvxopt",
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl','tables',
            'Tkconstants', 'Tkinter', 'zmq','PySide','pysideuic']

packages = ['scipy', 'matplotlib', 'PyPDF2', 'xhtml2pdf']

if sys.version[0] == '2':
    # causes syntax error on py2
    excludes.append('PyQt5.uic.port_v3')


base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {'excludes': excludes, 'packages':packages,
    'includes':includes}

setup(name = "SERVOGLU",
      version = "0.1",
      description = "SERVOGLU",
      options = {"build_exe": build_exe_options},
      executables = [Executable("main.py", base=base)])

# rename C:\Users\iferrer\PycharmProjects\Servoglu\build\exe.win-amd64-3.5\scipy\spatial\cKDTree.cp35-win_amd64.pyd ckdtree.cp35-win_amd64.pyd