# ラウド26曲 09「Down Is the Only Way」（仮。もとの仮題「罰の階段」）。2026-10-24 素材から作り直し
# スタイル: グルーヴメタル＋バロックのパッサカリア（下りていく低音の上で変奏をくり返す）＋チェンバロ。C 短調・92・4/4
# 物語: 罪人が9段の階段を下りていく。1段ごとに罪がひとつ裁かれ、重くなる。いちばん下で判決の槌。
# 形: 9段（10小節ずつ）。低音が C → B → B♭ → A → A♭ → G → F♯ → F → E と半音ずつ下り続け（調は C 短調のまま）、その上で同じ主題を段ごとに変奏する。
#      02（同じ16小節ごと半音ずつ上がる）と違い、ここは調は変えず、低音だけが下りる。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   1段（0）: チェンバロの主題と低音だけ／2段（1）: クリーンのギター／3段（1）: ドラムが静かに、リードが主題の欠片
#   4段（2）: 重いうねりのリフ／5段（2）: リードが6度上の対旋律／6段（2→3）: 3連で迫る
#   7段（3）: 16分で砕ける／8段（3）: いちばん遅く重い（4分の1の速さの感じ）。リードは長い音で耐える
#   9段（3）: 主題が逆さに上る（最後の抵抗）→ 判決（全員の槌）
# 旋律の性格: 下りる主題の変奏（段ごとにリズムの細かさと区切り方を変える）。チェンバロと受け答え
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 92, 4
bar = Bars(BEATS)
R4 = bar.rest()

PEDAL = ["C", "B", "A#", "A", "G#", "G", "F#", "F", "E"]
STEP_CH = [["Cm", "Fm", "Cm", "Ab", "Cm", "Fm", "Cm", "Ab", "Cm", "Cm"],
           ["G", "G7", "G", "Bdim", "G", "G7", "G", "Bdim", "G", "G7"],
           ["Cm7", "Eb", "Cm7", "Gm", "Cm7", "Eb", "Gm", "Gm", "Cm7", "Eb"],
           ["F", "Am7b5", "F", "D7", "F", "Am7b5", "D7", "D7", "F", "Am7b5"],
           ["Ab", "Fm", "Ab", "Db", "Ab", "Fm", "Db", "Db", "Ab", "Fm"],
           ["G", "Cm", "G", "Eb", "G", "Cm", "G7", "G7", "G", "G7"],
           ["F#dim7", "D7", "F#dim7", "D7", "F#dim7", "D7", "F#dim7", "D7", "F#dim7", "D7"],
           ["Fm", "Fm", "Db", "Db", "Fm", "Fm", "Bbm", "Bbm", "Fm", "Fm"],
           ["C", "C", "Em", "Em", "C", "C", "Em", "Em", "C", "C"]]
FORM = [("door", 4)] + [(f"step{k + 1}", 10) for k in range(9)] + [("verdict", 6)]
CH = {"door": ["Cm"] * 4, "verdict": ["C5"] * 6, **{f"step{k + 1}": STEP_CH[k] for k in range(9)}}
song = Song("罰の階段（仮）",
            "仮: ラウド26曲の9曲目（2026-10-24 素材から作り直し）。グルーヴメタル＋バロックのパッサカリア＋チェンバロ。C 短調・92。"
            "低音が C から E まで半音ずつ9段下り続け、その上で同じ主題を段ごとに変奏する。最後は判決の槌。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 罪人が9段の階段を下り、1段ごとに罪が裁かれて重くなり、いちばん下で判決の槌が鳴る。"
song.kinds = {"door": "intro", "verdict": "outro", "step1": "intro", "step2": "verse", "step3": "verse", "step4": "pre", "step5": "chorus",
              "step6": "chorus", "step7": "break", "step8": "break", "step9": "chorus"}
SECS, NB = song.secs, song.nb

CMIN = scale_pcs("C", "harmonic")
# 段ごとの旋律のリズム（同じ形を続けない。段ごとに細かさと区切り方が変わる）
RH = {
    3: [[-1, 0.5, 0.5, 1, -1], [-0.5, 0.5, 0.5, 0.5, 2], [-2, 0.5, 0.5, 1]],
    4: [[-0.5, 0.75, 0.25, 0.5, 0.5, 1, -0.5], [0.75, 0.75, 0.5, -1, 0.5, 0.5], [-0.5, 0.5, 0.25, 0.25, 0.5, 1, -1]],
    5: [[0.5, 0.5, 0.5, 0.5, 1, -1], [-1, 0.5, 0.5, 0.5, 0.5, 1], [1, 0.5, 0.5, -0.5, 0.5, 1]],
    6: [[1 / 3] * 3 + [1, -1] + [1 / 3] * 3, [1, 1 / 3, 1 / 3, 1 / 3, 1, -1], [-1] + [1 / 3] * 6 + [1]],
    7: [[0.25] * 8 + [-2], [-1] + [0.25] * 8 + [-1], [0.25, 0.25, 0.5, 0.25, 0.25, 0.5, -2]],
    8: [[3, -1], [2, 2], [-1, 3]],
    9: [[0.5, 0.5, 1, 0.5, 0.5, 1], [-0.5, 0.5, 0.5, 0.5, 1, 1], [1, 1, 0.5, 0.5, -1]],
}
RH = {k: [[0.3333 if abs(abs(x) - 1 / 3) < 1e-6 else x for x in r] for r in v] for k, v in RH.items()}
# 主題: 下りる。9段目だけ逆さ（上る）
TOP = {3: ("G5", "C5"), 4: ("D#5", "G4"), 5: ("F5", "C5"), 6: ("E5", "G4"), 7: ("D5", "F4"), 8: ("C5", "G4"), 9: ("C4", "E5")}
LEAD = {}
for k, (a, b) in TOP.items():
    contour = (1, 1, -1, 1, 2) if k == 9 else ((-1, -1, -1, 2) if k != 7 else (-1, 1, -2, 1, -1))
    LEAD[k] = [bar(x) for x in melody_walk(CMIN, a, b, RH[k], k, STEP_CH[k - 1], contour=contour, lo="F3", hi="F#5")]
# チェンバロ: 右手は主題（下りる8分）と16分の分散、左手は下りる段
THEME = ["G5:0.5 F5:0.5 D#5:0.5 D5:0.5 C5:1 R:1", "D#5:0.5 D5:0.5 C5:0.5 B4:0.5 C5:1 R:1", "C5:0.5 A#4:0.5 G#4:0.5 G4:0.5 F4:1 R:1", "G4:0.5 G#4:0.5 B4:0.5 D5:0.5 C5:1 R:1"]


def hps_arp(ch, band=False):
    """チェンバロの分散和音。バンドが鳴っている所（band）は、歪んだギターとリードの帯域を避けて1オクターブ上（C5〜C7）で、8分に間引く
    （2026-10-24 人間「09 の 1:29 あたりの音の重なりが大分濁ってる」: 4段目からリフ・リード・チェンバロの16分・チェンバロの左手の低音が
    同じ中低域に重なっていた）"""
    t = chord_tones(ch.split("/")[0], "C5" if band else "C4", "C7" if band else "C6")[:4]
    while len(t) < 4: t.append(up(t[-3], 1))
    seq = [t[0], t[1], t[2], t[3], t[2], t[1]] * 3
    if band: return bar(" ".join(f"{n}:0.5" for n in seq[:8]))
    return bar(" ".join(f"{n}:0.25" for n in seq[:16]))


P = {k: [] for k in ["riff", "rhy", "lead", "clean", "hr", "hl", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = clean = hr = hl = R4
    if name == "door":
        hr = bar(THEME[i]); hl = bar("C3:4") if i % 2 == 0 else bar("C3:2 G2:2")
        b = R4
    elif name == "verdict":
        riff = rhy = bar("C2:1! R:3") if i < 3 else (bar("C2:0.5! C2:0.5! C2:1! R:2") if i == 3 else (bar("C2:4!") if i == 4 else R4))
        hr = bar("C5:4") if i == 5 else R4
        b = unison_low(riff, -1, "B0") if i < 5 else R4
    else:
        k = int(name[4:]); ped = PEDAL[k - 1]
        pg = {"C": "C2", "B": "B1", "A#": "A#1", "A": "A1", "G#": "G#1", "G": "G1", "F#": "F#1", "F": "F2", "E": "E2"}[ped]
        if k <= 2:
            th = THEME[i % 4] if k == 1 else THEME[i % 4].replace("C5:1", "B4:1").replace("D#5", "D5")   # 2段目（低音 B）は、主題の終わりを B に
            hr = bar(th) if i % 5 != 4 else hps_arp(ch)
        elif k == 3:
            hr = hps_arp(ch) if i % 2 == 0 else bar(THEME[i % 4])
        elif k == 4:
            hr = hps_arp(ch, True) if i % 2 == 0 else bar(shift_oct(THEME[i % 4], 1))
        elif k in (5, 6):
            hr = R4 if i % 2 == 0 else hps_arp(ch, True)    # リードと受け答え
        elif k == 9:
            hr = hps_arp(ch, True)
        # チェンバロの左手の低い音は、バンドが入ったら（4段目から）弾かない（ベースと同じ低い所で重なって濁る）
        hl = bar(f"{ped}3:2 {ped}2:2") if k <= 3 else R4
        if k >= 2: clean = bar(" ".join(f"{t}:1" for t in (chord_tones(ch.split('/')[0], 'G3', 'G4') * 2)[:4])) if k <= 3 else R4
        if k >= 3: lead = LEAD[k][i] if k in LEAD else R4
        if k >= 4:
            if k == 8:      # 4分の1の速さの感じ: 2小節に一撃
                riff = rhy = bar(f"{pg}:4!") if i % 2 == 0 else bar(f"R:2 {pg}:1! {pg}:0.5 R:0.5")
            elif k == 7:
                riff = rhy = bar(" ".join(f"{pg}:0.25{'!' if j % 3 == 0 else ''}" for j in range(16)))
            else:
                # 最後の音は半音上（♭2）だと、上の和音（F/A・D7/A など）の A とぶつかって濁るので、オクターブ上の低音へ
                #   途中の音も、短3度に決め打ちせず、上の和音にある音（3〜7半音上）を選ぶ（5・6段目で B と C、B♭ と B がぶつかっていた）
                cp = chord_pcs(ch.split("/")[0]); iv = next((d for d in (3, 4, 5, 7) if (midi(pg) + d) % 12 in cp), 7)
                riff = rhy = bar(f"{pg}:0.75! {pg}:0.25 R:0.5 {pg}:0.5! {tr(pg, iv)}:0.5 {pg}:0.5 R:0.5 {up(pg, 1)}:0.5")
        b = bar(f"{ped}1:4") if k <= 2 else (bar(f"{ped}1:2! {ped}1:2") if k != 7 else bar(" ".join(f"{ped}1:0.5{'!' if j % 2 == 0 else ''}" for j in range(8))))
        if k >= 4 and k != 7 and k != 8: b = unison_low(riff, -1, "B0")
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["clean"].append(clean); P["hr"].append(hr); P["hl"].append(hl); P["bass"].append(b)
    kit.add("X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
HPS = dict(reverb=0.35, attack=0.002, release=0.5, fx=[{"type": "eq", "low": -3, "mid": 0, "midHz": 1500, "high": 0}, {"type": "plate", "mix": 0.2}])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(clean_part(J("clean"), vol=0.07, pan=0.25, role="クリーンの和音"))
song.add(part("チェンバロ（右手）", "harpsichord", J("hr"), volume=0.12, pan=-0.2, **HPS))
song.add(part("チェンバロ（左手）", "harpsichord", J("hl"), volume=0.1, pan=-0.1, **HPS))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "dark-electro-rock"

from lm25_plans import apply_plan
apply_plan(song, "09")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-09-kaidan.json"
    song.write(out)
    check_clash(song)
