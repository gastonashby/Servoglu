from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\vvvvvvvvvvvvv\\Anaconda3\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\vvvvvvvvvvvvv\\Anaconda3\\tcl\\tcl8.6"

base = None


executables = [Executable("main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "servoglu",
    options = options,
    version = "1",
    description = 'servoglu',
    executables = executables
)
