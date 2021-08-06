
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
python C:\Users\yxt5273\Documents\GitHub\storm-control\storm_control\hal4000\hal4000.py xml\yuan_test_all.xml

rem Deactivate the environment
call conda deactivate