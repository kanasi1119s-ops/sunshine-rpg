# ドラムの組み立て部品（2026-10-15、人間の指示「ドラムに強弱、アクセント、フィルをしっかり入れよう」）。
# 『あの夏のとなり』『ミッドナイト・ベルベット』で使う。グリッド 1文字＝16分。X＝アクセント、x＝ふつう、o＝ゴースト（弱い）、O＝オープンハイハット。
# 決まりごと:
#  - 拍の頭をアクセント、裏は弱く、16分の間にゴースト（ハイハット・スネア）。
#  - 4小節ごとに短いフィル（最後の1拍。スネアの o→x→X）、8小節ごとにタムのフィル（最後の2拍）、
#    セクションの終わりは次のセクションへ向けて盛り上がるフィル（最後の2拍。タムとスネアを強くしていく）。
#  - 静かなセクションへ入る前は「止め」（1拍目だけ叩いて休む）。
#  - クラッシュはセクションの頭と、サビの8小節ごと。クラッシュと同時のハイハットは消す（手は2本）。
#  - 強弱の流れ（barGain）はドラムだけ大きめに: Aメロ 0.8→、Bメロでだんだん強く、サビ頭 1.05、落ちサビ・ブリッジは弱く。
Z = "................"

def tomtok(tm, pit=("E3", "E3", "C3", "C3", "A2", "A2")):
    hits = [j for j, c in enumerate(tm) if c in "xXo"]; toks = []; k = 0
    for c in tm:
        if c in "xXo":
            toks.append(pit[min(len(pit) - 1, k * len(pit) // max(1, len(hits)))] + ":0.25" + ("!" if c == "X" else ("," if c == "o" else ""))); k += 1
        else: toks.append("R:0.25")
    return toks

def cut_hat(hh, frm):
    return hh[:frm] + "." * (16 - frm)

# フィルの型（スネア, タム, どこからハイハットを消すか）
FILL_SMALL = ("....X.......oxXX", None, 12)
FILL_TOM = ("....X...........", "........xxXXxxXX", 8)
FILL_BIG = ("....X...ooxxXXXX", "............xXXX", 8)
FILL_LIFT = ("o.o.x.x.xxxxXXXX", "............XXXX", 0)   # 落ちサビ・ブリッジから戻るとき（1小節かけて強く）

def build(SEC, groove, quiet=("bridge", "otosabi"), stops=(), fills_off=()):
    """SEC: [(名前, コード, 転調, 何回目)]。groove(s, n, b, L) → (kick, snare, hat, ride?, crash?) の通常の小節。
    stops: 最後の小節を「止め」にするセクション名の集合（または (名前, 何回目) の組）。返り値: 各パートの小節リストと、ドラム用の barGain。"""
    KICK, SNARE, HAT, CRASH, TOM, RIDE, DG = [], [], [], [], [], [], []
    for si, (s, pr, k, n) in enumerate(SEC):
        kb, sb, hb, cb, tb, rb = [], [], [], [], [], []
        L = len(pr)
        nxt = SEC[si + 1][0] if si + 1 < len(SEC) else None
        for b in range(L):
            kk, sn, hh, ride, crash = groove(s, n, b, L)
            tm = None
            last = b == L - 1
            fill = None
            if s not in fills_off and (kk != Z or sn != Z):
                if last:
                    if s in stops or (s, n) in stops: fill = "stop"
                    elif s in quiet: fill = FILL_LIFT
                    else: fill = FILL_BIG
                elif b % 8 == 7: fill = FILL_TOM
                elif b % 4 == 3: fill = FILL_SMALL
            if fill == "stop":
                kk, sn, hh, ride = "X...............", "X...............", Z, False
            elif fill and sn != Z:
                fs, ft, cut = fill
                sn = "".join(f if f != "." else (sn[j] if j < (cut if cut else 16) else ".") for j, f in enumerate(fs))
                hh = cut_hat(hh, cut) if cut else Z
                tm = ft
                ride = False if (ft or not cut) else ride   # フィル中はライドを止める（手は2本）
                if ft: kk = kk[:8] + "".join("X" if (j % 4 == 0) else "." for j in range(8))
            if crash and hh: hh = "." + hh[1:]
            kb.append("g:" + kk); sb.append("g:" + sn); hb.append("g:" + hh)
            cb.append("g:X..............." if crash else "R:4")
            rb += ["D2:0.5"] * 8 if ride else ["R:4"]
            tb += tomtok(tm) if tm else ["R:4"]
        KICK.append(kb); SNARE.append(sb); HAT.append(hb); CRASH.append(cb); TOM.append(tb); RIDE.append(rb)
    return KICK, SNARE, HAT, CRASH, TOM, RIDE

def drum_gain(SEC, base):
    """ドラム用の強弱の流れ（ほかのパートより大きめの差）。base: セクション名 → (はじめ, おわり)。"""
    out = []
    for s, pr, k, n in SEC:
        a, z = base.get(s, (0.9, 0.9))
        L = len(pr)
        for i in range(L):
            g = a + (z - a) * (i / max(1, L - 1))
            if s == "chorus" and i == 0: g = max(g, 1.05)   # サビ頭は強く
            out.append(round(min(1.08, g), 3))
    return out
