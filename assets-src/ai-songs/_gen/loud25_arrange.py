# ラウドロック・ラウドメタル25曲の編曲（loud25_lib.py のエンジンで、1曲の設計からパートを組み立てる）
import random
from loud25_lib import Song, name, midi, at_least, fold, merge_long, dur_of

DRUM_INST = ("kick", "snare", "hihat", "tom", "crash")
TOM = {"1": "C4", "2": "A3", "3": "F3", "4": "D3"}
CYM = {"c": "C2", "g": "G2", "r": "D2", "R": "D2", "u": "F2", "n": "B2", "s": "A2"}

def typ(sid):
    for t in ("intro", "verse", "pre", "chorus", "inter", "bridge", "break", "solo", "outro", "open", "drop"):
        if sid.startswith(t): return t
    return sid

def cyc(lst, k):
    return lst[k % len(lst)]

def build(spec):
    S = Song(spec)
    NB, steps, beats, n16 = S.NB, S.steps, S.beats, S.n16
    D = spec["drums"]
    R = spec["rhythm"]
    parts = []

    # ── 刻み ──
    def riff_for(i):
        sid, kind, ch, k, n, no = S.bars[i]
        t = typ(sid)
        pats = R.get(sid) or R.get(t)
        if pats is None: return None
        if isinstance(pats, str): pats = [pats]
        pt = cyc(pats, k)
        return None if pt == "-" else pt
    pm_types = set(R.get("pm", []))
    open_rows, pm_rows = [], []
    for i in range(NB):
        sid, kind, ch, k, n, no = S.bars[i]
        pat = riff_for(i)
        if pat is None:
            open_rows.append(S.rest()); pm_rows.append(S.rest()); continue
        bar = S.riff_bar(pat, ch)
        if typ(sid) in pm_types or sid in pm_types:
            pm_rows.append(bar); open_rows.append(S.rest())
        else:
            open_rows.append(bar); pm_rows.append(S.rest())
    rt = R["tone"]
    rbase = {"instrument": "distGuitar", "volume": 0.1, "pan": 0, "guitarTone": rt, "gainDb": R.get("db", -5)}
    if R.get("noPower"): rbase["powerChord"] = False
    parts.append({**rbase, "role": "刻み（左右）", "notes": S.join(open_rows, "刻み")})
    if any(r != S.rest() for r in pm_rows):
        parts.append({**rbase, "role": "刻み（ブリッジミュート）", "palmMute": R.get("pmDepth", True), "notes": S.join(pm_rows, "ミュート")})

    # ── 旋律（リード・バイオリンなど）──
    L = spec["lead"]
    mel_rows = {inst: [S.rest()] * NB for inst in ("lead", "violin", "keys", "synth", "cello")}
    for sec_ids, conf in L["sections"].items():
        idx = [i for i in range(NB) if S.sec_of(i) in sec_ids.split(",")]
        if not idx: continue
        # 同じ種類のセクションごとに作る（2回目以降は var を変える）
        groups = {}
        for i in idx: groups.setdefault(S.bars[i][5], []).append(i)
        for gn, (no, bars_idx) in enumerate(sorted(groups.items())):
            inst = conf.get("inst", "lead")
            lo, hi = midi(conf.get("lo", "A4")), midi(conf.get("hi", "A5"))
            if conf.get("up") and gn == len(groups) - 1 and len(groups) > 1:
                lo += conf["up"]; hi += conf["up"]
            rows = S.melody(bars_idx, conf["rhythm"], lo, hi, peak_bar=conf.get("peak"), var=gn * 13 + conf.get("seed", 0))
            for j, i in enumerate(bars_idx):
                mel_rows[inst][i] = rows[j]
    lt = L.get("tone", "bmth-lead")
    if any(r != S.rest() for r in mel_rows["lead"]):
        parts.append({"instrument": "leadGuitar", "role": "リード（旋律）", "volume": 0.13, "pan": 0, "guitarTone": lt, "double": False, "noRestrike": True, "phrase": 8,
                      "notes": S.join(mel_rows["lead"], "リード")})
    if any(r != S.rest() for r in mel_rows["violin"]):
        # バイオリン: 柔らかく力強く透き通る（docs/sound/banned-sounds.md 21）
        parts.append({"instrument": "strings", "patch": "violin", "role": "バイオリン（旋律）", "volume": 0.17, "pan": -0.15, "reverb": 0.45, "gainDb": 3, "bright": -0.15,
                      "attack": 0.12, "release": 0.6, "doubleDetune": {"cents": 5, "spread": 0.3}, "phrase": 8,
                      "fx": [{"type": "eq", "low": 2, "mid": -2.5, "midHz": 2800, "high": 0}, {"type": "delay", "beats": 0.75, "mix": 0.08, "feedback": 0.2}, {"type": "reverb", "mix": 0.22}],
                      "notes": S.join(mel_rows["violin"], "バイオリン")})
    if any(r != S.rest() for r in mel_rows["cello"]):
        parts.append({"instrument": "strings", "patch": "cello", "role": "チェロ（旋律）", "volume": 0.17, "pan": -0.2, "reverb": 0.45, "attack": 0.1, "release": 0.6, "phrase": 8,
                      "fx": [{"type": "eq", "low": 1, "mid": -1.5, "midHz": 2500, "high": 0}, {"type": "reverb", "mix": 0.2}], "notes": S.join(mel_rows["cello"], "チェロ旋律")})
    if any(r != S.rest() for r in mel_rows["keys"]):
        parts.append({"instrument": "piano", "role": "ピアノ（旋律）", "volume": 0.12, "pan": 0.1, "reverb": 0.25, "phrase": 8, "notes": S.join(mel_rows["keys"], "ピアノ旋律")})
    if any(r != S.rest() for r in mel_rows["synth"]):
        parts.append({"instrument": "lead", "patch": "sawLead", "role": "シンセの旋律", "volume": 0.07, "breath": True, "pan": 0.1, "reverb": 0.3,
                      "fx": [{"type": "delay", "beats": 0.75, "mix": 0.15, "feedback": 0.3}], "notes": S.join(mel_rows["synth"], "シンセ旋律")})

    # ── スウィープ・タッピング・ソロ ──
    T = spec.get("tech", {})
    if T:
        tech = [S.rest()] * NB
        tpos = [0]
        def triad(ch):
            return ch.root, ch.third()
        def sweep(ch):
            r, t3 = triad(ch)
            b = at_least(r, midi("E3"))
            seq = [b, b + t3, b + 7, b + 12, b + 12 + t3, b + 19, b + 24, b + 19, b + 12 + t3, b + 12, b + 7, b + t3, b, b + t3, b + 7, b + 12]
            seq = (seq * 2)[:n16]
            return " ".join(f"{name(m)}:0.25" + ("!" if j % 8 == 0 else "_") for j, m in enumerate(seq))
        def tap(ch):
            r, t3 = triad(ch)
            hi = at_least(r, midi("C#5")) + 7
            if hi > midi("E6"): hi -= 12
            g = [hi, hi - 7 + t3, hi - 7]
            toks = []
            for _ in range(n16):
                j = tpos[0] % 3; tpos[0] += 1
                toks.append(f"{name(g[j])}:0.25" + ("!" if j == 0 else "_"))
            return " ".join(toks)
        for sid, how in T.items():
            idx = [i for i in range(NB) if S.sec_of(i) == sid]
            for j, i in enumerate(idx):
                ch = S.bars[i][2]
                h = how[j % len(how)]
                if h == "s": tech[i] = sweep(ch)
                elif h == "t": tech[i] = tap(ch)
                elif h == "m":   # ソロの旋律（16分と8分を混ぜた速い動き）
                    rhy = [[0.25] * 8 + [0.5, 0.5, 1] + [1] * (beats - 4)] if beats >= 4 else [[0.25] * 4 + [0.5] * (beats * 2 - 2)]
                    tech[i] = S.melody([i], rhy, midi("D5"), midi("D6"), var=j, end_long=False)[0]
                elif h == "-": tech[i] = S.rest()
        parts.append({"instrument": "leadGuitar", "role": "スウィープ・タッピング・ソロ", "volume": 0.11, "pan": 0.1, "guitarTone": lt, "double": False, "noRestrike": True, "legato": True,
                      "fx": [{"type": "eq", "low": -2, "mid": 3, "midHz": 1800, "high": 1}, {"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.2}, {"type": "plate", "mix": 0.12}],
                      "notes": S.join(tech, "技")})

    # ── ベース ──
    B = spec["bass"]
    brow = []
    seen = {}
    occ = {}
    for i in range(NB):
        sid, kind, ch, k, n, no = S.bars[i]
        if k == 0:
            seen[typ(sid)] = seen.get(typ(sid), -1) + 1
        o = seen.get(typ(sid), 0)
        m = B.get(sid) or B.get(typ(sid))
        # 後半（k が半分より後）は「答え」の動機（_b）があればそちら。2回目以降の同じ種類のセクションは、並びを1つずらして同じ4小節のくり返しを避ける
        if k >= n // 2 and (B.get(sid + "_b") or B.get(typ(sid) + "_b")):
            m = B.get(sid + "_b") or B.get(typ(sid) + "_b")
        if m is None or m == "-":
            brow.append(S.rest()); continue
        if isinstance(m, str): m = [m]
        motif = cyc(m, k + o)
        if k == n - 1 and (sid + "_end") in B: motif = B[sid + "_end"]
        elif k == n - 1 and (typ(sid) + "_end") in B: motif = B[typ(sid) + "_end"]
        brow.append(S.bass_bar(motif, ch, S.nxt(i)))
    parts.append({"instrument": "bass", "role": "ベース（旋律）", "volume": 0.19, "pan": 0, "amp": "bassGrind", "ampDrive": B.get("drive", 0.75), "notes": S.join(brow, "ベース")})  # 2026-10-21 人間「歪ませていいけど、音がこもっていてラウドのベースじゃなかった」「指弾きの方がいい」: 明るい歪み（bassGrind）＋指弾きの録音（--bass finger）

    # ── ドラム ──
    rows = {"k": [], "s": [], "h": []}
    cym_rows, tom_rows = [], []
    for i in range(NB):
        sid, kind, ch, k, n, no = S.bars[i]
        d = D.get(sid) or D.get(typ(sid)) or {}
        def pick(key, default):
            v = d.get(key, default)
            return cyc(v, k) if isinstance(v, list) else v
        kk = pick("k", "." * steps)
        if kk == "sync":
            pat = riff_for(i) or ("X" + "." * (steps - 1))
            kk = "".join("X" if c == "X" else ("x" if c not in "-=" else ".") for c in pat)
        ss = pick("s", "." * steps); hh = pick("h", "." * steps); cc = pick("c", "." * steps); tt = pick("t", "." * steps)
        last = k == n - 1 and not d.get("nofill")
        if last and i + 1 < NB:
            fill = d.get("fill", "snare")
            q = steps - 4
            if fill == "snare":
                ss = ss[:q] + "xxXX"; hh = hh[:q] + "...."; cc = cc[:q] + "...."
            elif fill == "tom":
                ss = ss[:steps - 8] + "........"; tt = "." * (steps - 8) + "11223344"; hh = hh[:steps - 8] + "." * 8; cc = cc[:steps - 8] + "." * 8
                kk = kk[:steps - 8] + "x.x.x.x."
            elif fill == "stop":
                kk = kk[:q] + "...."; ss = ss[:q] + "...."; hh = hh[:q] + "...."; cc = cc[:q] + "...."
            elif fill == "kick":
                kk = kk[:q] + "XXXX"; ss = ss[:q] + "...X"; cc = cc[:q] + "...."
        if k == 0 and d.get("crash", True) and kk[0] != ".":
            cc = "c" + cc[1:]
        # 同時に叩けない組み合わせを外す（シンバル・タムと重なるハイハットは休む）
        hh = "".join("." if (cc[j] != "." or tt[j] != ".") else hh[j] for j in range(steps))
        for key, v in (("k", kk), ("s", ss), ("h", hh)):
            assert len(v) == steps, (spec["slug"], sid, key, v)
            rows[key].append(v)
        # シンバル・タムを音名の並びに
        def to_notes(g, table):
            toks = []; j = 0
            while j < steps:
                c = g[j]; m = j + 1
                while m < steps and g[m] == ".": m += 1
                d_ = (m - j) * S.res
                if c == ".": toks.append(f"R:{d_:g}")
                else: toks.append(f"{table[c]}:{d_:g}" + ("!" if c in "cnRs" or c.isdigit() and j % 4 == 0 else ""))
                j = m
            return " ".join(toks)
        cym_rows.append(to_notes(cc, CYM)); tom_rows.append(to_notes(tt, TOM))
    drum = {"pan": 0, "amp": "auto", "gainDb": spec.get("drumDb", -4)}
    parts += [
        {"instrument": "kick", "role": "キック", "volume": 0.22, **drum, "trigger": spec.get("trigger", "punch"), "notes": S.grid(rows["k"], "キック")},
        {"instrument": "snare", "role": "スネア", "volume": 0.18, **drum, "push": 0.02, "notes": S.grid(rows["s"], "スネア")},
        {"instrument": "hihat", "role": "ハイハット", "volume": 0.05, **drum, "push": -0.01, "notes": S.grid(rows["h"], "ハット")},
        {"instrument": "tom", "role": "タム", "volume": 0.15, **drum, "notes": S.join(tom_rows, "タム")},
        {"instrument": "crash", "role": "シンバル", "volume": 0.057, **drum, "notes": S.join(cym_rows, "シンバル")},
    ]

    # ── 追加の楽器 ──
    X = spec.get("extras", {})
    def voices(i, lo_name, n=3):
        ch = S.bars[i][2]
        Rr = at_least(ch.root, midi(lo_name))
        third = Rr + ch.third()
        top = Rr + (ch.seventh() if len(ch.iv) > 3 else 7)
        if top <= third: top += 12
        return [Rr, third, top][:n]
    def active(i, secs):
        if not secs: return False
        return any(S.sec_of(i).startswith(p) for p in secs.split(","))
    if "piano" in X:
        cfg = X["piano"]
        arp, chd = [], [[], [], []]
        for i in range(NB):
            ch = S.bars[i][2]; k = S.bars[i][3]
            if active(i, cfg.get("arp", "")):
                Rr = at_least(ch.root, midi(cfg.get("arpLo", "C5")))
                pat = [Rr, Rr + 7, Rr + 12, Rr + 12 + ch.third(), Rr + 19, Rr + 12 + ch.third(), Rr + 12, Rr + 7]
                pat = [m - 12 if m > midi("C7") else m for m in pat]
                rate = cfg.get("arpRate", 0.25)
                seq = (pat * 8)[: int(round(beats / rate))]
                arp.append(" ".join(f"{name(m)}:{rate:g}" + ("!" if j % 4 == 0 else ",") for j, m in enumerate(seq)))
            else:
                arp.append(S.rest())
            if active(i, cfg.get("chords", "")):
                vs = voices(i, cfg.get("chordLo", "A3"))
                rhy = cfg.get("chordRhythm", [beats])
                for v in range(3):
                    chd[v].append(" ".join(f"{name(vs[v])}:{d:g}" + ("!" if q == 0 else "") for q, d in enumerate(rhy)))
            elif active(i, cfg.get("soft", "")):
                vs = voices(i, cfg.get("chordLo", "A3"))
                for v in range(3): chd[v].append(f"{name(vs[v])}:{beats},")
            else:
                for v in range(3): chd[v].append(S.rest())
        if any(a != S.rest() for a in arp):
            parts.append({"instrument": "piano", "role": "キーボード（右手）", "volume": 0.09, "pan": 0.2, "reverb": 0.22, "notes": S.join(arp, "ピアノ右手")})
        if any(c != S.rest() for c in chd[0]):
            for v in range(3):
                parts.append({"instrument": "piano", "role": f"キーボード（和音）{v + 1}", "volume": 0.07, "pan": -0.15, "reverb": 0.22, "notes": S.join(chd[v], "ピアノ和音")})
    if "strings" in X:
        cfg = X["strings"]
        cello, ens = [], [[], [], []]
        for i in range(NB):
            ch = S.bars[i][2]; k = S.bars[i][3]; nb = S.nxt(i)
            if active(i, cfg.get("cello", "")):
                Rr = at_least(ch.root, midi("C3"))
                cm = cfg.get("celloMotif", [f"R:{beats}"]); cm = [cm] if isinstance(cm, str) else cm
                motif = cyc(cm, k)
                cello.append(" ".join(f"{name(fold(S.bass_tone(ch, nb, t.split(':')[0], midi('C3'), midi('E4')), midi('C3'), midi('E4')))}:{t.split(':')[1]}" for t in motif.split()))
            else:
                cello.append(S.rest())
            if active(i, cfg.get("pad", "")):
                vs = voices(i, "G3")
                for v in range(3): ens[v].append(f"{name(vs[v])}:{beats}")
            else:
                for v in range(3): ens[v].append(S.rest())
        if any(c != S.rest() for c in cello):
            parts.append({"instrument": "strings", "patch": "cello", "role": "チェロ（対旋律）", "volume": 0.14, "pan": 0.25, "reverb": 0.4, "release": 0.5, "attack": 0.08,
                          "notes": S.join(cello, "チェロ")})
        if any(c != S.rest() for c in ens[0]):
            for v in range(3):
                parts.append({"instrument": "strings", "patch": "stringEnsemble", "role": f"弦の合奏 {v + 1}", "volume": 0.05, "pan": 0, "reverb": 0.5, "release": 0.8,
                              "notes": merge_long([x if x.startswith("R") else x + "," for x in ens[v]], beats)})
    if "synth" in X:
        cfg = X["synth"]
        wall = [[], [], []]; pl = []
        for i in range(NB):
            ch = S.bars[i][2]
            if active(i, cfg.get("wall", "")):
                vs = voices(i, "B3")
                for v in range(3): wall[v].append(f"{name(vs[v])}:{beats}")
            else:
                for v in range(3): wall[v].append(S.rest())
            if active(i, cfg.get("pluck", "")):
                Rr = at_least(ch.root, midi("C4"))
                pat = [Rr, Rr + 7, Rr + 12, Rr + 7]
                pl.append(" ".join(f"{name(m)}:0.5" for m in (pat * beats)[: beats * 2]))
            else:
                pl.append(S.rest())
        if any(w != S.rest() for w in wall[0]):
            for v in range(3):
                parts.append({"instrument": "pad", "patch": "supersawPad", "role": f"シンセの壁 {v + 1}", "volume": 0.035, "pan": 0, "reverb": 0.3, "duck": 0.35,
                              "fx": [{"type": "eq", "low": -4, "mid": 0, "midHz": 1000, "high": 1}], "notes": S.join(wall[v], "壁")})
        if any(p != S.rest() for p in pl):
            parts.append({"instrument": "lead", "patch": cfg.get("pluckPatch", "pluckSynth"), "role": "シンセの刻み", "volume": 0.06, "breath": True, "pan": -0.2, "reverb": 0.25,
                          "fx": [{"type": "delay", "beats": 0.75, "mix": 0.18, "feedback": 0.3}], "notes": S.join(pl, "シンセ刻み")})
    if "choir" in X:
        cfg = X["choir"]
        ch3 = [[], [], []]
        for i in range(NB):
            if active(i, cfg):
                vs = voices(i, "A3")
                for v in range(3): ch3[v].append(f"{name(vs[v])}:{beats}")
            else:
                for v in range(3): ch3[v].append(S.rest())
        for v in range(3):
            parts.append({"instrument": "choir", "role": f"合唱（あー）{v + 1}", "volume": 0.06, "breath": True, "pan": 0, "reverb": 0.5, "notes": S.join(ch3[v], "合唱")})
    if "gated" in X:
        g = []
        for i in range(NB):
            ch = S.bars[i][2]
            if active(i, X["gated"]):
                Rr = at_least(ch.root, midi("C4"))
                g.append(f"{name(Rr)}:{beats / 2:g} {name(Rr + 7)}:{beats / 2:g}")
            else:
                g.append(S.rest())
        parts.append({"instrument": "guitar", "role": "加工ギター（拍で刻む）", "volume": 0.035, "pan": 0.3, "guitarTone": "electro-rock-gated", "notes": S.join(g, "加工")})
    if "open" in X:   # 全弦開放のかき鳴らし（最初の小節）
        notes6 = X["open"]
        for j, nn in enumerate(notes6):
            row = [f"{nn}:{beats}!" if (S.sec_of(i).startswith("open") and S.bars[i][3] == 0) else S.rest() for i in range(NB)]
            parts.append({"instrument": "distGuitar", "role": f"全弦開放（{j + 1}弦目）", "volume": 0.07, "pan": 0, "guitarTone": rt, "double": False, "ampDrive": 0.25, "ampGate": 0,
                          "powerChord": False, "sustain": 3, "reverb": 0.4, "push": round(j * 12 / 1000 * spec["bpm"] / 60, 3), "notes": S.join(row, "開放")})
    # ライザー（3小節前から。頂点が次の場面の頭）
    if spec.get("riser", True):
        targets = set(spec.get("riserTo", ["chorus", "solo", "break"]))
        rz = []
        skip = 0
        for i in range(NB):
            if skip:
                skip -= 1; continue
            hit = i + 3 < NB and S.first_of_sec(i + 3) and typ(S.sec_of(i + 3)) in targets and S.bars[i][3] == S.bars[i][4] - 3
            if hit and beats * 3 <= 16:
                rz.append(f"C4:{beats * 3}"); skip = 2
            else:
                rz.append(S.rest())
        parts.append({"instrument": "pad", "patch": "fxRiser", "role": "ライザー", "volume": 0.08, "pan": 0, "notes": " ".join(rz)})

    sections = [{"kind": kind, "bars": n} for (sid, kind, n, prog) in spec["form"]]
    song = {
        "title": spec["title"], "description": "仮: " + spec["desc"] + "（ラウドロック・ラウドメタル25曲。自作）",
        "bpm": spec["bpm"], "beats": beats, "chords": " ".join(b[2].label() for b in S.bars), "barsPerChord": 1, "repeats": 1,
        "autoAccompaniment": False, "feel": "rock", "tone": "metal", "dynamics": True, "human": spec.get("human", 0.3),
        "sections": sections, "diGuitar": "emily", "autoScoop": False, "guitarWobble": False,
        "drumMix": {"kick": {"level": 1.15}, "crash": {"level": 1.1}},
        "parts": parts,
    }
    if spec.get("modulate"): song["modulate"] = {"at": "lastChorus", "semitones": spec["modulate"]}
    if beats != 4 and spec.get("grouping"): song["grouping"] = spec["grouping"]
    return song, S
