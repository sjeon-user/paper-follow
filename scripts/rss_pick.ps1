# Randomly pick N unseen papers from the RSS catalog.
# Usage: powershell -ExecutionPolicy Bypass -File scripts\rss_pick.ps1 -N 5 [-Catalog rss-catalog.json] [-Seen rss-seen.json] [-OutFile "$env:TEMP\rss_pick.json"]
param(
  [int]$N = 5,
  [string]$Catalog = "rss-catalog.json",
  [string]$Seen = "rss-seen.json",
  [string]$OutFile = "$env:TEMP\rss_pick.json"
)
$ErrorActionPreference = "Stop"
$cat = Get-Content $Catalog -Raw -Encoding UTF8 | ConvertFrom-Json
$seenIds = @()
if(Test-Path $Seen){ $seenIds = @((Get-Content $Seen -Raw -Encoding UTF8 | ConvertFrom-Json).featured) }
$pool = @($cat.papers | Where-Object { $seenIds -notcontains $_.id })
Write-Host "VOLUME: $($cat.volume)  TOTAL: $($cat.count)  SEEN: $($seenIds.Count)  UNSEEN: $($pool.Count)"
if($pool.Count -eq 0){ Write-Host "NO UNSEEN PAPERS LEFT"; exit 0 }
$pick = @($pool | Get-Random -Count ([Math]::Min($N, $pool.Count)) | Sort-Object num)
$pick | ConvertTo-Json -Depth 5 | Out-File -FilePath $OutFile -Encoding utf8
Write-Host "PICKED $($pick.Count) -> $OutFile"
foreach($p in $pick){ Write-Host ("  {0}  {1}  [{2}]  {3}" -f $p.id, $p.doi, ($p.authors -join ', '), $p.title) }
