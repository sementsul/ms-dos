@ECHO Off
BEN Cls LightGray / GrowFilledBox 5 3 76 23 White Blue 1 / GetCD
Set S=%BEN%
BEN Locate 1 5 / WriteC Yellow Blue MBFU~RETRO~-~MS-DOS~USB~SETUP
BEN Locate 1 12 / WriteC White Blue Welcome!~Everything~happens~here,~in~DOS.
BEN Locate 1 14 / WriteC White Blue MS-DOS~is~(c)~Microsoft.~You~must~own~a~license.
BEN Locate 1 15 / WriteC White Blue Norton~Commander~has~its~own~owner.~License~needed.
BEN Locate 1 21 / WriteC Cyan LightBlue Accept~both~licenses?~(Y/N) / Ask YN / Sound 50 50
If Errorlevel 2 Goto Bye

:NC
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightCyan Blue Install~Norton~Commander~4.0?
BEN Locate 1 15 / WriteC White Blue Two-panel~file~manager,~the~classic~choice.
BEN Locate 1 21 / WriteC Cyan LightBlue Install~NC?~(Y/N) / Ask YN
If Errorlevel 2 Goto SkipNC
echo FORCE > FORCE_NC
Goto Ver
:SkipNC
echo SKIP > SKIP_NC

:Ver
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightCyan Blue Which~MS-DOS~to~install?
BEN Locate 1 15 / WriteC White Blue 6.22~-~latest~classic~(recommended)
BEN Locate 1 16 / WriteC White Blue 5.00~-~lighter,~good~for~286
BEN Locate 1 21 / WriteC Cyan LightBlue Install~6.22?~Y=6.22,~N=5.00 / Ask YN
If Errorlevel 2 Goto Do5
Goto Do6

:Do6
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightCyan Blue Target~drive:
TYPE TARGET.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Start~install~of~MS-DOS~6.22?~(Y/N) / Ask YN
If Errorlevel 2 Goto Bye
msd6s.BAT
Goto End

:Do5
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightCyan Blue Target~drive:
TYPE TARGET.TXT
BEN Locate 1 21 / WriteC Cyan LightBlue Start~install~of~MS-DOS~5.00?~(Y/N) / Ask YN
If Errorlevel 2 Goto Bye
msd5s.BAT
Goto End

:Bye
BEN FilledBox 6 11 75 21 Blue Blue 0 / Locate 1 12 / WriteC LightRed Blue Bye!~No~changes~made.
BEN Locate 1 21 / WriteC Cyan LightBlue Press~any~key...
pause > Nul
:End
BEN CleanUp / Locate 1 25
exit
