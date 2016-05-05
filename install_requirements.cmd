pushd ..\%1

for %%X in (python.exe) do (set PythonPath=%%~$PATH:X)
IF NOT DEFINED PythonPath GOTO PythonMissing

pip install -v -r ..\%2\requirements.txt
popd
python -m pip install --upgrade pip

goto end
:PythonMissing
ECHO Python is missing 
EXIT /B 1

:end