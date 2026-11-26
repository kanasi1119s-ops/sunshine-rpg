#!/usr/bin/env python3
"""ギターの音の種類の見本を、同じフレーズ（自作・4小節）で書き出すための JSON を作る（2026-11-26 人間「ギターの音の種類を40種類ぐらい出して」）。
使い方: python3 tools/vt3/guitar_tone_gallery.py <出力フォルダ>   → 01.json〜40.json と list.json（番号・名前・説明）
フレーズ: 1〜2小節＝左右のギターで根音と5度を8分のダウン（D → G）、3〜4小節＝単音の旋律（Bm → A）。テンポ 160。ギターだけ（ドラム・ベースなし）。"""
import json, sys, os
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
P8 = lambda n: " ".join(f"{n}:0.5%{104 if k % 4 == 0 else 96 if k % 2 == 0 else 86}" for k in range(8))
RH = [("6弦", f"{P8('D3')} {P8('G2')} R:8"), ("5弦", f"{P8('A3')} {P8('D3')} R:8"), ("4弦", f"{P8('D4')} {P8('G3')} R:8")]
LEAD = "R:8 B4:0.5%104 D5:0.5%90 F#5:1%104 E5:0.5%92 D5:0.5%88 C#5:1%100 A4:0.5%104 C#5:0.5%90 E5:1.5%106 D5:0.5%90 C#5:1%98"
V = []
def add(name, desc, spec, di="emily", inst="distGuitar", lead=None): V.append((name, desc, spec, di, inst, lead))
T = lambda t, **k: {"guitarTone": t, "ampGate": 0.5, **k}
add("jpop-rock-drive", "J-POP のギターロックの歪み（浅め・和音が聞こえる）。v5 の伴奏の音", T("jpop-rock-drive"))
add("marshall-mid", "マーシャル系の中くらいの歪み（中域が前）", T("marshall-mid"))
add("melodic-punk", "メロディックパンク（マーシャル系・中域が前）", T("melodic-punk"))
add("loud-mid", "ラウドロック B: 中くらいの歪み", T("loud-mid"))
add("loud-mid-hs", "ラウドロック B・左ハムバッカー／右シングルコイル", T("loud-mid-hs"))
add("loud-mid-b", "ラウドロック D: 別のハイゲインを絞った歪み", T("loud-mid-b"))
add("loud-high", "ラウドロック A: ハイゲイン（締まった壁）", T("loud-high"))
add("loud-builtin", "ラウドロック C: 内蔵アンプの太い歪み", T("loud-builtin"))
add("modern-metalcore", "現代のメタルコア（明るく広い）", T("modern-metalcore"))
add("nu-metal-wall", "2000年代のニューメタル（平らで太い壁）", T("nu-metal-wall"))
add("electro-rock", "エレクトロとロックの混ざったリフ（中域が太い・乾いた音）", T("electro-rock"))
add("warm-lead-a", "響く温かいリード（浅い歪み・中域が太い）。v5 のリードの音", {"guitarTone": "warm-lead-a"})
add("warm-lead-b", "こもった軽い歪みのリード（丸いキャビネット）", {"guitarTone": "warm-lead-b"})
add("bmth-lead", "電子音と混ざる明るいリード（高めの歪み＋1オクターブ上＋やまびこ）", {"guitarTone": "bmth-lead"})
add("jpop-rock-drive・歪み浅く", "J-POP の歪みを、入力 0.2 に（かなり浅い）", T("jpop-rock-drive", ampDrive=0.2))
add("jpop-rock-drive・歪み深く", "J-POP の歪みを、入力 0.6 に", T("jpop-rock-drive", ampDrive=0.6))
add("marshall-mid・歪み浅く", "マーシャルを、入力 0.4 に", T("marshall-mid", ampDrive=0.4))
add("marshall-mid・歪み中", "マーシャルを、入力 0.7 に", T("marshall-mid", ampDrive=0.7))
add("melodic-punk・歪み浅く", "メロディックパンクを、入力 0.5 に", T("melodic-punk", ampDrive=0.5))
add("loud-mid・歪み浅く", "ラウドロック B を、入力 0.25 に", T("loud-mid", ampDrive=0.25))
add("jpop-rock-drive・グリーンバック", "J-POP の歪み＋キャビネットを Greenback 4x12 に（左右とも）", T("jpop-rock-drive", ampCabIr="jd-greenback-4x12-01", double={"irR": "jd-greenback-4x12-02"}))
add("jpop-rock-drive・V30 締まり", "J-POP の歪み＋キャビネットを V30 2x12（締まった置き方）に", T("jpop-rock-drive", ampCabIr="dd-v30-2x12-mix-tight", double={"irR": "dd-v30-2x12-mix-balanced"}))
add("jpop-rock-drive・重いキャビ", "J-POP の歪み＋キャビネットを重い 4x12 に", T("jpop-rock-drive", ampCabIr="jd-brutal-4x12-03", double={"irR": "jd-brutal-4x12-05"}))
add("jpop-rock-drive・V30 深い", "J-POP の歪み＋キャビネットを V30 2x12（深い置き方）に", T("jpop-rock-drive", ampCabIr="dd-v30-2x12-mix-deep", double={"irR": "dd-v30-2x12-mix-balanced"}))
add("jpop-rock-drive・別のギター", "J-POP の歪み＋録音のギターを別の1本（fsbs）に", T("jpop-rock-drive"), di="fsbs")
add("marshall-mid・別のギター", "マーシャル＋録音のギターを別の1本（fsbs）に", T("marshall-mid"), di="fsbs")
add("アンプの型なし・浅い歪み", "「ガラスごしブーケ」で OK が出た音（アンプの型なし・録音のギター）", {"release": 0.9})
for a, d in (("overdrive", "オーバードライブ"), ("distortion", "ディストーション"), ("hardrock", "ハードロック"), ("blues", "ブルース（軽い歪み）"), ("fuzz", "ファズ"), ("shoegaze", "シューゲイザー（歪み＋広い残響）"),
             ("loudrock", "ラウドロック（内蔵アンプ）"), ("metal", "メタル（内蔵アンプ）"), ("modernHigh", "現代的な高ゲイン（締まった低音）"), ("prs", "PRS 系")):
    add(f"内蔵アンプ {a}", f"作曲ソフトの内蔵アンプ「{d}」（録音のギターなし＝シンセのギター）", {"amp": a}, di=None)
add("クリーン jpopClean", "J-POP のクリーン（歪みなし・粒をそろえる）", {"amp": "jpopClean"}, di=None, inst="guitar")
add("クリーン crystal", "透き通るクリーン（耳にやさしい明るさ）", {"amp": "crystal"}, di=None, inst="guitar")
add("クリーン sparkleClean", "きらびやかなクリーン", {"amp": "sparkleClean"}, di=None, inst="guitar")
lst = []
for i, (name, desc, spec, di, inst, lead) in enumerate(V, 1):
    base = {"instrument": inst, "chorus": 0, "humanPitch": 0, "noScoop": True}
    parts = [{"role": f"左 {s}", **base, "volume": 0.07, "pan": -0.6, **spec, "notes": n} for s, n in RH] + [{"role": f"右 {s}", **base, "volume": 0.065, "pan": 0.6, **spec, "notes": n} for s, n in RH]
    parts.append({"role": "旋律", **base, "volume": 0.2, "pan": 0.0, **spec, "notes": LEAD})
    js = {"title": f"t{i:02d}", "description": f"ギターの音の見本 {i:02d}: {name}", "bpm": 160, "beats": 4, "barsPerChord": 1, "repeats": 1, "chords": "D G Bm A", "autoAccompaniment": False, "tone": "rock", "human": 0.2, "autoScoop": False, "guitarWobble": False, "parts": parts}
    if di: js["diGuitar"] = di
    json.dump(js, open(os.path.join(out, f"t{i:02d}.json"), "w", encoding="utf-8"), ensure_ascii=False); lst.append({"no": i, "name": name, "desc": desc, "di": di or "なし"})
json.dump(lst, open(os.path.join(out, "list.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1); print(len(lst), "種類")
