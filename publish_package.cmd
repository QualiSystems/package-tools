@ECHO OFF
IF [%1] == [] GOTO Usage
IF [%2] == [] GOTO Usage
IF [%3] == [] GOTO Usage

SET repo=%1
SET username=%2
SET password=%3

Call create_pypirc.cmd %1 %2 %3
Call python setup.py register -r %repo%
Call python setup.py sdist upload -r %repo%
del .pypirc.

GOTO End

:Usage
ECHO Usage
ECHO publish_package [pypi_repository] [username] [password] 
ECHO.
ECHO Sample:
ECHO publish_package pypi Quali PASSWORD 

:End
