@echo off
SET root=%~dp0
SET python="C:\Program Files (x86)\Python\Python36\python.exe"
%python% %root:~0,-1%\\src\\cli.py %1 %2 %3 %4 %5 %6
