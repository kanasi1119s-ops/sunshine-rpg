# ケルト・フルート100曲「銀の笛と百の夜」029 水が教える道 The Way the Water Teaches — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 霧の晴れた朝。小川はいくつにも分かれ、どれが山の上の泉へ続くのか分からない。エイラは水音に耳をすませ、
#   同じ素朴な節を何度も吹く。吹くたびに、水の細かな動き（装飾）が節にしみこみ、節は流れのように細かくなっていく。
#   最後に道が分かると、節はまた最初の素朴な形に戻って、静かに消える。
# 調べ: あいだ。形: 主題と変奏（ピーブロック型：主題 → 変奏ごとに装飾が密に → 最後に装飾のない主題へ戻る）。
# 拍子・速さ: 主題は自由（拍を感じさせない）→ 変奏は 6/8・付点4分＝80（1拍＝付点4分で書く。8分は 1/3 拍）。旋法: B ドリア。
# 主役は笛（主題は素朴、変奏で装飾が増える）。伴奏は弦のドローン（主音 B と5度 F♯）だけ。ほかの楽器は使わない。
# この曲だけ: 最後に装飾のない素朴な主題へ戻る静けさ（変奏でいちばん密になった直後に、何もない主題が来る）。
# 始まり: ドローン → 終わり: 主題に戻って消える。
# 山: 変奏ごとに密に（変奏3 がいちばん密）。
import sys, json, re
from c100_common import *
from c100_v2 import *

BPM = 80
S = Song("C100", "029-the-way-the-water-teaches", "水が教える道", "The Way the Water Teaches", BPM, 2, "B", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K = Key("B", "dorian", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
SC = [("ドローン", 4, "intro"), ("主題", 16, "verse"), ("変奏1", 32, "verse"), ("変奏2", 32, "verse"), ("変奏3", 32, "chorus"),
      ("変奏4", 32, "chorus"), ("主題ふたたび", 16, "verse"), ("消える", 4, "outro")]
for n, L, kd in SC: S.scene(n, L, kd, ["Bm"] * L)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ドローン", 0, 0.64), ("主題", 0, 0.66), ("変奏1", 0, 0.72), ("変奏2", 0, 0.78), ("変奏3", 0, 0.86), ("変奏4", 0, 0.9),
          ("変奏4", 31, 0.88), ("主題ふたたび", 0, 0.68), ("消える", 0, 0.64), ("消える", 3, 0.6)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ドローン", passing=True, tension=False)
S.fix_avoid = lambda t: 0
S.tempo = [{"bar": 1, "bpm": 66}, {"bar": c.s0["変奏1"] + 1, "bpm": 80}, {"bar": c.s0["主題ふたたび"] + 1, "bpm": 66}]
S.extra.update({"rubato": 0.3})
B = S.beats
G = c.g()
# 弦のドローン（B と F♯）。長い弦は立ち上がりが遅く小さい（007・004 で測った）→ チェロは B2 ではなく B3、ビオラ F♯4。2パートずつで弓を返す
DV = [S.track(f"弦のドローン（{nm_}）", "strings", patch=pt, volume=v, gainDb=gd, pan=p, reverb=0.65, release=0.3, barGain=[round(x * 1.4, 3) for x in G])
      for nm_, pt, v, gd, p in [("チェロ B3", "cello", 0.02, 2, -0.2), ("ビオラ F♯4", "viola", 0.017, 0, 0.22),
                                ("チェロ B3・弓返し", "cello", 0.02, 2, -0.2), ("ビオラ F♯4・弓返し", "viola", 0.017, 0, 0.22)]]

# ---------- 主題（B ドリア。1=B4 だと高いので 1=B3 の上、オクターブ4 で 5,=F♯4 から。8分＝1、1小節＝6） ----------
TH = ["1:6", "3:3 2:3", "1:3 7,:3", "5,:6", "6,:3 7,:3", "1:6", "2:3 1:3", "7,:6",
      "3:6", "4:3 3:3", "2:3 1:3", "6,:6", "7,:3 1:3", "2:3 3:3", "2:3 7,:3", "1:6"]
def var(level):
    """変奏：level 1＝付点のはずみ、2＝8分で流れる、3＝細かい回り込み、4＝最も密（16分の流れ）"""
    out = []
    for s_ in TH:
        tk = s_.split(); new = []
        for t in tk:
            d, L = t.split(":"); L = float(L)
            if level == 1: new += ([f"{d}:2", f"{d}:1"] * int(L // 3)) if L >= 3 else [t]
            elif level == 2: new += [f"{d}:1"] * int(L)
            elif level == 3:
                new += sum([[f"{d}:1", f"{d}:0.5", f"{d}:0.5"] for _ in range(int(L // 2))], []) + ([f"{d}:{L % 2:g}"] if L % 2 else [])
            else: new += [f"{d}:0.5"] * int(L * 2)
        out.append(" ".join(new))
    return out
play_melody(c, "主題", e2b(TH), 4, "air", key=K, density=0.0)
play_melody(c, "変奏1", e2b(var(1) * 2), 4, "march", key=K, density=0.2, seed=2901)
play_melody(c, "変奏2", e2b(var(2) * 2), 4, "march", key=K, density=0.4, seed=2902)
play_melody(c, "変奏3", e2b(var(3) * 2), 4, "march", key=K, density=0.6, seed=2903)
play_melody(c, "変奏4", e2b(var(4) * 2), 4, "march", key=K, density=0.8, seed=2904)
play_melody(c, "主題ふたたび", e2b(TH), 4, "air", key=K, density=0.0)
play_melody(c, "消える", e2b(["1:6", "1:6", "R:6", "R:6"]), 4, "air", key=K, density=0.0)

# ---------- ドローン（最後の小節まで。2小節ごとに交互に弓を返す） ----------
end = (c.NB - 1) * B
st, k = 0.0, 0
while st < end - 0.01:
    en = min(end, st + 4.2)
    DV[0 + 2 * (k % 2)].at(round(st, 3), f"B3:{round(en - st, 3)}{',' if st else ''}"); DV[1 + 2 * (k % 2)].at(round(st + 0.1, 3), f"F#4:{round(en - st - 0.1, 3)},")
    st += 4; k += 1

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.32 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の029（第3版）。いくつにも分かれた小川で、水音に耳をすませて道を探す。主題と変奏（ピーブロック型）、B ドリア。素朴な主題を、変奏ごとに装飾を密にして吹き（6/8・付点4分＝80）、伴奏は主音と5度の弦のドローンだけ。いちばん密になった直後に、装飾のない素朴な主題へ戻り、静かに消える。",
       harm_scenes=None, tail_scene="消える", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -27, "delay": 0.28, "lp": 2800, "rt": 3.6}}}
json.dump(air, open("/tmp/cel/w/air029.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
