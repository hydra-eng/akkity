[Setup]
AppId={{B4A07DA9-2434-4AE3-9F30-9FC694244F66}
AppName=Akkity
AppVersion=1.0.4
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

[Code]
var
  PersonalPage: TWizardPage;
  UserNameEdit: TNewEdit;
  AnimationsCheck: TNewCheckBox;
  IdleActionsCheck: TNewCheckBox;
  TapAnimationsCheck: TNewCheckBox;
  DoubleActionCombo: TNewComboBox;
  TripleActionCombo: TNewComboBox;

function SettingsPath: String;
begin
  Result := AddBackslash(GetEnv('LOCALAPPDATA')) + 'Akkity\settings.json';
end;

function JsonEscape(Value: String): String;
begin
  Result := Value;
  StringChangeEx(Result, '\', '\\', True);
  StringChangeEx(Result, '"', '\"', True);
  StringChangeEx(Result, #13, ' ', True);
  StringChangeEx(Result, #10, ' ', True);
  StringChangeEx(Result, #9, ' ', True);
end;

function JsonBoolean(Value: Boolean): String;
begin
  if Value then Result := 'true' else Result := 'false';
end;

function SelectedAction(Combo: TNewComboBox): String;
begin
  case Combo.ItemIndex of
    1: Result := 'jump';
    2: Result := 'wave';
    3: Result := 'left';
    4: Result := 'right';
    5: Result := 'review';
    6: Result := 'special';
  else
    Result := 'none';
  end;
end;

procedure AddPersonalLabel(Parent: TWinControl; Caption: String; Top: Integer; Size: Integer; Color: TColor; Bold: Boolean);
var
  LabelControl: TNewStaticText;
begin
  LabelControl := TNewStaticText.Create(PersonalPage);
  LabelControl.Parent := Parent;
  LabelControl.Left := 0;
  LabelControl.Top := Top;
  LabelControl.Width := Parent.Width;
  LabelControl.Caption := Caption;
  LabelControl.Font.Size := Size;
  LabelControl.Font.Color := Color;
  if Bold then LabelControl.Font.Style := [fsBold];
end;

procedure InitializeWizard;
var
  Surface: TNewNotebookPage;
  AccentColor: TColor;
begin
  AccentColor := $004850FF;
  PersonalPage := CreateCustomPage(wpLicense, 'Make Akkity yours', 'A little name, a few tiny choices, your own little desktop cat.');
  Surface := PersonalPage.Surface;
  Surface.Color := $00FFF5DC;
  AddPersonalLabel(Surface, 'A LITTLE PERSONALIZATION PARTY', 4, 9, AccentColor, True);
  AddPersonalLabel(Surface, 'What should Akkity call you?', 29, 13, $0024231F, True);
  UserNameEdit := TNewEdit.Create(PersonalPage);
  UserNameEdit.Parent := Surface;
  UserNameEdit.Left := 0;
  UserNameEdit.Top := 52;
  UserNameEdit.Width := Surface.Width;
  UserNameEdit.Text := '';
  AddPersonalLabel(Surface, 'Optional · leave blank if you prefer · stays on this computer', 79, 8, $005D584D, False);
  AnimationsCheck := TNewCheckBox.Create(PersonalPage);
  AnimationsCheck.Parent := Surface;
  AnimationsCheck.Left := 0;
  AnimationsCheck.Top := 106;
  AnimationsCheck.Width := Surface.Width;
  AnimationsCheck.Caption := 'Keep Akkity’s animations on';
  AnimationsCheck.Checked := True;
  IdleActionsCheck := TNewCheckBox.Create(PersonalPage);
  IdleActionsCheck.Parent := Surface;
  IdleActionsCheck.Left := 0;
  IdleActionsCheck.Top := 132;
  IdleActionsCheck.Width := Surface.Width;
  IdleActionsCheck.Caption := 'Let Akkity wander and do idle antics';
  IdleActionsCheck.Checked := True;
  TapAnimationsCheck := TNewCheckBox.Create(PersonalPage);
  TapAnimationsCheck.Parent := Surface;
  TapAnimationsCheck.Left := 0;
  TapAnimationsCheck.Top := 158;
  TapAnimationsCheck.Width := Surface.Width;
  TapAnimationsCheck.Caption := 'Animate double- and triple-tap actions';
  TapAnimationsCheck.Checked := True;
  AddPersonalLabel(Surface, 'DOUBLE-TAP MOVE', 190, 8, AccentColor, True);
  DoubleActionCombo := TNewComboBox.Create(PersonalPage);
  DoubleActionCombo.Parent := Surface;
  DoubleActionCombo.Left := 0;
  DoubleActionCombo.Top := 209;
  DoubleActionCombo.Width := Surface.Width;
  DoubleActionCombo.Style := csDropDownList;
  DoubleActionCombo.Items.Add('Off');
  DoubleActionCombo.Items.Add('Jump');
  DoubleActionCombo.Items.Add('Wave');
  DoubleActionCombo.Items.Add('Walk left');
  DoubleActionCombo.Items.Add('Walk right');
  DoubleActionCombo.Items.Add('Look thoughtful');
  DoubleActionCombo.Items.Add('Little celebration');
  DoubleActionCombo.ItemIndex := 1;
  AddPersonalLabel(Surface, 'TRIPLE-TAP MOVE', 240, 8, AccentColor, True);
  TripleActionCombo := TNewComboBox.Create(PersonalPage);
  TripleActionCombo.Parent := Surface;
  TripleActionCombo.Left := 0;
  TripleActionCombo.Top := 259;
  TripleActionCombo.Width := Surface.Width;
  TripleActionCombo.Style := csDropDownList;
  TripleActionCombo.Items.Add('Off');
  TripleActionCombo.Items.Add('Jump');
  TripleActionCombo.Items.Add('Wave');
  TripleActionCombo.Items.Add('Walk left');
  TripleActionCombo.Items.Add('Walk right');
  TripleActionCombo.Items.Add('Look thoughtful');
  TripleActionCombo.Items.Add('Little celebration');
  TripleActionCombo.ItemIndex := 6;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := (PageID = PersonalPage.ID) and FileExists(SettingsPath());
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  Json: String;
  FileName: String;
begin
  if (CurStep = ssPostInstall) and not FileExists(SettingsPath()) then begin
    ForceDirectories(ExtractFileDir(SettingsPath()));
    Json := '{"user_name":"' + JsonEscape(Trim(UserNameEdit.Text)) +
      '","animations_enabled":' + JsonBoolean(AnimationsCheck.Checked) +
      ',"autonomous":' + JsonBoolean(IdleActionsCheck.Checked) +
      ',"tap_animations":' + JsonBoolean(TapAnimationsCheck.Checked) +
      ',"double":"' + SelectedAction(DoubleActionCombo) +
      '","triple":"' + SelectedAction(TripleActionCombo) + '"}';
    FileName := SettingsPath();
    SaveStringToFile(FileName, UTF8Encode(Json), False);
  end;
end;
