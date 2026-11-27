#!/usr/bin/env python3
"""音の見本（sound_gallery.py・guitar_tone_gallery.py で作って書き出した .wav）を、再生ボタンつきの1ページ（HTML）にまとめる。
使い方: python3 tools/vt3/gallery_page.py <見本のフォルダ（j/list.json と o/tNN.wav がある）> <題> <説明の文> <出力.html> [--lufs -16]
  大きさをそろえて mp3 にし（音はページの中にうめこむ）、音が出ていない見本（-45dB 未満）を数えて知らせる。明るさ（2.5kHz より上）と低音（250Hz より下）の目もりを付ける。"""
import json, sys, os, base64, html, subprocess, numpy as np, soundfile as sf
d, title, lead, out = sys.argv[1:5]; lufs = sys.argv[sys.argv.index("--lufs") + 1] if "--lufs" in sys.argv else "-16"
L = json.load(open(os.path.join(d, "j", "list.json"))); os.makedirs(os.path.join(d, "mp3"), exist_ok=True); quiet = []; rows = {}
for e in L:
    w = os.path.join(d, "o", f"t{e['no']:02d}.wav")
    if not os.path.exists(w): quiet.append((e["no"], e["name"], "書き出せなかった")); continue
    y, sr = sf.read(w); m = y.mean(1) if y.ndim > 1 else y; rms = 20 * np.log10(max(1e-9, float(np.sqrt(np.mean(m ** 2)))))
    S = np.abs(np.fft.rfft(m * np.hanning(len(m)))) ** 2; f = np.fft.rfftfreq(len(m), 1 / sr); tot = S[(f >= 30) & (f < 12000)].sum() + 1e-12
    e["hi"] = float(10 * np.log10(S[(f >= 2500) & (f < 12000)].sum() / tot + 1e-12)); e["lo"] = float(10 * np.log10(S[(f >= 30) & (f < 250)].sum() / tot + 1e-12)); e["rms"] = rms
    if rms < -45: quiet.append((e["no"], e["name"], f"{rms:.0f}dB"))
    mp = os.path.join(d, "mp3", f"t{e['no']:02d}.mp3"); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", w, "-af", f"loudnorm=I={lufs}:TP=-1.5:LRA=20", "-ac", "2", "-b:a", "112k", mp])
    rows[e["no"]] = "data:audio/mpeg;base64," + base64.b64encode(open(mp, "rb").read()).decode()
his = [e["hi"] for e in L if "hi" in e]; los = [e["lo"] for e in L if "lo" in e]
bar = lambda v, arr: max(4, min(100, round((v - min(arr)) / (max(arr) - min(arr) + 1e-9) * 100)))
body = ""; groups = []
for e in L:
    if e["group"] not in groups: groups.append(e["group"])
for g in groups:
    body += f'<section><h2>{html.escape(g)}</h2><ol>'
    for e in [x for x in L if x["group"] == g and x["no"] in rows]:
        body += f'''<li><button class="play" data-n="{e["no"]}" aria-label="{e["no"]}番を再生">▶</button><div class="txt"><p class="name"><span class="no">{e["no"]:02d}</span>{html.escape(e["name"])}</p><p class="desc">{html.escape(e["desc"])}</p></div>
<div class="meters" aria-hidden="true"><span>明るさ</span><i><b style="width:{bar(e["hi"], his)}%"></b></i><span>低音</span><i><b style="width:{bar(e["lo"], los)}%"></b></i></div></li>'''
    body += '</ol></section>'
page = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root{{--bg:#f6f4ef;--fg:#1d1b18;--mute:#6b665d;--line:#d9d4c8;--card:#fffdf8;--acc:#b4431f;--bar:#c9c2b2}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#171512;--fg:#ece7dc;--mute:#a39c8e;--line:#35312a;--card:#1f1c18;--acc:#ef8354;--bar:#4a453b;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#171512;--fg:#ece7dc;--mute:#a39c8e;--line:#35312a;--card:#1f1c18;--acc:#ef8354;--bar:#4a453b;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:15px/1.6 "Hiragino Sans","Yu Gothic UI","Noto Sans JP",system-ui,sans-serif;padding-block:28px 60px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
main{{max-width:760px;margin:0 auto;display:flex;flex-direction:column;gap:28px}}
h1{{font-size:26px;line-height:1.3;margin:0;text-wrap:balance}}
.lead{{color:var(--mute);margin:8px 0 0;max-width:60ch}}
h2{{font-size:13px;letter-spacing:.06em;color:var(--mute);font-weight:600;margin:0 0 8px;border-bottom:1px solid var(--line);padding-bottom:6px}}
ol{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}}
li{{display:flex;align-items:center;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 12px;flex-wrap:wrap}}
li.on{{border-color:var(--acc)}}
.play{{flex:none;width:42px;height:42px;border-radius:50%;border:1.5px solid var(--acc);background:transparent;color:var(--acc);font-size:15px;cursor:pointer}}
li.on .play{{background:var(--acc);color:var(--bg)}}
.play:focus-visible{{outline:2px solid var(--fg);outline-offset:2px}}
.txt{{flex:1 1 240px;min-width:0}}
.name{{margin:0;font-weight:600;overflow-wrap:anywhere}} .no{{font-variant-numeric:tabular-nums;color:var(--acc);margin-right:8px}}
.desc{{margin:0;color:var(--mute);font-size:13px}}
.meters{{flex:none;display:grid;grid-template-columns:auto 70px;gap:2px 6px;align-items:center;font-size:11px;color:var(--mute)}}
.meters i{{display:block;height:5px;background:var(--bar);border-radius:3px;overflow:hidden}} .meters b{{display:block;height:100%;background:var(--acc)}}
.note{{color:var(--mute);font-size:13px;margin:0}}
</style></head><body><main>
<header><h1>{html.escape(title)}</h1><p class="lead">{html.escape(lead)} ▶ を押すと鳴り、もう一度押すと止まります。</p></header>
{body}
<p class="note">「明るさ」は 2.5kHz より上の音の多さ、「低音」は 250Hz より下の音の多さを、このページの中でくらべた目もりです。耳では確かめていない見本です。</p>
</main>
<script>
const A={json.dumps(rows)};
let cur=null,curBtn=null;
function stop(){{if(cur){{cur.pause();cur=null}}if(curBtn){{curBtn.textContent="▶";curBtn.closest("li").classList.remove("on");curBtn=null}}}}
document.querySelectorAll(".play").forEach(b=>b.addEventListener("click",()=>{{
  const same=curBtn===b;stop();if(same)return;
  const a=new Audio(A[b.dataset.n]);cur=a;curBtn=b;b.textContent="■";b.closest("li").classList.add("on");
  a.addEventListener("ended",()=>{{if(cur===a)stop()}});a.play().catch(()=>stop());
}}));
</script></body></html>'''
os.makedirs(os.path.dirname(out), exist_ok=True); open(out, "w", encoding="utf-8").write(page)
print(f"{len(rows)}/{len(L)} 種類・{len(page) / 1e6:.1f}MB → {out}"); print("音が小さい・出ていない:", quiet or "なし")
for e in L:
    if "rms" in e: print(f"  {e['no']:02d} {e['name'][:28]:30s} {e['rms']:6.1f}dB 明るさ {e['hi']:6.1f} 低音 {e['lo']:6.1f}")
