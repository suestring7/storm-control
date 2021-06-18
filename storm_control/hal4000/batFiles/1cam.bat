rem cmd /k C:\Users\yxt5273\.conda\envs\storm\python.exe C:\Users\yxt5273\Documents\GitHub\storm-control\storm_control\hal4000\hal4000.py C:\Users\yxt5273\Documents\GitHub\storm-control\storm_control\hal4000\xml\1cam_blackfly.xml

@echo OFF
rem How to run a Python script in a given conda environment from a batch file.

rem It doesn't require:
rem - conda to be in the PATH
rem - cmd.exe to be initialized with conda init

rem Define here the path to your conda installation
set CONDAPATH=C:\Users\yxt5273\.conda
rem Define here the name of the environment
set ENVNAME=storm

rem The following command activates the base environment.
rem call C:\ProgramData\Miniconda3\Scripts\activate.bat C:\ProgramData\Miniconda3
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)

rem Activate the conda environment
rem Using call is required here, see: https://stackoverflow.com/questions/24678144/conda-environments-and-bat-files
call C:\ProgramData\Anaconda3\Scripts\activate.bat %ENVPATH%
rem Run a python script in that environment
python C:\Users\yxt5273\Documents\GitHub\storm-control\storm_control\hal4000\hal4000.py C:\Users\yxt5273\Documents\GitHub\storm-control\storm_control\hal4000\xml\1cam_blackfly.xml


rem Deactivate the environment
call conda deactivate

rem If conda is directly available from the command line then the following code works.
rem call activate someenv
rem python script.py
rem conda deactivate

rem One could also use the conda run command
rem conda run -n someenv python script.py