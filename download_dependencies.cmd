pushd ..\%1

cd %1
dir

IF EXIST dependencies RMDIR /q /s dependencies
MKDIR dependencies

%programdata%\qualisystems\qspython27\Scripts\pip install --download dependencies\ dist\%2.zip
IF EXIST dependencies\%2.zip RMDIR /q /s dependencies\%2.zip

popd