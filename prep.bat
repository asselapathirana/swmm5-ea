python src\qrcgen.py res res
C:\Python27\Lib\site-packages\PyQt4\bin\pyrcc4 -o src/res_rc.py res.qrc
cd src
 C:\Python27\Lib\site-packages\PyQt4\bin\pyuic4.bat  mainwindow_.ui -o mainwindow_.py
echo "next"
rem C:\Python27\Lib\site-packages\PyQt4\bin\pyuic4.bat  parameters_dialog_.ui -o parameters_dialog_.py
rem C:\Python27\Lib\site-packages\PyQt4\bin\pyuic4.bat  swmmedit_dialog_.ui -o swmmedit_dialog_.py
C:\Python27\Lib\site-packages\PyQt4\bin\pyuic4.bat  about_dialog_.ui -o about_dialog_.py
cd ..

