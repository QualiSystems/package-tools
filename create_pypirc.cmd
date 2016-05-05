@ECHO OFF
IF [%1] == [] GOTO Usage
IF [%2] == [] GOTO Usage
IF [%3] == [] GOTO Usage

SET repo=%1
SET username=%2
SET password=%3
SET pypirc_path=%HOMEDRIVE%%HOMEPATH%\.pypirc

IF EXIST %pypirc_path% DEL /F /Q %pypirc_path%

echo [distutils]>> %pypirc_path%
echo index-servers =>> %pypirc_path%
echo   %repo%>> %pypirc_path%
echo[>> %pypirc_path%
echo [%repo%]>> %pypirc_path%
echo repository=https://%repo%.python.org/pypi>> %pypirc_path%
echo username=%username%>> %pypirc_path%
echo password=%password%>> %pypirc_path%
echo[>> %pypirc_path%

ECHO %pypirc_path% was successfully created

GOTO End

:Usage
ECHO Usage
ECHO publish_package [pypi_repository] [username] [password] 
ECHO.
ECHO Sample:
ECHO publish_package pypi Quali PASSWORD 
EXIT /B 1

:End
