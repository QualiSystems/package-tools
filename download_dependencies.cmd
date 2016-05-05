pushd ..\%1

for %%X in (python.exe) do (set PythonPath=%%~$PATH:X)
IF NOT DEFINED PythonPath GOTO PythonMissing

cd %1

IF EXIST dependencies RMDIR /q /s dependencies
MKDIR dependencies

pip download -r requirements.txt -d dependencies --no-cache-dir
popd

goto end
:PythonMissing
ECHO Python is missing 
EXIT /B 1

:end