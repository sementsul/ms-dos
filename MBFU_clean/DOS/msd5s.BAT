@ECHO Off
BEN Cls LightGray / GrowFilledBox 5 3 76 23 White Blue 1 / GetCD
Set S=%BEN%
Set drive=d:

BEN Locate 1 5 / WriteC Yellow Blue MS-DOS~5.00~FOR~USB~SETUP
BEN Locate 1 12 / WriteC White Blue This~program~will~install~MS-DOS~5.00~on~your~USB~media
BEN Locate 1 13 / WriteC White Blue The~author~of~the~program~Sementsul~Maxim~2025.~HTTPS:\\WWW.MICROSOFT.COM
BEN Locate 1 21 / WriteC Cyan LightBlue Do~you~want~to~continue?~(Y/N) / Ask YN / Sound 50 50
If Errorlevel 2 Goto CloseDown


:Core

BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightGreen Blue Please~wait~while~INSTALL~is~copying~files~;


Goto cdOK

:cdOK
Copy sourcr\MSDOS5\*.* %drive% > Nul





BEN FilledBox 6 12 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightCyan Blue Install~Norton~Commander
If Exist SKIP_NC Goto Read
If Exist FORCE_NC Goto DoNC
BEN Locate 1 15 / WriteC White Blue NC~Ver~4.0 / Locate 1 18 / WriteC LightRed Blue ?
BEN Locate 1 21 / WriteC Cyan LightBlue Press~press~Y~or~N. / Ask YN
If Errorlevel 2 goto Read
:DoNC
md %drive%\nc > Nul
Copy sourcr\NC\*.* %drive%\nc\ > Nul
echo NC\NC.EXE >> %drive%\AUTOEXEC.BAT

:Read
BEN Beep / FilledBox 6 12 75 21 Blue Blue 0 / Locate 1 12 / WriteC White Blue The~installation~process~is~completed.
BEN Locate 1 21 / WriteC Cyan LightBlue Do~you~want~to~read~the~README~file?~(Y/N) / Ask YN
If Errorlevel 2 Goto LastMessage
BEN List README README~(Press~ESC~to~quit)

:LastMessage
BEN FilledBox 6 13 75 21 Blue Blue 0 / Locate 1 12 / WriteC White Blue Thank~you~for~using~the~the~program~MBFU.
BEN Locate 1 14 / WriteC LightMagenta Blue The~author~of~the~program~Sementsul~Maxim~2025.
BEN Locate 1 15  / WriteC LightMagenta Blue MS-DOS~licensing:~WWW.MICROSOFT.COM
BEN Locate 1 17 / WriteC LightRed LightBlue Thank~you!
pause
:CloseDown
BEN CleanUp / Locate 1 25
exit
