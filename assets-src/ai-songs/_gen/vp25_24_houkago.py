# vp25 24「放課後の五人」Five After School（仮）— K-POP。A♭長調（全員で B♭長調）・118・4/4。主役の楽器: ピチカート（弦をはじく）
# 物語: 放課後のチャイム。教室に一人ずつ友だちが集まってくる。元気な子、のんびりした子、クールな子、おっちょこちょいな子、リーダー。
#   五人がそろって息を合わせ、全員で一つの歌に。夕方、一人ずつ帰っていく。
# 形: 5人が一人ずつ登場。人ごとにビートとジャンルが変わり（ダンスポップ・ボサノバ・トラップ・ファンク・ロック）、最後に全員
# 場面と強さ: 一人ずつ性格で違う強さ（元気＝大・のんびり＝小・クール＝中で低い・おっちょこちょい＝急に止まる・リーダー＝大）／
#   全員の前に息を合わせる1小節の無音／全員＝最大／帰り道＝一人ずつ抜けていく
# 旋律の性格: 5人それぞれの動機。最後にそれが一つのフックに組み合わさる（ピチカートがそれぞれの動機を弾く）
# 崩す所: 1曲で5つのジャンルを渡る
from vp25_lib import *

S = Song("24", "houkago", "放課後の五人（仮）", "Five After School", 118, 4, "Ab", "major", "K-POP")
S.kit = "jpop"   # 2026-10-25: 切り抜きで naked 6.83 → jpop 7.07
K = S.key
CH = {"元気": ["Ab", "Bbm7", "Cm7", "Db"], "のんびり": ["Dbmaj7", "Cm7", "Bbm7", "Eb7sus4"], "クール": ["Fm", "Fm", "Db", "Eb"],
      "おっちょこちょい": ["Ab7", "Db9", "Ab7", "Eb7"], "リーダー": ["Db", "Eb", "Fm", "Ab/C", "Db", "Eb", "Ab", "Ab"]}
S.scene("チャイム", 2, "intro", ["Ab", "Ab"])
for n in CH: S.scene(n, 16, {"元気": "verse", "のんびり": "verse", "クール": "pre", "おっちょこちょい": "bridge", "リーダー": "chorus"}[n], CH[n])
S.scene("息を合わせる", 1, "break", ["F7sus4"])
ALL = ["Bb", "F/A", "Ebmaj7", "F", "Gm7", "Dm7", "Ebmaj7", "F7sus4"]
S.scene("全員", 32, "chorus", ALL)
S.scene("帰り道", 16, "outro", ["Ebmaj7", "Dm7", "Cm7", "F7sus4", "Ebmaj7", "Dm7", "Cm7", "Bb"] * 2)
S.extra.update({"tone": "rock", "diGuitar": "emily"})
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags   # 2026-10-25: 参考の音で 7.07 → 7.62（09 の切り抜き）
KB = K.up(2)
T3, T3b = "0.3333", "0.3334"

PZ = S.track("主役: ピチカート", "strings", patch="pizzicato", volume=0.27, pan=-0.08, reverb=0.28, gainDb=6,
             fx=[{"type": "eq", "low": -3, "mid": 2.5, "midHz": 2200, "high": 1}])
PZ2 = S.track("ピチカート（2本目）", "strings", patch="pizzicato", volume=0.18, pan=0.4, reverb=0.3, gainDb=3)
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("squareLead", vol=0.17, pan=0.05, delay=0.5))
BASS = S.track("ベース", "bass", **rock_bass_spec(0.2))
EP = [S.track(f"エレピ{i + 1}", "keys", volume=0.09, pan=[-0.35, 0.35, 0][i], reverb=0.2) for i in range(3)]
NY = S.track("ナイロン弦（のんびり）", "guitar", patch="nylonGuitar", volume=0.13, pan=0.4, amp="clean", chorus=0, reverb=0.2, humanPitch=0, sustain=1.4)
GT = [S.track(f"ギター（リーダー{i}）", "distGuitar", **rock_gtr_spec(0.09, 0.0)) for i in range(2)]
SUB = S.track("808（クール）", "sub808", **sub_spec(0.2))
BELL = S.track("チャイム", "bell", volume=0.14, pan=0, reverb=0.45, sustain=2.0)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- 5人の動機（ピチカート） ----------
MOT = {"元気": "1':0.5 5:0.5 1':0.5 3':0.5 5':1 R:1",                 # 元気: 跳ねる
       "のんびり": f"3':{T3} 2':{T3} 1':{T3b} 6:1.5 R:1.5",               # のんびり: ゆるい3連
       "クール": "R:0.5 5:0.25 5:0.25 R:1 b7:0.5 R:1.5",                  # クール: 2音だけ
       "おっちょこちょい": "3':0.25 #2':0.25 2':0.25 #1':0.25 1':1 R:0.5 7:0.25 R:1.25",   # おっちょこちょい: 半音ですべる
       "リーダー": "1:1 4:1 7:1 3':1"}                                       # リーダー: 4度で上る
BAR_M = {n: K.mel(m, oct=4) for n, m in MOT.items()}
for n in CH:
    for i, b in enumerate(S.sc(n)):
        if i % 2 == 0: PZ.bar(b, K.mel(MOT[n] if i % 4 == 0 else seq_up(MOT[n], K, 2 if n != "クール" else -1), oct=4))
        elif n in ("元気", "おっちょこちょい"): PZ2.bar(b, K.mel(MOT[n], oct=4))   # 2026-10-25: 元気の2本目を1オクターブ下げた（10秒ごとの点 5.4）
# 歌の役: 人ごとの短い歌（後半の8小節）
SONGS = {"元気": ["5:0.5 5:0.5 6:0.5 1':0.5 2':1 1':1", "6:1 5:1 3:2", "4:0.5 4:0.5 5:0.5 6:0.5 1':1 6:1", "5:4"],
         "のんびり": ["3':2 2':1 1':1", "6:4", "2':2 1':1 6:1", "5:4"],
         "クール": ["R:1 5:0.5 b3:0.5 1:2", "R:4", "R:1 b7,:0.5 1:0.5 b3:2", "R:4"],
         "おっちょこちょい": ["1':0.5 7:0.5 b7:0.5 6:0.5 5:1 R:1", "R:0.5 3:0.5 4:0.5 #4:0.5 5:2", "1':0.5 7:0.5 b7:0.5 6:0.5 b6:1 R:1", "5:1 R:3"],
         "リーダー": ["1':1 2':1 3':2", "4':2 3':1 2':1", "3':1 4':1 5':2", "5':4"]}
for n in CH:
    for i, b in enumerate(S.sc(n)):
        if i >= 8: LEAD.bar(b, K.mel(SONGS[n][i % 4], oct=4))
# 全員: 5つの動機を組み合わせた一つのフック（B♭長調）
HOOK = ["1':0.5 5:0.5 1':0.5 3':0.5 5':1 4':0.5 3':0.5", f"3':{T3} 2':{T3} 1':{T3b} 6:1 R:0.5 5:0.25 5:0.25 b7:0.5 R:0.5",
        "3':0.25 #2':0.25 2':0.25 #1':0.25 1':1 4':1 7':1", "1'':4"]
for i, b in enumerate(S.sc("全員")):
    LEAD.bar(b, KB.mel(HOOK[i % 4] if i % 8 < 4 else ["5':2 4':1 3':1", "2':2 6:2", "1':1 2':1 3':1 4':1", "5':4"][i % 4], oct=4))
    PZ.bar(b, KB.mel(HOOK[i % 4], oct=4) if i >= 8 else KB.mel(MOT[["元気", "のんびり", "おっちょこちょい", "リーダー"][i % 4]], oct=4))
    if i >= 16: PZ2.bar(b, KB.mel(MOT[["リーダー", "元気", "クール", "のんびり"][i % 4]], oct=4))
# 帰り道: 一人ずつ抜けていく（動機が1つずつ減る）
LEAVE = ["元気", "のんびり", "クール", "おっちょこちょい", "リーダー"]
for i, b in enumerate(S.sc("帰り道")):
    left = LEAVE[min(4, i // 3):]
    who = left[i % len(left)] if i < 15 else "リーダー"
    PZ.bar(b, KB.mel(MOT[who], oct=4) if i < 15 else KB.mel("1':4", oct=4))
# チャイム（無音と一撃）
BELL.bar(S.sc("チャイム")[0], "R:2 C6:1 Ab5:1")
BELL.bar(S.sc("チャイム")[1], "Bb5:1 Eb5:3")

# ---------- 伴奏（人ごとのジャンル） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1"); v = voice(ch, 64, 3)
    if n == "元気":
        BASS.bar(b, bass_line(S, b, "oct8"))
        for j in range(3): EP[j].bar(b, "X:1.5 X:2.5".replace("X", nm(v[j], True)))   # 2026-10-25: 裏打ちの短い和音 → のばす和音
    elif n == "のんびり":
        BASS.bar(b, f"{nm(r, True)}:1.5 {nm(r + 7, True)}:0.5 {nm(r + 7, True)}:1.5 {nm(r, True)}:0.5")
        NY.bar(b, f"{nm(v[0], True)}:0.5 R:0.5 {nm(v[1], True)}:0.75 {nm(v[2], True)}:0.75 R:0.5 {nm(v[1], True)}:1")
    elif n == "クール":
        SUB.bar(b, f"{nm(r, True)}:2.5 {nm(r, True)}:1 R:0.5")
        for j in range(3): EP[j].bar(b, f"{nm(v[j], True)}:4" if i % 2 == 0 else "R:4")
    elif n == "おっちょこちょい":
        # ファンク。ときどき急に止まる（4小節ごとの最後の2拍）
        stop_ = i % 4 == 3
        BASS.bar(b, (f"{nm(r, True)}:0.5 R:0.25 {nm(r + 12, True)}:0.25 R:0.5 {nm(r + 10, True)}:0.5 R:2") if stop_ else
                 f"{nm(r, True)}:0.5 R:0.25 {nm(r + 12, True)}:0.25 R:0.5 {nm(r + 10, True)}:0.5 {nm(r + 7, True)}:0.5 R:0.25 {nm(r, True)}:0.25 {nm(r + 3, True)}:0.5 {nm(r + 4, True)}:0.5")
        for j in range(3): EP[j].bar(b, ("R:0.25 X:0.25 R:0.5 X:0.25 R:0.75 R:2" if stop_ else "R:0.25 X:0.25 R:0.5 X:0.25 R:0.75 R:0.25 X:0.25 R:0.5 X:0.25 R:0.75").replace("X", nm(v[j], True)))
    elif n == "リーダー":
        BASS.bar(b, bass_line(S, b, "root8"))
        pw = power(ch, "E2")   # 2026-10-25: 8分の刻み → 付点のリズムでのばす和音（10秒ごとの点 7.0）
        for j in range(2): GT[j].bar(b, f"{nm(pw[j], True)}:1.5! {nm(pw[j], True)}:1.5 {nm(pw[j], True)}:1")
    elif n == "全員":
        BASS.bar(b, bass_line(S, b, "oct8" if i < 16 else "root8"))
        for j in range(3): EP[j].bar(b, "X:1.5 X:1 X:1.5".replace("X", nm(v[j], True)))
        if i >= 16:   # 2026-10-25: 8分の刻み → のばす和音（全員で鳴る場面の点 6.6〜6.9）
            pw = power(ch, "E2")
            for j in range(2): GT[j].bar(b, f"{nm(pw[j], True)}:2.5! {nm(pw[j], True)}:1.5")
    elif n == "帰り道":
        if i < 12: BASS.bar(b, f"{nm(r, True)}:2 {nm(r + 7, True)}:2")
        if i < 14:
            for j in range(3): EP[j].bar(b, f"{nm(v[j], True)}:4")
cym_swell(CYM, S.sc("全員")[0], 4, "E4")

# ---------- ドラム（人ごとのジャンル） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "元気":
        put_groove(D, b, "four", ghosts=0.2, seed=b, hat_vary=False); D.H[b] = "x.x.x.x.x.x.x.O." if i % 2 == 1 else "x.x.x.x.x.x.x.x."
        if i == 0: crash(D, b)
    elif n == "のんびり":
        D.set(b, "X..X....X..X....", "...x..x....x..x." if i >= 4 else "." * 16, "x.xxx.xxx.xxx.xx")         # ボサノバ（スネアはリムの代わりに弱く）
    elif n == "クール":
        put_groove(D, b, ("X.....X...X.....", "........X.......", "x.x.x.x.xxxxx.x."), seed=b, hat_vary=False)
    elif n == "おっちょこちょい":
        put_groove(D, b, ("X.....X...X.....", "....X......oX..o", "xoxoxoxoxoxoxoxo"), ghosts=0.6, seed=b, hat_vary=False)
        if i % 4 == 3: D.set(b, "X.....X.........", "....X...........", "xoxoxoxo........")
    elif n == "リーダー":
        put_groove(D, b, "vocarock", ghosts=0.3, seed=b, hat_vary=False)
        if i % 8 == 0: crash(D, b, "C2")
        if last: put_fill(D, b, "tomdown")
    elif n == "全員":
        put_groove(D, b, ["four", "vocarock", ("X.....X...X.....", "........X.......", "x.x.x.x.xxxxx.x."), "four"][(i // 8) % 4], ghosts=0.3, seed=b, hat_vary=False)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "snare16")
    elif n == "帰り道":
        if i < 8: D.set(b, "X.......X.......", "....x.......x...", "x...x...x...x...")
    if n in ("元気", "のんびり", "クール", "おっちょこちょい") and last: put_fill(D, b, "small")

S.desc = ("仮: ボカロ曲のインスト25曲の24。K-POP。A♭長調（全員で B♭長調）・118。主役の楽器はピチカート。放課後の教室に、五人が一人ずつやってくる。"
          "元気（ダンスポップ・跳ねる動機）、のんびり（ボサノバ・ゆるい3連）、クール（トラップ・2音だけ）、おっちょこちょい（ファンク・半音ですべって急に止まる）、"
          "リーダー（ロック・4度で上る）。息を合わせる1小節の無音のあと、5つの動機を組み合わせたフックを全員で。帰り道、動機が一つずつ減っていく。自作")
S.write()
