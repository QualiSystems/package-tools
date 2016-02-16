#@ECHO OFF
IF EXIST dist RMDIR /q /s dist
IF EXIST %1-1.0.0 RMDIR /q /s %1-1.0.0
IF EXIST %1.egg-info RMDIR /q /s %1.egg-info

%programdata%\qualisystems\qspython27\python setup.py sdist --format zip

popd