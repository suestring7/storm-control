# STORM CONTROL


> conda activate storm

 FOR /f "tokens=*" %G IN ('dir /b *.ui') DO ( echo  %G:.ui=_ui.py ) 


python -m PyQt5.uic.pyuic -x z-stage.ui -o try.py


## I hate cmd.exe, how come there's no one get a shell that wrap it to a bash?
## I found it: WSL!!! but i need admin to allow that feature in this computer... Keep waiting!

# took me almost an hour to get the following line work =-=

 FOR /f "tokens=*" %G IN ('dir /b stage.ui') DO ( set ui=%G & set py=%ui:.py=_ui.py% & python -m PyQt5.uic.pyuic -x %G -o %py%)

# still wrong :)

# a work around:
 FOR /f "tokens=*" %G IN ('dir /b stage.ui') DO ( set ui=%G & set py=%ui:.py=_ui.py% & python -m PyQt5.uic.pyuic -x %ui% -o %py%)

# it's so ridiculous that I wasted so much time here

 FOR /f "tokens=*" %G IN ('dir /b stage.ui') DO ( echo %~G_ui.py )

# what an idiot i am, powershell and cmd.exe are two different things:)

# it seems to work...
FOR /f "tokens=*" %G IN ('dir /b *.ui') DO ( python -m PyQt5.uic.pyuic -x %G -o %~nG_ui.py )

# not sure if i should laugh or not, i found multiple files with same name there and I thought that's windows weird thing... and then i realize that was because the original file use '-' instead of '_', then why did their "*.py" file differed? I have the guess that they did it all manually. That relieves me a little bit. Hopefully I don't have to change file name later.


# Blocked by Visual Studio not installed / no admin
06/03/2021



# Install VS2019
## Error: M_PI not defined, solved
## 'cl.exe' not found
> "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars32.bat"
### this is for x86, and still not using cl but link, weird
## Error: library machine type 'x86' conflicts with target machine type 'x64'

## Error: 
> LINK : warning LNK4044: unrecognized option '/lm.lib'; ignored
> LINK : fatal error LNK1181: cannot open input file 'fftw3-3.lib'

# With the suggestions from Ruobo, I checked the note from the postdoc and found that they were using mingw instead of VS
# And it seems to work better after I installed mingw, as the warning -lm.lib thing goes away
# And then I encounter a second problem, '.dll' not recognized, googled and it seems to be uncompatible between 32bit gcc and 64bit library, I use somecommand to check library bit and comfirm that is 64bit, then managed to install the 64bit mingw
## the reason I chose msys64: in scons, the default path they look for mingw64
```
	mingw_paths = [
	    r'c:\MinGW\bin',
	    r'C:\cygwin64\bin',
	    r'C:\msys64',
	    r'C:\msys64\mingw64\bin',
	    r'C:\cygwin\bin',
	    r'C:\msys',
	    r'C:\ProgramData\chocolatey\lib\mingw\tools\install\mingw64\bin'
	]
```

>  instructions:

Install MSYS2 from the official website and update the packages accordingly
install below packages inside the MSYS2 with pacman -S <packageName>:
mingw64/mingw-w64-x86_64-gcc
mingw64/mingw-w64-x86_64-make
mingw64/mingw-w64-x86_64-cmake
mingw64/mingw-w64-x86_64-gcc-libgfortran and mingw64/mingw-w64-x86_64-gcc-fortran
mingw64/mingw-w64-x86_64-msmpi
mingw64/mingw-w64-x86_64-openblas
add C:\msys64\mingw64\bin folder to the Windows Environment Variables path
open cmd and go to the downloaded Elmer's source and create-go inside the build folder
run cmake -DCMAKE_C_COMPILER:FILEPATH=gcc -DCMAKE_CXX_COMPILER:FILEPATH=g++ .. -G "MinGW Makefiles"
run cmake --build .

## Credit to https://github.com/ElmerCSC/elmerfem/issues/200
## the version I downloaded(they just upload this one 1 hour ago!):
## http://repo.msys2.org/distrib/x86_64/msys2-x86_64-20210604.exe
# Specify the path here to force it to look for the mingw64 instead of mingw32
```
         env = DefaultEnvironment(tools = [compiler],
                                 ENV = {'PATH' : ['C:/msys64/mingw64/bin'],  #'PATH' : os.environ['PATH'],
                                        'TMP' : os.environ['TMP'],
                                        'TEMP' : os.environ['TEMP']})
```
# It finally seems to work now!

# To my surprise, the storm env folder has "Lib" instead of "lib" which the python can't look for ??? who made this???

# It does work now!

06/07/2021


```
import PyDAQmx
from PyDAQmx import Task
import numpy as np


data = np.array([0,1,1,0,1,0,1,0], dtype=np.uint8)
data = np.array([0,0,0,0,0,0,0,0,0], dtype=np.uint8)

data = np.array([0,1,1,0,1,0,1,0], dtype=np.uint8)


data = np.array([0,1,0,0,0,0,1,0,1], dtype=np.uint8)
task = Task()
task.CreateDOChan("/Dev1/port0/line8:16","",PyDAQmx.DAQmx_Val_ChanForAllLines)
task.StartTask()
task.WriteDigitalLines(1,1,10.0,PyDAQmx.DAQmx_Val_GroupByChannel,data,None,None)
task.StopTask()

```