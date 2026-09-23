@echo off
rem MBFU - создание загрузочной флешки MS-DOS 5.00 / 6.22
rem
rem  Использование:
rem    MSDOSBOOT.bat /MSD5 E: [метка] [NC]
rem    MSDOSBOOT.bat /MSD6 E: [метка] [NC]
rem    MSDOSBOOT.bat /MENU E: [метка] [NC] - DOS-мастер (Retro Edition)
rem  где E: - буква целевой USB-флешки (только буква с двоеточием!)
rem  метка - необязательно, латиница до 11 символов (по умолч. dos).
rem  NC    - программы для DOS: 1 = ставить Norton Commander без вопросов,
rem          0 = не ставить, пусто = спросить внутри установщика.
rem          По умолчанию (из GUI) - ставить.
rem  GUI передает метку и NC автоматически.
rem  Запускать с правами администратора.
setlocal EnableExtensions EnableDelayedExpansion

set "MODE=%~1"
set "TARGET=%~2"
set "VOLLABEL=%~3"
if "%VOLLABEL%"=="" set "VOLLABEL=dos"
set "NCFLAG=%~4"
if "%NCFLAG%"=="" set "NCFLAG=ask"

echo MBFU MS-DOS Boot From USB
echo Mode=%MODE% Target=%TARGET% Label=%VOLLABEL% NC=%NCFLAG%

if "%MODE%"=="" goto usage
if "%TARGET%"=="" goto usage
if /I "%MODE%"=="/MSD5" goto check_target
if /I "%MODE%"=="/MSD6" goto check_target
if /I "%MODE%"=="/MENU" goto check_target
if /I "%MODE%"=="/HELP" goto usage
if /I "%MODE%"=="/?" goto usage
echo Unknown mode "%MODE%". Expected /MSD5 or /MSD6.
goto usage

:check_target
rem --- грубая защита от записи на системный диск C: ---
if /I "%TARGET%"=="C:" echo REFUSING to write to system drive C: ! & exit /b 10
if /I "%TARGET%"=="C:\ " echo REFUSING to write to system drive C: ! & exit /b 10

echo Test > "%TARGET%\tdd.txt" 2>nul
if errorlevel 1 (
  echo Cannot write to %TARGET% - check drive letter and admin rights.
  exit /b 11
)

echo Testing disk, and installing MBR...
find "Test" < "%TARGET%\tdd.txt" >nul || (
  echo Disk write test failed for %TARGET%.
  exit /b 12
)
del "%TARGET%\tdd.txt" >nul 2>nul

rem --- найти номер PHYSICALDRIVE по букве тома ---
set "FOUND_DRIVE="
for /L %%N in (1,1,30) do (
  if not defined FOUND_DRIVE (
    call "%~dp0dskn.bat" %%N >nul 2>nul
    findstr /I /C:"%TARGET%" "%~dp0temp.txt" >nul 2>nul
    if not errorlevel 1 (
      set "FOUND_DRIVE=%%N"
    )
  )
)

if not defined FOUND_DRIVE (
  echo Disk error: cannot map %TARGET% to PHYSICALDRIVE number.
  echo Make sure the USB drive is inserted and visible in Explorer.
  exit /b 13
)

echo Found %TARGET% = PHYSICALDRIVE!FOUND_DRIVE!
echo Installing MBR / partitioning via RMPARTUSB backend...
"%~dp0MSDOSBOOT.exe" DRIVE=!FOUND_DRIVE! MSDOS CHS VOLUME %VOLLABEL%
if errorlevel 1 (
  echo MSDOSBOOT.exe failed with code %ERRORLEVEL%.
  exit /b %ERRORLEVEL%
)

echo Copying files via DOSBox...
rem --- выбор программ для DOS: флаг-файлы видит DOSBox как C:\ ---
del "%~dp0DOS\SKIP_NC" >nul 2>nul
del "%~dp0DOS\FORCE_NC" >nul 2>nul
if /I "%NCFLAG%"=="0" echo skip > "%~dp0DOS\SKIP_NC"
if /I "%NCFLAG%"=="1" echo force > "%~dp0DOS\FORCE_NC"
copy /Y "%~dp0cfg.conf" "%~dp0dosbox.conf" >nul
echo mount d %TARGET%\>> "%~dp0dosbox.conf"
if /I "%MODE%"=="/MSD5" "%~dp0dosbox.exe" -conf "%~dp0dosbox.conf" "DOS\msd5s.BAT"
if /I "%MODE%"=="/MSD6" "%~dp0dosbox.exe" -conf "%~dp0dosbox.conf" "DOS\msd6s.BAT"
if /I "%MODE%"=="/MENU" "%~dp0dosbox.exe" -conf "%~dp0dosbox.conf" "DOS\MENU.BAT"
if errorlevel 1 (
  echo DOSBox file-copy stage failed with code %ERRORLEVEL%.
  del "%~dp0DOS\SKIP_NC" >nul 2>nul
  del "%~dp0DOS\FORCE_NC" >nul 2>nul
  exit /b %ERRORLEVEL%
)
del "%~dp0DOS\SKIP_NC" >nul 2>nul
del "%~dp0DOS\FORCE_NC" >nul 2>nul

echo.
echo Done. USB %TARGET% (%MODE%) ready. You can safely remove it.
exit /b 0

:usage
echo Usage:
echo   MSDOSBOOT.bat /MSD5 E: [label] [NC]
echo   MSDOSBOOT.bat /MSD6 E: [label] [NC]
echo   MSDOSBOOT.bat /MENU E: [label] [NC] - DOS wizard (Retro Edition)
echo.
echo   /MSD5 - install MS-DOS 5.00, /MSD6 - install MS-DOS 6.22
echo   /MENU - ask version and NC inside DOSBox
echo   E:    - target USB drive letter (must exist, must NOT be C:)
echo   label - optional volume label, A-Z 0-9, default dos
echo   NC    - 1 install Norton Commander, 0 skip, empty ask inside
echo   Run as Administrator.
exit /b 2
