"""金髪ショートの歌い手 32×64（第2版・正面の1コマ）の絵の設計。エディタに打ちこむのは editor_drive.py。
2026-11-27 人間「もっと可愛く。画像の子に近づけて」。第1版から変えた所: 頭を大きく（62マス中22マス）、目を横4×縦4に（上が濃く下が明るいひとみ・光・白目）、口を開けた笑顔、ほほの赤み、
  前髪を分けておでこを見せる、毛先は下でふくらませず、あごの横で内へすぼめる（人間「髪の毛下のほうもっこりさせないで」）、耳かざり、スカーフにチェックの線、胸の前で手を組むポーズ、腰と足を細く。絵は横24マス（x4〜27）。"""
from art_blonde_v2 import PAL
W, H = 32, 64; OX, OY = 4, 2
ROWS = [
 "........34444443........", "......3455566554432.....", "....34556665555544322...", "...3455665545555544322..", "..345566554555455544322.",
 "..3TTTTTTTTTTTTTTTTTSS2.", ".3RSSSSSSSSSSSSSSSSSRR32", ".34554534554455434554332", "3455435bb4534bb345345432", "34543bbbbb43bbbbb3454432",
 "345432" "cbbbbbbbbbbc" "234543", "245432" "bXXXXbbXXXXb" "234542", "135431" "beaeebbeaeeb" "134531", "124531" "beffebbeffeb" "135421", "123432" "bwffwbbwffwb" "234321",
 ".23421" "ppbbbccbbbpp" "12432.", ".2342y" "bbbbmwwmbbbb" "y2432.", "..2321" "cbbbbttbbbbc" "1232..", "..232." ".cbbbbbbbbc." ".232..", "...2.." "..cbbbbbbc.." "..2...",
 "......" "...dccccd..." "......", "......" "....cccc...." "......",
 ".......RSTccccTSR.......", ".....wwRSrSTTSrSRww.....", "....wwvwRrSTTSrRwvww....", "...wwvwwwRSrrSRwwwvww...", "...wvwwwvSRwwRSvwwwvw...", "...bcvwwSrRwwRrSwwvcb...",
 "...bc.wwwwcbbcwwww.cb...", "...bc.wwwcabbacwww.cb...", "...bbcwbbbccccbbbwcbb...", "....bbbbcwwwvwwcbbbb....", ".......wwvwwwwvwu.......", ".......vwwwvwwwwu.......",
 ".......OQQOyyOQOo.......", "......NMMLMNNMMMNn......", ".....NMLMMNnnMMLMNn.....", ".....NMMLMNnnNMLMMn.....", ".....NMLMMNn.nMMLMNn....", ".....NMMLMNn.nNMLMMn....", ".....vLvLvLn.nLvLvLv....",
 "......bbbc....cbbb......", "......abbc....cbba......", "......abbc....cbba......", "......bbbc....cbbb......", ".......bbc....cbb.......", ".......abc....cba.......", ".......bcc....ccb.......",
 ".......bbc....cbb.......", ".......abc....cba.......", ".......bbc....cbb.......", ".......bbc....cbb.......", ".......bc......cb.......",
 "......wwwv....vwww......", "......wwvu....uvww......", "......OQQo....oQQO......", "......OyQO....OQyO......", "......OQQo....oQQO......", ".....OQyQo....oQyQO.....", "....QQQOOo....oOOQQQ....", "....oooooo....oooooo....",
]
assert len(ROWS) == 61 and all(len(r) == 24 for r in ROWS), (len(ROWS), [(i, len(r)) for i, r in enumerate(ROWS) if len(r) != 24])
g = [["."] * W for _ in range(H)]
for y, r in enumerate(ROWS):
    for x, ch in enumerate(r):
        if ch != ".": g[y + OY][x + OX] = ch
add = []
for y in range(H):
    for x in range(W):
        if g[y][x] == ".":
            nb = [g[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + a < W and 0 <= y + b < H and g[y + b][x + a] != "."]
            if nb: add.append((x, y, "1" if any(c in "123456" for c in nb) and y < OY + 21 else "X"))
for x, y, c in add: g[y][x] = c
FRAME_GRIDS = [("正面", 400, g)]
COLS = 1
