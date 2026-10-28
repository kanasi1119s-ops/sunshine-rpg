# ケルト100曲の1曲分を Windows で書き出す（run.sh の PowerShell 版）
# 使い方: pwsh tools\celtic100\run.ps1 019   （作業場所は $env:COMPOSER_WORK、なければ C:\Users\fujik\composer-work\cel）
param([Parameter(Mandatory = $true)][string]$N)

$ErrorActionPreference = "Continue"  # 5.1 は外部コマンドの stderr を例外にするので、終了コードで見る
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$work = if ($env:COMPOSER_WORK) { $env:COMPOSER_WORK } else { "C:\Users\fujik\composer-work\cel" }
$w = Join-Path $work "w"; $out = Join-Path $work "out"
New-Item -ItemType Directory -Force $w, $out | Out-Null
if (-not $env:HF_HOME) { $env:HF_HOME = Join-Path (Split-Path $work) "hf" }
$env:PYTHONIOENCODING = "utf-8"; $env:PYTHONUTF8 = "1"  # Windows の既定(cp932)で日本語の JSON が読めない対策

# 作曲ソフトは python3 を呼ぶ。Windows の python3 は Store の別物(3.14・部品なし)なので、3.12 の仮想環境(python3.exe)を先頭に置く
$shim = Join-Path (Split-Path $work) "venv\Scripts"
if (Test-Path (Join-Path $shim "python3.exe")) { $env:PATH = "$shim;$env:PATH" }

$started = Get-Date
Remove-Item -ErrorAction SilentlyContinue (Join-Path $w "done$N")
Set-Location $repo

# 1. 設計図(曲のスクリプトがある曲だけ)
$gen = Join-Path $repo "assets-src\ai-songs\_gen\c100_$N.py"
if (Test-Path $gen) { python $gen (Join-Path $w "c$N.json") *> (Join-Path $w "gen$N.log") }
$flags = @()
$flagFile = Join-Path $w "c$N.json.flags"
if (Test-Path $flagFile) { $flags = (Get-Content $flagFile -Raw).Trim() -split "\s+" | Where-Object { $_ } }

# 2. 音を作る
node tools\composer\song.mjs build (Join-Path $w "c$N.json") --wav @flags --out $out *> (Join-Path $w "b$N.log")

# 3. 空気を重ねる(設計図が作業場所になければ、リポジトリの控えを使う)
$airSrc = Join-Path $repo "assets-src\ai-songs\_gen\c100_air\air$N.json"
if (-not (Test-Path (Join-Path $w "air$N.json")) -and (Test-Path $airSrc)) { Copy-Item $airSrc (Join-Path $w "air$N.json") }
Push-Location (Join-Path $repo "assets-src\ai-songs\_gen")
python c100_air.py (Join-Path $out "c$N.wav") (Join-Path $w "air$N.json") (Join-Path $out "c$N.final.wav") *> (Join-Path $w "air$N.log")
Pop-Location

# 4. 検査(音量の段差 → 音質の点数)
$final = Join-Path $out "c$N.final.wav"
python tools\celtic100\qc.py $final *> (Join-Path $w "qc$N.log")
python tools\audio-check\aes-score-lowmem.py $final *> (Join-Path $w "pq$N.log")

New-Item -ItemType File -Force (Join-Path $w "done$N") | Out-Null
"{0} 曲 {1}: {2:N0} 秒" -f (Get-Date -Format "HH:mm:ss"), $N, ((Get-Date) - $started).TotalSeconds
Get-Content (Join-Path $w "pq$N.log") -Tail 1
Get-Content (Join-Path $w "qc$N.log") -Tail 3
