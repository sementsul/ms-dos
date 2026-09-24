@ECHO Off
BEN Cls Blue
BEN FilledBox 10 5 70 20 LightGray LightGray 0
BEN Locate 11 6 / WriteC Yellow Blue ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
BEN Locate 31 6 / WriteC Yellow Blue MS-DOS~SETUP~FOR~USB
BEN Locate 12 8 / WriteC Black LightGray Welcome!~Everything~happens~here,~in~DOS.
BEN Locate 12 10 / WriteC Black LightGray MS-DOS~is~(c)~Microsoft.
BEN Locate 12 11 / WriteC Black LightGray You~must~own~a~license.
BEN Locate 12 12 / WriteC Black LightGray Norton~Commander~has~its~own~owner.
BEN Locate 10 23 / WriteC White Blue F1=Help~~~F3=Exit
SLEEP 3
SLEEP 3
SLEEP 3
SLEEP 3
IF EXIST E:\DRIVES.TXT GOTO SHOW
BEN Locate 12 12 / WriteC LightRed LightGray Helper~not~answering.~Restart~program.
BEN Locate 12 19 / WriteC Black LightGray Press~any~key...
pause > Nul
Goto End

:SHOW
IF EXIST E:\EMPTY.TXT GOTO NOFLASH
TYPE E:\DRIVES.TXT
Goto PICK1

:NOFLASH
BEN FilledBox 10 5 70 20 LightGray LightGray 0
BEN Locate 11 6 / WriteC Yellow Blue ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
BEN Locate 31 6 / WriteC Yellow Blue MS-DOS~SETUP~FOR~USB
BEN Locate 12 10 / WriteC LightRed LightGray NO~USB~FLASH~FOUND.
BEN Locate 12 12 / WriteC Black LightGray Insert~a~flash~drive~and~rescan.
BEN Locate 12 14 / WriteC Black LightGray Rescan?~Y=scan,~N=quit / Ask YN
BEN Locate 10 23 / WriteC White Blue F1=Help~~~F3=Exit
If Errorlevel 2 Goto Quit
DEL E:\DRIVES.TXT > Nul
DEL E:\EMPTY.TXT > Nul
ECHO SCAN> E:\REQUEST.TXT
BEN Locate 12 12 / WriteC Black LightGray Scanning...~window~will~restart.
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
BEN Locate 12 17 / WriteC Black LightGray Format~THIS~drive?~ALL~DATA~LOST!
BEN Locate 12 19 / WriteC Black LightGray Y=yes,~~N=next~drive / Ask YN
If Errorlevel 2 Goto PICK2
ECHO FORMAT 1> E:\REQUEST.TXT
Goto WORKING
:PICK2
IF NOT EXIST E:\D2.TXT GOTO NOMORE
TYPE E:\D2.TXT
BEN Locate 12 17 / WriteC Black LightGray Format~THIS~drive?~ALL~DATA~LOST!
BEN Locate 12 19 / WriteC Black LightGray Y=yes,~~N=next~drive / Ask YN
If Errorlevel 2 Goto PICK3
ECHO FORMAT 2> E:\REQUEST.TXT
Goto WORKING
:PICK3
IF NOT EXIST E:\D3.TXT GOTO NOMORE
TYPE E:\D3.TXT
BEN Locate 12 17 / WriteC Black LightGray Format~THIS~drive?~ALL~DATA~LOST!
BEN Locate 12 19 / WriteC Black LightGray Y=yes,~~N=next~drive / Ask YN
If Errorlevel 2 Goto PICK4
ECHO FORMAT 3> E:\REQUEST.TXT
Goto WORKING
:PICK4
IF NOT EXIST E:\D4.TXT GOTO NOMORE
TYPE E:\D4.TXT
BEN Locate 12 17 / WriteC Black LightGray Format~THIS~drive?~ALL~DATA~LOST!
BEN Locate 12 19 / WriteC Black LightGray Y=yes,~~N=next~drive / Ask YN
If Errorlevel 2 Goto NOMORE
ECHO FORMAT 4> E:\REQUEST.TXT
Goto WORKING
:NOMORE
BEN Locate 12 12 / WriteC Black LightGray No~more~drives.
BEN Locate 12 14 / WriteC Black LightGray Rescan?~Y=scan,~N=quit / Ask YN
If Errorlevel 2 Goto Quit
DEL E:\DRIVES.TXT > Nul
DEL E:\EMPTY.TXT > Nul
ECHO SCAN> E:\REQUEST.TXT
BEN Locate 12 12 / WriteC Black LightGray Scanning...~window~will~restart.
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
BEN FilledBox 10 5 70 20 LightGray LightGray 0
BEN Locate 11 6 / WriteC Yellow Blue ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
BEN Locate 31 6 / WriteC Yellow Blue MS-DOS~SETUP~FOR~USB
BEN Locate 12 12 / WriteC Black LightGray Working...~window~will~restart.
BEN Locate 12 14 / WriteC Black LightGray Do~NOT~remove~the~drive.
BEN Locate 10 23 / WriteC White Blue F1=Help~~~F3=Exit
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
