# arXiv search for Physical AI paper follow-up (ASCII only; no non-ASCII literals).
# Usage: powershell -ExecutionPolicy Bypass -File arxiv_search.ps1 -Days 30 -OutFile "$env:TEMP\pf_results.json"
param(
  [int]$Days = 60,
  [string]$OutFile = "$env:TEMP\pf_results.json",
  [int]$PerQuery = 25
)
$ErrorActionPreference = "Stop"
$cutoff = (Get-Date).AddDays(-$Days)

# Focused keyword set (2026-08-06). Only these five themes are followed:
#   diffusion VLA / diffusion policy / Universal Manipulation Interface /
#   handheld gripper + retargeting / robotic manipulation of transparent objects or liquids.
# Previously followed but deliberately dropped: egocentric, motion capture,
# generic "robotic manipulation", self-driving lab, generic VLA, imitation learning.
$topics = @(
  # Diffusion-based VLA. Bare "vision-language-action" pulled in far too much, so both
  # halves must be present. "flow matching" is NOT included - the theme is diffusion.
  @{ tag="diffusion VLA";
     q='(abs:"vision-language-action" OR abs:"vision language action") AND abs:"diffusion"' },
  @{ tag="diffusion policy"; q='abs:"diffusion policy" AND (cat:cs.RO OR cat:cs.LG)' },
  # UMI. The spelled-out phrase is safe on its own; the bare acronym is not
  # (it collides with unrelated fields), so it is fenced behind cat:cs.RO.
  @{ tag="UMI";
     q='abs:"universal manipulation interface" OR (abs:"UMI" AND cat:cs.RO)' },
  # Handheld demonstration hardware + motion/hand retargeting. Both are about getting
  # human demonstrations onto a robot, so they share one tag.
  # NOTE: bare "retargeting" in cs.CV also means *image* retargeting (content-aware
  # resizing), which has nothing to do with robots - hence the robot-context filter2.
  @{ tag="handheld gripper / retargeting";
     q='(cat:cs.RO OR cat:cs.CV) AND (abs:"handheld gripper" OR abs:"hand-held gripper" OR abs:"portable gripper" OR abs:"handheld demonstration" OR abs:"handheld data collection" OR abs:"retargeting")';
     filter2='(?i)(\brobot\w*|humanoid|manipulat\w*|teleoperat\w*|embodiment|dexterous|gripper|\bend-effector)' },
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
     # tightened 2026-08-06: the theme is *manipulation of* transparent objects, so a
     # paper must actually talk about grasping/manipulating, not just perceive glass.
     filter2='(?i)\b(grasp\w*|manipulat\w*|pick\w*|placing|robot\w*)';
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
    $blob = ($e.title -replace '\s+',' ') + ' ' + ($e.summary -replace '\s+',' ')
    if($t.filter){
      $need = 2; if($t.minHits){ $need = [int]$t.minHits }
      if(([regex]::Matches($blob, $t.filter)).Count -lt $need){ continue }
    }
    # Secondary filter: must be present at least once (used to require a manipulation context).
    if($t.filter2 -and -not [regex]::IsMatch($blob, $t.filter2)){ continue }
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
