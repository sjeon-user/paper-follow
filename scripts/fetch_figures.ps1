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
  # arXiv serves the paper at /html/<id> or /html/<id>v<N>, and the img srcs come in two shapes:
  #   (a) bare filename          "x1.png"              -> resolve under the paper directory
  #   (b) version-prefixed path  "2512.23705v1/x1.png" -> already relative to /html/
  # Naive [uri] resolution breaks (a): with base ".../html/<id>" (no trailing slash) it treats
  # "<id>" as a filename and replaces it, yielding /html/x1.png -- a 404. Forcing a trailing
  # slash fixes (a) but then doubles the path for (b). So handle the two shapes separately.
  $baseDir = $base
  if($baseDir -notmatch '/$'){ $baseDir = "$baseDir/" }
  $ms = [regex]::Matches($r.Content, '<img[^>]*?src="([^"]+)"')
  $cands = @()
  foreach($m in $ms){
    $src = $m.Groups[1].Value
    if($src -match 'data:'){ continue }
    # affiliation/university crests sit at the top of many multi-institution papers and would
    # otherwise win as "first image" (seen on 2607.24744, which picked a PKU logo).
    if($src -match '(?i)/static/|logo|orcid|icon|mathjax|affiliation|univ|crest|badge'){ continue }
    if($src -notmatch '(?i)\.(png|jpg|jpeg)(\?|$)'){ continue }
    if($src -notmatch '^https?://'){
      $src = $src -replace '^\./',''
      if($src -match '^\d{4}\.\d{4,5}v\d+/'){ $src = "https://arxiv.org/html/$src" }   # shape (b)
      else { $src = ([uri]::new([uri]$baseDir, $src)).AbsoluteUri }                     # shape (a)
    }
    if($cands -notcontains $src){ $cands += $src }
  }
  Write-Host "CANDIDATES ($($cands.Count)):"
  $i=0; foreach($c in $cands){ $i++; Write-Host "  [$i] $c" }
  # Best guess, in order:
  #  1) a filename that names itself an overview/teaser/pipeline figure
  #  2) x1.png -- arXiv's LaTeX-to-HTML numbers figures in order, so x1 is usually Figure 1
  #  3) the first candidate that is NOT an obvious results plot
  # Charts of success rates are common early in a paper but make poor thumbnails
  # (seen on 2603.17720, which picked performance_comparison.png).
  $chartish = '(?i)(performance|result|ablation|comparison|accuracy|success|curve|chart|plot|table|bar)'
  $pick = $cands | Where-Object { $_ -match '(?i)(intro|overview|teaser|framework|pipeline|main|fig_?1|figure_?1)' -and $_ -notmatch $chartish } | Select-Object -First 1
  if(-not $pick){ $pick = $cands | Where-Object { $_ -match '(?i)/x1\.(png|jpg|jpeg)$' } | Select-Object -First 1 }
  if(-not $pick){ $pick = $cands | Where-Object { $_ -notmatch $chartish } | Select-Object -First 1 }
  if(-not $pick){ $pick = $cands | Select-Object -First 1 }
  if(-not $pick){ Write-Host "NO CANDIDATE"; continue }
  $out = Join-Path $OutDir "$id.png"
  # arXiv is inconsistent about which path actually serves the assets: some papers answer at
  # /html/<id>/..., others only at /html/<id>v<N>/... even though both return the HTML.
  # Try the URL as resolved, then the same relative path under each version.
  $tryUrls = @($pick)
  if($pick -match "/html/$([regex]::Escape($id))/(.+)$"){
    $rel = $Matches[1]
    foreach($v in 1..4){ $tryUrls += "https://arxiv.org/html/${id}v$v/$rel" }
  }
  $ok = $false
  foreach($u in $tryUrls){
    try {
      Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 60 -OutFile $out
      Write-Host "PICKED: $u"
      Write-Host "SAVED:  $out ($((Get-Item $out).Length) bytes)"
      $ok = $true
      break
    } catch { }
  }
  if(-not $ok){
    Write-Host "DL FAIL: all $($tryUrls.Count) URL(s) failed for $pick"
  }
  Start-Sleep -Seconds 2
}
Write-Host "OUTDIR: $OutDir"
