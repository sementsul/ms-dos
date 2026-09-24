@ECHO Off
BEN Cls LightGray / GrowFilledBox 5 3 76 23 White Blue 1 / GetCD
Set S=%BEN%
BEN Locate 1 5 / WriteC Yellow Blue MS-DOS~SETUP~FOR~USB~-~step~2
IF EXIST E:\ERR.TXT GOTO BAD
IF NOT EXIST E:\OK.TXT GOTO NORESULT
DEL E:\OK.TXT > Nul
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

:BAD
TYPE E:\ERR.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Back~to~menu?~Y=menu,~N=quit / Ask YN
If Errorlevel 2 Goto Quit
ECHO BACK> E:\BACK.TXT
Goto End

:NORESULT
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightRed Blue No~result~from~helper.~Restart~program.
BEN Locate 1 21 / WriteC Cyan LightBlue Press~any~key...
pause > Nul
Goto End

:Quit
ECHO QUIT> E:\REQUEST.TXT
:End
BEN CleanUp / Locate 1 25
exit
