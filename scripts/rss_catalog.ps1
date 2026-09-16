# Build a catalog of the newest RSS (Robotics: Science and Systems) proceedings volume.
# Usage: powershell -ExecutionPolicy Bypass -File scripts\rss_catalog.ps1 [-OutFile rss-catalog.json] [-Refresh] [-Volume rss22]
# - Detects the newest rssNN volume from roboticsproceedings.org (or use -Volume).
# - Skips scraping when the existing catalog already covers that volume with the same paper count (use -Refresh to force).
param(
  [string]$OutFile = "rss-catalog.json",
  [string]$Volume = "",
  [switch]$Refresh
)
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$base = "https://www.roboticsproceedings.org"

function Get-Html($url){ $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 40; [System.Text.Encoding]::UTF8.GetString($r.RawContentStream.ToArray()) }
function Clean($s){ [System.Net.WebUtility]::HtmlDecode(($s -replace '<[^>]+>','' -replace '\s+',' ')).Trim() }

if(-not $Volume){
  $homeHtml = Get-Html "$base/index.html"
  $vols = [regex]::Matches($homeHtml,'href="rss(\d{2})/index\.html"') | ForEach-Object { [int]$_.Groups[1].Value } | Sort-Object -Unique
  $Volume = "rss{0:D2}" -f ($vols | Select-Object -Last 1)
}
$index = Get-Html "$base/$Volume/index.html"
$volTitle = Clean ([regex]::Match($index,'<h1>(.*?)</h1>').Groups[1].Value)
$rows = [regex]::Matches($index,'<a href="(p\d+)\.html">(.*?)</a><br>\s*<i>(.*?)</i>',[System.Text.RegularExpressions.RegexOptions]::Singleline)
Write-Host "VOLUME: $Volume ($volTitle)  PAPERS IN INDEX: $($rows.Count)"
if($rows.Count -eq 0){ Write-Host "NO PAPERS PARSED - aborting without touching $OutFile"; exit 1 }

if((-not $Refresh) -and (Test-Path $OutFile)){
  try {
    $old = Get-Content $OutFile -Raw -Encoding UTF8 | ConvertFrom-Json
    if($old.volume -eq $Volume -and @($old.papers).Count -eq $rows.Count){
      Write-Host "CATALOG UP TO DATE: $OutFile ($(@($old.papers).Count) papers) - use -Refresh to rebuild"
      exit 0
    }
  } catch {}
}

$papers = @()
$n = 0
foreach($r in $rows){
  $n++
  $num = $r.Groups[1].Value
  $title = Clean $r.Groups[2].Value
  $authors = @((Clean $r.Groups[3].Value) -split ',\s*' | Where-Object { $_ })
  $abstract = ""; $doi = ""; $date = ""
  try {
    $d = Get-Html "$base/$Volume/$num.html"
    $m = [regex]::Match($d,'<b>Abstract:</b>\s*</p>\s*<p[^>]*>(.*?)</p>',[System.Text.RegularExpressions.RegexOptions]::Singleline)
    if($m.Success){ $abstract = Clean $m.Groups[1].Value }
    $doi = [regex]::Match($d,'DOI\s*=\s*\{([^}]+)\}').Groups[1].Value.Trim()
    $date = [regex]::Match($d,'citation_publication_date" content="([^"]+)"').Groups[1].Value -replace '/','-'
  } catch { Write-Host "  DETAIL FAIL [$num]: $($_.Exception.Message)" }
  $papers += [pscustomobject]@{
    id = "$Volume/$num"; num = $num; title = $title; authors = $authors
    abstract = $abstract; doi = $doi; date = $date
    page = "$base/$Volume/$num.html"; pdf = "$base/$Volume/$num.pdf"
  }
  if($n % 20 -eq 0){ Write-Host "  ... $n / $($rows.Count)" }
  Start-Sleep -Milliseconds 250
}
$firstDoi = ($papers | Where-Object { $_.doi } | Select-Object -First 1).doi
$year = [regex]::Match([string]$firstDoi,'RSS\.(\d{4})').Groups[1].Value
$cat = [pscustomobject]@{ volume = $Volume; title = $volTitle; year = $year; built = (Get-Date).ToString("yyyy-MM-dd"); count = $papers.Count; papers = $papers }
$cat | ConvertTo-Json -Depth 5 | Out-File -FilePath $OutFile -Encoding utf8
Write-Host "SAVED: $OutFile  ($($papers.Count) papers, $(@($papers | Where-Object { -not $_.abstract }).Count) without abstract)"
