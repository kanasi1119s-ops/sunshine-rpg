"""見本の動画のコマの時刻（*.timeline.json）に合わせて、効果音を並べた音（WAV）を作り、動画に入れる（2026-10-04）。

使い方:
  python3 se_mix.py lightning 動画.mp4 出力.mp4            # fx_preview.py の動画（雷の術）
  python3 se_mix.py attack 動画.mp4 出力.mp4 [--bgm 曲.mp3 --bgm-gain 0.3]   # anim_clip.py の動画（歩く・攻撃）
  python3 se_mix.py fx 動画.mp4 出力.mp4 --fxdir エフェクトのフォルダ [--bgm ...]   # コマに se を書いたエフェクト（炎の術など）
効果音は assets-src/se/（tools/sound/se_synth.py で作る）。
"""
import json
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np

SR = 48000
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "assets-src", "se")


def load(name):
    w = wave.open(os.path.join(ROOT, name + ".wav"))
    return np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1, 2).astype(float) / 32768


def place(dst, src, at, gain):
    i = int(at * SR)
    m = min(len(src), len(dst) - i)
    if m > 0:
        dst[i:i + m] += src[:m] * gain


def events_lightning(tl):
    ev = []
    order = [4, 0, 2, 5, 1, 3]               # lightning.py の make_storm と同じ順
    for e in tl:
        for name, i in e["effs"]:
            if name == "charge" and i == 0: ev.append((e["t"], "lightning/cast", 0.9))
            if name == "bolt":
                if i == 0: ev.append((e["t"], "lightning/leader", 0.5))
                if i == 3: ev.append((e["t"], "lightning/strike", 1.0))
                if i == 6: ev.append((e["t"], "lightning/restrike", 0.7))
            if name == "storm":
                if i == 0: ev.append((e["t"], "lightning/storm-rumble", 0.8))
                for j in range(len(order)):
                    if i == 2 + 2 * j: ev.append((e["t"], "lightning/leader", 0.22))
                    if i == 3 + 2 * j:
                        ev.append((e["t"], "lightning/strike", 0.95) if j == 0 else (e["t"], f"lightning/crack{j % 3 + 1}", 0.75))
    return ev


def events_fx(tl, fxdir):
    """エフェクトのコマに書いてある効果音（"se": [[名前, 音量], ...]）を、そのコマの時刻に鳴らす（炎の術など）"""
    cache, ev = {}, []
    for e in tl:
        for name, i in e["effs"]:
            if name not in cache:
                cache[name] = json.load(open(os.path.join(fxdir, name + ".json")))
            for se, g in cache[name]["frames"][i].get("se", []):
                ev.append((e["t"], se, g))
    return ev


def events_attack(tl):
    ev = []
    for e in tl:
        if e.get("pause"):
            continue
        k, i, t = e["kind"], e["i"], e["t"]
        if k == "flat_walk" and i in (0, 8): ev.append((t, "boss-attack/step", 0.45))
        if k in ("flat_attack", "flat_attack2", "flat_attack3"):
            if i == 1: ev.append((t, "boss-attack/windup", 0.6))
            if i == 6: ev.append((t, "boss-attack/whoosh", 0.85))
            if i == 8:
                if k == "flat_attack3":
                    ev.append((t, "boss-attack/slam", 1.0))
                else:
                    ev.append((t, "boss-attack/impact", 1.0))
                    if k == "flat_attack2": ev.append((t, "boss-attack/step", 0.6))   # 踏みこみ
    return ev


def main():
    mode, video, out = sys.argv[1:4]
    a = sys.argv[4:]
    bgm = a[a.index("--bgm") + 1] if "--bgm" in a else None
    bgm_gain = float(a[a.index("--bgm-gain") + 1]) if "--bgm-gain" in a else 0.3
    tl = json.load(open(os.path.splitext(video)[0] + ".timeline.json"))
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                               capture_output=True, text=True).stdout)
    mix = np.zeros((int(SR * (dur + 1)), 2))
    if mode == "lightning":
        ev = events_lightning(tl)
    elif mode == "fx":
        ev = events_fx(tl, a[a.index("--fxdir") + 1])
    else:
        ev = events_attack(tl)
    cache = {}
    for t, name, g in ev:
        if name not in cache: cache[name] = load(name)
        place(mix, cache[name], t, g)
    mix = mix[: int(SR * dur)]
    pk = np.abs(mix).max()
    if pk > 0.89:      # 重なって大きくなりすぎた所は、やわらかく押さえる
        mix = np.tanh(mix / pk * 1.4) / np.tanh(1.4) * 0.89
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "se.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())
    if bgm:
        st = max(0, dur - 3)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-i", bgm, "-filter_complex",
               f"[2:a]volume={bgm_gain},afade=t=in:d=1,afade=t=out:st={st}:d=3[b];[1:a][b]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89:level=false[a]",
               "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out]
    else:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-filter_complex", "[1:a]volume=3dB,alimiter=limit=0.89:level=false[a]",
               "-map", "0:v", "-map", "[a]", "-c:v", "copy",
               "-c:a", "aac", "-b:a", "192k", "-shortest", out]
    subprocess.run(cmd, check=True)
    print("効果音", len(ev), "回 →", out)


if __name__ == "__main__":
    main()
