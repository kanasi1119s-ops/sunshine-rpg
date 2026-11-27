"""金髪ショートの歌い手 32×64（第1版・正面の1コマ）の絵の設計。エディタに打ちこむのは editor_drive.py。
2026-11-27 人間「これドットを横32縦64で作ってみて」。26×40 の第2版（art_blonde_v2.py）と同じ色。絵は横20マス（x6〜25）・縦62マス、まわりに1マスのふち。"""
from art_blonde_v2 import PAL
W, H = 32, 64; OX, OY = 6, 1
ROWS = [
 "......34444433......", "....345556554432....", "...34556655554432...", "..3455665545554432..", ".345565545545554432.",
 ".3TTTTTTTTTTTTTTTS2.", "3RSSSSSSSSSSSSSSRR32",
 "34554" "3544553445" "44532", "34543" "5434554354" "34532", "34534" "c43c44c34c" "43542", "23543" "bcbbccbbcb" "34532",
 "23453" "bXXXbbXXXb" "35432", "13453" "bvfebbefvb" "35431", "12453" "bwfebbefwb" "35421", "12343" "bwafbbfawb" "34321",
 "12342" "pbbbccbbbp" "24321", "23432" "bbbcddcbbb" "23432", "34321" "cbbbbbbbbc" "12343", "3432." ".cbbbbbbc." ".2343",
 "4532." "..dccccd.." ".2354", "342.." "....cc...." "..243", ".2..." "....cc...." "...2.",
 "......RSTccTSR......", "....wwRSSTTSSRww....", "..wwvwwRSTTSRwwvww..", "..wvwwwvRTSRvwwwvw..", "..wvuwwSRwwRSwwuvw..",
 "..bc.wwRwwwwRww.cb..", "..bc.wwwwwwwwwv.cb..", "..ac.wwwwvwwwwv.ca..", "..bc.wwwwvwwwwu.cb..", "..bc.vwwwwwwwvu.cb..", "..bc.vwwwvwwwvu.cb..", "..ab.uvwwvwwvuu.ba..",
 "..bc.OQQOyyOQOo.cb..", "..cdNMMLMNNMMMNndc..", "....NMLMMNnMMLMNn...", "...NMMLMMNnMMMLMNn..", "...NMLMMNnnNMMLMNn..", "...NMMLMNn.nNMLMNn..", "...NMLMMNn.nNMMLNn..", "...vLvLvLn.nLvLvLv..",
 "....bbbbc...cbbbb...", "....abbbc...cbbba...", "....abbbc...cbbba...", "....bbbc.....cbbb...", "....bbbc.....cbbb...", "....abcc.....ccba...", "....bbbc.....cbbb...",
 ".....bbc.....cbb....", ".....abc.....cba....", ".....bbc.....cbb....", ".....bbc.....cbb....", ".....bbc.....cbb....",
 ".....wwv.....vww....", "....wwvu.....uvww...", "....OQQo.....oQQO...", "....OQyO.....OyQO...", "....OQQo.....oQQO...", "...OQyQo.....oQyQO..", "..QQQOOo.....oOOQQQ.", "..oooooo.....oooooo.",
]
assert len(ROWS) == 62 and all(len(r) == 20 for r in ROWS), (len(ROWS), [(i, len(r)) for i, r in enumerate(ROWS) if len(r) != 20])
g = [["."] * W for _ in range(H)]
for y, r in enumerate(ROWS):
    for x, ch in enumerate(r):
        if ch != ".": g[y + OY][x + OX] = ch
add = []
for y in range(H):
    for x in range(W):
        if g[y][x] == ".":
            nb = [g[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + a < W and 0 <= y + b < H and g[y + b][x + a] != "."]
            if nb: add.append((x, y, "1" if any(c in "123456" for c in nb) and y < OY + 22 else "X"))
for x, y, c in add: g[y][x] = c
FRAME_GRIDS = [("正面", 400, g)]
COLS = 1
