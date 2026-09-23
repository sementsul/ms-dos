; MBFU 1.3.0 — Inno Setup скрипт
; Сборка: Inno Setup 6.x -> открыть этот .iss -> Compile.
; На установке принимается ОБЪЕДИНЕННАЯ лицензия (MS-DOS + NC),
; факты принятия пишутся в %ProgramData%\MBFU, чтобы GUI их видел
; и не спрашивал повторно.
#define MyAppName "MS-DOS Boot From USB (MBFU)"
#define MyAppVersion "1.3.0"
#define MyAppPublisher "Sementsul Maxim"
#define MyAppURL "https://www.microsoft.com/"
#define SrcDir "MBFU_clean"

[Setup]
AppId={{3E8B0F2A-7C1A-4B2E-9F3A-MBFU130FINAL}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\MBFU
DefaultGroupName=MBFU
OutputDir=..
OutputBaseFilename=MBFU-1.3.0-setup
SetupIconFile=MBFU.ico
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
LicenseFile={#SrcDir}\LICENSE-SETUP-RU.txt
VersionInfoVersion=1.3.0.0
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Utility for creating MS-DOS 5.0/6.22 bootable USB drives
VersionInfoCopyright=(c) 2025 Sementsul Maxim
WizardStyle=modern
; НЕ ставить Password/Encryption — иначе детект как cryptor
; НЕ упаковывать Output UPX-ом

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: desktopicon; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Автономный GUI-EXE (PyInstaller, Python/установка не нужны).
; MBFU_GUI.py оставлен рядом как исходник для прозрачности.
Source: "{#SrcDir}\MBFU_GUI.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\MBFU_GUI.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\MBFU.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\LICENSE-MS-DOS-RU.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\LICENSE-NC-RU.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\LICENSE-SETUP-RU.txt"; DestDir: "{app}"; Flags: ignoreversion
; бэкенд
Source: "{#SrcDir}\MSDOSBOOT.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\dskn.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\Get-UsbDrive.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\MSDOSBOOT.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\MSDOSBOOT.exe.manifest"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\dosbox.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\SDL.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\SDL_net.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\cfg.conf"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SrcDir}\DOS\*"; DestDir: "{app}\DOS"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Автономный EXE — никаких Python/доп. программ на ПК пользователя.
; EXE сам запрашивает права администратора (UAC-манифест внутри).
Name: "{group}\MBFU — графический интерфейс"; Filename: "{app}\MBFU_GUI.exe"; WorkingDir: "{app}"; Comment: "Создание загрузочной флешки MS-DOS (GUI)"
Name: "{group}\MBFU — командная строка"; Filename: "{app}\MSDOSBOOT.bat"; WorkingDir: "{app}"; Comment: "MSDOSBOOT.bat /MSD5 E: или /MSD6 E: [метка]"
Name: "{group}\MS-DOS SETUP FOR USB"; Filename: "{app}\MBFU_GUI.exe"; Parameters: "--setup"; WorkingDir: "{app}"; Comment: "Выбор флешки и установка полностью в DOS-окне"
Name: "{group}\Лицензия MS-DOS"; Filename: "notepad.exe"; Parameters: """{app}\LICENSE-MS-DOS-RU.txt"""; WorkingDir: "{app}"
Name: "{group}\Лицензия Norton Commander"; Filename: "notepad.exe"; Parameters: """{app}\LICENSE-NC-RU.txt"""; WorkingDir: "{app}"
Name: "{group}\Удалить MBFU"; Filename: "{uninstallexe}"
Name: "{autodesktop}\MBFU"; Filename: "{app}\MBFU_GUI.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\MBFU_GUI.exe"; WorkingDir: "{app}"; Flags: postinstall skipifsilent shellexec runascurrentuser; Description: "Запустить MBFU GUI после установки"

[UninstallDelete]
Type: files; Name: "{commonappdata}\MBFU\license_accepted.json"
Type: files; Name: "{commonappdata}\MBFU\nc_license_accepted.json"

[Code]
{ Версии ниже — строго ASCII и должны совпадать с LICENSE_VERSION /
  NC_LICENSE_VERSION в MBFU_GUI.py. Кириллицу сюда нельзя:
  SaveStringToFile пишет в ANSI системной кодировки и GUI такой
  файл не признает. }
const
  LicenseVer = '1.0-2026-09-22';
  NcLicenseVer = '1.0-2026-09-22';

procedure WriteAccept(const Dir, Name, Ver: string);
var
  Json: string;
begin
  Json := '{' + #13#10 +
    '  "accepted": true,' + #13#10 +
    '  "license_version": "' + Ver + '",' + #13#10 +
    '  "app_version": "{#MyAppVersion}",' + #13#10 +
    '  "date": "installer",' + #13#10 +
    '  "source": "innosetup-license-page"' + #13#10 +
    '}';
  SaveStringToFile(Dir + '\' + Name, Json, False);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  Dir: string;
begin
  { До сюда доходят только после принятия объединенной лицензии }
  if CurStep = ssPostInstall then
  begin
    Dir := ExpandConstant('{commonappdata}\MBFU');
    ForceDirectories(Dir);
    WriteAccept(Dir, 'license_accepted.json', LicenseVer);
    WriteAccept(Dir, 'nc_license_accepted.json', NcLicenseVer);
  end;
end;
