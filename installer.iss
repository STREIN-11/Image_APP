[Setup]
AppName=Reddit Image Downloader
AppVersion=1.0
AppPublisher=HAVI
DefaultDirName={autopf}\RedditImageDownloader
DefaultGroupName=Reddit Image Downloader
OutputDir=installer
OutputBaseFilename=RedditImageDownloader_Setup
SetupIconFile=HAVI.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\RedditImageDownloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Reddit Image Downloader"; Filename: "{app}\RedditImageDownloader.exe"
Name: "{group}\Uninstall Reddit Image Downloader"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Reddit Image Downloader"; Filename: "{app}\RedditImageDownloader.exe"

[Run]
Filename: "{app}\RedditImageDownloader.exe"; Description: "Launch Reddit Image Downloader"; Flags: nowait postinstall skipifsilent
