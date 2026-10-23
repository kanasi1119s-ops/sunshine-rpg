# ラウド25曲（第2シリーズ）20「赦しの値段」（仮）。イメージ: 罪と罰×闇市（赦しを売る見世物小屋）。A 短調・120・5/4（2+3）。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: 木琴（シロフォン。呼びこみの口上・道化の笑い声）
# 物語: 見世物小屋の呼びこみ（木琴）が「赦し」を売る。一幕目・道化の笑い・二幕目・曲芸（タッピングと木琴とベースの掛け合い）・大団円・幕。
# 形（ほかの曲と変える）: 見世物小屋の幕ごとの構成。区間の境目に木琴の「笑い」が入る。5拍子のゆがんだ回転木馬
# しかけ:
#   - 看板リフ: 2+3 の5拍子で、A のペダルから半音でにじる（回転木馬が少しずつ傾く）
#   - ベースは旋律（Aメロの下で歌い、曲芸の場面でベースが主役の小節がある）
#   - サビ6小節目に B♭（♭Ⅱ）で一瞬の救い
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 120, 5
bar = Bars(BEATS)
R5 = bar.rest()

FORM = [("intro", 6), ("verse", 8), ("chorus", 8), ("laugh", 4), ("inter", 6), ("verse2", 8), ("pre", 4), ("chorus2", 8),
        ("circus", 12), ("chorus3", 8), ("curtain", 4)]
VERSE = ["Am", "Dm/A", "Am", "E7", "Fmaj7", "Dm", "E7", "Am"]
CHORUS = ["C", "G/B", "Am", "E/G#", "F", "Bb", "Dm", "E7"]
CH = {"intro": ["Am", "Am", "Am", "F", "Am", "E7"], "verse": VERSE, "chorus": CHORUS, "laugh": ["Am", "Am", "E7", "E7"],
      "inter": ["Am", "Am", "F", "E7", "Am", "E7"], "verse2": VERSE, "pre": ["Dm", "Bm7b5", "F", "E7"], "chorus2": CHORUS,
      "circus": ["Am", "E7", "Am", "E7", "Dm", "Am", "Bb", "E7", "Am", "Dm", "E7", "Am"], "chorus3": CHORUS, "curtain": ["Am", "Am", "Am", "A5"]}
song = Song("赦しの値段（仮）",
            "仮: ラウド25曲（第2シリーズ）の20曲目。イメージは罪と罰×闇市（赦しを売る見世物小屋）。A 短調・120・5/4（2+3）。木琴の呼びこみと道化の笑い、半音でにじる回転木馬のリフ、"
            "ベースは旋律、曲芸の場面はタッピングと木琴とベースの掛け合い、サビは B♭（♭Ⅱ）の救い。別の楽器は木琴。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 見世物小屋の呼びこみが赦しを売る。一幕目・道化の笑い・二幕目・曲芸・大団円・幕。"
song.kinds = {"laugh": "break", "circus": "solo", "curtain": "outro"}
SECS, NB = song.secs, song.nb

RIFF = {"Am": [bar("A1:0.5! A2:0.5 G#2:0.5 A2:0.5", "A1:0.5! E2:0.5 F2:0.5 E2:0.5 D2:0.5 C2:0.5"),
               bar("A1:0.5! A2:0.5 G#2:0.5 A2:0.5", "A1:0.5! C2:0.5 D2:0.5 D#2:0.5 E2:1")],
        "F": [bar("F1:0.5! F2:0.5 E2:0.5 F2:0.5", "F1:0.5! C2:0.5 D2:0.5 C2:0.5 A1:0.5 G#1:0.5")] * 2,
        "E7": [bar("E2:0.5! E3:0.5 D3:0.5 E3:0.5", "E2:0.5! G#2:0.5 B2:0.5 D3:0.5 F3:0.5 E3:0.5")] * 2}
XY_BARKER = [bar("E5:0.25 F5:0.25 F#5:0.25 G5:0.25 G#5:0.5 A5:0.5", "E5:0.5 C5:0.5 A4:0.5 G#4:0.5 A4:1"),
             bar("E5:0.25 F5:0.25 F#5:0.25 G5:0.25 G#5:0.5 A5:0.5", "C6:0.5 B5:0.5 A5:0.5 E5:0.5 A5:1")]


def laugh(top="A6", beats_len=5):
    """道化の笑い: 6連で半音ずつ下りる"""
    n = int(beats_len * 6)
    m0 = midi(top)
    return fix_len(" ".join(f"{nm(m0 - j)}:{1 / 6:.4f}{'!' if j % 6 == 0 else ''}" for j in range(n)), beats_len)


VERSE_MEL = [bar("R:1 E4:0.5 A4:0.5", "C5:1 B4:0.5 A4:0.5 E4:1"), bar("F4:1 A4:1", "D5:2 C5:1"), bar("R:0.5 C5:0.5 E5:0.5 D5:0.5", "C5:2 A4:1"),
             bar("G#4:1 B4:1", "D5:2 B4:1"), bar("A4:1 C5:1", "F5:2 E5:1"), bar("D5:1 F5:1", "A4:3"), bar("G#4:1 B4:1", "E5:1 D5:1 B4:1"), bar("A4:2", "R:3")]
VERSE2_MEL = [bar("R:1 A4:0.5 C5:0.5", "E5:1 D5:0.5 C5:0.5 A4:1"), bar("A4:1 D5:1", "F5:2 E5:1"), bar("R:0.5 E5:0.5 A5:0.5 G5:0.5", "E5:2 C5:1"),
              bar("B4:1 D5:1", "G#5:2 E5:1"), bar("C5:1 F5:1", "A5:2 G5:1"), bar("F5:1 A5:1", "D5:3"), bar("B4:1 D5:1", "G#5:1 E5:1 D5:1"), bar("C5:2", "R:3")]
PRE_MEL = [bar("F5:1 A5:1", "D5:3"), bar("F5:1 A5:1", "B5:2 A5:1"), bar("C6:1 A5:1", "F5:3"), bar("E5:1 G#5:1", "B5:1 R:2")]
CHORUS_MEL = [bar("E5:1 G5:1", "C6:2! D6:1"), bar("D6:1 B5:1", "G5:3"), bar("A5:1 C6:1", "E6:2! C6:1"), bar("B5:1 G#5:1", "E5:3"),
              bar("F5:1 A5:1", "C6:2 A5:1"), bar("D6:1 A#5:1", "F5:3!"), bar("A5:1 F5:1", "D6:2 C6:1"), bar("B5:2", "G#5:2 R:1")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("D6:1 G5:1", "B5:3")
CHORUS2_MEL[5] = bar("A#5:1 D6:1", "F6:3!".replace("F6", "A#5"))
CHORUS3_MEL = [bar("C6:5!"), bar("B5:2", "D6:3"), bar("C6:5!"), bar("B5:2", "G#5:3")] + CHORUS_MEL[4:6] + [bar("D6:1 F6:1".replace("F6", "A5"), "D6:3"), bar("E6:2!", "B5:3")]
VERSE_BASS = [bar("A1:1! C2:1", "E2:1 D2:0.5 C2:0.5 B1:1"), bar("A1:1 D2:1", "F2:2 E2:1"), bar("A1:1 E2:1", "A2:1 G2:1 E2:1"), bar("E2:1 G#2:1", "B2:2 G#2:1"),
              bar("F1:1 C2:1", "F2:1 E2:1 C2:1"), bar("D2:1 F2:1", "A2:2 D2:1"), bar("E2:1 B1:1", "G#1:1 B1:1 E2:1"), bar("A1:2", "E2:1 G#1:1 A1:1")]
CIRCUS = {"tap": {"Am": ["A4", "C5", "E5"], "E7": ["G#4", "B4", "E5"], "Dm": ["A4", "D5", "F5"], "Bb": ["A#4", "D5", "F5"]}}

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "tap", "xylo", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"


def g20(*pos, ch="X", base=None):
    return kit.grid(pos, ch, base)


RIDE23 = f"{BELL}:1! {RIDE}:1 {BELL}:1! {RIDE}:1 {RIDE}:1"

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    rf = R5
    if name in ("intro", "inter") and not (name == "intro" and i < 2):
        rf = RIFF[base_ch if base_ch in RIFF else "Am"][i % 2]
    elif name == "curtain" and last:
        rf = bar("A1:5!")
    P["riff"].append(rf)

    s = si = R5
    if name in ("verse", "verse2") and (i >= 4 or name == "verse2"):
        s = bar(f"{groot}:2 {groot}:3") if not last else bar(f"{groot}:2! R:3")
    elif name == "pre":
        s = bar(f"{groot}:2! {groot}:3") if not last else bar(f"{groot}:2! R:3")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: s = bar(f"{groot}:5!")
        elif last and name != "chorus3": s = bar(f"{groot}:2! R:3")
        else: s = bar(f"{groot}:2! {groot}:1.5 {groot}:1.5")
        si = s if not (name == "chorus3" and i < 4) else R5
    elif name == "circus":
        s = bar(f"{groot}:5") if i % 4 < 2 else R5
    elif name == "curtain" and last:
        s = si = bar("A2:5!")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = tapn = xy = R5
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name == "pre": lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 4: harm8 = shift_oct(strip_marks(lead), -1)
    if name == "intro":
        xy = XY_BARKER[i % 2] if i < 4 else R5
        if i < 2: tapn = bar(tap(CIRCUS["tap"]["Am"], 5, pattern=(2, 1, 0, 1)))
    elif name == "laugh":
        xy = bar(laugh("A6", 5)) if i % 2 == 0 else R5
    elif name == "inter":
        xy = XY_BARKER[i % 2] if i >= 2 else R5
    elif name == "circus":
        # 曲芸: 4小節ごとに タッピング → 木琴 → ベース が主役
        if i % 4 == 0: tapn = bar(tap(CIRCUS["tap"][ch], 4, pattern=(2, 1, 0, 1)), f"{CIRCUS['tap'][ch][2]}:1")
        elif i % 4 == 1: xy = bar(laugh("E6", 2), {"E7": "G#5:0.5 E5:0.5 D5:0.5 B4:1.5", "Am": "A5:0.5 E5:0.5 C5:0.5 A4:1.5"}.get(ch, "A5:0.5 F5:0.5 D5:0.5 A4:1.5"))
        elif i % 4 == 3: tapn = bar(tap(CIRCUS["tap"][ch], 3, pattern=(2, 0, 1, 0)), f"{CIRCUS['tap'][ch][1]}:2")
    elif name == "curtain":
        xy = bar(laugh("C7", 5)) if i < 2 else (bar(laugh("A6", 3), "R:2") if i == 2 else bar("A5:5"))
    elif name == "chorus3" and i >= 4:
        xy = shift_oct(strip_marks(lead), 0) if False else R5
    P["lead"].append(lead); P["harm8"].append(harm8); P["tap"].append(tapn); P["xylo"].append(xy)

    if name in ("intro", "inter"):
        b = unison_low(P["riff"][-1], -1, "B0") if P["riff"][-1] != R5 else bar("A1:2 A1:3")
    elif name in ("verse", "verse2"): b = VERSE_BASS[i]
    elif name == "pre": b = bar(" ".join(f"{root}:0.5{'!' if j in (0, 4) else ''}" for j in range(10))) if not last else bar(f"{root}:1! {root}:1 R:3")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: b = bar(f"{root}:2! {root}:3")
        elif last and name != "chorus3": b = bar(f"{root}:2! R:3")
        else:
            toks = [f"{root}:0.5{'!' if j in (0, 4) else ''}" for j in range(10)]
            if root_note(nxt) != root: toks[-1] = f"{approach_note(ch, nxt)}:0.5"
            b = bar(" ".join(toks))
    elif name == "laugh": b = bar(f"{root}:2 {fifth_of(base_ch)}:3")
    elif name == "circus":
        if i % 4 == 2:
            # ベースが主役の小節（旋律）
            tones = chord_tones(ch, root, up(root, 2))
            b = bar(" ".join(f"{tones[j % len(tones)]}:0.5{'!' if j == 0 else ''}" for j in (0, 1, 2, 3, 4, 3, 2, 1, 2, 0)))
        else: b = bar(f"{root}:2! {fifth_of(base_ch)}:1.5 {up(root, 1)}:1.5")
    elif name == "curtain": b = bar("A1:5!") if last else R5
    else: b = R5
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    if name in ("intro", "inter"):
        if name == "intro" and i < 2:
            cym = f"{BELL}:1 {BELL}:1 {BELL}:1 {BELL}:1 {BELL}:1" if i == 0 else f"{BELL}:1 {BELL}:1 R:3"
            if i == 1: tom = "R:2 " + tom_triplets_down(3)
        else:
            k = g20(0, 8, 14); s = g20(4, 12, 18); s = g20(*[p for p in (7, 17) if k[p] == "."], ch="o", base=s)
            cym = RIDE23
            if (name == "intro" and i == 2) or (name == "inter" and i == 0): cym = f"{CR}:1! " + RIDE23.split(" ", 1)[1]
            if last: k, s, tom = linear_fill(kit, 3, i); k = g20(0, base=k); s = g20(4, base=s); cym = None
    elif name in ("verse", "verse2"):
        # 5拍子のリニア（手と足が重ならない）
        k = [g20(0, 6, 8, 14), g20(0, 3, 8, 15), g20(0, 6, 8, 11, 14), g20(0, 8, 10, 16)][i % 4]
        s = g20(4, 12, 18)
        h = "".join("." if (k[j] != "." or s[j] != ".") else ("x" if j % 2 == 0 else "o") for j in range(20)) if name == "verse2" else None
        if name == "verse": cym = RIDE23
        if i == 0: cym = f"{CR2}:1! " + (RIDE23.split(" ", 1)[1] if name == "verse" else "R:4"); h = h and ("...." + h[4:])
        if last: k, s, tom = linear_fill(kit, 3, idx); k = g20(0, base=k); s = g20(4, base=s); h = None; cym = None
    elif name == "pre":
        k = [g20(0, 8), g20(0, 4, 8, 12, 16), g20(*range(0, 20, 2)), g20(*range(0, 12))][i]
        s = [g20(8), g20(4, 12, 18), g20(4, 12, 18), g20(12, 14, 16, 18)][i]
        h = [g20(*range(0, 20, 2), ch="x"), g20(*range(0, 20, 2), ch="x"), g20(*range(0, 20), ch="x"), None][i]
        if i == 0: cym = f"{CR2}:2! R:3"
        if i == 3: cym = f"{CHINA}:1! {CHINA}:1 {CHINA}:1! R:2"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 4
        if half:
            k = g20(0, 10); s = g20(8)
            cym = f"{CR}:2! {RIDE}:1 {RIDE}:1 {RIDE}:1" if i == 0 else f"{RIDE}:1! {RIDE}:1 {BELL}:1! {RIDE}:1 {RIDE}:1"
        else:
            k = [g20(0, 3, 8, 11, 14), g20(0, 3, 8, 14, 17)][i % 2]
            s = g20(4, 12, 18)
            h = "".join("X" if j in (0, 8) else ("x" if j % 2 == 0 else ".") for j in range(20))
            h = "".join("." if s[j] == "X" else c for j, c in enumerate(h))
            if i % 4 == 0: cym = (f"{CR}:1! " if i % 8 == 0 else f"{CR2}:1! ") + "R:4"; h = "...." + h[4:]
            if i == 5: cym = f"{CR}:1! R:4"; h = "...." + h[4:]
        if last and name != "chorus3":
            k, s, tom = linear_fill(kit, 3, 2); k = g20(0, base=k); s = g20(4, base=s); h = None; cym = None
        if name == "chorus3" and last:
            k, s, tom = linear_fill(kit, 3, 3); k = g20(0, base=k); s = g20(4, base=s); h = None; cym = None
    elif name == "laugh":
        k = g20(0) ; cym = f"{BELL}:2 {BELL}:3," if i % 2 == 0 else None
        if last: tom = "R:2 " + tom_triplets_down(3)
    elif name == "circus":
        k = "".join("X" if j % 2 == 0 else "x" for j in range(20)) if i % 4 == 0 else g20(0, 8, 14)
        s = g20(4, 12, 18) if i % 4 != 2 else g20(8)
        k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        cym = RIDE23
        if i % 4 == 0: cym = f"{CR}:1! " + RIDE23.split(" ", 1)[1]
        if last: k, s, tom = linear_fill(kit, 3, 1); k = g20(0, base=k); s = g20(4, base=s); cym = None
    elif name == "curtain":
        cym = f"{BELL}:1 {BELL}:1, {BELL}:1, {BELL}:1, {BELL}:1," if i < 2 else None
        if last: k = g20(0); s = g20(0); cym = f"{CR}:5!"
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx.startswith("chorus"): FX.append(bar("R:3 C4:2"))
    else: FX.append(R5)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tap"), role="タッピングのギター", vol=0.11, pan=0.05))
song.add(part("木琴", "xylophone", J("xylo"), volume=0.14, pan=-0.25, reverb=0.3, attack=0.002, release=0.4,
              fx=[{"type": "eq", "low": 0, "mid": 1, "midHz": 2500, "high": -1}, {"type": "plate", "mix": 0.18}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "deep-scoop-djent"
add_layer(song, "organ", "カーニバルの回る木馬のオルガン。")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-20-yurushi.json"
    song.write(out)
    check_clash(song)
