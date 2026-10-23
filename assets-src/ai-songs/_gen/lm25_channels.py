# MIDI のチャンネルあふれを直す（2026-10-23）。使い方: python3 lm25_channels.py <曲.json>（上書き）
# 作曲ソフトは、楽器・左右・残響・立ち上がりなどが違うパートを別のチャンネルにし、ドラム以外で15を超えると、
# 残りのパートを別の楽器のチャンネルへ回す。01 では、ピアノ5本がシンバルの効果音（逆再生クラッシュ・スウェル）のチャンネルで鳴り、
# ずっと「サー」と流れる音になっていた（人間「サーって流れてる音のせいで、音のバランスかなり悪くなってる」）。
# 作曲ソフトの点検（song.mjs build の「チャンネルが足りません」）が消えるまで、同じ楽器のパートの設定を順にそろえる。
import json, subprocess, sys, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SAME = ("pan", "reverb", "chorus", "bright", "duck", "detune", "attack", "release", "gainDb")   # gainDb もチャンネルごと


def overflow(path):
    r = subprocess.run(["node", "tools/composer/song.mjs", "build", path, "--out", "/tmp/lm25-chcheck"], cwd=ROOT, capture_output=True, text=True, timeout=600)
    return [l for l in (r.stdout + r.stderr).splitlines() if "チャンネルが足りません" in l]


def unify(parts, pick):
    ps = [p for p in parts if pick(p)]
    if len(ps) < 2: return False
    base = ps[0]; changed = False
    for p in ps[1:]:
        for k in SAME:
            if p.get(k) != base.get(k):
                if k in base: p[k] = base[k]
                else: p.pop(k, None)
                changed = True
    return changed


def steps(song):
    P = song["parts"]
    inst = lambda p: (p.get("instrument"), p.get("patch"))
    groups = {}
    for p in P:
        if p.get("instrument") in ("kick", "snare", "hihat", "tom", "crash"): continue
        groups.setdefault(inst(p), []).append(p)
    # 1) 鍵盤・弦・合唱・パッド・オルガン・金管など、同じ楽器の重ね（和音の声部）は1つのチャンネルに
    yield "同じ楽器の重ね（ギター以外）", lambda: any(unify(P, lambda p, k=k: inst(p) == k) for k, v in groups.items() if k[0] not in ("distGuitar", "guitar", "bass"))
    # 2) クリーンの和音・分散和音のギター
    yield "クリーン・分散和音のギター", lambda: unify(P, lambda p: p.get("instrument") == "distGuitar" and ("クリーン" in p["role"] or "分散和音のギター" in p["role"]))
    # 3) リードの重ね（オクターブ）をリードに。ハモリはここではそろえない（2026-10-23）: 同じチャンネル＝同じアンプに
    #   3度のハモリが入ると、歪みの中で2音がぶつかって濁る（人間「高音から下げて音が重なってるときに濁る」）。足りないときだけ最後に
    yield "リードの重ね", lambda: unify(P, lambda p: p.get("instrument") == "distGuitar" and p["role"].startswith("リード") and "ハモリ" not in p["role"])
    # 4) ベースの重ね
    yield "ベースの重ね", lambda: unify(P, lambda p: p.get("instrument") == "bass" and p.get("patch") != "bassMute")
    # 5) 透明感の層の別テイクをやめる
    def no_double():
        ch = False
        for p in P:
            if "透明感の層" in p["role"] and p.get("double"): p.pop("double"); ch = True
        return ch
    yield "透明感の層の別テイク", no_double
    # 6) 技のギターをリードに
    yield "技のギター", lambda: unify(P, lambda p: p.get("instrument") == "distGuitar" and (p["role"].startswith("リード") or p["role"].startswith("技") or "ギター（" in p["role"] and "空気" not in p["role"]) and "ハモリ" not in p["role"])
    # 7) それでも足りなければ、ハモリもリードと同じチャンネルに（濁りやすいので最後の手）
    yield "リードのハモリ（最後の手）", lambda: unify(P, lambda p: p.get("instrument") == "distGuitar" and p["role"].startswith("リード"))


def fit(path):
    song = json.load(open(path))
    done = []
    if not overflow(path): return done
    for name, fn in steps(song):
        if fn():
            json.dump(song, open(path, "w"), ensure_ascii=False); done.append(name)
            if not overflow(path): return done
    left = overflow(path)
    if left: done.append("まだあふれ: " + left[0][:120])
    return done


if __name__ == "__main__":
    print("チャンネルの直し:", ", ".join(fit(sys.argv[1])) or "（あふれなし）")
