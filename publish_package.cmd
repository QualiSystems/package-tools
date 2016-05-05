@ECHO OFF
IF [%1] == [] GOTO Usage
IF [%2] == [] GOTO Usage
IF [%3] == [] GOTO Usage
IF [%4] == [] GOTO Usage
IF [%5] == [] GOTO Usage

SET index_server=%1
SET repository=%2
SET username=%3
SET password=%4
SET package_relative_path=%5

python update_pypirc.py %index_server% %repository% %username% %password%
pushd %package_relative_path%
python setup.py sdist --format zip 
python setup.py register -r %repo% 
python setup.py sdist upload -r %repo%
popd

GOTO End

:Error
ECHO An error occurred during publish_package operation
EXIT /B %exit_code%
GOTO End

:Usage
ECHO Usage
ECHO publish_package [index_server] [repository] [username] [password] [package_relative_path]
ECHO.
ECHO Sample:
ECHO publish_package pypi http://pypi.python.org/pypi Quali PASSWORD package_relative_path
EXIT /B 1

:End
