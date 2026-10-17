# ピアノが主役の「空間の曲」25曲（2026-10-18、人間の依頼「ピアノをメインで他に楽器を7種類ほど入れて、ゆったりできる空間ソングを
#   4〜5分程度で25曲作ってください。いろんな自然を想像できたり、季節、朝昼夜などの要素を入れてもらいたい」）。
# 作り方はケルト20曲（celtic_suite.py）と同じ部品を使う（旋律の書き方・アヴォイド・ノートを避ける・音域を広く・やわらかいアコギ・根音のベース・
#   ピアノの左手と右手・フィドルの音・FX）。ここでは曲ごとの設計（季節・時間・自然・拍子・テンポ・調と旋法・定番から外したコード進行）だけを書く。
# ピアノ以外の8種類: 2つめの旋律（笛・クラリネット・オーボエ・フィドル・ホルンのどれか）、ハープ、弦（のばす）、チェロ、鉄琴、アコギ（指で弾く分散和音）、ベース、ボーラン風の刻み。
# ドラムはなし（ボーラン風の静かな刻みだけ）。書き出しは「ホール」の響き（--space hall 0.2）と仕上げ orch で空間を出す（人間の指示「自然を感じる曲はその空間が感じるような感じに」「空気を感じる音楽に全部」）。
# 使い方: python3 piano_suite.py <番号か id か all> [出力フォルダ（省略は assets-src/ai-songs）]
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import celtic_suite as cs
from celtic_suite import S_, F, METERS

TARGET = 280.0   # 1曲の長さの目安（秒）。4分半前後


def form(meter, bpm, lead2, intro=("piano", "harp", "glock")):
    """ピアノが半分以上の旋律を受けもつ形。目安の長さになるまで、A（ピアノ）と B（2つめの楽器・ピアノ）をくり返す"""
    bar = METERS[meter]["beats"] * 60 / bpm
    seq = [F("intro", 4, 1, only=list(intro))]
    cyc = [F("A", 16, 2, "A", "piano"), F("B", 16, 3, "B", lead2), F("A", 16, 3, "A", "piano", harm=lead2),
           F("break", 8, 2, only=["piano", "strings", "cello", "harp"]), F("B", 16, 4, "B", "piano", harm=lead2), F("A", 16, 3, "A", lead2),
           F("B", 16, 3, "B", "piano"), F("A", 16, 2, "A", "piano", harm=lead2)]
    t = 4 * bar; k = 0
    while t + 16 * bar + 6 * bar < TARGET + 20 and k < 12:
        s = cyc[k % len(cyc)]
        if t + s["bars"] * bar > TARGET - 6 * bar and s["kind"] == "break": k += 1; continue
        seq.append(s); t += s["bars"] * bar; k += 1
    seq.append(F("end", 6, 2, end="fade"))
    return seq


# 2026-10-18 点数（Audiobox の PQ）の試し（07『ひぐらしの夕暮れ』）: そのまま 7.92。チェロ↓旋律↑ 7.91、弦なし 7.93、アコギなし 7.89、ベースなし 7.93、
#   ピアノ +3dB 7.92、ハープなし 7.87、旋律の種を変える 7.94、ピアノの右手を和音 7.95、仕上げ orch 7.95・ambient 7.94、
#   ドラム（盛り上がりだけ）8.03、ボーラン風の静かな刻み（中くらい以上の所）8.04 → ボーランと仕上げ orch を全曲に
BAND = lambda lead2, **kw: dict(leads=["piano", lead2], harp=True, piano="flow", strings=True, cello=True, sparkle="glock", guitar="arp", bass="finger", drums="bodhran", **kw)

def P(id, title, en, image, meter, bpm, key, mode, A, B, lead2, extra, **kw):
    s = S_(id, title, image, meter, bpm, key, mode, {"A": A, "B": B}, BAND(lead2), form(meter, bpm, lead2), extra, rit=True, cello_db=-5, **kw)
    s["en"] = en
    return s

SONGS = [
    P("dawn-meadow", "朝霧の草原", "Misty Meadow at Dawn", "春・朝。朝霧がうすく残る草原に、最初の光がさしこむ", "4/4s", 70, "D", "lydian",
      ("D E/D Bm7 Gmaj7", "Em7 A/C# Bm7 Asus4", "Gmaj7 E/G# Asus4 D"), ("Gmaj7 A/G F#m7 Bm7", "Em7 Gmaj7 Asus4 A", "Gmaj7 Gm6 Asus4 D"), "flute",
      "リディアン（E のコード）で光がさす感じ。終わりは短調の Gm6 をくぐって D。"),
    P("cherry-river", "桜の川辺", "Cherry Blossom Riverside", "春・昼。川面に桜の花びらが流れていく、おだやかな昼", "3/4", 80, "F", "ionian",
      ("F C/E Dm7 Bbmaj7", "Gm7 C7sus4 Am7 Dm7", "Bbmaj7 Bbm6 C7sus4 F"), ("Bbmaj7 C/Bb Am7 Dm7", "Gm7 Eb C7sus4 C", "Bbmaj7 Db C7sus4 F"), "clarinet",
      "ワルツ。♭VII の Eb、♭VI の Db。"),
    P("spring-rain-window", "春雨の窓辺", "Spring Rain by the Window", "春・夜。窓をつたう春の雨を、灯りの下でながめる", "4/4s", 64, "Ab", "ionian",
      ("Abmaj7 Fm7 Dbmaj7 Eb/Db", "Cm7 Fm7 Bbm7 Ebsus4", "Dbmaj7 Dbm6 Ebsus4 Ab"), ("Dbmaj7 Eb/Db Cm7 Fm7", "Bbm7 Gb Ebsus4 Eb", "Dbmaj7 E Ebsus4 Ab"), "oboe",
      "♭VII の Gb、♭VI の E（Fb）が雨の陰。"),
    P("morning-birds", "小鳥のさえずる朝", "Birdsong Morning", "春・朝。木の枝で小鳥が鳴きかわす、晴れた朝", "6/8", 74, "G", "ionian",
      ("G D/F# Em7 Cmaj7", "Am7 D Bm7 Em7", "Cmaj7 Cm6 Dsus4 G"), ("Cmaj7 D/C Bm7 Em7", "Am7 F Dsus4 D", "Cmaj7 Bb Dsus4 G"), "flute",
      "6/8 で小鳥のはずみ。♭VII の F、♭III の Bb。"),
    P("tidepool-noon", "潮だまりの昼下がり", "Tide Pools in the Afternoon", "夏・昼。岩場の潮だまりに、きらきらと光がゆれる", "4/4s", 78, "E", "ionian",
      ("E B/D# C#m7 Amaj7", "F#m7 B C#m7 G#m7", "Amaj7 Am6 Bsus4 E"), ("Amaj7 B/A G#m7 C#m7", "F#m7 D Bsus4 B", "Amaj7 C Bsus4 E"), "fiddle",
      "♭VII の D、♭VI の C で光の色が変わる。"),
    P("summer-grove", "夏木立の木陰", "Shade of the Summer Grove", "夏・昼。大きな木の陰で、葉ずれの音を聞きながら休む", "3/4", 72, "C", "lydian",
      ("C D/C Em7 Am7", "Fmaj7 G/F Em7 Gsus4", "Fmaj7 D/F# Gsus4 C"), ("Am7 Em7 Fmaj7 D/F#", "Dm7 Bb Gsus4 G", "Fmaj7 Ab Gsus4 C"), "clarinet",
      "リディアン（D のコード）。♭VI の Ab。"),
    P("evening-cicadas", "ひぐらしの夕暮れ", "Evening Cicadas", "夏・夕。ひぐらしの声が遠くに聞こえる、夕焼けの帰り道", "4/4s", 62, "A", "aeolian",
      ("Am Fmaj7 C/G Dm7", "Am/G Fmaj7 Esus4 E", "Dm7 Bbmaj7 Esus4 Am"), ("Fmaj7 G Em7 Am7", "Dm7 G Cmaj7 E", "Fmaj7 Dm7 Esus4 Am"), "oboe",
      "ナポリの Bbmaj7 で夕暮れのせつなさ。"),
    P("firefly-stream", "蛍の小川", "Firefly Stream", "夏・夜。小川のほとりで、蛍がゆっくり光っては消える", "6/8", 56, "Bb", "ionian",
      ("Bbmaj7 Gm7 Cm7 F/A", "Dm7 Gm7 Ebmaj7 Fsus4", "Ebmaj7 Ebm6 Fsus4 Bb"), ("Gm7 Dm7/F Ebmaj7 Bb/D", "Cm7 Ab Fsus4 F", "Ebmaj7 Gb Fsus4 Bb"), "flute",
      "短調の Ebm6、♭VII の Ab、♭VI の Gb。"),
    P("starlit-lake", "星を映す湖", "Starlit Lake", "夏・夜。風のない湖に、満天の星がそのまま映る", "4/4s", 58, "Eb", "lydian",
      ("Eb F/Eb Gm7 Cm7", "Abmaj7 Bb/Ab Gm7 Bbsus4", "Abmaj7 F/A Bbsus4 Eb"), ("Cm7 Gm7 Abmaj7 F/A", "Fm7 Db Bbsus4 Bb", "Abmaj7 B Bbsus4 Eb"), "horn",
      "リディアン（F のコード）。ホルンが遠くから。♭VII の Db、♭VI の B（Cb）。"),
    P("after-shower", "夕立のあと", "After the Summer Shower", "夏・夕。夕立がやみ、ぬれた葉に夕日がさす", "4/4s", 74, "G", "mixolydian",
      ("G F/G C/G G", "Em7 F C/E Dsus4", "Cmaj7 F Dsus4 G"), ("Cmaj7 Am7 F Em7", "Am7 Bb Dsus4 D", "Cmaj7 F Dsus4 G"), "fiddle",
      "ミクソリディアン（F のコード）で雨上がりの明るさ。"),
    P("autumn-gorge", "紅葉の渓谷", "Crimson Gorge", "秋・昼。紅葉にそまった谷を、澄んだ川が流れる", "3/4", 70, "E", "dorian",
      ("Em A/E Em Bm7", "Cmaj7 G/B Am7 Bsus4", "Cmaj7 A/C# Bsus4 Em"), ("G D/F# Em7 A", "Cmaj7 Bm7 Am7 B", "Cmaj7 A7 Bsus4 Em"), "clarinet",
      "ドリアン（A のコード）。"),
    P("harvest-moon", "十五夜の月", "Harvest Moon", "秋・夜。すすきの向こうに、まるい月がのぼる", "6/8", 54, "F#", "aeolian",
      ("F#m E/G# Amaj7 Bm7", "Dmaj7 C#m7 Bm7 C#sus4", "Dmaj7 G C#sus4 F#m"), ("Amaj7 E/G# F#m7 Dmaj7", "Bm7 C#m7 Dmaj7 E", "Dmaj7 Bm7 C#sus4 F#m"), "flute",
      "ナポリの G で月の光。"),
    P("golden-wheat", "黄金の麦畑", "Golden Wheat Fields", "秋・夕。風が麦の穂をなでて、畑が金色の波になる", "4/4s", 72, "A", "ionian",
      ("A Dmaj7/A A C#m7", "F#m7 Bm7 Dmaj7 Esus4", "Bm7 Dm6 Esus4 A"), ("Dmaj7 C#m7 Bm7 Amaj7", "G D/F# Esus4 E", "Dmaj7 F Esus4 A"), "horn",
      "下がっていく B の和音（Dmaj7→C#m7→Bm7）。♭VII の G、♭VI の F。"),
    P("autumn-path", "秋の森の小径", "Autumn Forest Path", "秋・朝。落ち葉をふんで、朝の森の小径を歩く", "4/4s", 68, "D", "dorian",
      ("Dm G/D Dm Am7", "Bbmaj7 F/A Gm7 Asus4", "Bbmaj7 G/B Asus4 Dm"), ("F C/E Dm7 G", "Bbmaj7 Am7 Gm7 A", "Bbmaj7 G7 Asus4 Dm"), "oboe",
      "ドリアン（G のコード）。"),
    P("pampas-wind", "すすきの丘の風", "Wind over Silver Grass", "秋・夕。すすきの丘を、夕方の風がわたっていく", "3/4", 66, "B", "aeolian",
      ("Bm Gmaj7 D/A Em7", "Bm/A Gmaj7 F#sus4 F#", "Em7 Cmaj7 F#sus4 Bm"), ("Gmaj7 A F#m7 Bm7", "Em7 A Dmaj7 F#", "Gmaj7 Em7 F#sus4 Bm"), "fiddle",
      "ナポリの Cmaj7。"),
    P("first-snow", "初雪の朝", "First Snow Morning", "冬・朝。目がさめると、外が一面の初雪", "4/4s", 62, "C", "ionian",
      ("C Fmaj7/C C Em7", "Am7 Dm7 Fmaj7 Gsus4", "Am7 Fm6 Gsus4 C"), ("Fmaj7 Em7 Dm7 Cmaj7", "Bb F/A Gsus4 G", "Fmaj7 Ab Gsus4 C"), "flute",
      "短調の Fm6、♭VII の Bb、♭VI の Ab。"),
    P("frozen-lake", "凍った湖と冬空", "Frozen Lake under Winter Sky", "冬・昼。凍った湖の上に、どこまでも青い冬の空", "4/4s", 64, "F#", "dorian",
      ("F#m B/F# F#m C#m7", "Dmaj7 A/C# Bm7 C#sus4", "Dmaj7 B/D# C#sus4 F#m"), ("A E/G# F#m7 B", "Dmaj7 C#m7 Bm7 C#", "Dmaj7 B7 C#sus4 F#m"), "clarinet",
      "ドリアン（B のコード）。"),
    P("snow-lanterns", "雪夜のともしび", "Lanterns on a Snowy Night", "冬・夜。雪のつもる夜道に、家々の灯りがともる", "3/4", 58, "Eb", "ionian",
      ("Eb Abmaj7/Eb Eb Gm7", "Cm7 Abmaj7 Fm7 Bbsus4", "Abmaj7 Gm7 Fm7 Eb"), ("Cm Gm/Bb Abmaj7 Eb/G", "Fm7 Db Bbsus4 Bb", "Abmaj7 Abm6 Bbsus4 Eb"), "horn",
      "ワルツ。短調の Abm6、♭VII の Db。"),
    P("aurora", "オーロラの夜", "Aurora Night", "冬・夜。雪原の空に、オーロラがゆっくりゆれる", "4/4s", 56, "B", "lydian",
      ("B C#/B B C#/B", "G#m7 Emaj7 F#/E D#m7", "Emaj7 C#m7 F#sus4 B"), ("G#m7 D#m7 Emaj7 B/D#", "C#m7 A F#sus4 F#", "Emaj7 G F#sus4 B"), "fiddle",
      "リディアン（C# のコード）で光のゆれ。♭VII の A、♭VI の G。"),
    P("mountain-sunrise", "山頂の日の出", "Sunrise from the Summit", "朝。山の頂で、雲の向こうから日がのぼる", "4/4s", 68, "Bb", "lydian",
      ("Bb C/Bb Dm7 Gm7", "Ebmaj7 F/Eb Dm7 Fsus4", "Ebmaj7 C/E Fsus4 Bb"), ("Ebmaj7 Bb/D Cm7 F", "Gm7 Ebmaj7 Ab F", "Ebmaj7 Cm7 Fsus4 Bb"), "horn",
      "リディアン（C のコード）。ホルンが日の光。"),
    P("calm-sea", "凪の海の昼", "Calm Sea at Noon", "夏・昼。波のない海に、白い雲がうかぶ", "6/8", 64, "D", "ionian",
      ("D Gmaj7/D D F#m7", "Bm7 Em7 Gmaj7 Asus4", "Em7 Gm6 Asus4 D"), ("Gmaj7 F#m7 Em7 Dmaj7", "C G/B Asus4 A", "Gmaj7 Bb Asus4 D"), "clarinet",
      "短調の Gm6、♭VII の C、♭VI の Bb。"),
    P("dune-sunset", "砂丘の夕映え", "Dunes at Sunset", "夕。どこまでも続く砂丘が、夕日で赤くそまる", "4/4s", 62, "C#", "aeolian",
      ("C#m E/B Amaj7 F#m7", "Dmaj7 Amaj7 G#sus4 G#", "F#m7 D G#sus4 C#m"), ("Emaj7 B/D# C#m7 Amaj7", "F#m7 G#m7 Amaj7 B", "Amaj7 Dmaj7 G#sus4 C#m"), "oboe",
      "ナポリの D で砂の上のゆらめき。"),
    P("bamboo-rain", "竹林の雨", "Rain in the Bamboo Grove", "昼・雨。竹の葉に、しとしと雨が落ちる", "4/4s", 66, "G", "dorian",
      ("Gm7 Bbmaj7 C Gm7", "Ebmaj7 F Dsus4 D", "Cm7 Ebmaj7 Dsus4 Gm"), ("Ebmaj7 F/Eb Dm7 Gm7", "Cm7 F Bbmaj7 D", "Ebmaj7 C Dsus4 Gm"), "flute",
      "ドリアン（C のコード）。"),
    P("sea-of-clouds", "雲海の朝", "Sea of Clouds at Dawn", "朝。山から見下ろすと、足もとに雲の海が広がる", "3/4", 60, "Ab", "lydian",
      ("Ab Bb/Ab Cm7 Fm7", "Dbmaj7 Eb/Db Cm7 Ebsus4", "Dbmaj7 Bb/D Ebsus4 Ab"), ("Dbmaj7 Ab/C Bbm7 Eb", "Fm7 Dbmaj7 Gb Eb", "Dbmaj7 Bbm7 Ebsus4 Ab"), "fiddle",
      "リディアン（Bb のコード）。♭VII の Gb。"),
    P("moonlit-forest", "月夜の森", "Moonlit Forest", "夜。月の光が木々のあいだから、こけむした地面にさす", "6/8", 52, "E", "aeolian",
      ("Em Em/D Cmaj7 B7", "Am7 D Gmaj7 Cmaj7", "Am7 F B7sus4 Em"), ("Cmaj7 D/C Bm7 Em7", "Am7 Bm7 Cmaj7 B", "Cmaj7 Am7 B7sus4 Em"), "clarinet",
      "ナポリの F。"),
]

# 点数（Audiobox の PQ）で決めた曲ごとの調整（楽器の音量・入れかえなど。旋律は変えない）
FINAL = {}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "assets-src/ai-songs"
    tune = json.loads(os.environ["P25_TUNE"]) if "P25_TUNE" in os.environ else FINAL
    for n, s in enumerate(SONGS, 1):
        if which not in ("all", str(n), s["id"]): continue
        if f"{n:02d}" in tune:
            t = dict(tune[f"{n:02d}"]); top = {k: t.pop(k) for k in ("seed", "bpm", "mel_range", "cello_db", "lead_db", "gsoft", "gdb") if k in t}
            s = dict(s, band={**s["band"], **t}, **top)
        out = os.path.join(outdir, f"piano25-{n:02d}-{s['id']}.json")
        t = cs.build(s, out)
        j = json.load(open(out, encoding="utf-8")); j["titleEn"] = s["en"]
        json.dump(j, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{n:02d} {s['id']} {t:.0f}秒")
