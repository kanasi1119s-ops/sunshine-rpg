# ライブラリの型を並べた短いテスト曲（16小節）を作る。使い方の見本も兼ねる。
#   python3 test_song.py <出力.json> [種]
#   → node tools/composer/song.mjs build <出力.json> --wav --drums crocell --bass bnb --out <フォルダ>
# 前奏（分散和音＋ペダルのベース）→ Aメロ（リフ＋ユニゾンのベース）→ サビ（伸ばすバッキング＋根音のベース＋リードの短い句）→ ブレイクダウン（キックとベースを一致）
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "assets-src", "ai-songs", "_gen"))
import loud25_phrases as LP
from loud25_hand import put, LEAD_TONE, ARP_TONE

KEY, MODE, LOW = "D", "aeolian", "D2"
SECS = [("前奏", ["Dm", "Bb", "F", "C"]), ("Aメロ", ["Dm", "Dm", "Bb", "C"]), ("サビ", ["Bb", "C", "Dm", "Dm"]), ("ブレイクダウン", ["D5", "D5", "D5", "D5"])]

def make(out, seed=1):
    full = 16 * 4
    rest = f"R:{full}"
    # 和音の型は、声部ごとに別のパート（低い声・中・上）。同じ音色で、上の声ほど小さく
    riffs = [{"instrument": "distGuitar", "role": f"リフ・バッキング（{nm}）", "volume": v, "pan": pn, "guitarTone": "loud-mid", "powerChord": False, "double": True, "notes": rest}
             for nm, v, pn in (("低い声", 0.11, -0.6), ("中の声", 0.08, 0.6), ("上の声", 0.06, -0.3))]
    def put_voices(a, b, vs):
        for i, r in enumerate(riffs): put(r, a, b, vs[i] if i < len(vs) else "")
    arp = {"instrument": "distGuitar", "role": "分散和音", "volume": 0.09, "pan": 0.3, "powerChord": False, "double": False, "di": "emily", "autoScoop": False, **json.loads(json.dumps(ARP_TONE)), "notes": rest}
    lead = {"instrument": "distGuitar", "role": "リード", "volume": 0.12, "pan": 0.05, "powerChord": False, "double": False, "di": "emily", "autoScoop": False, **json.loads(json.dumps(LEAD_TONE)), "notes": rest}
    bass = {"instrument": "bass", "role": "ベース", "volume": 0.2, "pan": 0, "amp": "bassSplit", "ampDrive": 0.5, "duck": 0.25, "notes": rest}
    kick = {"instrument": "kick", "role": "キック", "volume": 0.22, "pan": 0, "amp": "auto", "notes": "g:" + "." * (full * 4)}
    snare = {"instrument": "snare", "role": "スネア", "volume": 0.16, "pan": 0, "amp": "auto", "notes": "g:" + "." * (full * 4)}
    hat = {"instrument": "hihat", "role": "ハイハット", "volume": 0.07, "pan": 0.25, "amp": "auto", "notes": "g:" + "." * (full * 4)}
    crash = {"instrument": "crash", "role": "シンバル", "volume": 0.08, "pan": -0.2, "amp": "auto", "notes": rest}
    used = []; log = []
    for k, (sec, chords) in enumerate(SECS):
        a = k * 16
        if sec == "前奏":
            g = LP.pick("guitar", role="アルペジオ", section="前奏", chords=chords[:1], energy=0.4, seed=seed, bars=4, src="gen")
            put(arp, a, a + 16, LP.render(g, chords, KEY, MODE, LOW))
            b = LP.pick("bass", role="ペダル", section="前奏", energy=0.3, seed=seed)
            put(bass, a + 8, a + 16, LP.render(b, chords[2:], KEY, MODE, "E1", bars=2))
            used += [g, b]
            put(hat, a + 8, a + 16, "x.x.x.x.x.x.x.x." * 2); put(kick, a + 8, a + 16, "x.......x.......x.......x.....x."); put(snare, a + 8, a + 16, "....x.......x.......x.......x.xx")
            put(crash, a + 8, a + 12, "C2:4!")
        elif sec == "Aメロ":
            p = LP.pick_pair("Aメロ", chords, KEY, MODE, energy=0.55, low=LOW, how="unison", avoid=[u["id"] for u in used], seed=seed, guitar_role="リフ")
            put_voices(a, a + 16, p["guitar"]["voices"]); put(bass, a, a + 16, p["bass"]["notes"])
            used += [p["guitar"]["phrase"]]
            put(kick, a, a + 16, "x.....x...x....." * 4); put(snare, a, a + 16, "....x.......x..." * 4); put(hat, a, a + 16, "x.x.x.x.x.x.x.x." * 4)
            put(crash, a, a + 4, "C2:4!")
        elif sec == "サビ":
            p = LP.pick_pair("サビ", chords, KEY, MODE, energy=0.85, low=LOW, how="split", avoid=[u["id"] for u in used], seed=seed)
            put_voices(a, a + 16, p["guitar"]["voices"]); put(bass, a, a + 16, p["bass"]["notes"])
            l1 = LP.pick("guitar", role="リード", section="サビ", chords=chords[:2], energy=0.6, seed=seed, src="gen", tech="チョーキング")
            l2 = LP.pick("guitar", role="リード", section="サビ", chords=chords[2:], energy=0.5, seed=seed + 1, src="gen", avoid=[l1["id"]])
            put(lead, a, a + 8, LP.render(l1, chords[:2], KEY, MODE, LOW)); put(lead, a + 8, a + 16, LP.render(l2, chords[2:], KEY, MODE, LOW))
            used += [p["guitar"]["phrase"], p["bass"]["phrase"], l1, l2]
            put(kick, a, a + 16, "x...x.x.x...x.x." * 4); put(snare, a, a + 16, "....x.......x..." * 4); put(hat, a, a + 16, "x.x.x.x.x.x.x.x." * 4)
            put(crash, a, a + 16, "C2:4! C2:4 C2:4! C2:4")
        else:
            p = LP.pick_pair("ブレイクダウン", chords, KEY, MODE, energy=0.6, low=LOW, seed=seed)
            put_voices(a, a + 16, p["guitar"]["voices"]); put(bass, a, a + 16, p["bass"]["notes"])
            used += [p["bass"]["phrase"]]
            put(kick, a, a + 16, "".join(x.replace("X", "x") for x in p["kick"][:4]))
            put(snare, a, a + 16, "........x......." * 4); put(crash, a, a + 16, "B2:2! B2:2 B2:2! B2:2 B2:2! B2:2 B2:2! B2:2")
    parts = riffs + [arp, lead, bass, kick, snare, hat, crash]
    song = {"title": "フレーズのライブラリのテスト", "description": "ライブラリの型を並べただけの確認用（16小節）", "bpm": 140, "beats": 4, "chords": "Dm Bb F C",
            "barsPerChord": 1, "repeats": 4, "autoAccompaniment": False, "feel": "rock", "tone": "rock", "dynamics": "natural", "parts": parts}
    json.dump(song, open(out, "w"), ensure_ascii=False, indent=1)
    for u in used: print(LP.describe(u))
    return song

if __name__ == "__main__":
    make(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1)
