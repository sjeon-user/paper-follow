# Download a representative figure per arXiv paper from its HTML version (ASCII only).
# Usage: powershell -ExecutionPolicy Bypass -File fetch_figures.ps1 -Ids "2607.15330,2607.17790" -OutDir "$env:TEMP\pf_img"
# For each id: prints ALL figure candidate URLs, and downloads a best-guess to <OutDir>\<id>.png.
# The caller should visually verify each downloaded image and, if it is a logo / "Journal Name"
# header / non-representative icon, re-download a better candidate (prefer figures/ overview images).
param(
  [Parameter(Mandatory=$true)][string]$Ids,
  [string]$OutDir = "$env:TEMP\pf_img"
)
$ErrorActionPreference = "Stop"
if(-not (Test-Path $OutDir)){ New-Item -ItemType Directory -Path $OutDir | Out-Null }
$idList = $Ids.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ }

foreach($id in $idList){
  Write-Host "===== $id ====="
  $htmlUrl = "https://arxiv.org/html/$id"
  try {
    $r = Invoke-WebRequest -Uri $htmlUrl -UseBasicParsing -TimeoutSec 40 -MaximumRedirection 5
    $base = $r.BaseResponse.ResponseUri.AbsoluteUri
    if(-not $base){ $base = $htmlUrl }
  } catch {
    Write-Host "HTML FAIL: $($_.Exception.Message)"; continue
  }
  $ms = [regex]::Matches($r.Content, '<img[^>]*?src="([^"]+)"')
  $cands = @()
  foreach($m in $ms){
    $src = $m.Groups[1].Value
    if($src -match 'data:'){ continue }
    if($src -match '(?i)/static/|logo|orcid|icon|mathjax'){ continue }
    if($src -notmatch '(?i)\.(png|jpg|jpeg)(\?|$)'){ continue }
    if($src -notmatch '^https?://'){ $src = ([uri]::new([uri]$base, $src)).AbsoluteUri }
    if($cands -notcontains $src){ $cands += $src }
  }
  Write-Host "CANDIDATES ($($cands.Count)):"
  $i=0; foreach($c in $cands){ $i++; Write-Host "  [$i] $c" }
  # best guess: prefer a 'figures/..intro|overview|teaser|framework' image, else first candidate
  $pick = $cands | Where-Object { $_ -match '(?i)figures/.*(intro|overview|teaser|framework|pipeline|main)' } | Select-Object -First 1
  if(-not $pick){ $pick = $cands | Select-Object -First 1 }
  if(-not $pick){ Write-Host "NO CANDIDATE"; continue }
  $out = Join-Path $OutDir "$id.png"
  try {
    Invoke-WebRequest -Uri $pick -UseBasicParsing -TimeoutSec 60 -OutFile $out
    Write-Host "PICKED: $pick"
    Write-Host "SAVED:  $out ($((Get-Item $out).Length) bytes)"
  } catch {
    Write-Host "DL FAIL: $($_.Exception.Message)"
  }
  Start-Sleep -Seconds 2
}
Write-Host "OUTDIR: $OutDir"
