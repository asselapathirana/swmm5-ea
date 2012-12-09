REM always run from the inspyred directory as ./src/build.bat(not from SRC): 

cd ./src 
(rmdir /s/q build   ) 1> copy.log
(rmdir /s/q build1  ) 1>> copy.log

(python E:\Urban_drainageI_II\2012\GA\inspyred\src\setup.py build ) 1> setup.log
mkdir build\exe.win32-2.7\projects
cd ..
xcopy /s/e/f/q projects src\build\exe.win32-2.7\projects
mkdir src\build\exe.win32-2.7\gnuplot
xcopy /s/q/f .\gnuplot\*.* src\build\exe.win32-2.7\gnuplot
cd src
ren build build1 
(python E:\Urban_drainageI_II\2012\GA\inspyred\src\setup-gui.py build) 1> setup2.log
cd ..
xcopy /f /q gui\*.gif src\build\exe.win32-2.7
