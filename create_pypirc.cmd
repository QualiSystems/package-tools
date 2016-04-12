@ECHO OFF
IF [%1] == [] GOTO Usage
IF [%2] == [] GOTO Usage
IF [%3] == [] GOTO Usage

SET repo=%1
SET username=%2
SET password=%3

IF EXIST .pypirc. DEL .pypirc.

echo [distutils]>> .pypirc.
echo index-servers =>> .pypirc.
echo   %repo%>> .pypirc.
echo[>> .pypirc.
echo [%repo%]>> .pypirc.
echo repository=https://%repo%.python.org/pypi>> .pypirc.
echo username=%username%>> .pypirc.
echo password=%password%>> .pypirc.
echo[>> .pypirc.

ECHO .pypirc was successfully created

GOTO End

:Usage
ECHO Usage
ECHO publish_package [pypi_repository] [username] [password] 
ECHO.
ECHO Sample:
ECHO publish_package pypi Quali PASSWORD 
EXIT 1

:End
