# SCARLET FREQUENCY 全25曲.mp4 の長さを直す（2026-10-27）
# 1曲目の終わりなどに残った「目次の箱（mfra）」を「読み飛ばす箱（free）」に書きかえ、全体の長さ（1時間49分16秒）を頭に書きこむ。
# 映像と音そのものには手をつけない（4文字ずつの書きかえだけ）。
$ErrorActionPreference = "Stop"
$file = Get-ChildItem -LiteralPath $PSScriptRoot -Filter "*.mp4" | Where-Object { $_.Length -gt 1GB } | Select-Object -First 1
if (-not $file) { Write-Host "動画が見つかりません"; exit 1 }
Write-Host ("直す動画: " + $file.FullName)
$fs = [System.IO.File]::Open($file.FullName, 'Open', 'ReadWrite', 'None')
function RU32 { $b = New-Object byte[] 4; [void]$fs.Read($b, 0, 4); [Array]::Reverse($b); return [BitConverter]::ToUInt32($b, 0) }
function RTYPE { $b = New-Object byte[] 4; [void]$fs.Read($b, 0, 4); return [Text.Encoding]::ASCII.GetString($b) }
function WU32([uint32]$v) { $b = [BitConverter]::GetBytes($v); [Array]::Reverse($b); $fs.Write($b, 0, 4) }
try {
  # 1) 目次の箱を読み飛ばす箱に
  $len = $fs.Length; [int64]$pos = 0; $n = 0
  while ($pos -lt $len) {
    $fs.Position = $pos; [uint64]$sz = RU32; $t = RTYPE
    if ($sz -eq 1) { $hi = RU32; $lo = RU32; $sz = [uint64]$hi * 4294967296 + $lo }
    if ($sz -lt 8) { throw "箱の大きさがおかしい所があります: $pos" }
    if ($t -eq "mfra") { $fs.Position = $pos + 4; $fs.Write([Text.Encoding]::ASCII.GetBytes("free"), 0, 4); $n++ }
    $pos += [int64]$sz
  }
  Write-Host ("目次の箱を書きかえた数: " + $n)
  # 2) 全体の長さを書きこむ（箱の名前を確かめてから）
  $spots = @(
    @{ at = 40;  name = "mvhd"; off = 60;  val = 6556243 },
    @{ at = 156; name = "tkhd"; off = 180; val = 6556130 },
    @{ at = 256; name = "mdhd"; off = 276; val = 80561727 },
    @{ at = 656; name = "tkhd"; off = 680; val = 6556243 },
    @{ at = 756; name = "mdhd"; off = 776; val = 314699657 }
  )
  foreach ($s in $spots) {
    $fs.Position = $s.at; $t = RTYPE
    if ($t -ne $s.name) { throw ("思っていた所に " + $s.name + " がありません（" + $t + "）") }
  }
  foreach ($s in $spots) { $fs.Position = $s.off; WU32 $s.val }
  Write-Host "全体の長さ（1時間49分16秒）を書きこみました。"
} finally { $fs.Close() }
Write-Host "おわり。動画を開いて、長さが 1:49:16 と出るか確かめてください。"
