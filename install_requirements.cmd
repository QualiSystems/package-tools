@ECHO OFF
pushd ..\%1
%programdata%\Qualisystems\QsPython27\Scripts\pip install -v -r ..\%2\requirements.txt
popd