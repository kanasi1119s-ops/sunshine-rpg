# 異世界ファンタジーのケルト曲 25曲（2026-10-20、人間の依頼「ケルト曲でフルート、アコギ、カホン、ウッドベースを使い、異世界ファンタジーみたいな曲を
#   25曲作ってください。平和な感じや楽しい感じ、明るい感じ、ゆったりした感じなどで作ってくれるといいです」）。
# 楽器はこの4つだけ: フルート（VSCO 2 CE の録音。ハモリにもう1本の笛）・アコギ（和音の刻み／分散和音、間奏では旋律）・カホン（VCSL の録音）・
#   ウッドベース（Sneakybass の録音。書き出しは --bass jazz）。
# 曲の部品（旋律の書き方・伴奏・打楽器）は celtic_fantasy_core.py（ケルト20曲の celtic_suite.py を写して、カホンとウッドベースを足したもの）。
# 旋律は曲ごとに決まった乱数で書く（既存の曲のメロディは使わない。CLAUDE.md 1-1）。
# 使い方: python3 celtic_fantasy.py <番号か id か all> [出力フォルダ]
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import celtic_fantasy_core as core
from celtic_fantasy_core import S_, F, METERS

# 2026-10-20 人間「曲ですが4分から5分でお願いします」: 200秒 → 270秒（4分30秒）。区間は最大18まで並べ、
#   同じ旋律が続きすぎないよう、A・B のほかに3つ目の旋律 C（B の2行目・A の1行目・A の終わりの行から作る進行）を入れる
TARGET = 270

def form_for(mood, meter, bpm, end="hit"):
    """雰囲気ごとの組み立て。16小節の区間を、長さの目安（4〜5分）に合うだけ並べる。w＝笛の旋律、wf＝笛2本のハモリ、gl＝アコギの旋律"""
    bar = METERS[meter]["beats"] * 60 / bpm
    W, WF, GL = ("wflute",), ("wflute", "flute"), ("gtrlead",)
    seq = {
        # 踊る曲: アコギとカホンだけで入る → 旋律 → 間奏はアコギの旋律 → 2本の笛のハモリで盛り上げる
        # 2026-10-20 後半が大きくなりすぎないよう、いちばん強い区間（5）は山場の1〜2回だけ。あとは 3〜4 を行き来する
        "dance": [("A", 3, W), ("B", 4, W), ("A", 3, GL), ("C", 4, W), ("A", 4, WF), ("B", 5, WF), ("A", 3, W), ("C", 3, GL), ("B", 4, W),
                  ("A", 4, WF), ("C", 3, W), ("B", 4, WF), ("A", 3, GL), ("B", 4, W), ("C", 4, WF), ("A", 4, WF), ("B", 5, WF), ("A", 4, WF)],
        "mid": [("A", 3, W), ("B", 4, W), ("A", 3, GL), ("C", 3, W), ("A", 4, WF), ("B", 4, WF), ("A", 3, W), ("C", 4, WF), ("B", 3, W),
                ("A", 3, GL), ("B", 4, WF), ("C", 3, W), ("A", 4, WF), ("B", 5, WF), ("A", 4, WF), ("B", 3, W)],
        # ゆったり: アコギの分散和音から。カホンは盛り上がる区間（3以上）だけ
        "calm": [("A", 2, W), ("B", 3, W), ("A", 2, GL), ("C", 2, W), ("A", 3, WF), ("B", 3, W), ("C", 3, GL), ("A", 2, W), ("B", 3, WF),
                 ("C", 2, W), ("A", 3, GL), ("B", 3, WF), ("C", 2, W), ("A", 3, WF), ("B", 2, W)],
    }[mood]
    blocks = [(m, lv, v[0]) + ((v[1],) if len(v) > 1 else ()) for m, lv, v in seq]
    intro = {"dance": F("intro", 8 if bar < 1.6 else 4, 3, only=["guitar", "drums"]), "mid": F("intro", 4, 2, only=["guitar", "bass"]),
             "calm": F("intro", 4, 1, only=["guitar"])}[mood]
    k = max(3, min(len(blocks), round((TARGET - (intro["bars"] + 4) * bar) / (16 * bar))))
    fm = [intro]
    for b in blocks[:k]:
        fm.append(F(b[0], 16, b[1], b[0], b[2], **({"harm": b[3]} if len(b) > 3 else {})))
    fm.append(F("end", 4, 4 if end == "hit" else 2, end=end))
    return fm

def band(mood):
    return dict(leads=["wflute"], guitar="arp" if mood == "calm" else True, gring=mood == "calm", bass="upright", drums="cajon")

def D(n, id, title, en, image, meter, bpm, key, mode, A, B, mood, end=None, **kw):
    end = end or ("fade" if mood == "calm" else "hit")
    C = (B[1], A[0], A[2])   # 3つ目の旋律の進行（4〜5分の曲で、A・B のくり返しばかりにならないように）
    s = S_(id, title, image, meter, bpm, key, mode, {"A": A, "B": B, "C": C}, band(mood), form_for(mood, meter, bpm, end),
           f"入り方: {'アコギとカホン' if mood == 'dance' else 'アコギとウッドベース' if mood == 'mid' else 'アコギの分散和音だけ'}。"
           f"間奏はアコギが旋律、後半は2本の笛のハモリ。終わり方: {'全員で一発' if end == 'hit' else '静かに消える'}。", **kw)
    s.update(n=n, en=en, mood=mood); return s

SONGS = [
    D(1, "village-morning", "始まりの村の朝", "Morning in the First Village", "明るい・旅のはじまり。朝日の差す小さな村、パン屋の煙と鳥の声",
      "6/8", 112, "D", "ionian", ("D A/C# Bm G", "Em7 G A7sus4 A", "G A7sus4 A7 D"), ("G D/F# Em7 A", "Bm F#m G A", "G Em7 Asus4 D"), "dance"),
    D(2, "windmill-hill", "風車の丘", "Windmill Hill", "楽しい・のどか。丘の上で大きな風車がまわり、子どもたちが駆けまわる",
      "4/4", 116, "G", "mixolydian", ("G F/G C/G G", "Em7 F C D", "C F Dsus4 G"), ("C G/B Am7 F", "C D Em F", "C F/A Dsus4 G"), "dance"),
    D(3, "forest-path", "木もれ日の小道", "Sunlit Forest Path", "ゆったり・森。木もれ日の差す森の小道を、のんびり歩く",
      "3/4", 84, "F", "ionian", ("F C/E Dm7 Bbmaj7", "Gm7 Am7 Bbmaj7 C", "Bbmaj7 Gm7 Csus4 F"), ("Bbmaj7 F/A Gm7 Dm7", "Ebmaj7 Bb/D Csus4 C", "Bbmaj7 Am7 Gm7 F"), "calm"),
    D(4, "guild-bustle", "冒険者ギルドのにぎわい", "Bustling Adventurers' Guild", "楽しい・にぎやか。依頼の紙が貼られた掲示板、笑い声の絶えないギルドの酒場",
      "2/4", 128, "A", "ionian", ("A E/G# F#m D", "Bm7 E A/C# D", "D E7sus4 E7 A"), ("D A/C# Bm7 E", "F#m C#m D E", "D Bm7 E7 A"), "dance"),
    D(5, "spirit-spring", "精霊の泉", "Spring of the Spirits", "平和・神秘。森の奥の澄んだ泉、小さな光の精霊がふわふわ漂う（リディアン）",
      "6/8", 60, "E", "lydian", ("E F#/E E F#/E", "C#m7 Amaj7 B G#m7", "Amaj7 F#/A# Bsus4 E"), ("Amaj7 E/G# F#m7 B", "C#m7 G#m7 Amaj7 Bsus4", "Amaj7 F#7/A# Bsus4 E"), "calm"),
    D(6, "harbor-market", "港町の朝市", "Harbor Town Morning Market", "明るい・活気。潮風の吹く港町、魚や果物の並ぶ朝市",
      "6/8", 120, "C", "ionian", ("C G/B Am F", "Dm7 G7 Em7 Am", "F G7sus4 G7 C"), ("F C/E Dm7 G", "Am Em F G", "F Dm7 G7 C"), "dance"),
    D(7, "starry-camp", "星降る草原の野宿", "Camping under Falling Stars", "ゆったり・夜。旅の途中、満天の星の下で焚き火を囲んで眠る（12/8）",
      "12/8", 60, "Bb", "ionian", ("Bb F/A Gm7 Ebmaj7", "Cm7 Dm7 Ebmaj7 F", "Ebmaj7 Cm7 Fsus4 Bb"), ("Ebmaj7 Bb/D Cm7 F", "Gm Dm/F Ebmaj7 Fsus4", "Ebmaj7 Ab Fsus4 Bb"), "calm"),
    D(8, "fairy-inn", "妖精の宿屋", "The Fairy's Inn", "楽しい・不思議。小さな妖精たちが営む宿屋、夜ごとの宴（スリップジグ 9/8）",
      "9/8", 112, "D", "mixolydian", ("D C/D G/D D", "Em7 C G A", "G C Asus4 D"), ("C G/B Am7 D", "G C Em A", "C G Asus4 D"), "dance"),
    D(9, "floating-isles", "雲の上の浮島", "Floating Isles above the Clouds", "平和・雄大。雲の上にいくつも浮かぶ島々、ゆっくり流れる時間（リディアン）",
      "4/4s", 76, "Eb", "lydian", ("Eb F/Eb Eb F/Eb", "Cm7 Abmaj7 Bb Gm7", "Abmaj7 F/A Bbsus4 Eb"), ("Abmaj7 Eb/G Fm7 Bb", "Cm7 Gm7 Abmaj7 Bbsus4", "Abmaj7 F7/A Bbsus4 Eb"), "calm"),
    D(10, "dragon-ride", "竜の背に乗って", "Riding a Dragon's Back", "明るい・冒険。仲良くなった竜の背に乗り、山々を越えて空を飛ぶ",
      "6/8", 124, "A", "mixolydian", ("A G/A D/A A", "F#m7 G D E", "D G Esus4 A"), ("D A/C# Bm7 G", "D E F#m G", "D G Esus4 A"), "dance"),
    D(11, "magic-academy", "魔法学校の昼休み", "Lunch Break at the Magic Academy", "楽しい・いたずら。魔法学校の中庭、ほうきや杖で遊ぶ昼休み（跳ねるリズム）",
      "4/4", 104, "F", "ionian", ("F Dm7 Gm7 C7", "Am7 D7 Gm7 C", "Bb C7sus4 C7 F"), ("Bb F/A Gm7 C", "A7 Dm7 G7 C", "Bb Bbm6 C7 F"), "mid", swing=0.4),
    D(12, "wheat-road", "麦畑の帰り道", "Home through the Wheat Fields", "ゆったり・夕方。金色の麦畑の中の道を、荷車を引いて村へ帰る（ワルツ）",
      "3/4", 92, "G", "ionian", ("G D/F# Em7 C", "Am7 D G/B C", "C D7sus4 D7 G"), ("C G/B Am7 D", "Em Bm C D", "C Am7 D7 G"), "mid"),
    D(13, "elf-village", "エルフの里の午後", "Afternoon in the Elven Village", "平和・静か。大樹の上にあるエルフの里、木の葉が揺れる午後（ドリアン）",
      "6/8", 72, "D", "dorian", ("Dm G/D Dm C", "Bbmaj7 F C Am7", "Bbmaj7 G Asus4 Dm"), ("F C/E Dm7 G", "Bbmaj7 F/A Gm7 Asus4", "Bbmaj7 C Asus4 Dm"), "calm"),
    D(14, "departure-road", "旅立ちの街道", "The Road of Departure", "明るい・希望。仲間と一緒に、まだ見ぬ国へ続く街道を歩き出す（ミクソリディアン）",
      "4/4", 112, "E", "mixolydian", ("E D/E A/E E", "C#m7 D A B", "A D Bsus4 E"), ("A E/G# F#m7 D", "A B C#m D", "A D Bsus4 E"), "mid"),
    D(15, "lakeside-picnic", "湖のほとりのピクニック", "Lakeside Picnic", "楽しい・晴れ。湖のほとりでお弁当を広げ、水切りをして遊ぶ（ポルカ）",
      "2/4", 116, "C", "ionian", ("C E7/B Am F", "Dm7 G C/E F", "F G7sus4 G7 C"), ("F G Em Am", "Dm7 Em F G", "F Fm6 G7 C"), "dance"),
    D(16, "after-rain", "雨あがりの石畳", "Cobblestones after the Rain", "ゆったり・しっとり。雨の上がった城下町、石畳に空が映る（ドリアン）",
      "4/4s", 80, "A", "dorian", ("Am D/A Am G", "Fmaj7 C/E Dm7 Esus4", "Fmaj7 D/F# Esus4 Am"), ("C G/B Am7 D", "Fmaj7 Em7 Dm7 E", "F D7 Esus4 Am"), "calm"),
    D(17, "harvest-dance", "実りの祭りの輪踊り", "Harvest Festival Ring Dance", "楽しい・祭り。実りを祝う村の広場、みんなで輪になって踊る",
      "6/8", 132, "G", "ionian", ("G C/G D/G G", "Em C D Bm", "C D7sus4 D7 G"), ("C D Bm Em", "Am7 D G/B C", "C Am7 D7 G"), "dance"),
    D(18, "herb-hill", "薬草摘みの丘", "Herb-Gathering Hill", "平和・やさしい。花の咲く丘で、薬草を摘みながら歌う（リディアン）",
      "3/4", 76, "C", "lydian", ("C D/C C D/C", "Am7 Fmaj7 G Em7", "Fmaj7 D/F# Gsus4 C"), ("Fmaj7 C/E Dm7 G", "Am7 Em7 Fmaj7 Gsus4", "Fmaj7 D7/F# Gsus4 C"), "calm"),
    D(19, "sunset-town", "夕焼けの城下町", "Castle Town at Sunset", "ゆったり・郷愁。夕焼けに染まる城下町、家々に明かりがともる",
      "6/8", 84, "Ab", "ionian", ("Ab Eb/G Fm7 Db", "Bbm7 Eb Cm7 Fm", "Db Eb7sus4 Eb7 Ab"), ("Db Ab/C Bbm7 Eb", "Fm Cm Db Eb", "Db Bbm7 Eb7 Ab"), "mid"),
    D(20, "dwarf-smithy", "ドワーフの鍛冶場", "The Dwarves' Forge", "楽しい・力強い。山の中のドワーフの鍛冶場、槌の音が響く（7拍子）",
      "7/8", 180, "E", "dorian", ("Em D/E Em A", "C G/B Am7 D", "C D B7sus4 Em"), ("G D/F# Em A", "C D Bm Em", "C Am7 Bsus4 Em"), "dance"),
    D(21, "sky-ship", "空飛ぶ帆船", "The Flying Sailship", "明るい・爽快。雲の海をすべる空飛ぶ帆船、甲板で風を受ける（スリップジグ 9/8）",
      "9/8", 120, "A", "ionian", ("A D/A E/A A", "F#m D E C#m", "D E7sus4 E7 A"), ("D E C#m F#m", "Bm7 E A/C# D", "D Bm7 E7 A"), "dance"),
    D(22, "moon-flowers", "月明かりの花畑", "Moonlit Flower Field", "平和・夜。月の光で花びらが白く光る花畑（リディアン・12/8）",
      "12/8", 58, "G", "lydian", ("G Cmaj7/G G A/G", "Bm7 Em7 Cmaj7 D", "Am7 A/C# Dsus4 G"), ("Cmaj7 G/B Am7 D", "Em7 Bm7 Cmaj7 Dsus4", "Cmaj7 A7/C# Dsus4 G"), "calm"),
    D(23, "bard-campfire", "吟遊詩人の焚き火", "The Bard's Campfire", "ゆったり・物語。焚き火を囲み、吟遊詩人が昔話を語る夜（ドリアン）",
      "6/8", 96, "B", "dorian", ("Bm E/B Bm A", "G D/F# Em7 F#sus4", "G E F#sus4 Bm"), ("D A/C# Bm7 E", "G D A Bm", "G A F#sus4 Bm"), "mid"),
    D(24, "royal-festival", "王都の祝祭", "Festival in the Royal Capital", "明るい・華やか。旗のはためく王都の大通り、パレードと花吹雪",
      "4/4", 120, "D", "ionian", ("D G/D A/D D", "Bm G A F#m", "G A7sus4 A7 D"), ("G A F#m Bm", "Em7 A D/F# G", "G Em7 A7 D"), "dance"),
    D(25, "world-tree", "世界樹のふもとで", "At the Foot of the World Tree", "平和・おだやか。天まで届く世界樹の根もと、旅の終わりにひと休み",
      "4/4s", 66, "F", "ionian", ("F C/E Bb/D F/C", "Dm7 Am7 Bbmaj7 Csus4", "Bbmaj7 Gm7 Csus4 F"), ("Bbmaj7 C/Bb Am7 Dm7", "Gm7 Ebmaj7 Csus4 C", "Bbmaj7 Bbm6 Csus4 F"), "calm"),
]

# 点数（音質の採点 PQ 8点以上）の試しで決めた調整（曲番号 → band や曲の値の上書き）。試しは環境変数 CF_TUNE='{"03": {"seed": "2"}}' で
FINAL = {
    # 2026-10-20 4〜5分・ナイロンギターの録音で全曲 PQ 8.00〜8.29（書き出しは --guitar nylon。real_bass の曲だけ --bass upright、ほかは --bass jazz）
    "01": {"bpm": 123}, "02": {"bpm": 128, "seed": "2"}, "03": {"bpm": 116}, "05": {"bpm": 83}, "06": {"seed": "3"},
    "07": {"bpm": 84, "lift": 2, "meter": "6/8"}, "08": {"bpm": 129}, "09": {"bpm": 96, "lift": 2, "meter": "6/8"},
    "11": {"bpm": 120, "real_bass": True}, "12": {"bpm": 110, "real_bass": True}, "13": {"bpm": 104, "seed": "3"},
    "14": {"bpm": 130, "seed": "3"}, "16": {"bpm": 110, "lift": 2}, "17": {"seed": "3"}, "18": {"bpm": 99, "lift": 2, "real_bass": True},
    "19": {"bpm": 92}, "20": {"bpm": 210, "seed": "3"}, "21": {"bpm": 140, "seed": "3", "real_bass": True},
    "22": {"bpm": 80, "lift": 2, "meter": "6/8"}, "23": {"bpm": 110}, "24": {"seed": "2"}, "25": {"bpm": 91, "lift": 2},
}
# ゆったりの曲（2026-10-20 点数の試し『精霊の泉』）: 分散和音だけ 7.55 → やさしいストローク＋区間を1段にぎやかに（カホンが静かに入る）7.70
#   → テンポを約2割上げて 7.81、本物のフルートの録音で CE 6.58→7.24。ゆったりの7曲にこの組み合わせを入れる
# 2026-10-20 人間「アコギはナイロンの録音の音を使おう」: 全曲のアコギを、ナイロン弦のスパニッシュギターの録音（FreePats。CC0）に。書き出しは --guitar nylon
ALL_SONGS = {"gpatch": "nylonGuitar"}
CALM = {"guitar": True, "gring": False, "lift": 1, "lead_patch": "flute"}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "assets-src/ai-songs"
    tune = dict(FINAL, **(json.loads(os.environ["CF_TUNE"]) if "CF_TUNE" in os.environ else {}))
    ALL = dict(ALL_SONGS, **json.loads(os.environ.get("CF_ALL", "{}")))   # 全曲に足す設定（曲ごとの設定より先に入れ、曲ごとの設定が優先）
    if ALL: tune = {f"{s['n']:02d}": {**ALL, **tune.get(f"{s['n']:02d}", {})} for s in SONGS}
    pre = os.environ.get("CF_PRE", "")
    for s in SONGS:
        n = s["n"]
        if which not in ("all", str(n), f"{n:02d}", s["id"]): continue
        if s["mood"] == "calm" and os.environ.get("CF_CALM", "1") == "1":
            tune.setdefault(f"{n:02d}", {}); tune[f"{n:02d}"] = {**CALM, "bpm": round(s["bpm"] * 1.22), **tune[f"{n:02d}"]}
        if f"{n:02d}" in tune:
            t = dict(tune[f"{n:02d}"]); top = {k: t.pop(k) for k in ("seed", "bpm", "mel_range", "lead_db", "gsoft", "gdb", "cajon_vol", "lead_patch", "lift", "fmood", "real_bass", "bass_vol", "meter") if k in t}
            s = dict(s, band={**s["band"], **t}, **top)
            if top.get("bpm") and not top.get("fmood"):   # テンポを変えたら、4〜5分になるよう区間の数を数えなおす
                s["form"] = form_for(s["mood"], s["meter"], s["bpm"], "fade" if s["mood"] == "calm" else "hit")
            if top.get("fmood"):   # 組み立てだけ別の雰囲気の形にする（ゆったりの曲を「中くらい」の形に、など）
                s["form"] = form_for(top["fmood"], s["meter"], s.get("bpm", s["bpm"]), "fade" if s["mood"] == "calm" else "hit")
            if top.get("lift"):   # 区間の強さを1段上げる（ゆったりの曲でもカホンが静かに入る）
                s["band"].pop("lift", None)
                s["form"] = [dict(f, level=min(5, f["level"] + int(top["lift"]))) if f["kind"] != "end" else f for f in s["form"]]
        out = os.path.join(outdir, f"{pre}fantasy25-{n:02d}-{s['id']}.json")
        t = core.build(s, out)
        print(f"{n:02d} {s['id']} {int(t // 60)}分{int(t % 60):02d}秒 {len(s['form'])}区間")
