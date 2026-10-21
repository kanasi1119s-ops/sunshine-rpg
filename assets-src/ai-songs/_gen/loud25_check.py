# 設計表の長さの点検（ベースの動機・チェロの動機・旋律のリズム・リフの文字数）。間違いをまとめて表示する
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from loud25 import SPECS
bad = 0
for sp in SPECS:
    b = sp.get("beats", 4); res = sp.get("res", 0.25); st = int(round(b / res))
    def tot(m): return sum(float(t.split(":")[1].rstrip("!',")) for t in m.split())
    for k, v in sp["bass"].items():
        if k in ("drive", "style"): continue
        for m in ([v] if isinstance(v, str) else v):
            if m != "-" and abs(tot(m) - b) > 1e-6: print(sp["no"], "ベース", k, tot(m), m); bad += 1
    for k, v in sp["rhythm"].items():
        if k in ("tone", "pm", "db", "noPower", "pmDepth"): continue
        for m in ([v] if isinstance(v, str) else v):
            if m != "-" and len(m) != st: print(sp["no"], "リフ", k, len(m), m); bad += 1
    for k, c in sp["lead"]["sections"].items():
        for r in c["rhythm"]:
            if abs(sum(r) - b) > 1e-6: print(sp["no"], "旋律", k, sum(r), r); bad += 1
    st_ = sp.get("extras", {}).get("strings", {})
    cm = st_.get("celloMotif", [])
    for m in ([cm] if isinstance(cm, str) else cm):
        if abs(tot(m) - b) > 1e-6: print(sp["no"], "チェロ", tot(m), m); bad += 1
    for sec, d in sp["drums"].items():
        for key in ("k", "s", "h", "c", "t"):
            v = d.get(key)
            if v is None: continue
            for m in ([v] if isinstance(v, str) else v):
                if m != "sync" and len(m) != st: print(sp["no"], "ドラム", sec, key, len(m), m); bad += 1
print("問題", bad, "件")
