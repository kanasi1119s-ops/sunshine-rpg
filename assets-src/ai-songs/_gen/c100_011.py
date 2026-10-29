# ケルト・フルート100曲「銀の笛と百の夜」011 草を渡る風 Wind Through the Grass — 第3版（2026-10-30 作り直し。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第2章のはじまり。船を下りたエイラは、どこまでも続く草原を歩く。風が草をなでるたびに、草はいっせいに倒れて、また起きる。
#   遠くで羊飼いの子が吹くホイッスルが聞こえ、エイラの笛と重なる（この章は「笛が人に届く」章）。
# 調べ: 喜び。形: スリップ・ジグ（9/8。A 8小節・B 8小節）を AABB で4回。いきなり B（高い所）から始まる。
# 拍子・速さ: 9/8・付点4分＝104（8分＝312）。旋法: G リディア（C♯ が草原の明るい風）。
# 主役は笛: 中〜高音、ロールを少し。脇: ティン・ホイッスル（羊飼いの子。2回目と4回目の B で笛と同じ旋律、3回目の A で1人で）。
# 伴奏の主役: 左右のナイロン弦ギター（開いた和音のストローク。3回目だけ指弾きの分散和音）。竪琴・ピアノ・弦・パッド・打楽器は使わない。
# この曲だけ: B 部の頭の8分1つだけ、全員の音を抜く（草が倒れる）。次の8分で全員が戻る（草が起きる）。
# 始まり: いきなり B 部（高い所）から → 終わり: 最後の音（主音）を長くのばす。
# 山: 2回目（ホイッスルが加わり、左右のギターがそろう）。最初が大きい形にはしない（始まりの B は笛とギター1本だけ）。
import sys, json
from c100_common import *
from c100_v2 import *
import c100_v2 as _v2
_oc = _v2.open_chord
_v2.open_chord = lambda ch, lo=52, hi=76: _oc(ch, lo, hi)   # ギターの最低音を E2 以上に（010 で D2 が出た）

# 作曲ソフトの速さの上限は 260 なので、1拍＝付点4分（♩.=104）、1小節＝3拍で書く。8分音符＝1/3拍（旋律は8分＝1で書いて e2b で直す）
BPM = 104
S = Song("C100", "011-wind-through-the-grass", "草を渡る風", "Wind Through the Grass", BPM, 3, "G", "lydian", "ケルト（幻想）")
def e2b(bars):
    out = []
    for s_ in bars:
        out.append(" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()))
    return out
T3 = 1 / 3
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("G", "lydian", 4)
CA = ["G", "A", "G", "D", "G", "A", "Em", "G"]
CB = ["G", "A", "G", "D", "Em", "A", "D", "G"]
S.scene("風のはじまり", 8, "intro", CB)
for r in range(1, 5):
    S.scene(f"{r}回目A", 16, "verse", CA + CA)
    S.scene(f"{r}回目B", 16, "chorus" if r in (2, 4) else "verse", CB + CB)
S.scene("のばす", 2, "outro", ["G", "G"])
NAMES = ["風のはじまり"] + [f"{r}回目{p}" for r in range(1, 5) for p in "AB"] + ["のばす"]
c = make(S, NAMES,
         [("風のはじまり", 0, 0.7), ("1回目A", 0, 0.68), ("1回目B", 0, 0.74), ("2回目A", 0, 0.78), ("2回目B", 0, 0.88), ("2回目B", 15, 0.9),
          ("3回目A", 0, 0.68), ("3回目B", 0, 0.72), ("4回目A", 0, 0.78), ("4回目B", 0, 0.84), ("4回目B", 15, 0.84), ("のばす", 0, 0.78), ("のばす", 1, 0.7)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="風のはじまり", passing=True, tension=False)
S.fix_avoid = lambda t: 0      # リディアの C♯ を直されないように
B = S.beats
# ホイッスル：試しの書き出しで、volume 0.2 だと笛より約10dB大きかった。長い音は約3.5秒で消える（短い音だけにする）
WH = S.track("ティン・ホイッスル（羊飼いの子）", "panflute", patch="tinWhistle", volume=0.06, pan=0.4, reverb=0.45, barGain=c.g())
GL = [S.track(f"左のギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.055, pan=-0.35 - 0.05 * i, reverb=0.3, barGain=c.g()) for i in range(5)]
GR = [S.track(f"右のギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.045, pan=0.3 + 0.05 * i, reverb=0.3, barGain=c.g()) for i in range(4)]
GP = S.track("ギター（指弾き）", "guitar", patch="nylonGuitar", volume=0.08, pan=-0.2, reverb=0.35,
             barGain=[round(x * 2.0, 3) for x in c.g()])   # 3回目は指弾き1本だけになるので大きめに（楽器1つの場面は沈みやすい）

# ---------- スリップ・ジグ（G リディア。1=G4。8分＝1） ----------
A = ["1:2 2:1 3:2 5:1 3:2 1:1", "2:2 3:1 4:2 3:1 2:3", "1:2 2:1 3:2 5:1 6:2 5:1", "5:2 4:1 3:2 2:1 5,:3",
     "1:2 2:1 3:2 5:1 3:2 1:1", "2:2 3:1 4:2 6:1 5:3", "6:2 5:1 3:2 2:1 3:2 5:1", "1:2 3:1 2:3 1:3"]
Bp = ["5:2 1':1 2':2 1':1 7:2 5:1", "6:2 2':1 3':2 2':1 1':3", "5:2 1':1 2':2 3':1 2':2 1':1", "7:2 5:1 4:2 2:1 5:3",
      "6:2 1':1 3':2 1':1 6:2 5:1", "4:2 6:1 2':2 6:1 4:3", "5:2 7:1 2':2 7:1 6:2 4:1", "1':2 7:1 5:2 3:1 1:3"]
def drop(bars):
    """B 部の頭の8分1つを休みにする（草が倒れる）"""
    out = list(bars); t = out[0].split(); n, L = t[0].split(":")
    out[0] = " ".join(["R:1", f"{n}:{float(L) - 1:g}"] + t[1:]) if float(L) > 1 else " ".join(["R:1"] + t[1:])
    return out
DENS = {1: 0.4, 2: 0.6, 3: 0.35, 4: 0.7}
play_melody(c, "風のはじまり", e2b(drop(Bp)), 4, "march", key=K, density=0.3, seed=1100)
for r in range(1, 5):
    play_melody(c, f"{r}回目A", e2b(A + A[:7] + ["1:2 3:1 2:3 5,:3"]), 4, "march", key=K, density=DENS[r], seed=1100 + 10 * r)
    nb = play_melody(c, f"{r}回目B", e2b(drop(Bp) + drop(Bp)), 4, "march", key=K, density=DENS[r], seed=1105 + 10 * r)
    if r in (2, 4):                                   # ホイッスルが笛と同じ旋律で（短い音だけ。長い音は 1.5 拍まで）
        for st, L, m, mk in nb:
            if L >= 0.3: WH.at(round(st + 0.01, 3), f"{nm(m if m >= 72 else m + 12)}:{round(min(L, 0.5), 4)}{mk}")
# 3回目 A：羊飼いの子のホイッスルが1人で A を吹き、笛は休む（呼びかけ）。後半8小節は笛が答える
s3 = c.s0["3回目A"]
c.FLUTE.ev = [e for e in c.FLUTE.ev if not (s3 * B <= e[0] < (s3 + 8) * B)]
for t, L, m in section_events(c, "3回目A", e2b(A), 5, key=K):
    WH.at(round(t, 4), f"{nm(m)}:{round(min(L, 0.5), 4)}")
play_melody(c, "のばす", ["1:3", "1:2 R:1"], 4, "air", key=K, density=0.0)

# ---------- ギター ----------
SJ = [(0, 1, "d", "!"), (1, 1, "d", ""), (2, 2 * T3, "d", ","), (2 + 2 * T3, T3, "u", ",")]
SJ_R = [(1, 2 * T3, "d", ","), (2, 2 * T3, "d", ","), (2 + 2 * T3, T3, "u", ",")]          # 右は2つ目・3つ目の拍に（左とずらす）
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    head = (n.endswith("B") or n == "風のはじまり") and i % 8 == 0     # B 部の頭：8分1つ、全員が抜ける
    off = T3 if head else 0
    if n == "のばす":
        strum(GL, b, B, ch, [(0, 3 if i == 0 else 2, "d", "!" if i == 0 else ",")]); continue
    if n.startswith("3回目"):                     # 3回目：指弾きの分散和音だけ（風が弱まる）
        v = _v2.open_chord(ch)
        GP.bar(b, " ".join(f"{nm(v[q % len(v)])}:{round(T3, 4)}{',' if q % 3 else ''}" for q in (0, 2, 3, 1, 2, 4, 1, 3, 2)))
        continue
    strum(GL, b, B, ch, [(max(p, off), L - (off if p < off else 0), d, mk) for p, L, d, mk in SJ])
    if n.startswith("2回目") or n.startswith("4回目"): strum(GR, b, B, ch, SJ_R)

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.24 --master -15 --widen 1.25 --side-hpf 200",
       "ケルト・フルート100曲の011（第3版）。第2章のはじまり、草原を渡る風。スリップ・ジグ（9/8・付点4分＝104）、G リディア。いきなり B 部（高い所）から始まり、AABB を4回。B 部の頭は8分1つだけ全員の音を抜き（草が倒れる）、次の8分で戻る（草が起きる）。伴奏は左右のナイロン弦ギター、脇に羊飼いの子のティン・ホイッスル。山は2回目、最後は主音を長くのばす。",
       harm_scenes=None, tail_scene="のばす", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 5.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.2, "lp": 3000, "rt": 2.4}}}
json.dump(air, open("/tmp/cel/w/air011.json", "w"), ensure_ascii=False)

# 1/3 拍の位置を丸めると「R:0」ができて書き出しが止まる（010 で分かった）。長さ0の休みを取りのぞく
_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
