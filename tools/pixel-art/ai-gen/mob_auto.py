"""雑魚の敵（200種）を、人の手を待たずに順番に作りつづける（2026-10-05、人間の指示「雑魚敵も200種類全部違うのでお願いします。時間はいくらかかってもいいです」）。

手順は monster.md と同じ「AIの下絵 → ドット絵化 → 手直し → エディタで描く」。このうち手直し以外を自動で行い、
手直し（目を光らせる・形を整える）は、まとめて見た人（Claude）があとで足す。

使い方（リポジトリの最上位で。とても長くかかるので nohup で裏で動かす）:
  nohup python3 tools/pixel-art/ai-gen/mob_auto.py [--batch 3] [--limit 999] > /tmp/monster-work/mob_auto.log 2>&1 &
1回分（--batch 体）ごとに:
  1. 下絵を2枚ずつ描く（monster_batch.py draft。1枚 約5分）
  2. 全身が入っていて額縁でない下絵を選ぶ。切れていたら外側を描き足す（extend）。どれもだめなら、種を変えてもう一度
  3. ドット絵化（96×96・20色）→ ドット絵エディタで描く（editor-draw.mjs --import、食い違い0マスを確かめる）→ final → done
  4. 書き出し（monster_batch.py export → export-game-data.mjs）と、見比べの一覧画像（WORK/auto/batch-*.png）
画像生成とブラウザ（エディタ）は同時に動かさない（メモリが足りなくなる）。この道具は1つずつ順番に動かす。
止めるときは、WORK/auto/STOP というファイルを置く（1回分が終わったところで止まる）。
"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
AI = os.path.join(ROOT, "tools", "pixel-art", "ai-gen")
ART = os.path.join(ROOT, "assets-src", "monsters")
WORK = os.environ.get("WORK", "/tmp/monster-work")
AUTO = os.path.join(WORK, "auto")
ROSTER = os.path.join(AI, "monster-roster.json")


def log(*a):
    print(time.strftime("%m-%d %H:%M"), *a, flush=True)


def run(cmd, env=None, timeout=None):
    r = subprocess.run(cmd, cwd=ROOT, env=dict(os.environ, **(env or {})), capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        log("失敗:", " ".join(cmd[:4]), (r.stderr or r.stdout)[-400:])
    return r.returncode == 0


def roster():
    return json.load(open(ROSTER))


def check(i, k):
    p = f"{WORK}/raw/{i}_{k}.png.check.json"
    return json.load(open(p)) if os.path.exists(p) else None


def choose(i, seeds):
    """全身が入っていて額縁でない下絵の番号。無ければ、切れた下絵を描き足して使う。だめなら None"""
    cands = []
    for k in range(seeds):
        c = check(i, k)
        if c is None:
            continue
        if c.get("ok") and not c.get("framed"):
            return str(k)
        if not c.get("framed") and c.get("parts", 0) >= 0.85:
            cands.append((len(c.get("cut", [])), k))
    for _, k in sorted(cands)[:1]:
        if run(["python3", f"{AI}/monster_batch.py", "extend", i, str(k)], timeout=1500):
            c = check(i, f"x{k}")
            if c and c.get("ok") and not c.get("framed"):
                return f"x{k}"
    return None


def editor_stage(i):
    d = f"{ART}/{i}"
    out = f"{WORK}/auto/ed_{i}.png"
    ok = run(["node", "tools/pixel-practice/editor-draw.mjs", f"{d}/{i}.txt", f"{d}/{i}.json", out, "--zoom", "8", "--import"], timeout=900)
    if not ok or not os.path.exists(out + ".rows.txt"):
        return False
    a = [r for r in open(f"{d}/{i}.txt").read().split("\n") if r.strip()]
    b = [r for r in open(out + ".rows.txt").read().split("\n") if r.strip()]
    bad = sum(1 for y in range(len(a)) for x in range(len(a[y])) if y >= len(b) or x >= len(b[y]) or a[y][x] != b[y][x])
    if bad:
        log(i, "エディタの食い違い", bad)
        return False
    for ext in ("txt", "json"):
        open(f"{d}/final.{ext}", "w").write(open(f"{d}/{i}.{ext}").read())
    os.replace(out, f"{d}/final-editor.png")
    return run(["python3", f"{AI}/monster_batch.py", "done", i])


def sheet(ids, path):
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 14)
    names = {e["id"]: e["name"] for e in roster()}
    s = Image.new("RGB", (len(ids) * 200, 220), (40, 36, 52))
    for n, i in enumerate(ids):
        p = f"{ART}/{i}/{i}.png"
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA"); bg = Image.new("RGBA", im.size, (40, 36, 52, 255)); bg.alpha_composite(im)
            s.paste(bg.convert("RGB").resize((192, 192), Image.NEAREST), (n * 200 + 4, 24))
        ImageDraw.Draw(s).text((n * 200 + 4, 2), f"{names.get(i, i)}", font=f, fill=(255, 220, 120))
    s.save(path)


def main():
    a = sys.argv[1:]
    batch = int(a[a.index("--batch") + 1]) if "--batch" in a else 3
    limit = int(a[a.index("--limit") + 1]) if "--limit" in a else 999
    os.makedirs(AUTO, exist_ok=True)
    tries = {}
    made = 0
    n_batch = 0
    while made < limit:
        if os.path.exists(f"{AUTO}/STOP"):
            log("STOP があるので止まります"); break
        mobs = [e for e in roster() if e.get("kind") != "boss" and e.get("prompt")]
        # ドット絵化まで済んでエディタで止まったものは、エディタからやり直す
        for e in [e for e in mobs if e.get("status") == "picked" and tries.get("ed:" + e["id"], 0) < 2]:
            tries["ed:" + e["id"]] = tries.get("ed:" + e["id"], 0) + 1
            if editor_stage(e["id"]):
                made += 1; log(e["id"], "できた（エディタのやり直し）")
                open(f"{AUTO}/done.txt", "a").write(e["id"] + "\n")
        todo = [e for e in mobs if e.get("status") in ("todo", "draft") and tries.get(e["id"], 0) < 3]
        if not todo:
            log("作る敵が残っていません"); break
        ids = [e["id"] for e in todo[:batch]]
        n_batch += 1
        seed_base = str(2000 + 997 * max(tries.get(i, 0) for i in ids))
        log(f"[{n_batch}] 下絵:", ids, "種", seed_base)
        if not run(["python3", f"{AI}/monster_batch.py", "draft", *ids, "--seeds", "2"], env={"SEED_BASE": seed_base}, timeout=7200):
            for i in ids: tries[i] = tries.get(i, 0) + 1
            continue
        finished = []
        for i in ids:
            tries[i] = tries.get(i, 0) + 1
            k = choose(i, 2)
            if k is None:
                log(i, "使える下絵が無い（もう一度、別の種で）"); continue
            if not run(["python3", f"{AI}/monster_batch.py", "pick", i, k], timeout=900):
                continue
            if editor_stage(i):
                finished.append(i); made += 1
                log(i, "できた（下絵", k, "）")
        if finished:
            run(["python3", f"{AI}/monster_batch.py", "export"]); run(["node", "tools/pixel-art/export-game-data.mjs"], timeout=900)
            sheet(finished, f"{AUTO}/batch-{n_batch:03d}.png")
            open(f"{AUTO}/done.txt", "a").write("\n".join(finished) + "\n")
    log("おわり。できた数:", made)


if __name__ == "__main__":
    main()
