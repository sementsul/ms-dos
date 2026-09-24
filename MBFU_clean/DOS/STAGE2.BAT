@ECHO Off
BEN Cls Blue
BEN FilledBox 10 5 70 20 LightGray LightGray 0
BEN Locate 12 6 / WriteC Yellow Blue MS-DOS~SETUP~FOR~USB~-~step~2
BEN Locate 10 23 / WriteC White Blue F1=Help~~~F3=Exit
Set S=%BEN%
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
BEN Locate 12 8 / WriteC Black LightGray Disk~ready.
BEN Locate 12 10 / WriteC Black LightGray MS-DOS~is~(c)~Microsoft.
BEN Locate 12 11 / WriteC Black LightGray You~must~own~a~license.
BEN Locate 12 12 / WriteC Black LightGray Norton~Commander~has~its~own~owner.
BEN Locate 12 14 / WriteC Black LightGray Accept~both~licenses?~(Y/N) / Ask YN / Sound 50 50
If Errorlevel 2 Goto Quit

:NCQ
BEN FilledBox 10 5 70 20 LightGray LightGray 0
BEN Locate 12 6 / WriteC Yellow Blue Install~Norton~Commander~4.0
BEN Locate 12 10 / WriteC Black LightGray Two-panel~file~manager,~the~classic~choice.
BEN Locate 12 12 / WriteC Black LightGray Install~NC?~(Y/N) / Ask YN
BEN Locate 10 23 / WriteC White Blue F1=Help~~~F3=Exit
If Errorlevel 2 Goto SkipNC
echo FORCE > FORCE_NC
Goto VERQ
:SkipNC
echo SKIP > SKIP_NC

:VERQ
BEN FilledBox 10 5 70 20 LightGray LightGray 0
BEN Locate 12 6 / WriteC Yellow Blue Which~MS-DOS~to~install?
BEN Locate 12 10 / WriteC Black LightGray 6.22~-~latest~classic~(recommended)
BEN Locate 12 11 / WriteC Black LightGray 5.00~-~lighter,~good~for~286
BEN Locate 12 13 / WriteC Black LightGray Install~6.22?~Y=6.22,~N=5.00 / Ask YN
BEN Locate 10 23 / WriteC White Blue F1=Help~~~F3=Exit
If Errorlevel 2 Goto Do5
msd6s.BAT
Goto End
:Do5
msd5s.BAT
Goto End

:BAD
TYPE E:\ERR.TXT
BEN Locate 12 14 / WriteC Black LightGray Back~to~menu?~Y=menu,~N=quit / Ask YN
BEN Locate 10 23 / WriteC White Blue F1=Help~~~F3=Exit
If Errorlevel 2 Goto Quit
ECHO BACK> E:\BACK.TXT
Goto End

:NORESULT
BEN FilledBox 10 5 70 20 LightGray LightGray 0
BEN Locate 12 6 / WriteC Yellow Blue MS-DOS~SETUP~FOR~USB~-~step~2
BEN Locate 12 10 / WriteC LightRed LightGray No~result~from~helper.
BEN Locate 12 12 / WriteC Black LightGray Restart~the~program.
BEN Locate 12 14 / WriteC Black LightGray Press~any~key...
pause > Nul
BEN Locate 10 23 / WriteC White Blue F1=Help~~~F3=Exit
Goto End

:Quit
ECHO QUIT> E:\REQUEST.TXT
:End
BEN CleanUp / Locate 1 25
exit
