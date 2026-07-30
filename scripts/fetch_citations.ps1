# fetch_citations.ps1
# 보관함(keep.html) 논문들의 인용 수를 Semantic Scholar API에서 조회합니다.
#
#   powershell -ExecutionPolicy Bypass -File scripts\fetch_citations.ps1 -Ids "2303.04137,2402.10329"
#
# 출력: 각 id별 "id | cites=N | title" 한 줄씩 + JSON(-OutFile 지정 시)
# 조회에 실패한 id는 cites=NULL 로 표시되며, 이 경우 keep.html의 citations 필드는
# 기존 값을 유지하거나 생략하세요(0으로 덮어쓰지 마세요 — 0은 '인용 없음'을 뜻합니다).

param(
  [Parameter(Mandatory = $true)][string]$Ids,
  [string]$OutFile = ""
)

$ErrorActionPreference = "Stop"
$idList = $Ids -split "[,\s]+" | Where-Object { $_ -match '\S' }
if (-not $idList) { Write-Error "조회할 arXiv id가 없습니다."; exit 1 }

$endpoint = "https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,citationCount,year,externalIds"
$body = @{ ids = @($idList | ForEach-Object { "ARXIV:$_" }) } | ConvertTo-Json

$resp = $null
for ($attempt = 1; $attempt -le 3; $attempt++) {
  try {
    $resp = Invoke-RestMethod -Uri $endpoint -Method Post -Body $body `
      -ContentType "application/json" -TimeoutSec 60
    break
  } catch {
    Write-Warning "시도 $attempt 실패: $($_.Exception.Message)"
    if ($attempt -lt 3) { Start-Sleep -Seconds (3 * $attempt) }
  }
}
if ($null -eq $resp) { Write-Error "Semantic Scholar 조회에 실패했습니다(3회 시도)."; exit 1 }

$results = @()
for ($i = 0; $i -lt $idList.Count; $i++) {
  $id = $idList[$i]
  $p = $resp[$i]
  if ($p) {
    $results += [pscustomobject]@{ arxiv_id = $id; citations = $p.citationCount; title = $p.title }
    Write-Output ("{0} | cites={1} | {2}" -f $id, $p.citationCount, $p.title)
  } else {
    # Semantic Scholar에 아직 색인되지 않은 논문(주로 갓 올라온 프리프린트)
    $results += [pscustomobject]@{ arxiv_id = $id; citations = $null; title = $null }
    Write-Output ("{0} | cites=NULL | (Semantic Scholar 미색인)" -f $id)
  }
}

Write-Output ""
Write-Output ("CITE_DATE: " + (Get-Date -Format "yyyy-MM-dd"))

if ($OutFile) {
  @{ cite_date = (Get-Date -Format "yyyy-MM-dd"); papers = $results } |
    ConvertTo-Json -Depth 5 | Set-Content -Path $OutFile -Encoding UTF8
  Write-Output "SAVED: $OutFile"
}
