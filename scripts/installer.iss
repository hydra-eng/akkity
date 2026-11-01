[Setup]
AppId={{B4A07DA9-2434-4AE3-9F30-9FC694244F66}
AppName=Akkity
AppVersion=1.0.3
AppPublisher=Akkity
AppPublisherURL=https://akkity.web.app
DefaultDirName={localappdata}\Programs\Akkity
DefaultGroupName=Akkity
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
DisableProgramGroupPage=yes
DisableDirPage=yes
DisableWelcomePage=yes
LicenseFile=..\licenses\DISTRIBUTION-TERMS.txt
OutputDir=..\releases
OutputBaseFilename=Akkity-Setup
SetupIconFile=..\app\akkity.ico
UninstallDisplayIcon={app}\Akkity.exe
Compression=lzma2/fast
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes
RestartApplications=no

[Files]
Source: "..\dist\Akkity\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\Akkity"; Filename: "{app}\Akkity.exe"; Comment: "Your offline desktop cat companion"
Name: "{autodesktop}\Akkity"; Filename: "{app}\Akkity.exe"; HotKey: "ctrl+alt+a"

[Run]
Filename: "{app}\Akkity.exe"; Description: "Meet Akkity"; Flags: nowait postinstall skipifsilent
