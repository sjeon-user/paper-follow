# arXiv search for Physical AI paper follow-up (ASCII only; no non-ASCII literals).
# Usage: powershell -ExecutionPolicy Bypass -File arxiv_search.ps1 -Days 30 -OutFile "$env:TEMP\pf_results.json"
param(
  [int]$Days = 30,
  [string]$OutFile = "$env:TEMP\pf_results.json",
  [int]$PerQuery = 25
)
$ErrorActionPreference = "Stop"
$cutoff = (Get-Date).AddDays(-$Days)

$topics = @(
  @{ tag="egocentric";       q='all:egocentric AND (cat:cs.RO OR cat:cs.CV)' },
  @{ tag="motion capture";   q='abs:"motion capture"' },
  @{ tag="retargeting";      q='all:retargeting AND (cat:cs.RO OR cat:cs.GR OR cat:cs.CV)' },
  @{ tag="robot arm";        q='abs:"robotic manipulation" AND cat:cs.RO' },
  @{ tag="self-driving lab"; q='abs:"autonomous laboratory" OR abs:"self-driving laboratory"' },
  @{ tag="VLA";              q='abs:"vision-language-action"' }
)

$all = @{}
foreach($t in $topics){
  $enc = [uri]::EscapeDataString($t.q)
  $url = "http://export.arxiv.org/api/query?search_query=$enc&sortBy=submittedDate&sortOrder=descending&max_results=$PerQuery"
  try {
    $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 40
    $x = [xml]$resp.Content
  } catch {
    Write-Host "QUERY FAIL [$($t.tag)]: $($_.Exception.Message)"
    Start-Sleep -Seconds 3; continue
  }
  $entries = $x.feed.entry
  if($null -eq $entries){ Start-Sleep -Seconds 3; continue }
  foreach($e in $entries){
    $pub = [datetime]$e.published
    if($pub -lt $cutoff){ continue }
    $m = [regex]::Match($e.id, '(\d{4}\.\d{4,5})(v\d+)?')
    $aid = $m.Groups[1].Value
    if(-not $aid){ continue }
    $cats = @(); if($e.category){ $cats = @($e.category | ForEach-Object { $_.term }) }
    $authors = @(); if($e.author){ $authors = @($e.author | ForEach-Object { $_.name }) }
    if($all.ContainsKey($aid)){
      if($all[$aid].topics -notcontains $t.tag){ $all[$aid].topics += $t.tag }
      continue
    }
    $all[$aid] = [pscustomobject]@{
      id = $aid
      title = ($e.title -replace '\s+',' ').Trim()
      published = $pub.ToString("yyyy-MM-dd")
      authors = $authors
      categories = $cats
      topics = @($t.tag)
      summary = ($e.summary -replace '\s+',' ').Trim()
    }
  }
  Start-Sleep -Seconds 3
}

$list = $all.Values | Sort-Object published -Descending
$list | ConvertTo-Json -Depth 6 | Out-File -FilePath $OutFile -Encoding utf8
Write-Host "TOTAL UNIQUE (last $Days days): $($list.Count)"
Write-Host "SAVED: $OutFile"
foreach($p in $list){
  Write-Host ("[{0}] {1}  {{{2}}}  ({3})  {4}" -f $p.published,$p.id,($p.topics -join ', '),($p.categories -join ','),$p.title)
}
