REM always run from the inspyred directory as ./src/build.bat(not from SRC): 

cd ./src 
(del /s /f  /q dist\*.* ) 1> copy.log
(python E:\Urban_drainageI_II\2012\GA\inspyred\src\setup.py py2exe ) 1> setup.log
(python E:\Urban_drainageI_II\2012\GA\inspyred\src\setup-gui.py py2exe) 1> setup2.log
mkdir dist\projects
cd ..
xcopy /s/e/f/q projects src\dist\projects
mkdir src\dist\gnuplot
xcopy /s/q/f .\gnuplot\*.* src\dist\gnuplot
xcopy /f dos.bat src\dist
xcopy /f /q *.gif src\dist
cd ./src
cd dist
rem ga3.exe
cd ..
