@ECHO Off
BEN Cls LightGray / GrowFilledBox 5 3 76 23 White Blue 1 / GetCD
Set S=%BEN%
BEN Locate 1 5 / WriteC Yellow Blue MS-DOS~SETUP~FOR~USB
BEN Locate 1 12 / WriteC White Blue Welcome!~Pick~a~USB~drive~below.
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
IF EXIST E:\DRIVES.TXT GOTO SHOW
BEN Locate 1 12 / WriteC LightRed Blue Helper~not~answering.~Restart~the~program.
BEN Locate 1 21 / WriteC Cyan LightBlue Press~any~key...
pause > Nul
Goto End

:SHOW
IF EXIST E:\EMPTY.TXT GOTO NOFLASH
TYPE E:\DRIVES.TXT
Goto PICK1

:NOFLASH
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightRed Blue NO~USB~FLASH~FOUND.
BEN Locate 1 14 / WriteC White Blue Insert~a~flash~drive~and~rescan.
BEN Locate 1 21 / WriteC Cyan LightBlue Rescan?~Y=scan,~N=quit / Ask YN
If Errorlevel 2 Goto Quit
DEL E:\DRIVES.TXT > Nul
DEL E:\EMPTY.TXT > Nul
ECHO SCAN> E:\REQUEST.TXT
BEN Locate 1 12 / WriteC LightCyan Blue Scanning...~window~will~restart.
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
Goto End

:PICK1
IF NOT EXIST E:\D1.TXT GOTO SHOW
TYPE E:\D1.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Format~THIS~drive?~ALL~DATA~LOST!~(Y/N) / Ask YN
If Errorlevel 2 Goto PICK2
ECHO FORMAT 1> E:\REQUEST.TXT
Goto WORKING
:PICK2
IF NOT EXIST E:\D2.TXT GOTO NOMORE
TYPE E:\D2.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Format~THIS~drive?~ALL~DATA~LOST!~(Y/N) / Ask YN
If Errorlevel 2 Goto PICK3
ECHO FORMAT 2> E:\REQUEST.TXT
Goto WORKING
:PICK3
IF NOT EXIST E:\D3.TXT GOTO NOMORE
TYPE E:\D3.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Format~THIS~drive?~ALL~DATA~LOST!~(Y/N) / Ask YN
If Errorlevel 2 Goto PICK4
ECHO FORMAT 3> E:\REQUEST.TXT
Goto WORKING
:PICK4
IF NOT EXIST E:\D4.TXT GOTO NOMORE
TYPE E:\D4.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Format~THIS~drive?~ALL~DATA~LOST!~(Y/N) / Ask YN
If Errorlevel 2 Goto NOMORE
ECHO FORMAT 4> E:\REQUEST.TXT
Goto WORKING
:NOMORE
BEN Locate 1 12 / WriteC White Blue No~more~drives.
BEN Locate 1 21 / WriteC Cyan LightBlue Rescan?~Y=scan,~N=quit / Ask YN
If Errorlevel 2 Goto Quit
DEL E:\DRIVES.TXT > Nul
DEL E:\EMPTY.TXT > Nul
ECHO SCAN> E:\REQUEST.TXT
BEN Locate 1 12 / WriteC LightCyan Blue Scanning...~window~will~restart.
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
Goto End

:WORKING
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightCyan Blue Working...~window~will~restart,~do~NOT~remove~drive.
BEN Locate 1 14 / WriteC White Blue If~stuck~here,~helper~died:~close~window,~restart~program.
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
SLEEP 5
Goto End

:Quit
ECHO QUIT> E:\REQUEST.TXT
:End
BEN CleanUp / Locate 1 25
exit
