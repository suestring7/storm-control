
<<<<<<< Updated upstream
set CONDAPATH=C:\Users\yxt5273\Anaconda3
=======
set CONDAPATH=C:\Users\turnkey\.conda
>>>>>>> Stashed changes
rem Define here the name of the environment
set ENVNAME=storm

rem The following command activates the base environment.
rem call C:\ProgramData\Miniconda3\Scripts\activate.bat C:\ProgramData\Miniconda3
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)

rem Activate the conda environment
rem Using call is required here, see: https://stackoverflow.com/questions/24678144/conda-environments-and-bat-files
<<<<<<< Updated upstream
call C:\Users\yxt5273\Anaconda3\Scripts\activate.bat %ENVPATH%
rem Run a python script in that environment
python C:\Users\yxt5273\Documents\GitHub\storm-control\storm_control\hal4000\hal4000.py C:\Users\yxt5273\Documents\GitHub\storm-control\storm_control\hal4000\xml\turnkey_config.xml
=======
call C:\ProgramData\Anaconda3\Scripts\activate.bat %ENVPATH%
rem Run a python script in that environment
python C:\Users\turnkey\Documents\GitHub\storm-control\storm_control\hal4000\hal4000.py C:\Users\turnkey\Documents\GitHub\storm-control\storm_control\hal4000\xml\turnkey_config.xml
>>>>>>> Stashed changes

rem Deactivate the environment
call conda deactivate


rem Stay the window open
cmd /k