# ライブラリの全部の型を、いろいろなキー・和音・チューニングで音の並びにして、機械的に確かめる
#   - 拍の合計が「小節数×4」ちょうど
#   - 作曲ソフトの書き方（音名:拍＋印）として読める（src/audio/ai-song.ts の parseNotes と同じ正規表現）
#   - 音域: ギター F1〜E6（low は E2・D2・B1・F1 で試す）、ベース B0〜G3
#   - 強拍で鳴らす長い音どうし（ギターの最低音とベース）が、短2度でぶつからない（ペアの選び方 pick_pair を 300 回）
#   python3 verify_library.py
import sys, os, re, random, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "assets-src", "ai-songs", "_gen"))
import loud25_phrases as LP

TOK = re.compile(r"^(R|x|[A-G]#?-?\d):(\d+(?:\.\d+)?)((?:~\.|[!,'_~*<]|>(?![A-G])|[\^/\\]\.?(?:@\d+(?:\.\d+)?)?)*)(?:>([A-G][#b]?-?\d))?$")
CHORD_OF = {"m": "m", "m7": "m7", "M": "", "maj7": "maj7", "7": "7", "5": "5", "sus": "sus2", "dim": "dim"}
MODE_OF = {"m": "aeolian", "m7": "dorian", "M": "ionian", "maj7": "ionian", "7": "mixolydian", "5": "aeolian", "sus": "aeolian", "dim": "aeolian"}

def notes_of(s):
    out = []; t = 0.0
    for tk in s.split():
        m = TOK.match(tk)
        if not m: raise ValueError(f"読めない: {tk}")
        d = float(m.group(2))
        if m.group(1) not in ("R", "x"): out.append((t, d, LP.midi(m.group(1)), m.group(3)))
        t += d
    return out, t

def main():
    rng = random.Random(1)
    bad = []; n = 0
    for inst in ("guitar", "bass"):
        lo, hi = LP.RANGE[inst]
        for ph in LP.load(inst):
            for trial in range(4):
                cls = rng.choice(ph["fits"])
                roots = [rng.randrange(12) for _ in range(ph["bars"] + 1)]
                key = LP.NAMES[roots[0]]
                chords = [LP.NAMES[r] + CHORD_OF[cls] for r in roots[:ph["bars"]]]
                low = rng.choice(["E2", "D2", "B1", "F1"]) if inst == "guitar" else rng.choice(["E1", "B0"])
                try:
                    vs = LP.render_voices(ph, chords, key=key, mode=MODE_OF[cls], low=low)
                except Exception as e:
                    bad.append((ph["id"], "書き出せない", str(e))); break
                for v in vs:
                    try: ns, tot = notes_of(v)
                    except ValueError as e: bad.append((ph["id"], str(e))); continue
                    if abs(tot - ph["bars"] * 4) > 1e-6: bad.append((ph["id"], f"拍の合計 {tot}"))
                    for t, d, m, mk in ns:
                        snd = m + (2 if "^^" in mk else 1 if "^" in mk else 0)
                        if m < lo or snd > hi: bad.append((ph["id"], f"音域の外 {LP.name(m)} low={low}")); break
                n += 1
    # ペアの確認
    clash = 0; pairs = 0
    secs = ["前奏", "Aメロ", "Bメロ", "サビ", "看板リフ", "ブリッジ", "ブレイクダウン"]
    progs = [["Dm", "Bb", "C", "Am"], ["E5", "E5", "C5", "D5"], ["Am", "F", "G", "Em"], ["C", "G", "Am", "F"], ["F#m", "D", "A", "E"]]
    for i in range(300):
        pr = rng.choice(progs); sec = rng.choice(secs)
        k = LP.parse_chord(pr[0]); minor = k.cls in ("m", "5")
        try:
            p = LP.pick_pair(sec, pr, key=LP.NAMES[k.root], mode="aeolian" if minor else "ionian", energy=rng.random(), low=rng.choice(["E2", "D2"]), seed=i)
        except LookupError as e:
            bad.append(("pair", str(e))); continue
        pairs += 1
        g, _ = notes_of(p["guitar"]["notes"]); b, _ = notes_of(p["bass"]["notes"])
        for t, d, m, mk in b:
            if t % 2 or d < 1: continue
            for t2, d2, m2, mk2 in g:
                if t2 <= t < t2 + d2 and d2 >= 1 and (m2 - m) % 12 in (1, 11):
                    clash += 1; break
    print(json.dumps({"確かめた型×場面": n, "問題": len(bad), "例": bad[:15], "ペア": pairs, "強拍の長い音の半音のぶつかり": clash}, ensure_ascii=False, indent=1))
    return 0 if not bad else 1

if __name__ == "__main__":
    sys.exit(main())
