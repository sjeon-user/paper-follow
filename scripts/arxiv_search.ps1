# arXiv search for Physical AI paper follow-up (ASCII only; no non-ASCII literals).
# Usage: powershell -ExecutionPolicy Bypass -File arxiv_search.ps1 -Days 30 -OutFile "$env:TEMP\pf_results.json"
param(
  [int]$Days = 60,
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
  @{ tag="VLA";              q='abs:"vision-language-action"' },
  @{ tag="diffusion policy"; q='abs:"diffusion policy" AND (cat:cs.RO OR cat:cs.LG)' },
  @{ tag="imitation learning"; q='abs:"imitation learning" AND cat:cs.RO' },
  # Liquid manipulation has no single settled term, so OR the task vocabulary.
  # Deliberately excluded: "fluid" (matches aerial/aerodynamics work) and
  # "granular"/"viscous" (matches locomotion on sand / in viscous media, not manipulation).
  # The OR query alone is noisy - roughly half the hits only mention "pouring" once as a
  # demo task - so require the vocabulary to appear at least twice (filter/minHits below).
  @{ tag="liquid manipulation";
     q='cat:cs.RO AND (abs:"pouring" OR abs:"liquid" OR abs:"sloshing" OR abs:"stirring" OR abs:"scooping")';
     filter='(?i)\b(liquid|pour|slosh|stir|scoop)\w*'; minHits=2 },
  # Transparent-object manipulation. Bare abs:"transparent" is unusable here: in cs.RO it
  # mostly matches the OTHER sense of the word (explainability - "transparent decision
  # making", "transparent and trustworthy autonomy"). So anchor on optical noun phrases.
  # The second clause keeps this manipulation-facing: either the paper is robotics
  # (cat:cs.RO, which also catches cross-listed perception work) or it talks about
  # grasping/manipulation. Without it, pure rendering/Gaussian-splatting papers flood in.
  @{ tag="transparent object";
     q='(abs:"transparent object" OR abs:"glass object" OR abs:"glass segmentation" OR abs:"non-Lambertian" OR abs:"glassware") AND (cat:cs.RO OR abs:"grasping" OR abs:"manipulation")';
     filter='(?i)(\btransparen\w*|\btranslucen\w*|\bspecular\w*|\bglassware\b|\brefract\w*|non-Lambertian|\bglass\b)'; minHits=2 }
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
    # Optional precision filter: require the topic vocabulary to appear >= minHits times
    # in title+abstract. Used by broad OR queries that would otherwise match papers
    # mentioning the keyword only once, in passing.
    if($t.filter){
      $blob = ($e.title -replace '\s+',' ') + ' ' + ($e.summary -replace '\s+',' ')
      $need = 2; if($t.minHits){ $need = [int]$t.minHits }
      if(([regex]::Matches($blob, $t.filter)).Count -lt $need){ continue }
    }
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
