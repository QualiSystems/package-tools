pushd ..\%1
SET PythonPath=%programdata%\Qualisystems\QsPython27
IF NOT EXIST %PythonPath% GOTO PythonMissing

%PythonPath%\Scripts\pip install -v -r ..\%2\requirements.txt
popd
%PythonPath%\python -m pip install --upgrade pip

goto end
:PythonMissing
ECHO Python is missing 
EXIT /B 1

:end
