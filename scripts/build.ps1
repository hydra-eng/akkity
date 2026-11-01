param([Parameter(Mandatory=$true)][string]$PayloadRoot,[string]$Python='python',[string]$ISCC='ISCC.exe')
$ErrorActionPreference='Stop'
$ProjectRoot=Split-Path $PSScriptRoot -Parent
Push-Location $ProjectRoot
try {
    & $Python -m PyInstaller --noconfirm --clean --windowed --onedir --name Akkity --icon app/akkity.ico --add-data 'app/spritesheet.png:.' --add-data 'app/akkity.ico:.' --add-data 'app/motion:motion' --hidden-import pystray._win32 --hidden-import pypdf app/akkity.py
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller failed' }
    Copy-Item -LiteralPath (Join-Path $PayloadRoot 'runtime') -Destination 'dist/Akkity/runtime' -Recurse -Force
    New-Item -ItemType Directory -Force 'dist/Akkity/models/blobs','dist/Akkity/licenses' | Out-Null
    $BlobName='sha256-2f8c3d137f2496dcb4019e17a50f2974b89c1be1a742db3c80cc86f91cafeeef'
    $ModelPath=Join-Path $PayloadRoot "models/blobs/$BlobName"
    if ((Get-FileHash -LiteralPath $ModelPath -Algorithm SHA256).Hash.ToLower() -ne $BlobName.Substring(7)) { throw 'Model checksum mismatch' }
    Copy-Item -LiteralPath $ModelPath -Destination 'dist/Akkity/models/blobs/'
    Copy-Item 'licenses/*' 'dist/Akkity/licenses/' -Force
    Copy-Item 'LICENSE','NOTICE.txt' 'dist/Akkity/' -Force
    & $ISCC scripts/installer.iss
    if ($LASTEXITCODE -ne 0) { throw 'Installer compilation failed' }
    $Installer=Get-Item releases/Akkity-Setup.exe
    $Hash=(Get-FileHash $Installer.FullName -Algorithm SHA256).Hash.ToLower()
    "$Hash  Akkity-Setup.exe" | Set-Content releases/SHA256SUMS.txt
    @{version='1.0.1';size=('{0:N0} MB' -f ($Installer.Length/1000000));sha256=$Hash} | ConvertTo-Json | Set-Content site/release.json
} finally { Pop-Location }
