REM always run from the inspyred directory as ./src/build.bat(not from SRC): 
cls
cd ./src 
(rmdir /s/q build   ) 1> copy.log
(python E:\Urban_drainageI_II\2012\GA\inspyred\src\setup.py build ) 1> setup.log
cd ..
