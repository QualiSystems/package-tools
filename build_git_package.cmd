pushd ..\%1
for %%X in (python.exe) do (set PythonPath=%%~$PATH:X)
IF NOT DEFINED PythonPath GOTO PythonMissing

IF (%1 == 6.4) echo ##teamcity[setParameter name='global.package.version.prefix' value='1.0'] 
IF (%1 == dev) echo ##teamcity[setParameter name='global.package.version.prefix' value='2.0']
IF (%1 == dev_7.1) echo ##teamcity[setParameter name='global.package.version.prefix' value='2.1'] 


IF EXIST dist RMDIR /q /s dist
IF EXIST %2-1.0.0 RMDIR /q /s %2-1.0.0
IF EXIST %2.egg-info RMDIR /q /s %2.egg-info

python setup.py sdist --format zip

popd

goto end
:PythonMissing
ECHO Python is missing 
EXIT /B 1

:end


