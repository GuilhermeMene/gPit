# gPit package is part of the gPit software  (https://github.com/GuilhermeMene/gPit)
#Copyright (c) 2023 gPit Developers 
#Distributed under the terms of MIT License (https://github.com/GuilhermeMene/gPit/blob/main/LICENSE)

from tkinter import filedialog
from tkinter import *
import os
root = Tk()
root.withdraw()


print("############ gPit Software ############")
print("Please select the folder of log file.")

try: 
    directory = filedialog.askdirectory()

    LOGPATH = os.path.join(directory, 'Log.txt')

except Exception as e: print(e)

