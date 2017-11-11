# Build with `python setup.py build_exe`
from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "C:\\Python34\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Python34\\tcl\\tcl8.6"
import shutil
from glob import glob
# Remove the build folder
shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)
import sys

includes = ['PyQt5.QtCore', 'PyQt5.QtGui', 'sip',
            'pyqtgraph', 'pyqtgraph.debug', 'pyqtgraph.graphicsItems',
            'pyqtgraph.ThreadsafeTimer',
            'numpy.core._methods', 'numpy.lib.format', 'pygments',
            'pygments.lexers.python', 'pygments.lexers._mapping',
            'pygments.formatters.html', 'pyqtgraph.parametertree',
            'matplotlib.backends.backend_tkagg', 'tkinter.filedialog',
            'reportlab.graphics.barcode.common', 'reportlab.graphics.barcode.code128',
            'reportlab.graphics.barcode.code93', 'reportlab.graphics.barcode.code39',
            'reportlab.graphics.barcode.usps', 'reportlab.graphics.barcode.usps4s',
            'reportlab.graphics.barcode.ecc200datamatrix']
            #'numpy.core._methods', 'numpy.lib.format',
            #'numpy', 'atexit', 'PyPDF2', 'xhtml2pdf', 'matplotlib', 'matplotlib.backends.backend_tkagg']

excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', "cvxopt", 'pywin.dialogs', 'tables',
            'Tkconstants', 'Tkinter', 'zmq', 'PySide','pysideuic']

packages = []

includefiles = ['LanguageSupport.csv', 'SystemLanguageSupport.csv', 'View\\img\\next.png',
                'View\\img\\pause.png', 'View\\img\\play.png', 'View\\img\\reset.png',
                'C:\\Python34\\Lib\\site-packages\\scipy',
                'dlls\\msvcp100.dll', 'dlls\\msvcr100.dll']

# import scipy._distributor_init
# scipy_path = os.path.dirname(scipy._distributor_init.__file__)
# includefiles.append(scipy_path)

if sys.version[0] == '2':
    # causes syntax error on py2
    excludes.append('PyQt5.uic.port_v2')

base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {'excludes': excludes, 'packages':packages,
    'includes':includes,'include_files':includefiles}

setup(name = "SERVOGLU",
      version = "0.1",
      description = "SERVOGLU",
      options = {"build_exe": build_exe_options},
      executables = [Executable("main.py", base=base)])

# shutil.move('C:\\Users\\iferrer\\PycharmProjects\\Servoglu\\build\\exe.win-amd64-3.5\\scipy\\spatial\\cKDTree.cp35-win_amd64.pyd',
#             'C:\\Users\\iferrer\\PycharmProjects\\Servoglu\\build\\exe.win-amd64-3.5\\scipy\\spatial\\ckdtree.cp35-win_amd64.pyd')
#
# shutil.copytree('C:\\Users\\iferrer\\AppData\\Local\\Continuum\\Anaconda3\\Library\\plugins\\platforms', 'C:\\Users\\iferrer\\PycharmProjects\\Servoglu\\build\\exe.win-amd64-3.5\\platforms')

# rename C:\Users\iferrer\PycharmProjects\Servoglu\build\exe.win-amd64-3.5\scipy\spatial\cKDTree.cp35-win_amd64.pyd ckdtree.cp35-win_amd64.pyd