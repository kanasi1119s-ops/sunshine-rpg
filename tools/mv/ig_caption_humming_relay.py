# HUMMING RELAY のインスタ用キャプション（SECOND SIGNAL と同じ形）。2026-11-08
# サビの歌詞は、動画の歌詞（/tmp/yt3/lines）のかなを漢字まじりに直したもの。英語は動画の英訳と同じ（/tmp/yt3/chorus.json）
# ハッシュタグは #VOCALOID・#ボカロ（2026-11-07 人間の指示。#UTAU は使わない）
import json
CH = json.load(open("/tmp/yt3/chorus.json", encoding="utf-8"))
rows = [l.rstrip("\n").split("\t") for l in open("/tmp/yt3/songs.tsv", encoding="utf-8")]
S = {
"01": (["ハッピーバースデー 君へ", "ひとり目はわたし", "ハッピーバースデー ゼロの", "合図で送るよ"],
       "0時。日付が変わる瞬間に、いちばんに「おめでとう」を送ろうと、スマホを持って待つ歌。",
       "Midnight. She waits, phone in hand, to be the very first to say \"happy birthday\" the moment the date changes."),
"02": (["真夜中のラジオに", "チャンネル合わせ", "誰かの物語", "街じゅうの声を"],
       "1時。深夜ラジオに出したおたよりが読まれる。最後にDJが、短い鼻歌を口ずさむ。",
       "1 a.m. Her letter is read on late-night radio, and the DJ hums a short little tune at the end."),
"03": (["カフェオレのあたたかさ", "手のひらに残る", "今日もよくがんばったね", "自分に言うの"],
       "2時。病院の夜勤の休み時間。紙コップのカフェオレで、自分をいたわる歌。",
       "2 a.m. On a break from the hospital night shift, she takes care of herself with a paper cup of café au lait."),
"04": (["走れ走れ 夜明け前", "坂を下れ 風になれ", "誰より先 街の朝", "ひとつひとつ配るんだ オーオーオ"],
       "3時。まだ暗い町を、自転車で新聞を配る。誰も知らない早起きの記録。",
       "3 a.m. Delivering newspapers by bike through the dark town: an early-bird record no one knows about."),
"05": (["白んでゆく", "街の空", "ひとりきりの", "夜が溶け"],
       "4時。終電を逃して、駅のベンチで朝を待つ。空がだんだん白くなる。",
       "4 a.m. Having missed the last train, she waits on a station bench as the sky slowly turns pale."),
"06": (["ソーレ引け", "朝の海", "重い網を引け", "空が燃える"],
       "5時。漁船が港を出る。じいちゃんの船に、初めて乗る孫の歌。",
       "5 a.m. The fishing boats leave port, and a grandchild rides grandpa's boat for the very first time."),
"07": (["焼きたての朝を", "どうぞどうぞ", "ふわっと甘い湯気", "街に広がれ"],
       "6時。町のパン屋の朝。いちばん最初のパンが焼きあがる。",
       "6 a.m. Morning at the town bakery, as the very first bread comes out of the oven."),
"08": (["みんな歌え", "7時半", "満員でも", "ステージだ"],
       "7時。ぎゅうぎゅうの通勤電車が、急にミュージカルの舞台になる。",
       "7 a.m. A packed rush-hour train suddenly turns into a musical stage."),
"09": (["言いわけ選手権", "優勝は誰", "大きな話ほどね", "キラキラ光るの"],
       "8時。遅刻した理由を、どんどん大げさに考えていく歌。",
       "8 a.m. The excuses for being late keep getting bigger and bigger."),
"10": (["落書き行進だ", "ページを越えて", "数字もいっしょに踊る", "イチ・ニ・サン・シ・ゴー"],
       "9時。授業中、教科書のすみの落書きたちが動き出す。",
       "9 a.m. In the middle of class, the doodles in the corner of the textbook come to life."),
"11": (["洗濯日和だよ", "シーツはためく", "風のリズムに乗って", "空まで踊ろう"],
       "10時。晴れた日、ベランダで洗濯物を干しながら、つい踊ってしまう歌。",
       "10 a.m. On a sunny day, hanging laundry on the balcony turns into a dance."),
"12": (["図書館だからね", "声はダメよ", "まなざしで語る", "ないしょ話"],
       "11時。図書館で同じ本に手をのばした二人。声に出せない会話。",
       "11 a.m. Two people reach for the same library book and talk without saying a word."),
"13": (["お弁当の条約", "ここに結ぼうよ", "卵焼きとタコさん", "一個ずつ交換"],
       "12時。昼休み、おかずの交換を、大まじめに話し合う歌。",
       "Noon. At lunch break, trading side dishes becomes a very serious negotiation."),
"14": (["工事中のステップ", "カンカン ズンズン", "工事中のステップ", "空へのぼる"],
       "13時。ビルの工事現場。はたらく人たちの音が、そのままリズムになる。",
       "1 p.m. At a building site, the sounds of the workers become the rhythm."),
"15": (["ばあちゃんのスタンプ", "ポンポン届く", "笑顔の猫がまた", "おじぎしてるよ"],
       "14時。遠くに住むおばあちゃんが、はじめてスタンプを送ってくる。",
       "2 p.m. Grandma, who lives far away, sends her very first stickers."),
"16": (["おやつ戦争だ", "ゆずれないよ", "スプーンを抜けば", "雷鳴る"],
       "15時。兄弟で最後のプリンをめぐる大げんか（大まじめに、大げさに）。",
       "3 p.m. Siblings go to war over the last pudding, completely serious and completely over the top."),
"17": (["放課後のタップ", "指が踊る", "はみ出すリズム", "それもいいね"],
       "16時。放課後の空き教室で、軽音部が新しい曲をつくる。",
       "4 p.m. In an empty classroom after school, the light-music club writes a new song."),
"18": (["交代だ", "あかね色", "光のバトンを", "手渡すよ"],
       "17時。太陽と月が、空の当番を交代する。",
       "5 p.m. The sun and the moon change shifts in the sky."),
"19": (["ラストのセールだよ", "街じゅうで踊ろう", "街角のサンバだ", "鳴らせ鳴らせ"],
       "18時。閉店する商店街の店が、最後の日をお祭りにする。",
       "6 p.m. On their final day, the closing shops on the street throw a festival."),
"20": (["湯けむりスウィング", "みんなで揺れよう", "桶でリズムとり", "湯につかろう"],
       "19時。町の銭湯。湯船で、知らないおじさんたちと歌いだす。",
       "7 p.m. At the neighborhood bathhouse, she starts singing in the tub with strangers."),
"21": (["重なる声", "画面ごしに", "遠く離れ", "同じ歌を"],
       "20時。遠くの友だちと、画面ごしに一緒に歌う。",
       "8 p.m. Friends far apart sing together through a screen."),
"22": (["コインランドリーの", "青い夜の中", "回る思い出を", "干してゆこう"],
       "21時。夜のコインランドリー。回るドラムを見ながら、ひとりで考えごと。",
       "9 p.m. At a coin laundry at night, she watches the drum spin and thinks."),
"23": (["光れよ", "くらげよ", "夜の海", "飛んでけ"],
       "22時。閉館後の水族館。飼育員が、くらげの水そうの前でひとやすみ。",
       "10 p.m. After closing time at the aquarium, a keeper rests in front of the jellyfish tank."),
"24": (["明日のわたしは", "何を着てくの", "くるりと回れば", "決まらないの"],
       "23時。初デートの前の夜。鏡の前で、服を何度も着がえる。",
       "11 p.m. The night before a first date, trying on outfit after outfit in front of the mirror."),
"25": (["25時の歌", "さあ歌おう", "25時の歌", "明日へゆく"],
       "24時。日付がまた変わる。今日の24人が、それぞれの場所で同じ鼻歌を歌う。",
       "Midnight again. The 24 people of today all hum the same little tune, each in their own place."),
}
out = []
for no, jp, en, *_ in rows:
    lines, sj, se = S[no]
    eng = CH[no]["en"]
    out.append(f"""━━━━━━━━━━━━━━━━
♪ {no} / 25　{jp} / {en}
アルバム: ハミング・リレー / HUMMING RELAY
歌: 重音テト / Vocal: Kasane Teto

■ 歌詞（サビ） / Lyrics (chorus)
""" + "\n".join(lines) + "\n\n" + "\n".join(eng) + f"""

■ 世界観 / Story
{sj}
{se}

■ 制作 / Credits
作詞・作曲・編曲・映像: Sunshine Pixel Sound
すべてオリジナル曲です。 / All songs are original.

#重音テト #KasaneTeto #オリジナル曲 #VOCALOID #ボカロ #HUMMINGRELAY
""")
txt = """HUMMING RELAY（ハミング・リレー）Instagram キャプション（1曲ずつ）
ひとつの街の 0時から24時まで。1時の深夜ラジオで流れた短い鼻歌が、人から人へ伝わっていく全25曲。

""" + "\n".join(out)
open("/mnt/user-data/outputs/humming_relay/HUMMING RELAY Instagramキャプション.txt", "w", encoding="utf-8").write(txt)
print(out[0]); print(out[24])
