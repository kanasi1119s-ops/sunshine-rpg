# ギターのカッティングの組み立て部品（2026-10-15、人間の指示「リードギターに気持ちの良いカッティングも入れよう」）。
# banned-sounds 1（短い単音の高い刻みで「ピ、ピ」と切れる）を避けるため:
#  - 必ず4音の和音（G3〜G4 の1オクターブに詰めたクローズ・ボイシング）を、弦ごとに少しずつずらして鳴らす（ストローク）。
#  - 型の文字（1文字＝16分）: D＝ダウン（4弦・拍頭はアクセント）、U＝アップ（高い2弦だけ・少し弱く）、
#    x＝ミュートの「チャッ」（デッドノート）、g＝とても弱いミュート、.＝前の音をのばす、-＝休み。
#  - ダウンは「.」で 0.5拍くらいのばし、切れすぎないようにする。
#  - 音程の揺らぎ・しゃくりなし（humanPitch 0。曲の autoScoop は false にしておく）。
import re

def voicing4(pcs, lo=55, hi=74):
    """和音の音（根音・3度・5度・7度。長7度は半音でぶつかるので外す）を G3〜F#4 の1オクターブに詰めて並べる（クローズ・ボイシング）。
    3音しかないときは、いちばん下の音の1オクターブ上を足して4音にする。"""
    root = pcs[0]
    tones = [pcs[0], pcs[1], pcs[2] if len(pcs) > 2 else pcs[0]]
    if len(pcs) > 3 and (pcs[3] - root) % 12 != 11: tones.append(pcs[3])
    out = sorted({lo + ((p - lo) % 12) for p in tones})
    if len(out) < 4: out.append(out[0] + 12)
    return sorted(out)[:4]

def cut_parts(SEC, chord_pcs, nm, patterns, lo=55):
    """patterns(s, n, b) → 16文字の型 か None（その小節は休み）。返り値: 4本（低い弦→高い弦）の、セクションごとの音のリスト。"""
    voices = [[] for _ in range(4)]
    for s, pr, k, n in SEC:
        sec = [[] for _ in range(4)]
        for b, ch in enumerate(pr):
            pat = patterns(s, n, b)
            v = voicing4(chord_pcs(ch), lo)
            if not pat:
                for i in range(4): sec[i].append("R:4")
                continue
            # 文字を「打つ音とのばし」にまとめる
            toks = []
            for j, c in enumerate(pat):
                if c == "." and toks and toks[-1][0] in "DU": toks[-1][1] += 1
                elif c == ".": toks.append(["-", 1, j])
                else: toks.append([c, 1, j])
            for i in range(4):
                for c, steps, j in toks:
                    d = f"{steps * 0.25:g}"
                    if c == "D": sec[i].append(f"{nm(v[i])}:{d}" + ("!" if j % 4 == 0 else ""))
                    elif c == "U": sec[i].append(f"{nm(v[i])}:{d}," if i >= 2 else f"R:{d}")
                    # ミュート（デッドノート）は中ほどの弦だけ（作曲ソフトはミュートを低い音で鳴らすので、低い弦で鳴らすとベースと濁る）
                    elif c == "x": sec[i].append(f"x:{d}" if i in (1, 2) else f"R:{d}")
                    elif c == "g": sec[i].append(f"x:{d}," if i == 2 else f"R:{d}")
                    else: sec[i].append(f"R:{d}")
            # 小節の頭が x/g のとき、デッドノートの高さの元になる「直前の音」がないので、最初の小節の頭は休みにしておく
        voices_sec = [" ".join(x) for x in sec]
        for i in range(4): voices[i].append(voices_sec[i])
    # 曲の最初が x で始まらないようにする（直前の音がない）
    for i in range(4):
        first = voices[i][0].split()
        for t, tok in enumerate(first):
            if tok.startswith("x:"): first[t] = "R:" + tok.split(":")[1].rstrip(",!")
            elif not tok.startswith("R:"): break
        voices[i][0] = " ".join(first)
    return voices
