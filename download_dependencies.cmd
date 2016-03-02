pushd ..\%1
IF EXIST dependencies RMDIR /q /s dependencies
MKDIR dependencies

%programdata%\qualisystems\qspython27\Scripts\pip install --download dependencies\ dist\%2.zip

popd