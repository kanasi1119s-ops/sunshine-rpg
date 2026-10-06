"""2頭身のユーリ（左向き＝戦闘の向き）が「コスモリングライト」をまとった絵（2026-10-06、人間の依頼）。
白と金の鎧・顔をおおう兜（光る目のすじ・2枚の金のひれ）・胸の環の核・背の光の環・機械の羽（金の関節の骨組みと、
光る先の羽板）・まわりに浮かぶ6基の追尾砲台（砲口は敵のいる左）。
既存作のロボットのデザイン（V字の角・青い刃の翼・赤青白の配色・顔の通気口など）はまねしない（CLAUDE.md 1-1）。
光は左上。50×50（人間の指示「50x50でもいいよ」）。

書き出す絵:
  yuri2-cosmo.txt          見本（砲台つき・待機の姿）
  yuri2-cosmo-idle.txt     ゲーム用の待機の姿（砲台はゲームが動かして描く）
  yuri2-cosmo-attack.txt   ゲーム用の攻撃態勢（前の手を敵へつき出し、羽を大きく広げ、環が強く光る）
  cosmo-pod.txt            追尾砲台1基（ゲームが飛び回らせる）
パレットは全部共通（pal-cosmo.json）。"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
PAL = {
    "A": "#1a1018",                                                      # ふち
    "1": "#f6f8fc", "2": "#d2d9e6", "3": "#9ca6bc", "4": "#5a6480",     # 鎧（明→暗）
    "5": "#ffe27a", "6": "#d8a030", "7": "#8a5a14",                     # 金
    "8": "#7ae4ff", "9": "#2aa8e0", "0": "#16588c", "v": "#ffffff",     # 光
    "r": "#3a7cc0", "k": "#2c3148",                                      # 環の奥の暗い側・機械の骨の暗い色
}
W = H = 50
OX, OY = 17, 12        # 体（16×32）の左上。足の下に、浮いている分のすきま

class Grid:
    def __init__(self):
        self.g = [["."] * W for _ in range(H)]
    def put(self, x, y, c, over=True):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < W and 0 <= y < H and (over or self.g[y][x] == "."):
            self.g[y][x] = c
    def outline(self, chars):
        pts = [(x, y) for y in range(H) for x in range(W) if self.g[y][x] in chars]
        for x, y in pts:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= x+dx < W and 0 <= y+dy < H and self.g[y+dy][x+dx] == ".":
                    self.g[y+dy][x+dx] = "A"
    def stamp(self, rows, x0, y0, skip="_"):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == skip or ch == ".": continue
                self.put(x0+i, y0+j, ch)
    def text(self):
        return "\n".join("".join(r) for r in self.g) + "\n"

def ring(G, bright):
    cx, cy, R = OX + 9.5, OY + 15.5, 11.5
    for y in range(H):
        for x in range(W):
            d = math.hypot(x+.5-cx, y+.5-cy)
            if abs(d-R) < 0.62:
                c = math.cos(math.atan2(y+.5-cy, x+.5-cx) + 2.35)
                G.put(x, y, ("v" if c > 0.35 else "8") if bright else ("8" if c > 0.35 else ("9" if c > -0.5 else "r")))
    for q in range(6):
        a = q*math.pi/3 + math.pi/6
        G.put(cx+R*math.cos(a)-.5, cy+R*math.sin(a)-.5, "5")

def line(G, x0, y0, x1, y1, c, w=1):
    n = int(max(abs(x1-x0), abs(y1-y0))*2) + 1
    for i in range(n+1):
        t = i/n; x, y = x0+(x1-x0)*t, y0+(y1-y0)*t
        for dx in range(w):
            for dy in range(w):
                G.put(x+dx, y+dy, c)

def mech_wing(G, root, elbow, tip, vanes, far):
    """機械の羽: 金の関節でつながった2本の骨と、骨から下へ垂れる羽板（先が光る）。far=奥の羽（暗く小さく）"""
    body, edge, shade = ("3", "2", "4") if far else ("2", "1", "3")
    bone = "k" if far else "4"
    # 羽板（骨より先に描く＝骨の奥）
    for (t, ang, ln) in vanes:
        seg = (root, elbow) if t < 1 else (elbow, tip)
        tt = t if t < 1 else t-1
        bx, by = seg[0][0]+(seg[1][0]-seg[0][0])*tt, seg[0][1]+(seg[1][1]-seg[0][1])*tt
        a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); px, py = -uy, ux
        for s in range(ln):
            w = 1.4 if s < ln-3 else 1.4*(ln-s)/3
            x, y = bx+ux*s, by+uy*s
            for o in (-1, 0, 1):
                if abs(o) <= w: G.put(x+px*o*0.9, y+py*o*0.9, body)
            G.put(x-px*0.9, y-py*0.9, edge)
            G.put(x+px*0.9, y+py*0.9, shade) if s > 1 and s < ln-2 else None
        G.put(bx+ux*(ln-1), by+uy*(ln-1), "8" if not far else "9")
        G.put(bx+ux*(ln-2), by+uy*(ln-2), "v" if not far else "8")
    # 骨（2本）と、金の関節
    line(G, root[0], root[1], elbow[0], elbow[1], bone, 2)
    line(G, elbow[0], elbow[1], tip[0], tip[1], bone, 2 if not far else 1)
    line(G, root[0], root[1]-1, elbow[0], elbow[1]-1, "3" if not far else "4", 1)
    for (x, y) in (root, elbow, tip):
        G.put(x, y, "6"); G.put(x+1, y, "5" if not far else "6"); G.put(x, y+1, "7"); G.put(x+1, y+1, "6")

def wings(G, spread):
    """背（右）から2枚。上の奥の羽は暗く、下の手前の羽は明るい。攻撃態勢では、羽が上へ開く"""
    s = spread
    mech_wing(G, (OX + 11, OY + 19), (OX + 16 + s, OY + 8 - 2*s), (OX + 21 + 2*s, OY + 2 - 3*s),
              [(0.5, 60, 6), (1.0, 50, 7), (1.5, 38, 6), (1.95, 25, 5)], far=True)
    G.outline(set("234k59"))
    mech_wing(G, (OX + 12, OY + 21), (OX + 20 + s, OY + 14 - 2*s), (OX + 26 + 2*s, OY + 9 - 3*s),
              [(0.45, 70 - 6*s, 7), (0.95, 55 - 6*s, 8), (1.4, 40 - 6*s, 8), (1.95, 22 - 6*s, 6)], far=False)
    G.outline(set("1234k5678v"))

HELM = [
    "_____________AA___",   # -3 ひれの先
    "____________A5A___",   # -2
    "___________A56A___",   # -1
    "__________A567A_A_",   #  0
    "_________A567AA5A_",   #  1 2枚目のひれ
    "________A5567A56A_",   #  2
    ".....AAAA556AA67A_",   #  3 ひれの根もと・鉢のてっぺん
    "....A11112567A7A__",   #  4
    "...A1111222567AA__",   #  5
    "..A11112222233A___",   #  6
    "..A11122222333A___",   #  7
    ".A111222223334AA__",   #  8
    "A8v1222223334434A_",   #  9 額の宝石
    "AA555555555666434A",   # 10 金の帯・しころ1枚目
    "_A4AAAAAAA12334A4A",   # 11 ひさしの下のかげ・しころ2枚目
    "__A11122222333A434A",  # 12 面（顔をおおう板）
    "_A8v899999833A3A44A",  # 13 目の高さの、光る横のすじ（前へとがる）
    "__A1122222333A4A44A",  # 14
    "__A11A2223334AA_AA_",  # 15 小さな息の穴
    "___A156A23344A_____",  # 16 あご（金の筋）
    "____AA56A234A______",  # 17 とがったあご当て
]
# 体（2026-10-06 人間の指示「ロックマンエックスみたいなアーマーがいいな」）: 遊びの雰囲気（丸く大きな肩当て・
# 前の腕の腕砲・大きなブーツの、ずんぐりした機械の鎧）だけを参考にし、配色（青）・兜の形・印などはまねしない（CLAUDE.md 1-1）。
BODY_IDLE = [  # 18行目〜（x は体の左はしから）。前の腕の腕砲は下を向き、砲口が光る
    "....AA5666AA....",
    "..AAA11222A3AA..",
    ".A1111A2v82A333A",
    ".A1122A2898A334A",
    ".A2233A22223A44A",
    "..A33AA5667AAAA.",
    "..A112AA1223A...",
    ".A11223A1223A...",
    ".A22339A1A23A...",
    ".A88vv8A12A23A..",
    "..AAAAAA12A12A..",
    "...A11122A1122A.",
    "...A55666A5566A.",
    "...AAAAAAAAAAAA.",
]
BODY_ATTACK_X = -4   # 攻撃態勢は、腕砲を前（左）へつき出すので、体の左はしより4ドット前から描く
BODY_ATTACK = [  # 腕砲を敵（左）へまっすぐ向け、足を前後に大きくひらいてふんばる
    "........AA5666AA....",
    "......AAA11222A3AA..",
    "AAAAAA111A2v82A333A.",
    "v8811122A12898A334A.",
    "88vA2233A22223A44A..",
    "AAAAAAAA5667AAAA....",
    "......A11223A.......",
    ".....A11A1223A......",
    "....A12A..A123A.....",
    "...A12A....A12A.....",
    "..A112A.....A112A...",
    "..A5566A....A5566A..",
    "..AAAAAA....AAAAAA..",
]
POD = [
    "..AAAA...",
    "AA1112A..",
    "vA42223A9",
    "AA3334A..",
    "..AAAA...",
]
POD_SPOTS = [(1, 6), (0, 22), (3, 39), (38, 2), (41, 20), (39, 41)]

def compose(pose, pods):
    G = Grid()
    attack = pose == "attack"
    ring(G, bright=attack)
    wings(G, spread=1 if attack else 0)
    if pods:
        for (px, py) in POD_SPOTS:
            G.stamp(POD, px, py)
            G.put(px-1, py+2, "8"); G.put(px+4, py+1, "6"); G.put(px+4, py+3, "7")
    if attack:
        G.stamp(BODY_ATTACK, OX + BODY_ATTACK_X, OY+18)
    else:
        G.stamp(BODY_IDLE, OX, OY+18)
    G.stamp(HELM, OX, OY-3)
    return G

if __name__ == "__main__":
    outs = {
        "yuri2-cosmo": compose("idle", True),
        "yuri2-cosmo-idle": compose("idle", False),
        "yuri2-cosmo-attack": compose("attack", False),
    }
    used = set()
    for name, G in outs.items():
        open(os.path.join(HERE, f"{name}.txt"), "w").write(G.text())
        used |= set(G.text()) - {".", "\n"}
    pod = "\n".join(POD) + "\n"
    open(os.path.join(HERE, "cosmo-pod.txt"), "w").write(pod.replace("_", "."))
    used |= set(pod) - {".", "\n", "_"}
    json.dump({k: PAL[k] for k in PAL if k in used}, open(os.path.join(HERE, "pal-cosmo.json"), "w"))
    print(len(used), "colors")
