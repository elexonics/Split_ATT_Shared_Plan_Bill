#using cx_freeze

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = "Win32GUI"

setup(  name = "calcAtt",
        version = "0.1",
        description = "Calc and Split ATT phone bill",
        options = {"build_exe": build_exe_options},
        executables = [Executable("calcAttGUI.py", base=base)])
