import json, sys
sys.path.insert(0,".")
from walker import CHARS, render_sprite
letters="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
data={}
for n in [k for k in CHARS if not k.startswith('素体')]:
    pal=[]; idx={}
    frames={}
    for dr in ('down','up','left','right'):
        for f in range(3):
            out,colors=render_sprite(n,dr,f)
            rows=[]
            for row in out:
                s=""
                for v in row:
                    if v is None: s+="."; continue
                    col=colors[v]
                    if col not in idx: idx[col]=len(pal); pal.append(col)
                    s+=letters[idx[col]]
                rows.append(s)
            frames[f"{dr}{f}"]=rows
    data[n]={"palette":pal,"frames":frames}
body=json.dumps(data,ensure_ascii=False)
open("/home/user/sunshine-rpg/src/game/sprite/walker-data.generated.ts","w").write("// 自動生成: assets-src/pixel-practice/r19-walkers/export_walkers.py（手で編集しない）。主要キャラのマップ用ドット絵（16×32、4方向×3コマ）\nexport interface WalkerData {\n  palette: string[];\n  frames: Record<string, string[]>;\n}\n\nexport const WALKERS: Record<string, WalkerData> = "+body+";\n")
print({k:len(v['palette']) for k,v in data.items()})

# 素体（実行時に色を塗り替える）: 色は役割の番号（0〜23）で持つ
ARCH={}
for style in ('short','long','twin'):
    n={'short':'素体-short','long':'素体-long','twin':'素体-twin'}[style]
    frames={}; fixedpal=[]; fidx={}
    for dr in ('down','up','left','right'):
        for f in range(3):
            out,colors=render_sprite(n,dr,f)
            rows=[]
            for row in out:
                s2=""
                for v in row:
                    if v is None: s2+="."; continue
                    col=colors[v]
                    if col.startswith('#10') and len(col)==7 and col[3:5]==col[5:7] and 0x10<=int(col[3:5],16)<=0x10+23:
                        s2+=letters[int(col[3:5],16)-16]
                    else:
                        if col not in fidx: fidx[col]=len(fixedpal); fixedpal.append(col)
                        s2+=letters[24+fidx[col]]
                    # 24以降は固定色
                rows.append(s2)
            frames[f"{dr}{f}"]=rows
    ARCH[style]={"fixed":fixedpal,"frames":frames}
open("/home/user/sunshine-rpg/src/game/sprite/walker-data.generated.ts","a").write("\n/** 素体（髪・肌・服の色で塗り替える。文字 A〜X=役割色0〜23、Y以降=固定色）。 */\nexport const ARCHETYPES: Record<string, { fixed: string[]; frames: Record<string, string[]> }> = "+json.dumps(ARCH,ensure_ascii=False)+";\n")
print({k:len(v['fixed']) for k,v in ARCH.items()})
