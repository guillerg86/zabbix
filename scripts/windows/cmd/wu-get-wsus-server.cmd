@echo off
REM ------------------------------------------------------------
REM @author: Guille Rodriguez https://github.com/guillerg86
REM 
REM Permite saber que servidor WSUS tiene configurada el equipo
REM Windows y mediante Zabbix disparar un trigger en caso de que
REM no sea el servidor correcto
REM ------------------------------------------------------------
FOR /F "tokens=2* skip=2" %%a in ('reg query "HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate" /v "WUServer"') do echo %%b