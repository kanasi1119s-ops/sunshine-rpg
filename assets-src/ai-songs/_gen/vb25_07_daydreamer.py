# vb25 07「全速力デイドリーマー」Full-Speed Daydreamer（仮）— ロック（高速ロック・生のバンド）。B短調（サビは平行調の D長調）・196・4/4。
#   最後のサビは +1（E♭長調）
# 2026-10-25 作り直し: 物語の気持ちを強く（こわがりの自分をはげます空想）、歌を人が歌える旋律（8分と4分。16分の早口をやめた）に、テトの歌の版を足した。
# 物語: 大事な日の朝に寝坊した。駅まで全力で走りながら、頭の中では悪者をなぎ倒すヒーローになっている。本当の自分はこわがりだと
#   わかっているけれど、空想の中の強い自分に背中を押されて走る。信号待ちで一瞬だけ現実に戻り、青信号でまた走り出して、閉まりかけた扉に滑り込む。
# 場面と強さ: 目覚まし三秒前（ドラムだけ）→ 寝坊だ（ギター2本のリフ）→ 玄関を飛び出す（Aメロ）→ 空想スイッチ（Bメロ・溜め → 止め1）
#   → あと500メートル（サビ1）→ 全力ダッシュ（後サビ・短い呼びかけ）→ ヒーローのリフ（間奏）→ 商店街（2番。BGM はピアノが歌を受け取る）
#   → 空想スイッチ2（止め2）→ あと300メートル（サビ2）→ 全力ダッシュ2 → 信号待ち（全員休み）→ 本当の自分（Cメロ・Half feel）
#   → 必殺のギター（ソロ）→ 青信号（だんだん上がる → 止め → 1拍の完全な無音）→ 駅に滑り込む（最後のサビ・+1）→ 最後の全力ダッシュ → 扉が閉まる和音
# 旋律の性格: Aメロは8分で、句の頭を半拍休んで飛び込む。サビは同じ音を3つ置いてから下がる「はしれはしれ」。最高音 F#5（後サビ）。
# ほかの曲とちがう所: いちばん速い曲。生のギター2本・ベース・ドラム中心のロック、ピアノの合いの手、全員の止めが4回。
from vb25_lib import *

S = Song("07", "daydreamer", "全速力デイドリーマー（仮）", "Full-Speed Daydreamer", 196, 4, "B", "minor", "ロック（高速ロック・ボカロ）")
S.kit = "crocell-punch-heavy"   # 2026-10-26 人間「トリガーの音がバスドラの重さを掻き消しちゃってる。トリガー無くさなくていい」
S.extra.update({"tone": "rock", "diGuitar": "emily"})
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
K = S.key                    # B 短調
KD = Key("D", "major")       # サビ（平行調）
KC = Key("C", "minor")       # 最後の後サビ（+1）
KE = Key("Eb", "major")      # 最後のサビ（+1）


def chk(*lists):
    for L in lists:
        for x in L:
            t = sum(float(tok.split(":", 1)[1].rstrip("!,'_~^/\\")) for tok in x.split())
            assert abs(t - 4) < 1e-6, ("4拍ではない行", t, x)


RIFF_CH = ["Bm", "G", "A", "F#m", "Bm", "G", "A", "F#"]
A_CH = ["Bm", "G", "A", "F#m", "Bm", "G", "Em7", "F#"]
B_CH = ["Gmaj7", "A", "F#m7", "Bm7", "Em7", "A", "F#sus4", "F#"]
C_CH = ["G", "A", "F#m", "Bm", "G", "A", "D", "D/F#", "G", "A", "F#7", "Bm", "Em7", "A", "Bb", "A"]   # F#7＝vi への副属和音、Bb＝♭VI（借用）
HALF = ["Em", "F#m", "G", "A", "Em", "F#m", "G", "A#dim", "Gmaj7", "A", "Bm", "Bm/A", "G6", "Em7", "F#sus4", "F#"]   # A#dim＝vi（Bm）へ入る減三和音
GREEN = ["G", "A", "Bm", "Bm/A", "G", "A", "Bb", "Bb"]                                    # Bb＝次の調（E♭長調）の V

S.scene("目覚まし三秒前", 4, "intro", ["Bm"] * 4)
S.scene("寝坊だ", 12, "intro", RIFF_CH + RIFF_CH[:4])
S.scene("玄関を飛び出す", 16, "verse", A_CH)
S.scene("空想スイッチ", 8, "pre", B_CH)
S.scene("あと500メートル", 16, "chorus", C_CH)
S.scene("全力ダッシュ", 8, "interlude", RIFF_CH)
S.scene("ヒーローのリフ", 8, "interlude", RIFF_CH)
S.scene("商店街を駆け抜け", 16, "verse", A_CH)
S.scene("空想スイッチ2", 8, "pre", B_CH)
S.scene("あと300メートル", 16, "chorus", C_CH)
S.scene("全力ダッシュ2", 8, "interlude", RIFF_CH)
S.scene("信号待ち", 2, "break", ["F#", "F#"])
S.scene("空想の戦い", 16, "bridge", HALF)
S.scene("必殺のギター", 16, "solo", RIFF_CH)
S.scene("青信号", 8, "build", GREEN)
S.scene("駅に滑り込む", 32, "chorus", [tr_chord(c, 1) for c in C_CH + C_CH[:8] + ["G", "A", "Bm", "Bm", "G", "A", "D", "D"]])
S.scene("最後の全力ダッシュ", 8, "interlude", [tr_chord(c, 1) for c in RIFF_CH])
# 2026-10-26 人間「エイトビートもライドで刻むとか、ハイハット以外もつかって曲に合うように変えてほしい。これ重要」:
#   空想の場面（Bメロ）はライドでふわっと、2回目のサビはライドのカップ、ギターのソロは裏の開いたハイハット、駅に滑り込む最後のサビはクラッシュの4分
# 2026-10-26 人間「オープンとクローズのハイハットの使い分けとかね」: 玄関を飛び出す=closed・あと500メートル=openq
S.keepers = {'空想スイッチ': 'ride', '空想スイッチ2': 'ride', 'あと300メートル': 'bell', '必殺のギター': 'open', '駅に滑り込む': 'wash', '玄関を飛び出す': 'closed', 'あと500メートル': 'openq'}
# 2026-10-26 人間「シンプルなドラムのフレーズ色々入れて欲しい」「曲に合ったものを」「全部同じにするとつまらなくなる」:
#   1回目の Aメロの前半はキックが食う8ビートで、走り出しの足どり。サビにはどれも半拍前から食って飛びこむ（扉に滑り込む）
S.dmoves = [('玄関を飛び出す', 'beat', '8sync', 0, 7), ('あと500メートル', 'kui'), ('あと300メートル', 'kui'), ('駅に滑り込む', 'kui')]
S.scene("扉が閉まる", 4, "outro", ["Ab", "Bb", "Bb", "Ebadd9"])

# ================= パート =================
V = Voice(S, vol=0.22, delay=0.75, patch="fifths", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
GT = [S.track(f"ギター1（{['根音', '5度', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.095, 0.0)) for i in range(3)]
LG = S.track("ギター2（リフ）", "leadGuitar", **lead_gtr_spec(0.13, -0.05))
# 2026-10-26 人間（07）「リフのギターの音が強すぎて、楽器のソロパートが聞こえなくなっちゃってる」:
#   → 続けて「リフの音いい感じするから、ソロの音を大きくした方がいいかも」: リフと刻みはそのまま、ソロだけ別のパートで大きく（0.13→0.19）
LGS = S.track("ギター2（ソロ）", "leadGuitar", **lead_gtr_spec(0.19, 0.0))
LGS.spec["fx"] = [{"type": "tubescreamer", "pre": True, "gain": 0.45, "level": 0.6}] + list(LGS.spec["fx"]) + \
    [{"type": "pingpong", "beats": 0.75, "mix": 0.22, "feedback": 0.35}, {"type": "reverb", "mix": 0.16}]   # ソロだけペダルを踏みかえる
# 2026-10-26 人間（07）「ピロピロ音小さくてよく聞こえない」→ 16分の速い合いの手（サビのギター・ピアノの駆け下り）を別のパートにして前に
LGF = S.track("ギター2（サビの合いの手）", "leadGuitar", **lead_gtr_spec(0.2, 0.08))
PMF = S.track("ピアノ（16分の駆け下り）", "piano", volume=0.23, pan=-0.1, reverb=0.2, fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 2500, "high": 1.5}])
# 2026-10-26 人間（07）「ピロピロ聞こえないかな」（サビのギターの合いの手・ピアノの駆け下り・前奏と間奏のギターのリフ・ギターソロの4つとも）:
#   音量を上げるだけでは歪みの壁と同じ高さでぶつかって埋もれるので、ミックスで場所を作る:
#   ① 速いフレーズの4パートは 1.25 倍（リフ 0.13→0.16・ソロ 0.19→0.24・合いの手 0.2→0.25・ピアノ 0.23→0.29）と、輪郭の 2.5kHz を +3dB
#   ② 伴奏の歪みギター（パワーコード）は、速いフレーズの居場所の 2〜3kHz を −3.5dB へこませ、音量を 0.095→0.085 に
#   ③ ピアノの駆け下りは左（−0.3）へ寄せて、真ん中のギターとぶつからないように
for t_ in (LG, LGS, LGF):
    t_.spec["volume"] = round(t_.spec["volume"] * 1.25, 3)
    t_.spec["fx"] = list(t_.spec["fx"]) + [{"type": "eq", "low": 0, "mid": 3, "midHz": 2500, "high": 0.5}]
PMF.spec["volume"] = 0.29; PMF.spec["pan"] = -0.3
# 2026-10-26 人間（07）「聞こえるけどもう少し響かせてもいいかも」→ 速いフレーズに響きを足す:
#   リフと合いの手のギターは付点8分のピンポンディレイ（0.75拍・18%）とプレート（22%）、ピアノの駆け下りは残響 0.2→0.34 と短いディレイ
for t_ in (LG, LGF):
    t_.spec["fx"] = list(t_.spec["fx"]) + [{"type": "pingpong", "beats": 0.75, "mix": 0.18, "feedback": 0.3}, {"type": "plate", "mix": 0.22}]
PMF.spec["reverb"] = 0.34
PMF.spec["fx"] = list(PMF.spec["fx"]) + [{"type": "delay", "beats": 0.75, "mix": 0.14, "feedback": 0.25}]
for g_ in GT:
    g_.spec["volume"] = 0.085
    g_.spec["fx"] = list(g_.spec["fx"]) + [{"type": "eq", "low": 0, "mid": -3.5, "midHz": 2400, "high": 0}]
BASS = S.track("ベース（指弾き・歌うベース）", "bass", **rock_bass_spec(0.25))
# 2026-10-26 人間（07）「ベースを表に出してメロディ聞こえるようにしよう」→ 0.21→0.25（リフギターの曲の 1.2 倍で 0.30）、
#   指の当たりの 1.2kHz を +2.5dB（低い所だけでなく旋律の輪郭が聞こえるように）。下の「ベース」で場面ごとに旋律にした
BASS.spec["fx"] = list(BASS.spec["fx"]) + [{"type": "eq", "low": 0, "mid": 2.5, "midHz": 1200, "high": 0}]
PNFX = [{"type": "eq", "low": -2, "mid": -1.5, "midHz": 350, "high": 1}]
PM = S.track("ピアノ（合いの手・歌の受け渡し）", "piano", volume=0.15, pan=-0.15, reverb=0.22, fx=PNFX)
PC = [S.track(f"ピアノ（和音{i + 1}）", "piano", volume=0.1, pan=-0.15, reverb=0.22, fx=PNFX) for i in range(3)]
STR = [S.track(f"ストリングス{i + 1}（最後のサビ）", "strings", patch="stringEnsemble", volume=0.08, pan=0.25, reverb=0.35, sustain=1.5) for i in range(3)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（Aメロ・Bメロ・後サビ・Cメロは B短調 oct=3＝B3、サビは D長調 oct=4＝D4、最後のサビは E♭長調 oct=4） =================
VERSE = ["R:0.5 5:0.5 5:0.5 1':0.5 1':0.5 7:1 R:0.5", "6:1 5:1.5 R:1.5",
         "R:0.5 4:0.5 4:0.5 7:0.5 7:0.5 1':1 R:0.5", "7:1 5:1.5 R:1.5",
         "R:0.5 1':0.5 1':0.5 2':0.5 3':0.5 2':1 R:0.5", "1':2 R:2",
         "R:0.5 4:0.5 5:0.5 6:1 7:1 R:0.5", "#7:2 R:2",
         "R:0.5 3':0.5 3':0.5 3':0.5 2':0.5 1':1 R:0.5", "6:1 1':1.5 R:1.5",
         "R:0.5 2':0.5 2':0.5 2':0.5 1':0.5 7:1 R:0.5", "5:1 7:1.5 R:1.5",
         "R:0.5 5:0.5 1':0.5 3':0.5 5':0.5 4':1 R:0.5", "3':1 1':1.5 R:1.5",
         "R:0.5 4':0.5 3':0.5 2':1 1':1 R:0.5", "#7:2 R:2"]
V1 = "めざましのおと/とけいがわらう/うそでしょうと/とびおきる/ぱんをくわえて/くつをはいたら/げんかんのどあ/けりあけた"
V2 = "しょうてんがいを/かけぬけながら/あたまのなか/ひーろーだ/わるものたちを/なぎたおしてく/ほんとのわたし/うさぎのこ"
BM = ["R:0.5 6:0.5 6:0.5 7:0.5 1':0.5 2':0.5 3':1", "2':1 1':1.5 R:1.5", "R:0.5 5:0.5 5:0.5 7:0.5 2':0.5 3':1 R:0.5", "3':1 1':1.5 R:1.5",
      "R:0.5 4:0.5 4:0.5 6:0.5 1':0.5 3':1 R:0.5", "2':1 7:1.5 R:1.5", "R:0.5 1':0.5 2':0.5 3':0.5 4':0.5 5':1 R:0.5", "5':1 R:3"]
P1 = "めをとじればほら/ちがうせかいで/ゆめよろいきて/かぜになるの"
P2 = "こころのなかでは/りゅうさえたおす/そんなわたしで/いさせてよね"
CH = ["R:0.5 2':0.5 2':0.5 2':0.5 1':1 6:1", "7:2 R:2",
      "R:0.5 5:0.5 7:0.5 2':0.5 7:1 5:1", "6:1 1':1.5 R:1.5",
      "R:0.5 2':0.5 2':0.5 2':0.5 1':0.5 7:0.5 6:1", "1':1 7:1 5:1 R:1",
      "R:0.5 3:0.5 5:0.5 1':0.5 2':2", "1':1 7:1 R:2",
      "R:0.5 2':0.5 2':0.5 2':0.5 1':0.5 7:1 R:0.5", "1':1 5:1.5 R:1.5",
      "R:0.5 #5:0.5 7:0.5 2':0.5 2':1 R:1", "1':1 6:1.5 R:1.5",
      "R:0.5 2':0.5 2':0.5 2':0.5 1':0.5 7:0.5 5:1", "6:1 7:1.5 R:1.5",
      "R:0.5 b3:0.5 b3:0.5 4:0.5 b6:1 1':1", "7:1 5:1.5 R:1.5"]
C1 = "はしれはしれ/まだまにあうよ/あとごひゃくめーとる/かぜをこえて/はりぼてでいい/ゆめでもいい/わたしがわたしを/たすけにゆくの"
C2 = "はしれはしれ/しんごうまでは/のこりはあとすこし/はいがもえて/それでもいいの/あしをとめず/わたしのみらいを/まもりにゆくの"
LASTX = ["R:0.5 1':0.5 1':0.5 1':0.5 2':1 1':1", "7:1 5:1.5 R:1.5", "R:0.5 1':0.5 1':0.5 7:0.5 6:1 5:1", "6:1 1':1.5 R:1.5",
         "R:0.5 4:0.5 5:0.5 6:0.5 1':1 2':1", "1':1 7:1.5 R:1.5", "R:0.5 5:0.5 1':0.5 2':0.5 1':2", "2':1 1':3"]
LASTV = "とびらのむこう/あたらしいあさ/ゆめのつづきへ/いまいくから"
DASH = ["R:0.5 3':0.5 3':0.5 R:0.5 3':0.5 2':0.5 1':1", "R:0.5 4':0.5 4':0.5 R:0.5 4':0.5 3':0.5 1':1",
        "R:0.5 5':0.5 5':0.5 R:0.5 5':0.5 4':0.5 2':1", "5':0.5 R:0.5 #7:0.5 R:0.5 5:2"]
DASHm = DASH[:3] + ["5':0.5 R:0.5 7:0.5 R:0.5 5:2"]
DV = "ぜんりょくで/かけぬけろ/よろいきてはしれ/ぜんりょくで/かけぬけろ/このゆめではしれ"
HM = ["3':2 2':1 1':1", "2':3 R:1", "1':2 5:1 7:1", "1':2 3':2", "4':2 3':1 2':1", "2':3 R:1", "5':2 4':1 3':1", "4':2 2':1 R:1",
      "1':1 3':1 5':2", "4':2 2':2", "3':3 R:1", "2':1 1':1 7:1 6:1", "5:2 R:2", "6:1 1':1 4':2", "5':3 4':1", "#7:2 R:2"]
HV = "わかるよ/はりぼてのよろいだ/それでもね/はしりたいの/まえをむく/いまはしるよ"
GR = ["R:0.5 3:0.5 6:0.5 1':0.5 3':1 1':1", "R:0.5 4:0.5 7:0.5 2':0.5 4':1 2':1", "R:0.5 5:0.5 1':0.5 3':0.5 5':1 3':1", "4':1 3':1 2':1 1':1",
      "R:0.5 3':0.5 3':0.5 3':0.5 4':2", "4':1 5':1 4':1 2':1"]
GRE = ["5:1 7:1 2':1 R:1", "R:1 5:2 R:1"]
GV = "しんごうが/あおになる/いまだよとかぜがね/よろいがなくてもいける/よ"
chk(VERSE, BM, CH, LASTX, DASH, DASHm, HM, GR, GRE)
LY = Lyrics(S)
def put(name, key, lines, text, low=True, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m, low=low)
    LY.flow(bars, mel, text, name)
put("玄関を飛び出す", K, VERSE, V1)
if VOCAL: put("商店街を駆け抜け", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("商店街を駆け抜け")):
        if i < 8: PM.bar(b, K.mel(VERSE[i], oct=4))                   # BGM: 2番の前半は、ピアノが歌を受け取る（1オクターブ上）
        else: V.bar(b, K.mel(VERSE[i], oct=3))
put("空想スイッチ", K, BM, P1); put("空想スイッチ2", K, BM, P2)
put("あと500メートル", KD, CH, C1, o=4); put("あと300メートル", KD, CH, C2, o=4)
for name in ("全力ダッシュ", "全力ダッシュ2"):
    put(name, K, [(DASHm if i < 4 else DASH)[i % 4] for i in range(8)], DV)     # 4小節目は F#m（A）、8小節目は F#（A#）
bars = S.sc("空想の戦い"); mel = [K.mel(x, oct=3) for x in HM]
for i, (b, m) in enumerate(zip(bars, mel)): V.bar(b, m, low=(i >= 8))
LY.flow(bars, mel, HV, "空想の戦い")
bars = S.sc("青信号"); mel = [K.mel(x, oct=3) for x in GR] + [KE.mel(x, oct=4) for x in GRE]
for b, m in zip(bars, mel): V.bar(b, m)
LY.flow(bars, mel, GV, "青信号")
put("駅に滑り込む", KE, CH + CH[:8] + LASTX, C1 + "/" + "/".join(C2.split("/")[:4]) + "/" + LASTV, o=4)
for i, b in enumerate(S.sc("最後の全力ダッシュ")): V.bar(b, KC.mel((DASHm if i < 4 else DASH)[i % 4], oct=3))   # 最後のダッシュは歌の役（リード）だけ


# ================= ギター =================
# リフ（ギター2）: 16分＋休符の刻みと、オクターブの跳び。D3〜D5
RIFF = ["1:0.25 R:0.25 1:0.25 1':0.25 R:0.25 1:0.25 7:0.25 1':0.25 R:0.25 1:0.25 5:0.25 R:0.25 4:0.25 3:0.25 2:0.25 R:0.25",
        "6,:0.25 R:0.25 6,:0.25 6:0.25 R:0.25 6,:0.25 5:0.25 6:0.25 R:0.25 6,:0.25 3:0.25 R:0.25 2:0.25 1:0.25 7,:0.25 R:0.25",
        "7,:0.25 R:0.25 7,:0.25 7:0.25 R:0.25 7,:0.25 6:0.25 7:0.25 R:0.25 7,:0.25 4:0.25 R:0.25 3:0.25 2:0.25 1:0.25 R:0.25",
        "5,:0.25 R:0.25 5,:0.25 5:0.25 R:0.25 5,:0.25 4:0.25 5:0.25 2:0.5 7,:0.5 5,:1"]
RIFF8 = RIFF[:3] + ["5,:0.25 R:0.25 5,:0.25 5:0.25 R:0.25 5,:0.25 4:0.25 5:0.25 2:0.5 #7,:0.5 5,:1"]
# 必殺のギター（ソロ）
SOLO = ["1':0.5 2':0.5 3':0.5 5':0.5 4':1 3':1", "6:0.5 1':0.5 3':0.5 6':0.5 5':1 3':1", "7:0.5 2':0.5 4':0.5 7':0.5 6':1 4':1", "5':2 4':0.5 3':0.5 2':1",
        "1':0.25 2':0.25 3':0.25 4':0.25 5':0.5 3':0.5 1'':1 7':0.5 5':0.5", "6':0.25 5':0.25 3':0.25 1':0.25 6:0.5 1':0.5 3':1 R:1",
        "4':0.25 5':0.25 6':0.25 1'':0.25 7':0.5 6':0.5 5':1 4':1", "5':1 #7':3",
        "1'':0.5 7':0.25 5':0.25 3':0.5 5':0.5 1'':0.5 7':0.25 5':0.25 3':0.5 1':0.5",
        "6':0.5 5':0.25 3':0.25 1':0.5 3':0.5 6':0.5 5':0.25 3':0.25 1':0.5 6:0.5",
        "7':0.5 6':0.25 4':0.25 2':0.5 4':0.5 7':0.5 6':0.25 4':0.25 2':0.5 7:0.5", "5':1 4':1 2':1 5:1",
        "3':0.25 3':0.25 R:0.25 3':0.25 R:0.25 3':0.25 4':0.25 5':0.25 R:0.25 1'':0.25 R:0.25 7':0.25 5':1",
        "1'':0.25 1'':0.25 R:0.25 1'':0.25 R:0.25 7':0.25 6':0.25 5':0.25 R:0.25 3':0.25 R:0.25 1':0.25 3':1",
        "4':0.5 6':0.5 1'':0.5 2'':0.5 1'':1 7':1", "#7':2 R:2"]
chk(RIFF, RIFF8, SOLO)
for name in ("寝坊だ", "全力ダッシュ", "ヒーローのリフ", "全力ダッシュ2"):
    for i, b in enumerate(S.sc(name)): LG.bar(b, K.mel((RIFF if i % 8 < 4 else RIFF8)[i % 4], oct=3))
for i, b in enumerate(S.sc("最後の全力ダッシュ")): LG.bar(b, KC.mel((RIFF if i < 4 else RIFF8)[i % 4], oct=4))
# 2026-10-26 人間「どこかの曲でギターリフからのギターソロとかもあっていいかも」「ソロのところでエフェクト変える感じ」:
#   必殺のギターの頭4小節は、ギター2がリフ（乾いた音のまま）を弾き、5小節目からソロへ（ソロの音はペダルを踏みかえる:
#   オーバードライブのペダルで中域を押し出し、付点8分のピンポンディレイとホールの残響で広げる）
for i, b in enumerate(S.sc("必殺のギター")):
    if i < 4: LG.bar(b, K.mel(RIFF[i], oct=3))
    else: LGS.bar(b, K.mel(SOLO[i], oct=3))
# サビの4小節目ごとに、ギター2の短い合いの手（歌の伸ばしの所）
for name, kk in (("あと500メートル", KD), ("あと300メートル", KD), ("駅に滑り込む", KE)):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3 and i < 24: LGF.bar(b, kk.mel("R:2 5:0.25 6:0.25 1':0.25 2':0.25 3':0.5 1':0.5", oct=3))

# ギター1（パワーコード）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    pw = power(S.chords[b], "E2")
    if n in ("目覚まし三秒前", "信号待ち"): continue
    chorus = n in ("あと500メートル", "あと300メートル", "駅に滑り込む")
    if n == "寝坊だ" and i < 4: pat = "X:2! X:2"                                   # 最初は伸ばして、リフを聞かせる
    elif n in ("玄関を飛び出す", "商店街を駆け抜け"):
        pat = "X:1.5! X:1 X:1.5" if i < 8 else " ".join("X:0.5" + ("!" if j % 2 == 0 else "") for j in range(8))
    elif n.startswith("空想スイッチ"): pat = "X:1! X:1 X:1! X:1" if i < 7 else "X:1! X:1! R:2"
    elif n == "空想の戦い": pat = "X:4!" if i % 2 == 0 else "X:2! X:2"
    elif n == "最後の全力ダッシュ" or (n == "駅に滑り込む" and i >= 24): pat = "X:4!"          # 2026-10-26 人間「07、最後らへんのギターの音は伸ばしてもいいかも」
    elif n == "青信号": pat = " ".join("X:0.5" for _ in range(8)) if i < 7 else "X:1! R:3"
    elif n == "扉が閉まる": pat = {0: "X:0.5! R:0.5 X:0.5! R:2.5", 1: "X:4!", 2: "R:4", 3: "X:1! R:3"}[i]
    else: pat = " ".join("X:0.5" + ("!" if j % 2 == 0 else "") for j in range(8))
    if chorus and i == L - 1 and n != "駅に滑り込む": pat = "X:0.5! X:0.5 X:0.5 X:0.5 X:2!"
    # 2026-10-26 人間（07）「ピロピロ聞こえないかな」→ 測ると、速いフレーズは「ほかの全部」と同じくらいの大きさ（サビで −0.3〜−0.8dB・
    #   全力ダッシュ2 で −1.4dB）なのに聞こえにくい＝大きさより、同じ高さ（D3〜D5）でパワーコードのオクターブの音とぶつかって埋もれていた。
    #   リフの場面（寝坊だ・全力ダッシュ・ヒーローのリフ・最後の全力ダッシュ）と、サビの合いの手の小節では、パワーコードのオクターブ（上の音）を休ませる
    riffy = n in ("寝坊だ", "全力ダッシュ", "ヒーローのリフ", "全力ダッシュ2", "最後の全力ダッシュ") or (n == "必殺のギター") or (chorus and i % 4 == 3 and i < 24)
    for j in range(3):
        if j == 2 and riffy: continue
        GT[j].bar(b, pat.replace("X", nm(pw[j])))

# ================= ピアノ（合いの手・サビの和音） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    chorus = n in ("あと500メートル", "あと300メートル", "駅に滑り込む")
    v = voice(ch, 72, 3)
    if chorus:
        for j in range(3): PC[j].bar(b, " ".join(f"{nm(v[j])}:0.5" + ("" if q % 2 == 0 else ",") for q in range(8)))
    elif n == "空想の戦い":
        for j in range(3): PC[j].bar(b, f"{nm(v[j])}:4")
    # 合いの手: 歌のすき間（Aメロの4小節目ごと・間奏）に、16分の駆け下り
    if n in ("玄関を飛び出す",) and i % 4 == 3:
        PMF.bar(b, K.mel("R:3 5':0.25 4':0.25 3':0.25 1':0.25", oct=4))
    if n == "ヒーローのリフ":
        PMF.bar(b, K.mel(["R:2 1'':0.25 7':0.25 5':0.25 3':0.25 1':1", "R:2 3'':0.25 1'':0.25 7':0.25 5':0.25 3':1"][i % 2], oct=3))
    if n == "商店街を駆け抜け" and i >= 8 and i % 4 == 3:
        PMF.bar(b, K.mel("R:3 1'':0.25 7':0.25 5':0.25 4':0.25", oct=3))

# ストリングス（最後のサビだけ。急に生の弦が入る）
for i, b in enumerate(S.sc("駅に滑り込む")):
    v = voice(S.chords[b], 66, 3)
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")

# ================= ベース =================
def bfold(line, lo=28, hi=52):
    """ベースの音域（E1〜E3）に収める（低すぎる音は1オクターブ上、高すぎる音は1オクターブ下）"""
    out = []
    for t in line.split():
        nm_, rest = t.split(":", 1)
        if nm_ == "R": out.append(t); continue
        mm = midi(nm_)
        while mm < lo: mm += 12
        while mm > hi: mm -= 12
        out.append(f"{nm(mm)}:{rest}")
    return " ".join(out)

for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n in ("目覚まし三秒前", "信号待ち"): continue
    # 2026-10-26: 根音の8分だけだったのを、場面ごとに歌うベースに（sing_bass の walk/climb/drive/run/fall/ride）
    #   リフの場面（全力ダッシュ・ヒーローのリフ・最後の全力ダッシュ）は、ギター2のリフを2オクターブ下でいっしょに弾く（ユニゾンのリフ）
    if n == "寝坊だ": BASS.bar(b, f"{nm(r)}:2 {nm(r)}:2" if i < 4 else sing_bass(S, b, "run" if i % 4 == 3 else "drive"))
    elif n in ("玄関を飛び出す", "商店街を駆け抜け"):
        BASS.bar(b, sing_bass(S, b, ("walk" if i % 2 == 0 else "fall") if i < 8 else ("climb" if i % 2 == 0 else "drive")))
    elif n.startswith("空想スイッチ"): BASS.bar(b, sing_bass(S, b, "climb") if i < 7 else f"{nm(r)}:0.5 {nm(r)}:0.5 R:3")
    elif n in ("あと500メートル", "あと300メートル", "駅に滑り込む"):
        if n == "駅に滑り込む" and i >= 24: BASS.bar(b, sing_bass(S, b, "ride"))
        else: BASS.bar(b, sing_bass(S, b, "run" if i % 4 == 1 else "drive"))
    elif n in ("全力ダッシュ", "全力ダッシュ2", "ヒーローのリフ"):
        BASS.bar(b, bfold(K.mel((RIFF if i % 8 < 4 else RIFF8)[i % 4], oct=1)))
    elif n == "最後の全力ダッシュ": BASS.bar(b, bfold(KC.mel((RIFF if i < 4 else RIFF8)[i % 4], oct=1)))
    elif n == "必殺のギター": BASS.bar(b, bfold(K.mel(RIFF[i], oct=1)) if i < 4 else sing_bass(S, b, "walk" if i < 8 else ("drive" if i % 2 == 0 else "climb")))
    elif n == "空想の戦い": BASS.bar(b, bass_line(S, b, "half"))
    elif n == "青信号": BASS.bar(b, sing_bass(S, b, "climb") if i < 7 else f"{nm(r)}:1 R:3")
    elif n == "扉が閉まる": BASS.bar(b, {0: f"{nm(r)}:0.5 R:0.5 {nm(r)}:0.5 R:2.5", 1: f"{nm(r)}:4", 2: "R:4", 3: f"{nm(r)}:1 R:3"}[i])

# ================= 扉が閉まる =================
BD = S.sc("扉が閉まる")
PM.bar(BD[2], KE.mel("R:1 5':1 3':2", oct=4))                       # 発車のチャイム（ピン・ポーン）
FX.bar(BD[2], "R:2 E4:2")                                            # 扉の「プシュー」（ダウンリフター）
vE = voice("Ebadd9", 67, 4)
for j in range(3): PC[j].bar(BD[3], f"{nm(vE[j + 1])}:1!")
PM.bar(BD[3], f"{nm(vE[0] + 12)}:1!")
V.bar(BD[3], KE.mel("2':1", oct=4), low=False)
LY.bar(BD[3], KE.mel("2':1", oct=4), "ー")                       # 9度（F5）を、最後の和音の上で

riser(FX, S.sc("あと500メートル")[0], 4, "C4"); riser(FX, S.sc("あと300メートル")[0], 4, "C4")
riser(FX, S.sc("駅に滑り込む")[0] - 0.25, 8, "D4")
cym_swell(CYM, S.sc("寝坊だ")[0], 2, "C4"); cym_swell(CYM, S.sc("必殺のギター")[0], 2, "C4")
cym_swell(CYM, S.sc("空想の戦い")[0], 2, "E4")

# ================= ドラム（TRiDENT の音・crocell-punch） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    chorus = n in ("あと500メートル", "あと300メートル", "駅に滑り込む")
    if n == "目覚まし三秒前":
        # ドラムだけ: 8ビート → タムの回し → 16分のスネアで助走
        if i < 2: vgroove(D, b, "vrock2", ghosts=0.4, seed=b)
        elif i == 2: D.set(b, "X.......X.......", "....X.......X...", "." * 16); D.tom(b, "R:1 C4:0.25 C4:0.25 A3:0.5 R:1 F3:0.25 F3:0.25 D3:0.5!")
        else: D.set(b, "X.......X.X.X.X.", "....X...xxXXXXXX", "x.x.x.x........."); D.cym(b, "R:3.5 B2:0.5")
        if i == 0: D.cym(b, "D2:0.5 " * 8); D.H[b] = "." * 16
    elif n in ("寝坊だ", "全力ダッシュ", "ヒーローのリフ", "全力ダッシュ2", "最後の全力ダッシュ"):
        vgroove(D, b, "vrock", ghosts=0.35, seed=b)
        if i % 4 == 0: crash(D, b, "C2" if i % 8 == 0 else "G2")
        if n == "ヒーローのリフ" and i % 4 != 0: D.cym(b, "D2:0.5 " * 8); D.H[b] = "." * 16
        if i % 4 == 3 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "tomdown" if n != "最後の全力ダッシュ" else "snare16")
    elif n in ("玄関を飛び出す", "商店街を駆け抜け"):
        vgroove(D, b, "vrock2" if i < 8 else "vrock", ghosts=0.4, seed=b)
        if n == "商店街を駆け抜け" and i < 8: D.cym(b, ("F2:0.5 " if i % 2 == 0 else "D2:0.5 ") + "D2:0.5 " * 7); D.H[b] = "." * 16
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "tomtrip")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("空想スイッチ"):
        vgroove(D, b, "half" if i < 4 else "vrock2", ghosts=0.3, seed=b)
        if i == 0: crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2); crash(D, b, "C2", 4)                         # 止め（後ろ2拍は全員休み）
    elif chorus:
        name = "vrock"
        if n == "あと300メートル" and i < 8: name = "beat8"                  # 2回目のサビの前半は8ビート寄りに入れかえる
        vgroove(D, b, name, ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomtrip")
        if last and n != "駅に滑り込む": put_fill(D, b, "tomdown")
        if last and n == "駅に滑り込む": put_fill(D, b, "lift")
    elif n == "信号待ち":
        D.set(b, "." * 16, "." * 16, "." * 16)                               # 全員休み
    elif n == "空想の戦い":
        vgroove(D, b, "half", ghosts=0.3, seed=b, h="." * 16)
        D.cym(b, ("C2:1 " if i % 8 == 0 else "E2:1 ") + "E2:1 E2:1 E2:1")
        if i == 7: put_fill(D, b, "tomtrip")
        if last: put_fill(D, b, "build")
    elif n == "必殺のギター":
        vgroove(D, b, "vrock", ghosts=0.35, seed=b)
        if i % 4 == 0: crash(D, b, "C2" if i % 8 == 0 else "B2")
        if i % 4 == 3: put_fill(D, b, "snare16" if i % 8 == 7 else "small")
    elif n == "青信号":
        vgroove(D, b, "vrock2" if i < 4 else "vrock", ghosts=0.3, seed=b)
        if i in (0, 4): crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1); crash(D, b, "C2", 3)                        # 止め4（1拍目だけ）
    elif n == "扉が閉まる":
        if i == 0: D.set(b, "X.....X.........", "X.....X.........", "." * 16); crash(D, b, "G2", 4)
        elif i == 1: D.set(b, "X...............", "....X...XXXXXXXX", "." * 16); crash(D, b, "C2", 4)
        elif i == 2: D.set(b, "." * 16, "." * 16, "." * 16)
        else: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)

SIL.add(S.sc("空想スイッチ")[-1], 2, 4)              # 止め1
SIL.add(S.sc("空想スイッチ2")[-1], 2, 4)             # 止め2
SIL.add(S.sc("青信号")[-1], 1, 3)                    # 止め4（1拍目のあと、少し伸ばしの歌だけ残す）
SIL.add(S.sc("青信号")[-1], 3, 4)                    # 最後のサビの前の1拍は、完全な無音
SIL.add(BD[3], 1, 4)                                 # 扉が閉まる和音のあとは、何も鳴らさない（シンバルの余韻だけ）
SIL.apply()
V.bar(S.sc("青信号")[-1], KE.mel("R:1 5:2 R:1", oct=4))            # 止めの間に、歌の役だけが B♭4 を伸ばす

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の07。ロック（高速ロック・生のバンド）。B短調（サビは D）・196。最後のサビは +1（E♭）。"
          "大事な日に寝坊して、空想の中の強い自分に背中を押されて駅まで走る。ドラムだけで始まり、ギター2本のリフ、8分で飛び込む Aメロ、止め、「はしれはしれ」のサビ、"
          "短い呼びかけの後サビ、ピアノの合いの手、信号待ちの全員休み、Half feel の Cメロ、ギターのソロ、青信号の止めと1拍の無音、+1 の最後のサビ、扉が閉まる和音で切る。自作")
S.no_depth = True
teto(S, LY, V, special={"駅に滑り込む": 0.55, "空想の戦い": -0.45, "青信号": 0.15}, vib={"build": 30, "interlude": 28})
