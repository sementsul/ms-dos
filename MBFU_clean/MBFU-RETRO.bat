@echo off
rem MBFU Retro Edition: весь интерфейс — DOS-мастер внутри DOSBox.
rem Этот скрипт только находит флешку и форматирует ее, дальше все в DOS.
setlocal EnableExtensions EnableDelayedExpansion

net session >nul 2>nul
if errorlevel 1 echo Run as Administrator! & pause & exit /b 1

echo Looking for USB drives...
powershell -NoProfile -NonInteractive -Command "Get-Disk | Where-Object {$_.BusType -eq 'USB'} | Format-Table Number,FriendlyName,@{n='GB';e={[math]::Round($_.Size/1GB,1)}} -AutoSize"

set "AUTO="
for /f "delims=" %%L in ('powershell -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "%~dp0Find-UsbDrive.ps1"') do set "AUTO=%%L"

set "TARGET="
if not "%AUTO%"=="" (
  echo Found single USB drive: %AUTO%:
  set "TARGET=%AUTO%:"
) else (
  set /P TARGET="Enter USB drive letter (e.g. E:): "
)
if "%TARGET%"=="" echo No drive selected. & exit /b 2
if /I "%TARGET%"=="C:" echo REFUSING system drive C:. & exit /b 10

echo Target USB drive: %TARGET% > "%~dp0DOS\TARGET.TXT"
echo Volume label: dos >> "%~dp0DOS\TARGET.TXT"
echo Inside this DOS session it is drive D: >> "%~dp0DOS\TARGET.TXT"
echo Starting DOS wizard...
call "%~dp0MSDOSBOOT.bat" /MENU %TARGET% dos ask
