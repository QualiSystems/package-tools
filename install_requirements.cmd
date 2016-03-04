pushd ..\%1
%programdata%\Qualisystems\QsPython27\Scripts\pip install -v -r ..\%2\requirements.txt
popd
%programdata%\Qualisystems\QsPython27\python -m pip install --upgrade pip