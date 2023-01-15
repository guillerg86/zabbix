@echo off
REM ------------------------------------------------------------
REM @author: Guille Rodriguez https://github.com/guillerg86
REM 
REM Permite saber el display version (21H1, 21H2, 22H1 ...)
REM del sistema operativo instalado 
REM 
REM https://en.wikipedia.org/wiki/List_of_Microsoft_Windows_versions
REM ------------------------------------------------------------
FOR /F "tokens=2* skip=2" %%a in ('reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v "DisplayVersion"') do echo %%b