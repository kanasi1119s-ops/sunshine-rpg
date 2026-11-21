# HUMMING RELAY 作り直し版（2026-11-22）の動画情報: アルバムの説明文・1曲ずつの YouTube の題名と説明文とタグ・Instagram のキャプション。
# サビの歌詞は動画の歌詞（かな）を漢字まじりに直したもの。英語は動画の英訳に合わせた。ハッシュタグは #VOCALOID・#ボカロ（2026-11-07 人間の指示）。
#   python3 hr2_info.py <songs.tsv> <songs_all.txt（番号・JSON・mp3）> <出力フォルダ>
import sys, subprocess, os
TSV, ALL, DST = sys.argv[1:4]
rows = [l.rstrip("\n").split("\t") for l in open(TSV, encoding="utf-8") if l.strip()]
mp3 = {l.split("\t")[0]: l.rstrip("\n").split("\t")[2] for l in open(ALL, encoding="utf-8") if l.strip()}
S = {
"01": ("0時", "Midnight", ["ハッピーバースデー 君へ", "ひとり目はわたし", "ハッピーバースデー ゼロの", "合図で送るよ"], ["Happy birthday to you", "The very first one is me", "Happy birthday, at the signal", "of zero o'clock, I'll send it"],
       "日付が変わる瞬間に、いちばんに「おめでとう」を送ろうと、スマホを持って待つ歌。", "She waits, phone in hand, to be the very first to say \"happy birthday\" the moment the date changes."),
"02": ("1時", "1 a.m.", ["眠れないかもめ", "夜を渡るよ", "眠れないかもめ", "誰かの窓へ"], ["Sleepless Seagull", "crosses the night", "Sleepless Seagull", "to someone's window"],
       "深夜ラジオに出したおたよりが読まれる。最後に、短い鼻歌が流れる。", "Her letter is read on late-night radio, and a short little tune is hummed at the end."),
"03": ("2時", "2 a.m.", ["あったかいね あったかいね", "手のひらの中で", "あったかいね あったかいね", "紙コップひとつで"], ["It's warm, it's warm", "in the palms of my hands", "It's warm, it's warm", "with just one paper cup"],
       "病院の夜勤の休み時間。紙コップのカフェオレで、自分をいたわる歌。", "On a break from the hospital night shift, she takes care of herself with a paper cup of café au lait."),
"04": ("3時", "3 a.m.", ["チリンチリン 朝を配るよ", "チリンチリン 街じゅうの窓へ", "風になる 夜明けへ", "誰も知らない一番乗り"], ["Ring-a-ling, I hand out the morning", "Ring-a-ling, to every window in town", "I become the wind, toward the dawn", "the very first, and nobody knows"],
       "まだ暗い町を、自転車で新聞を配る。誰も知らない早起きの記録。", "Delivering newspapers by bike through the dark town: an early-bird record no one knows about."),
"05": ("4時", "4 a.m.", ["あと少し", "あと少し", "おはようまで", "もう少し"], ["Just a little more", "just a little more", "until \"good morning\"", "a little bit more"],
       "終電を逃して、駅のベンチで朝を待つ。空がだんだん白くなる。", "Having missed the last train, she waits on a station bench as the sky slowly turns pale."),
"06": ("5時", "5 a.m.", ["網を引け 朝の海", "網を引け 空が燃え", "じいちゃんの横 並んでね", "海の子だ"], ["Haul the net! The morning sea", "Haul the net! The sky's on fire", "Side by side with Grandpa", "I'm a child of the sea"],
       "漁船が港を出る。じいちゃんの船に、初めて乗る孫の歌。", "The fishing boats leave port, and a grandchild rides Grandpa's boat for the very first time."),
"07": ("6時", "6 a.m.", ["ふくらめ ふくらめ", "今日が焼きあがる", "もうすぐ もうすぐ", "街じゅうの朝が"], ["Rise up, rise up", "Today is baking", "Almost, almost", "the morning of the whole town"],
       "町のパン屋の朝。いちばん最初のパンが焼きあがる。", "Morning at the town bakery, as the very first bread comes out of the oven."),
"08": ("7時", "7 a.m.", ["イチ・ニ・サン ゆれる車内", "舞踏会のよう", "イチ・ニ・サン つり革たち", "シャンデリアになる"], ["One two three, the swaying car", "is like a ballroom", "One two three, the hanging straps", "turn into chandeliers"],
       "ぎゅうぎゅうの通勤電車が、急にミュージカルの舞台になる。", "A packed rush-hour train suddenly turns into a musical stage."),
"09": ("8時", "8 a.m.", ["ちがうんです 寝坊じゃない", "ちがうんです 聞いてほしい", "ちがうんです 本当です", "ちがうんです わけがあるの"], ["It's not that! I didn't oversleep", "It's not that! Please listen", "It's not that! It's true", "It's not that! There's a reason"],
       "遅刻した理由を、どんどん大げさに考えていく歌。", "The excuses for being late keep getting bigger and bigger."),
"10": ("9時", "9 a.m.", ["ふわり ふわり 飛ぶよ", "ふわり ふわり 笑う", "中は秘密だよ", "ふわり ふわり 君へ"], ["Floating, floating, off they fly", "Floating, floating, smiling", "What's inside is a secret", "Floating, floating, to you"],
       "駅前で風船を配るくま。外では元気に踊り、中では汗だくで息を整える歌。", "A bear hands out balloons by the station: dancing outside, dripping with sweat and catching a breath inside."),
"11": ("10時", "10 a.m.", ["水たまりには", "空が落ちてる", "飛びこえるたび", "雲をまたぐよ"], ["In every puddle", "the sky has fallen", "Each time I jump across", "I step over a cloud"],
       "雨が上がって、水たまりをとび石のように跳んで渡る歌。", "The rain lets up, and she hops across the puddles like stepping stones."),
"12": ("11時", "11 a.m.", ["るるるるる 静かな歌", "るるるるる 響いてる", "るるるるる 声はなくて", "るるるるる 伝わるよ"], ["Loo loo loo, a quiet song", "Loo loo loo, is echoing", "Loo loo loo, without a voice", "Loo loo loo, it still gets across"],
       "図書館で、となりの席の小さな鼻歌が、本だなをこえて広がっていく。", "In the library, a little hummed tune from the next seat spreads beyond the bookshelves."),
"13": ("12時", "Noon", ["交換しよ", "卵焼き 交換しよ", "からあげと", "二つと一つでどう"], ["Let's trade", "A rolled omelet, let's trade", "for fried chicken", "two for one, how about it?"],
       "昼休み、おかずの交換を、大まじめに話し合う歌。", "At lunch break, trading side dishes becomes a very serious negotiation."),
"14": ("13時", "1 p.m.", ["トンテンカン 響く音", "トンテンカン 空高く", "何もない場所に", "明日を建てる"], ["Clang, clang, clang, the echoing sound", "Clang, clang, clang, high in the sky", "where there was nothing", "we build tomorrow"],
       "ビルの工事現場。はたらく人たちの音が、そのままリズムになる。", "At a building site, the sounds of the workers become the rhythm."),
"15": ("14時", "2 p.m.", ["ピコンピコン 届いたよ", "おじぎの猫に 花のくまね", "ピコンピコン また来たよ", "ハートが三つも並んでるよ"], ["Ping, ping, it's arrived", "A bowing cat, and a bear with a flower", "Ping, ping, another one", "Three hearts all in a row"],
       "遠くに住むおばあちゃんが、はじめてスタンプを送ってくる。", "Grandma, who lives far away, sends her very first stickers."),
"16": ("15時", "3 p.m.", ["いくさの鐘 鳴りひびく", "月はひとつだけ", "銀の剣をかかげて", "ゆずれぬ三時だ"], ["The bell of battle rings out", "There is only one moon", "Raising my silver sword", "it's three o'clock, no backing down"],
       "冷蔵庫の最後のプリン（金色の月）をめぐる、大まじめで大げさな決闘。", "A completely serious, completely over-the-top duel over the last pudding in the fridge: the golden moon."),
"17": ("16時", "4 p.m.", ["タッピング タッピング 響け", "川をこえていけよ", "名前のない鳥 はばたけ", "夕焼けの向こうへ"], ["Tapping, tapping, ring out", "Go on, cross the rivers", "Nameless bird, flap your wings", "beyond the sunset"],
       "放課後の教室で、まだ名前のない曲が生まれる。", "In a classroom after school, a song that has no name yet is born."),
"18": ("17時", "5 p.m.", ["またあした", "あとを頼む", "またあした", "夜空を"], ["See you tomorrow", "I leave the rest to you", "See you tomorrow", "the night sky is yours"],
       "太陽と月が、空の当番を交代する。", "The sun and the moon change shifts in the sky."),
"19": ("18時", "6 p.m.", ["もうひと声 最後の日だから", "いちばんにぎやか", "涙はおまけに", "つけとくよ"], ["\"One more discount!\" Because it's the last day", "it's the liveliest of all", "The tears are thrown in", "for free"],
       "閉店する商店街の店が、最後の日をお祭りにする。", "On their final day, the closing shops on the street throw a festival."),
"20": ("19時", "7 p.m.", ["白いもやの中", "今日が溶けていく", "壁の向こう側", "声がふたつある"], ["Inside the white haze", "today melts away", "On the other side of the wall", "there are two voices"],
       "町の銭湯。壁の向こうの知らない誰かと、同じ鼻歌を歌う。", "At the neighborhood bathhouse, she hums the same tune as a stranger on the other side of the wall."),
"21": ("20時", "8 p.m.", ["天井が消えた部屋で", "街がまぶたを閉じたら", "隠れてた光たちが", "いま降りそそいでる"], ["In the room where the ceiling vanished", "when the town closed its eyelids", "the lights that had been hiding", "are pouring down now"],
       "街の明かりが消えた夜。屋上に上がると、隠れていた星が降ってくる。", "On a night when the town's lights go out, she climbs to the roof and the hidden stars come pouring down."),
"22": ("21時", "9 p.m.", ["海になる窓", "波うつシャツは", "泳いでるのは", "きのうのわたし"], ["The window becomes a sea", "The shirt rolls like waves", "The one who's swimming", "is yesterday's me"],
       "夜のコインランドリー。回る丸い窓を見ながら、ひとりで考えごと。", "At a coin laundry at night, she watches the round window spin and thinks."),
"23": ("22時", "10 p.m.", ["透明な傘 ひらいたら", "夜がわたしを 運んでく", "眠らなくても いいんだよ", "夢より遠く 行けるから"], ["When I open my see-through umbrella", "the night carries me away", "You don't have to sleep, it's all right", "we can go farther than dreams"],
       "眠れない夜、くらげのように、街の明かりの上をただよう。", "On a sleepless night, she drifts above the lights of the town like a jellyfish."),
"24": ("23時", "11 p.m.", ["あれでもない", "これでもない", "鏡の中で", "首をかしげる"], ["Not that one", "not this one", "In the mirror", "I tilt my head"],
       "明日着ていく服が決まらない。鏡の前で、何度も着がえる。", "She can't decide what to wear tomorrow, trying on outfit after outfit in front of the mirror."),
"25": ("24時", "Midnight again", ["ラララララ 聞こえるよ", "ラララララ 同じ節", "ラララララ 街じゅうで", "ラララララ 起きている"], ["La la la, I can hear it", "La la la, the same tune", "La la la, all over town", "La la la, we're awake"],
       "日付がまた変わる。今日の24人が、それぞれの場所で同じ鼻歌を歌う。", "The date changes again. The 24 people of today all hum the same little tune, each in their own place."),
}
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def ts(t):
    t = int(t); h, m, s = t // 3600, t // 60 % 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
PAD = float(os.environ.get("PAD", "0")); durs = [dur(mp3[r[0]]) for r in rows]
tot = sum(durs) + PAD * len(durs); acc = 0; tl = []
for r, d in zip(rows, durs): tl.append(f"{ts(acc)} {r[1]} - {r[2]}"); acc += d + PAD
h, m = int(tot // 3600), int(tot % 3600 // 60)
CRED = """■ クレジット / Credits
作詞・作曲・編曲・映像: Sunshine Pixel Sound
歌: 重音テト（UTAU） / Vocal: Kasane Teto (UTAU)
すべてオリジナル曲です。 / All songs are original compositions.
フォント: DotGothic16・Orbitron（SIL Open Font License）

#重音テト #KasaneTeto #ボカロ #VOCALOID"""
album = f"""HUMMING RELAY 全25曲・約{h}時間{m}分 | 歌：重音テト・歌詞つき（日本語・英語） | 25 Songs feat. Kasane Teto (JP/EN Lyrics)

重音テトの第3弾アルバム。ひとつの街の0時から24時まで、1時間ずつ進む全25曲。
1時の深夜ラジオで流れた短い鼻歌が、パン屋、満員電車、銭湯、屋上…と、人から人へ伝わっていき、最後の曲で全員がその節を歌います。
どの曲にも、その鼻歌がどこかに隠れています。探しながら聞いてみてください。日本語の歌詞と英訳つきです。
The third album by Kasane Teto: 25 original songs, one for each hour of a day in one town, from midnight to midnight.
A short tune hummed on late-night radio at 1 a.m. passes from person to person, and in the final song everyone sings it together.
The tune is hidden in every song. Try to find it! With Japanese lyrics and English translations.

■ 曲目 / Tracklist
""" + "\n".join(tl) + "\n\n" + CRED + f"""

■ タグ（YouTubeのタグ欄に貼る）
重音テト, テト, Kasane Teto, Teto, UTAU, UTAUオリジナル曲, 合成音声, 歌声合成, オリジナル曲, 歌詞付き, 英訳付き, 歌詞 英語, 全25曲, {h}時間{m}分, 第3弾, メドレー, 作業用BGM, 歌入り, HUMMING RELAY, ハミング・リレー, ボカロ, VOCALOID, original song, with lyrics
"""
open(f"{DST}/HUMMING RELAY 説明文（アルバム）.txt", "w", encoding="utf-8").write(album)
yt = ["HUMMING RELAY（ハミング・リレー）1曲ずつの YouTube 動画情報（題名・説明文・タグ）\n"]; ig = ["HUMMING RELAY（ハミング・リレー）Instagram キャプション（1曲ずつ）\nひとつの街の 0時から24時まで。1時の深夜ラジオで流れた短い鼻歌が、人から人へ伝わっていく全25曲。\n"]
for r in rows:
    no, jp, en = r[:3]; hj, he, cj, ce, sj, se = S[no]
    lyr = "■ 歌詞（サビ） / Lyrics (chorus)\n" + "\n".join(cj) + "\n\n" + "\n".join(ce)
    yt.append(f"""════════════════════════════════
■■ {no} {jp} ■■
【題名】
{jp} / {en} | 歌：重音テト・歌詞つき（日本語・英語） | HUMMING RELAY {no}

【説明文】
{jp} - {en}
アルバム「HUMMING RELAY（ハミング・リレー）」{int(no)}曲め（{hj}） / Track {int(no)} ({he}) from the album "HUMMING RELAY"

{hj}。{sj}
{he}. {se}
日本語の歌詞と英訳つきです。 / With Japanese lyrics and English translation.

{lyr}

{CRED}

【タグ】
重音テト, テト, Kasane Teto, Teto, UTAU, UTAUオリジナル曲, 合成音声, 歌声合成, オリジナル曲, 歌詞付き, 英訳付き, 歌詞 英語, {jp}, HUMMING RELAY, ハミング・リレー, ボカロ, VOCALOID, original song, with lyrics
""")
    ig.append(f"""━━━━━━━━━━━━━━━━
♪ {no} / 25　{jp} / {en}
アルバム: ハミング・リレー / HUMMING RELAY
歌: 重音テト / Vocal: Kasane Teto

{lyr}

■ 世界観 / Story
{hj}。{sj}
{he}. {se}

■ 制作 / Credits
作詞・作曲・編曲・映像: Sunshine Pixel Sound
すべてオリジナル曲です。 / All songs are original.

#重音テト #KasaneTeto #オリジナル曲 #VOCALOID #ボカロ #HUMMINGRELAY
""")
open(f"{DST}/HUMMING RELAY 動画情報（1曲ずつ・YouTube）.txt", "w", encoding="utf-8").write("\n".join(yt))
open(f"{DST}/HUMMING RELAY Instagramキャプション.txt", "w", encoding="utf-8").write("\n".join(ig))
# 1曲ずつのサムネに入れる、ひとことの紹介（時刻つき）
open(f"{DST}/.taglines.tsv", "w", encoding="utf-8").write("".join(f"{r[0]}\t{S[r[0]][0]}。{S[r[0]][4]}\n" for r in rows))
print(f"全体 {h}時間{m}分・{len(rows)}曲")
