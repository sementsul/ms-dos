@echo off
rem ============================================================
rem  MBFU - dskn.bat (cleaned version)
rem  Определяет буквы томов для \\.\PHYSICALDRIVE<N>
rem  и записывает их в temp.txt
rem  WMIC заменен на PowerShell Get-CimInstance
rem  (WMIC deprecated в Win10/11 и часто триггерит эвристику АВ)
rem  Использование: call dskn.bat <номер_диска 1..30>
rem ============================================================
setlocal EnableExtensions
set "disknum=%~1"
if "%disknum%"=="" echo Usage: dskn.bat ^<drive_number^>&2 & exit /b 2

where powershell.exe >nul 2>nul
if errorlevel 1 (
  echo PowerShell not found>&2
  exit /b 3
)

powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "%~dp0Get-UsbDrive.ps1" -DiskNumber %disknum% -OutFile "%~dp0temp.txt"
exit /b %ERRORLEVEL%
