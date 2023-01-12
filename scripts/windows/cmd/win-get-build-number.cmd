@echo off
REM ------------------------------------------------------------
REM @author: Guille Rodriguez https://github.com/guillerg86
REM 
REM Permite saber el release ID del sistema operativo instalado
REM pudiendo en Zabbix crear una alerta si la build number es inferior
REM a cierta release. Por ejemplo build number 19044 equivale a W10 21H2
REM 
REM https://en.wikipedia.org/wiki/List_of_Microsoft_Windows_versions
REM ------------------------------------------------------------
FOR /F "tokens=2* skip=2" %%a in ('reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v "ReleaseID"') do echo %%b