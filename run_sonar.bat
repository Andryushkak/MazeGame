@echo off
REM Run coverage
coverage run -m unittest discover
coverage xml

REM Run sonar-scanner
sonar-scanner
pause
