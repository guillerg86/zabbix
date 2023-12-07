@echo off
REM ------------------------------------------------------------
REM @author: Guille Rodriguez https://github.com/guillerg86
REM 
REM Permite saber cuantos usuarios están conectados en ese mismo 
REM momento en la máquina.
REM ------------------------------------------------------------


qwinsta | find /I "Activ" /c