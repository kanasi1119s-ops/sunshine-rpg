#!/usr/bin/env python3
"""歌の「余韻」と「音程」を数字で見る（2026-11-17 人間「歌の余韻とか音程が素人っぽく」）。
使い方: python3 tools/vt3/vocal_shape.py <歌入りの JSON> [響きなしで歌わせた wav]
  wav がなければ、主旋律だけを響きなしで歌わせてから測る（tools/singer/sing.py）。
見るもの:
  音の長さ … 0.5秒以上の音・句の最後の音の長さ（のばす音がないと、ビブラートも余韻もつけようがない）
  余韻 … 句の最後の音が終わってから −30dB まで下がる時間、終わりぎわ 0.15秒の音程の下がり
  音程 … 音の真ん中での狙いからのずれ（セント）、狙いの ±25 セントに入っている時間の割合、音が変わってから落ちつくまでの時間
  ビブラート … かかっている音の数と深さ"""
import sys, os, json, subprocess, tempfile
import numpy as np, soundfile as sf, pyworld as pw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "singer"))
import sing as SG

def main():
    jp = sys.argv[1]; js = json.load(open(jp, encoding="utf-8")); v = js["vocals"][0]; bpm = float(js["bpm"])
    if len(sys.argv) > 2: wav = sys.argv[2]
    else:
        d = tempfile.mkdtemp(); j2 = dict(js); j2["vocals"] = [v]; json.dump(j2, open(d + "/a.json", "w"), ensure_ascii=False); wav = d + "/a.wav"
        subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "singer", "sing.py"), "render", d + "/a.json", wav, "--dry"], capture_output=True)
    x, sr = sf.read(wav); x = x.mean(1) if x.ndim > 1 else x
    spb = 60 / bpm; t = 0.0; notes = []
    for tok in v["notes"].split():
        p = tok.split(":"); L = float(p[1]) * spb
        if p[0] != "R": notes.append((t, t + L, SG.midi_of(p[0])[0], p[2] if len(p) > 2 else ""))
        t += L
    notes = [n for n in notes if n[2] is not None]
    f0, tt = pw.harvest(x.astype(np.float64), sr, f0_floor=150, f0_ceil=1000, frame_period=5.0)
    semi = np.where(f0 > 0, 69 + 12 * np.log2(np.maximum(f0, 1) / 440), np.nan) - float(v.get("transpose", 0))
    env = np.sqrt(np.convolve(x ** 2, np.ones(int(sr * 0.01)) / int(sr * 0.01), "same")); edb = 20 * np.log10(env + 1e-9)
    D = np.array([b - a for a, b, _, _ in notes]); n = len(notes)
    ends = [i for i in range(n) if i == n - 1 or notes[i + 1][0] - notes[i][1] > 0.2]
    print(f"■ {js.get('title','')}  テンポ {bpm:.0f}  音の数 {n}  句の数 {len(ends)}")
    print(f"  音の長さ: 中央値 {np.median(D):.2f}秒 ／ 0.5秒以上 {100*np.mean(D>=0.5):.0f}% ／ 1秒以上 {100*np.mean(D>=1.0):.0f}%")
    De = D[ends]; print(f"  句の最後の音: 中央値 {np.median(De):.2f}秒 ／ 0.5秒以上 {100*np.mean(De>=0.5):.0f}% ／ 0.25秒より短い {100*np.mean(De<0.25):.0f}%")
    rel, fall = [], []
    for i in ends:
        a, b, m, _ = notes[i]; k = int(b * sr); ref = np.median(edb[int((a + (b - a) * 0.3) * sr):int((a + (b - a) * 0.8) * sr) + 1])
        seg = edb[k:k + int(0.8 * sr)]; w = np.where(seg < ref - 30)[0]; rel.append((w[0] / sr) if len(w) else 0.8)
        s1 = semi[(tt >= b - 0.15) & (tt < b)]; s0 = semi[(tt >= a + (b - a) * 0.3) & (tt < b - 0.15)]
        if np.isfinite(s1).sum() > 5 and np.isfinite(s0).sum() > 5: fall.append(100 * (np.nanmedian(s1[-10:]) - np.nanmedian(s0)))
    print(f"  余韻: 句の最後の音が終わってから −30dB まで {np.median(rel)*1000:.0f}ミリ秒（中央値。4分の1〜4分の3: {np.percentile(rel,25)*1000:.0f}〜{np.percentile(rel,75)*1000:.0f}）")
    if fall: print(f"  句の終わりぎわの音程: 中央値 {np.median(fall):+.0f} セント（4分の1〜4分の3: {np.percentile(fall,25):+.0f}〜{np.percentile(fall,75):+.0f}）")
    err, inr, settle, vibn, vibd, longn = [], [], [], 0, [], 0
    for i, (a, b, m, ly) in enumerate(notes):
        sel = (tt >= a) & (tt < b); s = semi[sel]; ok = np.isfinite(s)
        if ok.sum() < 6: continue
        c = 100 * (s - m); mid = c[len(c) // 3: max(len(c) // 3 + 1, len(c) * 5 // 6)]; mid = mid[np.isfinite(mid)]
        if len(mid) >= 3: err.append(np.median(mid))
        inr.append(np.mean(np.abs(c[ok]) <= 25))
        if i > 0 and a - notes[i - 1][1] < 0.05 and notes[i - 1][2] != m:
            w = np.where(np.isfinite(c) & (np.abs(c) <= 25))[0]; settle.append(w[0] * 0.005 if len(w) else (b - a))
        if b - a >= 0.5:
            longn += 1; z = c[int(0.25 / 0.005):]; z = z[np.isfinite(z)]
            if len(z) >= 40:
                z = z - np.convolve(np.pad(z, 20, mode="edge"), np.ones(41) / 41, "valid"); sp = np.abs(np.fft.rfft(z * np.hanning(len(z)), 1024)); fr = np.fft.rfftfreq(1024, 0.005)
                band = (fr >= 4) & (fr <= 7.5); pk = sp[band].max(); 
                if pk > 3 * np.median(sp[(fr > 1) & (fr < 20)]) and np.std(z) * 1.41 >= 8: vibn += 1; vibd.append(np.std(z) * 1.41)
    err = np.array(err)
    print(f"  音程: 音の真ん中のずれ 中央値 {np.median(err):+.0f} セント・ばらつき（4分の1〜4分の3） {np.percentile(err,25):+.0f}〜{np.percentile(err,75):+.0f} ／ 30セント以上ずれた音 {100*np.mean(np.abs(err)>=30):.0f}%")
    print(f"        狙いの ±25セントに入っている時間 {100*np.mean(inr):.0f}% ／ 音が変わってから落ちつくまで {np.median(settle)*1000:.0f}ミリ秒（中央値）")
    print(f"  ビブラート: 0.5秒以上の音 {longn} のうち、かかっている音 {vibn}（深さ 中央値 {np.median(vibd) if vibd else 0:.0f} セント）")
    # 旋律と和音: のばす音（1拍以上）と句の最後の音が、その小節の和音に合っているか
    #   和音の音（根音・3度・5度・7度）／にごる音（和音の音の半音上。長くのばすと「音程が外れた」ように聞こえる）／そのほか（9度など、きれいにひびく音）
    chs = str(js.get("chords", "")).split(); beats = int(js.get("beats", 4)); bpc = int(js.get("barsPerChord", 1))
    def tones(ch):
        r = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[ch[0]]; q = ch[1:]
        if q[:1] == "#": r += 1; q = q[1:]
        elif q[:1] == "b": r -= 1; q = q[1:]
        q = q.split("/")[0]
        if q.startswith("maj7"): iv = [0, 4, 7, 11]
        elif q.startswith("m7b5"): iv = [0, 3, 6, 10]
        elif q.startswith("dim"): iv = [0, 3, 6, 9]
        elif q.startswith("m7") or q.startswith("m9"): iv = [0, 3, 7, 10]
        elif q.startswith("m"): iv = [0, 3, 7]
        elif q.startswith("7") or q.startswith("9"): iv = [0, 4, 7, 10]
        elif q.startswith("sus4"): iv = [0, 5, 7]
        else: iv = [0, 4, 7]
        return {(r + i) % 12 for i in iv}
    if chs:
        cnt = {"和音の音": 0, "にごる音": 0, "そのほか": 0}; bad = []
        for i, (a, b, m, ly) in enumerate(notes):
            if not ((b - a) >= spb * 0.99 or i in ends): continue
            bar = int((a / spb + 1e-6) // beats); c = chs[min(len(chs) - 1, bar // bpc)]
            if "|" in c: c = c.split("|")[0 if ((a / spb) % beats) < beats / 2 else 1]
            try: T = tones(c)
            except Exception: continue
            pc = int(m) % 12
            if pc in T: cnt["和音の音"] += 1
            elif (pc - 1) % 12 in T: cnt["にごる音"] += 1; bad.append(f"{int(a//60)}:{a%60:04.1f}「{ly}」({c})")
            else: cnt["そのほか"] += 1
        tot = sum(cnt.values()) or 1
        print(f"  のばす音・句の最後の音と和音（{tot} 音）: 和音の音 {100*cnt['和音の音']/tot:.0f}% ／ きれいにひびくそのほかの音 {100*cnt['そのほか']/tot:.0f}% ／ にごる音 {100*cnt['にごる音']/tot:.0f}%")
        if bad: print("    にごる音の場所: " + " ".join(bad[:24]))
if __name__ == "__main__": main()
