@echo off

setlocal

SET root=%~dp0
SET PYTHONPATH=%PYTHONPATH%;%root%

SET python="C:\Program Files (x86)\Python\Python36-32\python.exe"

IF EXIST %python% (
%python% "%root:~0,-1%\src\cli.py" %1 %2 %3 %4 %5 %6
) ELSE (
echo Could not find Python interpreter.
)