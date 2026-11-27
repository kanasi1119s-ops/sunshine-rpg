#!/usr/bin/env python3
"""音の種類の見本を、同じフレーズ（自作）で書き出すための JSON を作る（2026-11-27 人間「ベースの音の種類も40種類ぐらいだして。スラップも含めて」「キーボードとシンセ、FXも40種類だして」）。
使い方: python3 tools/vt3/sound_gallery.py bass|keys|fx <出力フォルダ>   → t01.json… と list.json（番号・名前・説明・書き出しのフラグ）
ギターの見本は tools/vt3/guitar_tone_gallery.py。"""
import json, sys, os
kind, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True); V = []
NM = lambda m: "C C# D D# E F F# G G# A A# B".split()[m % 12] + str(m // 12 - 1)
def add(group, name, desc, parts, flags="", bpm=112, chords="Em Em Am B7", extra=None): V.append((group, name, desc, parts, flags, bpm, chords, extra or {}))

if kind == "bass":
    FING = "E2:0.5! E2:0.5 R:0.25 E2:0.25 G2:0.5 A2:0.5 B2:0.5! D3:0.5 E3:0.5 E2:0.75! E2:0.25 R:0.5 D2:0.5 E2:1! G2:0.5 B2:0.5"
    SLAP = "A1:0.5! A2:0.25! A2:0.25 R:0.25 A1:0.25 G2:0.5 A1:0.5! A2:0.5! C3:0.5 D3:0.5 B1:0.5! B2:0.25! B2:0.25 R:0.25 B1:0.25 A2:0.5 B2:1! D#3:0.5! F#3:0.5"
    N = FING + " " + SLAP
    ROCK = lambda d: {"amp": "bassSplit", "ampDrive": d, "fx": [{"type": "eq", "low": 0, "mid": 4, "midHz": 900, "high": 0}, {"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 2}]}
    def b(spec=None, inst="bass"): return [{"role": "ベース", "instrument": inst, "volume": 0.22, "pan": 0, **(spec or {}), "notes": N}]
    for k, d in ((None, "標準のエレキベース（音源の指定なし）"), ("finger", "指弾き（FreePats の録音）"), ("pick", "ピック弾き"), ("rock", "ロック用"), ("metal", "メタル用"), ("jazz", "ジャズ用のエレキ"), ("jpop", "J-POP 用"),
                 ("growly", "うなるジャズベース（Karoryfer）"), ("bnb", "5弦ベースの指弾き（強さ4層の録音）"), ("bnb-loud", "同じ5弦ベースを、明るくゴリッと"), ("upright", "ウッドベース（ピチカート）"), ("rubner", "ジャズのウッドベース（指弾き）")):
        add("録音のベース（音源ちがい）", k or "標準", d, b(), f"--bass {k}" if k else "")
    add("録音のベース＋アンプ", "bnb-loud＋アンプ（歪み 0.3）", "「終電バイバイ」のベース。2つに分けて歪ませるアンプ", b(ROCK(0.3)), "--bass bnb-loud")
    add("録音のベース＋アンプ", "bnb-loud＋アンプ（歪み 0.55）", "バンド曲の標準の歪み", b(ROCK(0.55)), "--bass bnb-loud")
    add("録音のベース＋アンプ", "bnb＋アンプ（歪み 0.4）", "明るくしていない5弦ベースにアンプ", b(ROCK(0.4)), "--bass bnb")
    add("録音のベース＋アンプ", "pick＋アンプ（歪み 0.5）", "ピック弾きにアンプ", b(ROCK(0.5)), "--bass pick")
    add("録音のベース＋アンプ", "metal＋アンプ（歪み 0.7）", "メタル用に深い歪み", b(ROCK(0.7)), "--bass metal")
    add("録音のベース＋アンプ", "finger＋アンプ（歪み 0.3）", "指弾きに浅い歪み", b(ROCK(0.3)), "--bass finger")
    add("スラップ", "slap", "スラップベース（楽器 slap）", b(inst="slap"))
    add("スラップ", "slap＋アンプ（歪み 0.3）", "スラップに浅い歪みと中域", b(ROCK(0.3), inst="slap"))
    add("スラップ", "slapBass", "はじけるスラップ（シンセの音色 slapBass）", b({"patch": "slapBass"}))
    for pch, d in (("fretlessBass", "なめらかに歌うフレットレス"), ("acousticBass", "ウッド寄り"), ("synthBass1", "太く丸いシンセベース"), ("synthBass2", "硬くとがったシンセベース"), ("reeseBass", "うねるリースベース"),
                   ("modernBass", "現代的なシンセベース"), ("bassLead", "低音と旋律を兼ねる"), ("kfbSub", "低い正弦波のベース（Kawaii future bass）"), ("kfbFmBass", "はじく FM のベース"), ("kfbGrowlBass", "うなるベース"), ("kfbNeuroBass", "ねじれる暗いベース"),
                   ("surgeBassPasty", "ねばりのある太い"), ("surgeBassAnalogBassImaged", "アナログ風の広がる"), ("surgeBassCatBass", "うなる"), ("surgeBassWarmSquare", "あたたかい矩形波"), ("surgeBassEmulation", "本物のシンセベースのような"),
                   ("surgeBassPop", "はずむポップなベース"), ("surgeBassModernDirtyFat", "現代的に汚れて太い")):
        add("シンセのベース", pch, d, b({"patch": pch}))
    add("シンセのベース", "sub808", "808 の重低音（楽器 sub808）", b(inst="sub808"))
elif kind == "keys":
    CH = [("F4", "G4"), ("A4", "B4"), ("C5", "D5")]; RY = lambda a, c: f"{a}:1.5! {a}:0.5 R:0.5 {a}:0.5 {a}:1 {c}:2! {c}:1 {c}:1 R:8"
    MEL = "R:8 E5:0.5! G5:0.5 B5:1 A5:0.5 G5:0.5 E5:1 A5:1.5! G5:0.5 E5:1 C#5:1"
    def k(inst, spec=None): return [{"role": f"和音{i + 1}", "instrument": inst, "volume": 0.12, "pan": (-0.2, 0, 0.2)[i], **(spec or {}), "notes": RY(*CH[i])} for i in range(3)] + [{"role": "旋律", "instrument": inst, "volume": 0.2, "pan": 0, **(spec or {}), "notes": MEL}]
    KB = (("piano", None, "ピアノ"), ("keys", None, "エレピ"), ("fmEpiano", None, "FM のエレピ（すっきり丸い）"), ("keys", "popKeys", "ポップな鍵盤"), ("keys", "honkyTonk", "ホンキートンクのピアノ"), ("keys", "clavinet", "クラビネット（はじく鍵盤）"),
          ("keys", "vibraphone", "ビブラフォン"), ("drawbarOrgan", None, "ドローバーオルガン"), ("keys", "rockOrgan", "ロックのオルガン"), ("keys", "percussiveOrgan", "打つオルガン"), ("keys", "kfbGlassEp", "ガラスのようなエレピ"), ("keys", "kfbBoops", "ぽこぽこ鳴る FM の鍵盤"),
          ("keys", "kfbCharmOrgan", "かわいいオルガン"), ("keys", "surgeKeysDxEp", "FM のエレピ（Surge XT）"), ("keys", "surgeKeysFmPiano1", "FM のピアノ"), ("keys", "surgeKeysBellPiano", "ベルの混ざったピアノ"), ("keys", "surgeKeysAliasGlassPiano2", "ガラスのピアノ"), ("keys", "surgeKeysLightEp", "軽いエレピ"))
    for inst, pch, d in KB: add("キーボード", pch or inst, d, k(inst, {"patch": pch} if pch else None), bpm=120, chords="Dm7 G Em7 A")
    SY = (("squareLead", "丸く芯のある矩形波のリード"), ("sawLead", "明るくぎらつくノコギリ波のリード"), ("modernLead", "現代的なリード"), ("brightLead", "明るいリード"), ("popLeadClear", "すっきりしたポップなリード"), ("picoLead", "小さく鳴るリード"),
          ("kfbSquareLead", "矩形波のリード（Kawaii future bass）"), ("kfbDreamLead", "やわらかい電子のリード"), ("kfbFormantLead", "声のようなリード"), ("kfbTranceLead", "はじくトランスのリード"), ("kfbChipLead", "チップ風のリード"), ("kfbWobbleLead", "ゆれる中空のリード"),
          ("surgeTropics", "明るく抜けるリード（Surge XT）"), ("surgeHappySaws", "あたたかいノコギリ波の重ね"), ("kfbSupersaw", "厚いスーパーソウ"), ("kfbSupersawWide", "空気感を足したスーパーソウ"), ("kfbSawStab", "短く切れるノコギリ波の和音"), ("kfbSquarePluck", "明るい矩形波のプラック"),
          ("modernPluck", "現代的なプラック"), ("glassPluck", "ガラスのようにきらめくプラック"), ("modernPad", "現代的なパッド"), ("kfbSparklePad", "きらめくパッド"))
    for pch, d in SY: add("シンセ", pch, d, k("lead", {"patch": pch}), bpm=120, chords="Dm7 G Em7 A")
elif kind == "fx":
    def f(pch, key, L=2): return [{"role": "効果音", "instrument": "guitar", "patch": pch, "volume": 0.2, "pan": 0, "reverb": 0.1, "modulate": False, "notes": (f"{key}:{L} R:{4 - L} {key}:{L} R:{4 - L}" if L < 4 else f"{key}:4 {key}:4")}]
    for m, n, d in ((60, "bubble", "泡"), (61, "drop", "しずく"), (62, "sparkle-up", "きらめき（上がる）"), (63, "sparkle-down", "きらめき（下がる）"), (64, "squeak", "きゅっ"), (65, "boing", "ぴょん"), (66, "riser", "上がっていく音"), (67, "downer", "下がっていく音"),
                    (68, "revcym", "逆回しのシンバル"), (71, "clap", "手びょうし"), (72, "snap", "指パッチン"), (78, "hardkick", "硬いキック"), (79, "impact", "当たる音"), (80, "subdrop", "低く落ちる音"), (81, "laser", "レーザー"), (82, "vinyl", "レコードの針の音"), (87, "glitch", "グリッチ")):
        add("かわいい効果音（kawaiiFx）", n, d, f("kawaiiFx", NM(m), 4 if n in ("riser", "downer", "revcym", "subdrop", "vinyl") else 2), bpm=120, chords="C C")
    for m, n, d in ((60, "汽笛（短い）", "おもちゃの汽笛"), (61, "汽笛（2回）", "おもちゃの汽笛"), (62, "汽笛（下がる）", "おもちゃの汽笛"), (63, "玉入りの笛", "ホイッスル"), (65, "サイレンの笛", "うなる笛"), (67, "フレクサトーン", "ゆれる金属の音"), (69, "ラチェット", "ガラガラ"),
                    (71, "スラップスティック", "ぱちん"), (72, "ビブラスラップ", "カーッ"), (73, "ウインドチャイム（上がる）", "しゃらら"), (74, "ウインドチャイム（下がる）", "しゃらら"), (75, "フィンガーシンバル", "ちーん"), (76, "トライアングル", "ちーん")):
        add("おもちゃと小物（toysFx）", n, d, f("toysFx", NM(m), 4), bpm=120, chords="C C")
    for key, n, d in (("C4", "逆回しのクラッシュ", "音符の終わりに山が来る"), ("D4", "逆回しのチャイナ", "音符の終わりに山が来る"), ("E4", "シンバルのスウェル", "ロールでだんだん大きく")):
        add("本物のシンバルの効果音（cymbalFx）", n, d, f("cymbalFx", key, 4), bpm=120, chords="C C")
    add("そのほか", "fxRiser", "合成の上がっていく音", f("fxRiser", "C4", 4), bpm=120, chords="C C")
    add("そのほか", "impactHit", "映画の「ドン！」", [{"role": "効果音", "instrument": "impactHit", "patch": "impactHit", "volume": 0.2, "notes": "C2:4 C3:4"}], bpm=120, chords="C C")
    add("そのほか", "ギターのピックスクレイプ", "弦をピックでこする長い音（guitarFx）", f("guitarFx", "C2", 4), bpm=120, chords="C C")
    add("そのほか", "ギターのハーモニクス", "本物のナチュラルハーモニクス（guitarFx）", [{"role": "効果音", "instrument": "guitar", "patch": "guitarFx", "volume": 0.2, "notes": "E4:2 B4:2 E5:2 G#5:2"}], bpm=120, chords="C C")
    for key, n, d in (("F4", "風鈴", "季節の音"), ("E4", "雨", "季節の音"), ("D5", "花火", "季節の音")):
        add("季節の音（seasonFx）", n, d, f("seasonFx", key, 4), bpm=120, chords="C C")
lst = []
for i, (group, name, desc, parts, flags, bpm, chords, extra) in enumerate(V, 1):
    js = {"title": f"t{i:02d}", "description": f"音の見本 {kind} {i:02d}: {name}", "bpm": bpm, "beats": 4, "barsPerChord": 1, "repeats": 1, "chords": chords, "autoAccompaniment": False, "human": 0.15, "parts": parts, **extra}
    json.dump(js, open(os.path.join(out, f"t{i:02d}.json"), "w", encoding="utf-8"), ensure_ascii=False); lst.append({"no": i, "group": group, "name": name, "desc": desc, "flags": flags})
json.dump(lst, open(os.path.join(out, "list.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1); print(kind, len(lst), "種類")
