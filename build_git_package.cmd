@ECHO OFF
pushd ..\%1
IF EXIST dist RMDIR /q /s dist
IF EXIST %2-1.0.0 RMDIR /q /s %2-1.0.0
IF EXIST %2.egg-info RMDIR /q /s %2.egg-info

%programdata%\qualisystems\qspython27\python setup.py sdist --format zip

popd