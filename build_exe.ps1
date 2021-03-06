<#
.NOTES
	Author:	Viesturs Skila
	Version: 1.0.3
#>
[CmdletBinding()] 
param (
    [Parameter(Position = 0, Mandatory = $true)]
    [ValidateScript( {
            if ( -NOT ( $_ | Test-Path -PathType Leaf) ) {
                Write-Host "File does not exist"
                throw
            }#endif
            if ( $_ -notmatch ".py") {
                Write-Host "The file specified in the path argument must be Python script file"
                throw
            }#endif
            return $True
        } ) ]
    [System.IO.FileInfo]
    $FileName,
    [Parameter(Position = 1, Mandatory = $true)]
    [string]
    $Major,
    [Parameter(Position = 2, Mandatory = $true)]
    [string]
    $Minor,
    [Parameter(Position = 3, Mandatory = $true)]
    [string]
    $Patch
)

# Atrodam scripta darba direktoriju
#$__ScriptName = $MyInvocation.MyCommand
$__ScriptPath = Split-Path (Get-Variable MyInvocation -Scope Script).Value.Mycommand.Definition -Parent

# Ielasām datņu objektus
$File = Get-ChildItem -Path $FileName
$IconFile = Get-ChildItem -Path ".\erj-logo.ico"

#Izveidojam versijas datnes ceļu un nosaukumu
$VersionFile = "$__ScriptPath\GrabVersion.ini"

# Izveidojam brūvējuma numuru
$buildNumber = "$(Get-Date -Format "yMMddHHmmss")"

# Aizpildām komilācijas versijas datnei nepeiciešamos mainīgos
$CompanyName = "Viesturs Šķila"
$FileDescription = "Helper for admins"
$FileVersion = "$Major.$Minor.$Patch.$buildNumber"
$InternalName = "ExpoRemoteJobGUI"
$OriginalFilename = "$($File.BaseName)$($File.Extension)"
$ProductName = "RemoteJobGUI"
$ProductVersion = "$Major.$Minor.$Patch.$buildNumber"

# Izveidojam komilācijas versijas datnes saturu
$verFileBody = @"
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
filevers=($Major, $Minor, $Patch, $buildNumber),
prodvers=($Major, $Minor, $Patch, $buildNumber),
# Contains a bitmask that specifies the valid bits 'flags'r
mask=0x3f,
# Contains a bitmask that specifies the Boolean attributes of the file.
flags=0x0,
# The operating system for which this file was designed.
# 0x4 - NT and there is no need to change it.
OS=0x4,
# The general type of file.
# 0x1 - the file is an application.
fileType=0x1,
# The function of the file.
# 0x0 - the function is not defined for this fileType
subtype=0x0,
# Creation date and time stamp.
date=(0, 0)
),
  kids=[
StringFileInfo(
  [
  StringTable(
    u'040904B0',
    [StringStruct(u'CompanyName', u'$CompanyName'),
    StringStruct(u'FileDescription', u'$FileDescription'),
    StringStruct(u'FileVersion', u'$FileVersion'),
    StringStruct(u'InternalName', u'$InternalName'),
    StringStruct(u'LegalCopyright', u'Copyright (c) $CompanyName'),
    StringStruct(u'OriginalFilename', u'$OriginalFilename'),
    StringStruct(u'ProductName', u'$ProductName'),
    StringStruct(u'ProductVersion', u'$ProductVersion')])
  ]), 
VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"@
# izveidojam komilācijas versijas datni failu sistēmā, ja datne eksistē - pārrakstām
$verFileBody | Out-File -FilePath $VersionFile -Encoding utf8 -Force

# Ja atrodam vecās exe un bck datnes - dzēšam, pārsaucam esošo exe par bck 
$FileExe = "$__ScriptPath\$($File.BaseName).exe"
$FileExeBck = "$__ScriptPath\$($File.BaseName)_exe.bck"
if (Test-Path -Path $FileExe -PathType Leaf) {
    if (Test-Path -Path $FileExeBck -PathType Leaf) {
        Remove-Item -Path $FileExeBck -Force
        Write-Host "[Compiler] Delete old bck [$FileExeBck] file."
    }#endif
    if (Test-Path -Path "$__ScriptPath\dist\$($File.BaseName).exe" -PathType Leaf) {
        Remove-Item -Path "$__ScriptPath\dist\$($File.BaseName).exe" -Force
        Write-Host "[Compiler] Delete old distr [$__ScriptPath\dist\$($File.BaseName).exe] file."
    }#endif
    Rename-Item -Path $FileExe -NewName $FileExeBck -Force
    Write-Host "[Compiler] Found old exe [$FileExe] file"
    Write-Host "[Compiler] Renamed it to [$FileExeBck]."
}#endif

# izpildam komandrindā python instalācijas komandu ar parametriem
Invoke-Expression "& pyinstaller --onefile $($File.FullName) --noconsole --version-file=$VersionFile --icon=$($IconFile.FullName)"

# kopējam exe datni no distr mapes uz root mapi
Copy-Item -Path "$__ScriptPath\dist\$($File.BaseName).exe" -Destination "$__ScriptPath" -Force
Write-Host "[Compiler] the new file [$($File.BaseName).exe] copied to the directory [$__ScriptPath]"
