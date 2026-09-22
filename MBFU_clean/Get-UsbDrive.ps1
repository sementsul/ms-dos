#Requires -Version 3.0
<#
.SYNOPSIS
  MBFU helper: map \\.\PHYSICALDRIVE<N> -> drive letters, write to temp.txt
  Replacement for old dskn.bat + dskn.exe (WMIC based).
.DESCRIPTION
  Uses modern Get-CimInstance (fallback to Get-WmiObject on PS 3-4).
  No network, no registry writes, no raw disk access - only reads.
.PARAMETER DiskNumber
  Number N of PHYSICALDRIVE (1..30 as used by MSDOSBOOT.bat)
.PARAMETER OutFile
  File to write space-separated drive letters into (temp.txt)
#>
param(
  [Parameter(Mandatory=$true)][int]$DiskNumber,
  [Parameter(Mandatory=$true)][string]$OutFile
)

$ErrorActionPreference = 'Stop'
try {
  $deviceId = "\\.\PHYSICALDRIVE$DiskNumber"
  $letters = @()

  if (Get-Command Get-CimInstance -ErrorAction SilentlyContinue) {
    $diskParts = Get-CimInstance -ClassName Win32_DiskDriveToDiskPartition | Where-Object { $_.Antecedent.DeviceID -eq $deviceId -or $_.Antecedent -match [regex]::Escape($deviceId) }
    foreach ($dp in $diskParts) {
      # Antecedent = DiskPartition.DeviceID="Disk #N, Partition #M"
      $partId = $dp.Dependent.DeviceID
      $maps = Get-CimInstance -ClassName Win32_LogicalDiskToPartition | Where-Object { $_.Antecedent.DeviceID -eq $partId -or $_.Antecedent -match [regex]::Escape($partId) }
      foreach ($m in $maps) {
        if ($m.Dependent.DeviceID) { $letters += $m.Dependent.DeviceID.Trim() }
      }
    }
  } else {
    # very old PowerShell fallback
    $diskParts = Get-WmiObject -Class Win32_DiskDriveToDiskPartition | Where-Object { $_.Antecedent -match [regex]::Escape($deviceId) }
    foreach ($dp in $diskParts) {
      $partId = ([wmi]$dp.Dependent).DeviceID
      $maps = Get-WmiObject -Class Win32_LogicalDiskToPartition | Where-Object { $_.Antecedent -match [regex]::Escape($partId) }
      foreach ($m in $maps) {
        $ld = ([wmi]$m.Dependent).DeviceID
        if ($ld) { $letters += $ld.Trim() }
      }
    }
  }

  $line = ($letters -join ' ').Trim()
  # keep compatible format: leading space like old " E:" build, findstr still matches
  if ($line -ne '') { $line = ' ' + $line + ' ' }
  Set-Content -LiteralPath $OutFile -Value $line -Encoding Ascii -NoNewline
  exit 0
} catch {
  Write-Error $_.Exception.Message
  exit 1
}
