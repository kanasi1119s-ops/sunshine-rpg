# SECOND SIGNAL のインスタ用キャプション（前回 NEON FROSTLINE と同じ形）
# 歌詞（サビ）は台本のかな歌詞を漢字まじりに直したもの。英語は動画の英訳と同じ。
import json
EN = json.load(open("/tmp/ig/chorus_pairs.json", encoding="utf-8"))
rows = [l.rstrip("\n").split("\t") for l in open("/tmp/yt2/songs.tsv", encoding="utf-8")]
# 番号: (サビの漢字まじり4行, 英語の行の範囲（動画の歌詞の行番号）, 世界観 和, 世界観 英)
S = {
"01": (["ハロー きみの声 ちゃんと聞こえるよ", "ノイズの向こうに きみがいたの", "ハロー 朝の街 耳をすましたら", "きみのおはようが いちばんに届く"], None,
       "イヤホンで世界にふたをして通学していた子が、片方だけ外して、きみの声を聞く朝の歌。",
       "A girl who rode to school with her earphones shutting out the world takes one of them out, and hears your voice."),
"02": (["シャボン玉 いま 空へのぼってゆく", "わたしの声も 飛んでいけよ", "フォルテッシモへと フォルテッシモの空", "届け みんなへ 笑って歌う"], None,
       "引っこみ思案の子が、合唱コンクールで、はじめて大きな声を出す歌。",
       "A shy girl lets out her voice, loud and clear, for the first time at the school choir contest."),
"03": (["まだ起きてる？ うん 起きてる", "それだけの言葉 あたたかいよ", "まだ起きてる？ もう少しね", "夜明けが来るまで このままでね"], None,
       "眠れない夜、通話をつないだまま、何も話さずにそれぞれの作業をする友だちの歌。",
       "On a sleepless night, two friends keep a call open, saying almost nothing, each working on their own."),
"04": (["ありがとう言うよ シャッターの前でね", "エプロンたたんで またねって言う", "ラストオーダーは さよならじゃないよ", "明日のわたしへ 続くからね"], None,
       "アルバイト最後の夜。閉店後の店で、店長と仲間に言えなかった「ありがとう」を伝える歌。",
       "The last night at a part-time job. After closing, she finally says the thank-you she never could."),
"05": (["ペンギンステップで 踊るんだよ", "よちよちのリズム わたしのもの"], None,
       "ダンスの授業が苦手な子が、自分のよちよち歩きのリズムでいいんだと気づく歌。",
       "A kid who struggles in dance class realizes her own little waddling rhythm is just fine."),
"06": (["カラーパレットの まんなかに立つよ", "どの色よりも 赤くなれる"], None,
       "地方から上京して、色の多すぎる街で、自分の色をさがす歌。",
       "Moving to the big city from a small town, she searches for her own color in a place with too many colors."),
"07": (["本当のことをね 今から言うから", "宇宙人じゃない ただのわたし", "それでもいいなら もう一度言うね", "はじめましてだよ よろしくだね"], None,
       "転校初日に「宇宙人です」とうそをついた。そのうそで、最初の友だちができた。本当のことを言う日の歌。",
       "On her first day at a new school she lied, \"I'm an alien,\" and made her first friend. Now she tells the truth."),
"08": (["はなまるちょうだい このわたしに", "できなかったことも 小さなまる", "はなまるの数を 数えないで", "がんばった自分に まるつけよう"], None,
       "大人になって失敗した日、小学校の先生がくれた「はなまる」を思い出す歌。",
       "On a day of failure as a grown-up, she remembers the flower-circle stamps her elementary school teacher gave her."),
"09": (["ヘッドライトの先 海が見える", "眠る母にそっと 口ずさむの", "母の子守唄 いまわたしが", "セレナーデにして 返すからね"], None,
       "免許をとって初めての夜のドライブ。助手席で眠る母を、家まで送りとどける歌。",
       "Her first night drive after getting her license, carrying her sleeping mother home in the passenger seat."),
"10": (["ゆびきりのルール 数えなくて", "いいんだよって きみ 笑ってくれた", "数えた数より 大事なこと", "守れなかった日も そばにいたい"], None,
       "約束を数えるのが癖の子が、守れなかった約束に向き合う歌。",
       "A girl who always counts her promises faces the one she couldn't keep."),
"11": (["クロスフェードして 気持ちがゆれるよ", "悲しい歌から 明るい歌", "クロスフェードして 次の曲へとね", "好きって気持ちだけ 変わらないの"], None,
       "好きな人のプレイリストを聞く。曲が変わるたびに、気持ちがゆれる歌。",
       "Listening to the playlist of the person she likes, her heart sways every time the song changes."),
"12": (["天気雨 青空に 光る粒 泣きながら", "天気雨 さよならは 晴れの日に 会うといい"], (8, 12),
       "卒業式のあと、晴れているのに雨が降る。泣いているのを、空のせいにする歌。",
       "After graduation, rain falls under a sunny sky, and she blames her tears on the weather."),
"13": (["ビー玉の中 夏がゆれてる", "あの日の空は 水色だね", "ビー玉の中 みんながいるよ", "なくさないよう にぎりしめる"], None,
       "祖母の家の縁側。ビー玉をのぞくと、去年の夏が映る歌。",
       "On the veranda of her grandmother's house, she looks into a marble and sees last summer."),
"14": (["ポップコーン はじけ 夜中の台所", "がんばれわたしって 小さく言う", "ポップコーンだから まだかたいけれど", "明日はきっとほら はじけるんだ"], (12, 19),
       "受験勉強の夜。こっそりポップコーンを作りながら、自分で自分を応援する歌。",
       "Studying late for exams, she secretly makes popcorn and cheers herself on."),
"15": (["ガラスの靴はね はかないもん", "自分の足でね 走るんだよ", "王子さまなんか 待たないから", "十二時すぎても 止まらないの"], None,
       "待っているだけはやめた。自分の足で走ると決める歌。",
       "No more just waiting. She decides to run on her own two feet."),
"16": (["おやすみを言うよ 同じ月の下", "はなれていてもね ここにいるよ"], None,
       "遠距離の恋人と、同じ月を見ながら電話で「おやすみ」を言う歌。",
       "Far apart, two people look at the same moon and say goodnight over the phone."),
"17": (["シンクロするんだ 縄の音あわせ", "みんなの息がね ひとつになる", "シンクロするんだ 引っかかってもいいよ", "もう一回跳ぼう いち・に・の・さん"], None,
       "大縄跳びの大会。クラスみんなで息を合わせる歌。",
       "At the long-rope jumping contest, the whole class breathes and jumps as one."),
"18": (["からくりのワルツ 最後に踊ってよ", "ねじを巻いたなら 動きだすよ", "からくりのワルツ 祖父の手のあとが", "歯車の中に 生きているよ"], None,
       "時計職人の祖父の店をたたむ日。からくり人形が最後に踊る歌。",
       "The day her clockmaker grandfather's shop closes, the clockwork doll dances one last time."),
"19": (["いいねの数だけ 笑えていたかな", "スマホを置いたら 空があるね"], None,
       "SNSの数字に疲れた子が、スマホを置いて夕焼けを見る歌。",
       "Tired of the numbers on social media, she puts down her phone and watches the sunset."),
"20": (["センパイのとなり ちょっとだけブルース", "まあいいかって言う その横顔"], None,
       "部活の先輩の引退試合。言えなかった「あこがれていました」の歌。",
       "Her club senpai's last game, and the words she never said: \"I always looked up to you.\""),
"21": (["シュガーレスな声で 好きってそのまま言う", "飾りは何もない ラブコールだよ"], None,
       "甘い言葉が苦手な二人の、ぶっきらぼうな告白の歌。",
       "A blunt, sugar-free confession between two people who are bad at sweet words."),
"22": (["明日の天気は 晴れのちハレルヤ", "涙の雨あと 虹がかかる", "傘をたたんだら きみに会いにいく", "あの交差点で ハレルヤだね"], None,
       "結婚式の前の夜。姉に「おめでとう」を伝える妹の歌。",
       "On the night before her sister's wedding, a younger sister finds the words to say congratulations."),
"23": (["光を追いかけ 夜をこえてゆく", "眠る街の空 帰る場所へ"], (8, 11),
       "夜行バスで、久しぶりにふるさとへ帰る歌。",
       "Riding the night bus, she heads home to her hometown for the first time in years."),
"24": (["ねこじゃらし ゆらゆらり", "左右 くるくるり", "つかまえた と思ったら", "逃げられた"], None,
       "拾った子猫と暮らしはじめた春。日だまりで、ねこじゃらしで遊ぶ歌。",
       "The spring she started living with a kitten she found: playing with a foxtail in the sunlight."),
"25": (["フィナーレはきみの 声で歌おうよ", "小さな声でも 届くからね"], (8, 12),
       "アルバムの最後。歌うのがこわかった「わたし」が、自分の声で歌いきる歌。",
       "The album's finale: the girl who was afraid to sing sings it through in her own voice."),
}
ALL = json.load(open("/tmp/ig/en_all.json", encoding="utf-8"))
out = []
for no, jp, en, *_ in rows:
    lines, rng, sj, se = S[no]
    if rng: eng = ALL[no][rng[0]:rng[1]]
    else: eng = [b for _, b in EN[no]]
    out.append(f"""━━━━━━━━━━━━━━━━
♪ {no} / 25　{jp} / {en}
アルバム: セカンド・シグナル / SECOND SIGNAL
歌: 重音テト / Vocal: Kasane Teto

■ 歌詞（サビ） / Lyrics (chorus)
""" + "\n".join(lines) + "\n\n" + "\n".join(eng) + f"""

■ 世界観 / Story
{sj}
{se}

■ 制作 / Credits
作詞・作曲・編曲・映像: Sunshine Pixel Sound
すべてオリジナル曲です。 / All songs are original.

#重音テト #KasaneTeto #オリジナル曲 #UTAU #SECONDSIGNAL
""")
open("/tmp/ig/SECOND SIGNAL Instagramキャプション.txt", "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out[:2])); print(out[11]); print(out[24])
