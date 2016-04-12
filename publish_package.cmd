@ECHO OFF
IF [%1] == [] GOTO Usage
IF [%2] == [] GOTO Usage
IF [%3] == [] GOTO Usage
IF [%4] == [] GOTO Usage

SET repo=%1
SET username=%2
SET password=%3
SET package_relative_path=%4

Call create_pypirc.cmd %1 %2 %3
pushd %package_relative_path%
python setup.py sdist --format zip
python setup.py register -r %repo%
python setup.py sdist upload -r %repo%
popd

GOTO End

:Usage
ECHO Usage
ECHO publish_package [pypi_repository] [username] [password] [package_relative_path]
ECHO.
ECHO Sample:
ECHO publish_package pypi Quali PASSWORD package_relative_path

:End
