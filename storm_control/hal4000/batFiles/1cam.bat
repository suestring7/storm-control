
rem Define here the path to your conda installation
set CONDAPATH=C:\Users\%username%\.conda
rem Define here the name of the environment
set ENVNAME=storm

rem The following command activates the base environment.
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)

rem Activate the conda environment
call C:\ProgramData\Anaconda3\Scripts\activate.bat %ENVPATH%

rem Run a python script in that environment
cd C:\Users\%username%\Documents\GitHub\storm-control\storm_control\hal4000\
python hal4000.py xml\1cam_blackfly.xml


rem Deactivate the environment
call conda deactivate


@echo OFF
cmd /k