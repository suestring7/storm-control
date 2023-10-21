
set CONDAPATH=C:\Users\%username%\.conda
rem Define here the name of the environment
set ENVNAME=storm

rem The following command activates the base environment.
rem call C:\ProgramData\Miniconda3\Scripts\activate.bat C:\ProgramData\Miniconda3
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)

rem Activate the conda environment
rem Using call is required here, see: https://stackoverflow.com/questions/24678144/conda-environments-and-bat-files
call C:\ProgramData\Anaconda3\Scripts\activate.bat %ENVPATH%
rem Run a python script in that environment
cd C:\Users\%username%\Documents\GitHub\storm-control\storm_control\hal4000\
python hal4000.py xml\yuan_test_all_pvcam.xml

rem Deactivate the environment
call conda deactivate

rem Stay the window open
cmd /k