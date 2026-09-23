# Находит букву единственной USB-флешки (печатает ее) или ничего.
# Только чтение, ничего не меняет. Вызывается из MBFU-RETRO.bat.
$ErrorActionPreference = 'SilentlyContinue'
$u = @(Get-Disk | Where-Object { $_.BusType -eq 'USB' -and -not $_.IsSystem })
if ($u.Count -eq 1) {
    $p = @(Get-Partition -DiskNumber $u[0].Number |
        Where-Object { $_.DriveLetter } | Select-Object -First 1)
    if ($p.Count -eq 1) { $p[0].DriveLetter }
}
