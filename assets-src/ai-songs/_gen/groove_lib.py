# リズムの取り方（グルーブ）の型を、曲で使う（型の中身は tools/vt3/grooves.json）。
# 2026-11-25 人間「リズムの取り方も変えれるようにしよう。なんか、グルーブがのっぺりしていて感じられないんだよね」
#   のっぺりの元（考えたこと）: ハイハットの強さが2段だけ・ゴーストがほぼ無い／キック・ベース・和音の打つ所が毎小節同じ／ずれ（はね・あと乗り・前のめり）を曲に書いていなかった。
# 使い方:
#   G = Groove("bounce")                     # 型を選ぶ（形のくじ form_dice.py が「リズムの取り方」を引く）
#   G.drums(D, b, i)                         # その小節のキック・スネア・ハイハット（i は場面の中の小節番号。4小節で1まわり）
#   G.B[i % 4] ／ G.C[i % 4]                 # ベースの型／和音の打ち方（曲の bass()・saw() にそのまま渡す）
#   G.apply(js)                              # 書き出しの前に、はね・ノリ（ぴったり／あと乗り／前のめり）・人間らしさの量を曲に書く
import json, os
_TAB = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools", "vt3", "grooves.json"), encoding="utf-8"))
NAMES = [k for k in _TAB if not k.startswith("_")]


class Groove:
    def __init__(self, key):
        assert key in _TAB, (key, NAMES); t = _TAB[key]; self.key = key; self.name = t["name"]; self.K, self.S, self.H, self.B, self.C = t["K"], t["S"], t["H"], t["B"], t["C"]; self.t = t
        for arr in (self.K, self.S, self.H, self.B, self.C): assert all(len(x) == 16 for x in arr), (key, arr)

    def drums(self, D, b, i, hat=None, kick=None, snare=None): D.set(b, kick or self.K[i % 4], snare or self.S[i % 4], hat or self.H[i % 4])

    def apply(self, js):
        t = self.t
        if t.get("swing16"): js["swing16"] = t["swing16"]
        js["grooveFeel"] = t.get("feel", "tight"); js["human"] = t.get("human", 0.35); js["lockToKick"] = True      # キックと同じ所のベースは、同じだけずらす
        return js
