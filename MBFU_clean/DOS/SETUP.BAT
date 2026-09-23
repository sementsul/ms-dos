@ECHO Off
BEN Cls LightGray / GrowFilledBox 5 3 76 23 White Blue 1 / GetCD
Set S=%BEN%
BEN Locate 1 5 / WriteC Yellow Blue MS-DOS~SETUP~FOR~USB
BEN Locate 1 12 / WriteC White Blue Welcome!~Pick~a~USB~drive~below.
SLEEP 3
SLEEP 3
IF EXIST E:\DRIVES.TXT GOTO SHOW
BEN Locate 1 12 / WriteC LightRed Blue Helper~not~answering.~Check~Windows~side.
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
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
IF EXIST E:\DRIVES.TXT GOTO SHOW
BEN Locate 1 12 / WriteC LightRed Blue Still~nothing.~Check~Windows~side.
BEN Locate 1 21 / WriteC Cyan LightBlue Menu?~Y=menu,~N=quit / Ask YN
If Errorlevel 2 Goto Quit
Goto SHOW

:PICK1
IF NOT EXIST E:\D1.TXT GOTO SHOW
TYPE E:\D1.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Format~THIS~drive?~ALL~DATA~LOST!~(Y/N) / Ask YN
If Errorlevel 2 Goto PICK2
ECHO FORMAT 1> E:\REQUEST.TXT
Goto DOFORMAT
:PICK2
IF NOT EXIST E:\D2.TXT GOTO NOMORE
TYPE E:\D2.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Format~THIS~drive?~ALL~DATA~LOST!~(Y/N) / Ask YN
If Errorlevel 2 Goto PICK3
ECHO FORMAT 2> E:\REQUEST.TXT
Goto DOFORMAT
:PICK3
IF NOT EXIST E:\D3.TXT GOTO NOMORE
TYPE E:\D3.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Format~THIS~drive?~ALL~DATA~LOST!~(Y/N) / Ask YN
If Errorlevel 2 Goto PICK4
ECHO FORMAT 3> E:\REQUEST.TXT
Goto DOFORMAT
:PICK4
IF NOT EXIST E:\D4.TXT GOTO NOMORE
TYPE E:\D4.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Format~THIS~drive?~ALL~DATA~LOST!~(Y/N) / Ask YN
If Errorlevel 2 Goto NOMORE
ECHO FORMAT 4> E:\REQUEST.TXT
Goto DOFORMAT
:NOMORE
BEN Locate 1 12 / WriteC White Blue No~more~drives.
BEN Locate 1 21 / WriteC Cyan LightBlue Rescan?~Y=scan,~N=quit / Ask YN
If Errorlevel 2 Goto Quit
DEL E:\DRIVES.TXT > Nul
DEL E:\EMPTY.TXT > Nul
ECHO SCAN> E:\REQUEST.TXT
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
Goto SHOW

:DOFORMAT
DEL E:\OK.TXT > Nul
DEL E:\ERR.TXT > Nul
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightCyan Blue Formatting...~do~NOT~remove~the~drive.
:WFMT
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
IF EXIST E:\OK.TXT GOTO GOTFMT
IF EXIST E:\ERR.TXT GOTO BADFMT
BEN Locate 1 21 / WriteC Cyan LightBlue Still~working.~Wait~more?~(Y/N) / Ask YN
If Errorlevel 2 Goto SHOW
Goto WFMT
:BADFMT
TYPE E:\ERR.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Back~to~menu?~(Y/N) / Ask YN
If Errorlevel 2 Goto Quit
Goto SHOW

:GOTFMT
IF EXIST E:\USE_A.TXT MOUNT D A:\ > Nul
IF EXIST E:\USE_B.TXT MOUNT D B:\ > Nul
IF EXIST E:\USE_C.TXT MOUNT D C:\ > Nul
IF EXIST E:\USE_D.TXT MOUNT D D:\ > Nul
IF EXIST E:\USE_E.TXT MOUNT D E:\ > Nul
IF EXIST E:\USE_F.TXT MOUNT D F:\ > Nul
IF EXIST E:\USE_G.TXT MOUNT D G:\ > Nul
IF EXIST E:\USE_H.TXT MOUNT D H:\ > Nul
IF EXIST E:\USE_I.TXT MOUNT D I:\ > Nul
IF EXIST E:\USE_J.TXT MOUNT D J:\ > Nul
IF EXIST E:\USE_K.TXT MOUNT D K:\ > Nul
IF EXIST E:\USE_L.TXT MOUNT D L:\ > Nul
IF EXIST E:\USE_M.TXT MOUNT D M:\ > Nul
IF EXIST E:\USE_N.TXT MOUNT D N:\ > Nul
IF EXIST E:\USE_O.TXT MOUNT D O:\ > Nul
IF EXIST E:\USE_P.TXT MOUNT D P:\ > Nul
IF EXIST E:\USE_Q.TXT MOUNT D Q:\ > Nul
IF EXIST E:\USE_R.TXT MOUNT D R:\ > Nul
IF EXIST E:\USE_S.TXT MOUNT D S:\ > Nul
IF EXIST E:\USE_T.TXT MOUNT D T:\ > Nul
IF EXIST E:\USE_U.TXT MOUNT D U:\ > Nul
IF EXIST E:\USE_V.TXT MOUNT D V:\ > Nul
IF EXIST E:\USE_W.TXT MOUNT D W:\ > Nul
IF EXIST E:\USE_X.TXT MOUNT D X:\ > Nul
IF EXIST E:\USE_Y.TXT MOUNT D Y:\ > Nul
IF EXIST E:\USE_Z.TXT MOUNT D Z:\ > Nul
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightGreen Blue Disk~ready.
BEN Locate 1 14 / WriteC White Blue MS-DOS~is~(c)~Microsoft.~You~must~own~a~license.
BEN Locate 1 15 / WriteC White Blue Norton~Commander~has~its~own~owner.~License~needed.
BEN Locate 1 21 / WriteC Cyan LightBlue Accept~both~licenses?~(Y/N) / Ask YN / Sound 50 50
If Errorlevel 2 Goto Quit

:NCQ
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightCyan Blue Install~Norton~Commander~4.0?
BEN Locate 1 21 / WriteC Cyan LightBlue Install~NC?~(Y/N) / Ask YN
If Errorlevel 2 Goto SkipNC
echo FORCE > FORCE_NC
Goto VERQ
:SkipNC
echo SKIP > SKIP_NC

:VERQ
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightCyan Blue Which~MS-DOS?
BEN Locate 1 15 / WriteC White Blue 6.22~-~latest~classic~(recommended)
BEN Locate 1 16 / WriteC White Blue 5.00~-~lighter,~good~for~286
BEN Locate 1 21 / WriteC Cyan LightBlue Install~6.22?~Y=6.22,~N=5.00 / Ask YN
If Errorlevel 2 Goto Do5
msd6s.BAT
Goto End
:Do5
msd5s.BAT
Goto End

:Quit
ECHO QUIT> E:\REQUEST.TXT
:End
BEN CleanUp / Locate 1 25
exit
