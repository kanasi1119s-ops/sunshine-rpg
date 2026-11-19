# ギターの弾き方の見本（2026-11-19。人間「色々な弾き方あるはずだから勉強して」）。弾き方ごとに4小節ずつ。和音は Bm・G・D・A のくり返し
# 使い方: python3 tools/vt3/gtr_styles_demo.py <出力.json> → node tools/composer/song.mjs build <出力.json> --wav $(cat <出力.json>.flags)
import sys, random as _r
sys.path.insert(0, "/home/claude/wt-mix/assets-src/ai-songs/_gen")
from vocalo_lib import *
import gtr2_lib as G2
CH = ["Bm", "G", "D", "A"]
STYLES = ["1 8分のかき鳴らし", "2 16分のカッティング", "3 ミュートの刻みと白玉", "4 オクターブ奏法", "5 単音リフとキメ", "6 アルペジオ", "7 コードの飾り", "8 裏打ちと合いの手"]
S = Song("97", "gtrstyles", "ギターの弾き方の見本", "guitar styles", 128, 4, "B", "minor", "見本")
S.kit = "naked-x"; S.flags = "--bass bnb-loud --ref-tone bright-nu-wall " + S.flags
for n in STYLES: S.scene(n, 4, "break", CH)
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}
V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False); D = S.drumkit(); LY = Lyrics(S); RNG = _r.Random(5)
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.16, -0.6, tone="nu-metal-wall")) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.15, 0.6, tone="nu-metal-wall")) for i in range(6)]
GM = [S.track(f"Lギター（ミュートの刻み）{i + 1}", "distGuitar", **{**rock_gtr_spec(0.16, -0.6, tone="nu-metal-wall"), "palmMute": "light"}) for i in range(3)]
CG = [S.track(f"クリーンのギター{i + 1}弦め", "guitar", amp="clean", volume=0.2, pan=0.5, reverb=0.3, chorus=0) for i in range(6)]
AG = [S.track(f"生のギター{i + 1}弦め", "guitar", patch="nylonGuitar", amp="clean", volume=0.2, pan=0.4, reverb=0.25, chorus=0) for i in range(6)]
BASS = S.track("ベース", "bass", **rock_bass_spec(0.2))
SL, SR, SC, SA = G2.Strummer(GL, S, 1), G2.Strummer(GR, S, 2), G2.Strummer(CG, S, 3), G2.Strummer(AG, S, 4); tri = None
N = nm
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); ch = CH[i]; tri = G2.triad(ch, tri); low_ = G2.low_shape(ch); r = low(ch, "E1")
    BASS.bar(b, " ".join(f"{N(r)}:0.5" for _ in range(8))); feel(D, b, "rock8" if i % 2 == 0 else "rock8b")
    s = n[0]
    if s == "1":      # 左＝8分をぜんぶダウン、右＝8分で下・上
        SL.bar(b, ("D-d-d-D-d-d-D-d-", "D-d-D-d-d-D-d-d-")[i % 2], low_, feel="down"); SR.bar(b, ("D-U-D-U---U-D-U-", "D---D-U-D-U-D-U-")[i % 2], tri)
    elif s == "2":    # 右＝16分のカッティング（短く切る音と、音程のないブラッシング「チャカ」）。左＝白玉
        SL.bar(b, "D---------------", low_, feel="down"); SR.bar(b, ("D.xUd.xUD.xxdUx.", "D.xxdUx.D.xUd.xU")[i % 2], tri, feel=16)
    elif s == "3":    # 左＝ブリッジミュートの刻み（やわらかめ）＋ 和音のアクセント、右＝白玉（強い拍だけ弾いてのばす）
        G2.palm(GM, S, b, "m-m-----m-m-m---" if i % 2 == 0 else "m-m-m-----m-----", low_, RNG); SL.bar(b, "------D-------D-" if i % 2 == 0 else "--------D-----D-", low_, feel="down"); SR.bar(b, "D-------D-------", tri)
    elif s == "4":    # 右＝オクターブ奏法の旋律、左＝8分のパワーコード
        SL.bar(b, "D-d-d-D-d-d-D-d-", G2.low_shape(ch, with_third=False), feel="down")
        G2.octaves(SR, 2, 4, S, b, ["F#3:1.5 D3:0.5 E3:1 F#3:1", "G3:1.5 B3:0.5 A3:1 G3:1", "F#3:1 A3:1 D4:1.5 C#4:0.5", "E3:1.5 C#3:0.5 E3:2"][i])
    elif s == "5":    # 左右で同じ単音リフ（ユニゾン）→ 4小節めは和音のキメ
        if i < 3:
            line = ["B2:0.5 B2:0.5 D3:0.5 B2:0.5 E3:0.5 D3:0.5 B2:0.5 A2:0.5", "G2:0.5 G2:0.5 B2:0.5 G2:0.5 D3:0.5 B2:0.5 G2:0.5 A2:0.5", "D3:0.5 D3:0.5 F#3:0.5 D3:0.5 A3:0.5 F#3:0.5 E3:0.5 D3:0.5"][i]
            SL.line(0, S.bar_beat(b), line); SR.line(0, S.bar_beat(b), line)
        else: SL.bar(b, "D-----D---D-....", low_, feel="down"); SR.bar(b, "D-----D---D-....", tri, feel="down")
    elif s == "6":    # 右＝クリーンのアルペジオ（弦ごとに鳴りつづける）、左＝白玉
        SL.bar(b, "D---------------", G2.low_shape(ch, with_third=False), feel="down"); SC.arp(b, ("0-2-3-2-4-2-3-2-", "0-3-2-4-3-2-4-3-")[i % 2], G2.open_shape(ch))
    elif s == "7":    # 生のギター: かき鳴らしの中で、1本だけ指を足して音を変える（sus4 → 3度）
        sh = G2.open_shape(ch); SA.bar(b, ("D---D-U---U-D-U-", "D-U-D-U---U-D-U-")[i % 2], sh)
        top3 = sorted(m for _, m in sh)[-2]; SA.hammer(b, 4, len(sh) - 2, top3 + 1); SA.hammer(b, 8, len(sh) - 2, top3)
        SL.bar(b, "D-------D-------", low_, feel="down")
    elif s == "8":    # 右＝裏打ち（「と」だけ短く）、左＝8分。4小節めに2本の弦の合いの手
        SL.bar(b, "D-d-d-d-D-d-d-d-", low_, feel="down"); SR.bar(b, "--U.--U.--U.--U.", tri)
        if i == 3: SR.line(4, S.bar_beat(b) + 2, "C#4:0.5 E4:0.5 C#4:0.5 A3:0.5"); SR.line(5, S.bar_beat(b) + 2, "E4:0.5 A4:0.5 E4:0.5 C#4:0.5")
for st in (SL, SR, SC, SA): st.end(S.nb)
S.desc = "ギターの弾き方の見本（弾き方ごとに4小節）"; finish(S, LY, V, 0)
from vt3x_lib import *
out = sys.argv[1]; js = load(out); n = sum(st.velocity(js) for st in (SL, SR, SC, SA)); save(out, js)
print("強さを付けた:", n, "音", {k: v for st in (SL, SR, SC, SA) for k, v in st.count.items() if k not in ("notes",)})
