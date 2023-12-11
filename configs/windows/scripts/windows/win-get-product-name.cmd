@echo off
REM ------------------------------------------------------------
REM @author: Guille Rodriguez https://github.com/guillerg86
REM 
REM Permite saber el nombre del sistema operativo que está instalado
REM en la máquina, de forma que en sistemas como Zabbix se pueda 
REM añadir al inventario de forma automática
REM ------------------------------------------------------------
FOR /F "tokens=2* skip=2" %%a in ('reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v "ProductName"') do echo %%b