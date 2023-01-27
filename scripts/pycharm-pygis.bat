@echo off
set OSGEO4W_ROOT=C:\OSGeo4W64
set path=%OSGEO4W_ROOT%\bin;%WINDIR%\System32;%WINDIR%;%WINDIR%\System32\wbem

call o4w_env.bat 
call qt5_env.bat
call py3_env.bat

@echo off
path %PATH%;%OSGEO4W_ROOT%\apps\qgis\bin
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis
set GDAL_FILENAME_IS_UTF8=YES
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis\qtplugins;%QT_PLUGIN_PATH%
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis\python;%PYTHONPATH%

set PYCHARM="c:\Program Files\JetBrains\PyCharm Community Edition 2020.3.0\bin\pycharm64.exe"
@echo on
start "PyCharm with QGIS knowledge!" /B %PYCHARM% %*
