"""ゲームの敵ぜんぶ（ボス24体・雑魚200種）の絵を、少しずつ作るための道具（2026-10-04、人間の指示「すべての敵キャラを生成」）。

手順は make-art の monster.md と同じ「AIの下絵 → ドット絵化 → 手直し → エディタで描く」。顔は右向き（戦闘画面では敵が左、味方が右）、全身が入る構図。
名簿: tools/pixel-art/ai-gen/monster-roster.json（id・名前・種類・地方・英語の指示文 prompt・状態 status）。
  status: todo（未着手）→ draft（下絵あり）→ picked（ドット絵化した）→ done（手直しとエディタの確認まで済み）

使い方（リポジトリの最上位で）:
  python3 tools/pixel-art/ai-gen/monster_batch.py roster            名簿を作る・ゲームの敵の増減を反映する（状態は残す）
  python3 tools/pixel-art/ai-gen/monster_batch.py next 4            次に作る4体（prompt が空なら、先に英語の指示文を名簿に書く）
  python3 tools/pixel-art/ai-gen/monster_batch.py draft ID...       下絵を3枚ずつ描く → 作業フォルダ/draft-<ID>.png（見比べ用）
  python3 tools/pixel-art/ai-gen/monster_batch.py pick ID 番号 [--mirror]   選んだ下絵をドット絵に（左向きなら --mirror で右向きに）
       → assets-src/monsters/<ID>/<ID>.{txt,json,png}。手直しは edits.py、エディタは editor-draw.mjs で行い、
         仕上げた絵を assets-src/monsters/<ID>/final.{txt,json} に置く
  python3 tools/pixel-art/ai-gen/monster_batch.py done ID           仕上げの確認（大きさ・色数）をして done にする
  python3 tools/pixel-art/ai-gen/monster_batch.py export            done の絵を tools/pixel-art/enemy-art.json に（export-game-data.mjs が読む）
作業フォルダは環境変数 WORK（既定は /tmp/monster-work）。
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
AI = f"{ROOT}/tools/pixel-art/ai-gen"
ROSTER = f"{AI}/monster-roster.json"
ART = f"{ROOT}/assets-src/monsters"
WORK = os.environ.get("WORK", "/tmp/monster-work")
NAMES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ボス24体（id・名前・どんな相手か）。絵の設定は docs/story/ と各章の敵データに合わせる
BOSSES = [
    ("chapter0-yugami", "灯里の歪み", "序章"), ("mugikano-yugami", "水涸れの歪み", "1章"), ("garasuko-yugami", "積荷の歪み", "2章"),
    ("tetsukusari-yugami", "実験の歪み", "3章"), ("sanone-yugami", "砂嵐の歪み", "4章"), ("kiri-yugami", "予言の歪み", "5章"),
    ("shimohara-yugami", "試作機の歪み", "6章"), ("fushima-yugami", "浮嶼の歪み", "7章"), ("toushin-yugami", "灯芯都の歪み", "8章"),
    ("kyotoukyu-yugami", "虚灯宮の歪み", "9章"), ("deep-yugami", "初源の歪み", "10章"), ("deep3-yugami", "深部3層の歪み", "10章"),
    ("god-1", "恵みの残照（女神）", "8神"), ("god-2", "理不尽の羽音（蟲神）", "8神"), ("god-3", "坩堝の顎（鬼神）", "8神"),
    ("god-4", "在らざる歌（無神）", "8神"), ("god-5", "透き徹る誓い（純神）", "8神"), ("god-6", "不敗の咎人（武神）", "8神"),
    ("god-7", "境界を見ぬ者（異神）", "8神"), ("god-8", "無音の弔鐘（冥神）", "8神"),
    ("tower2-guard", "塔の守り（2層）", "芯環塔"), ("kanou3-guard", "塔の守り（3層）", "環奥"), ("tower3-guard", "灯りの番人", "芯環塔"),
    ("zenkan", "全観", "環奥の最後"),
]


def load():
    return json.load(open(ROSTER)) if os.path.exists(ROSTER) else []


def save(r):
    json.dump(r, open(ROSTER, "w"), ensure_ascii=False, indent=1)


def zones():
    js = ("import {ENCOUNTER_ZONES as A, WORLD_ENCOUNTER_ZONES as B} from './src/game/encounter/encounter.ts';"
          "console.log(JSON.stringify({...A,...B}))")
    out = subprocess.run(["npx", "tsx", "-e", js], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return json.loads(out.strip().splitlines()[-1])


def cmd_roster():
    old = {e["id"]: e for e in load()}
    out = []
    for zid, z in zones().items():
        for i, n in enumerate(z["names"]):
            eid = f"enc-{zid}-{i}"
            e = old.get(eid, {"id": eid, "prompt": "", "status": "todo"})
            e.update({"key": f"enemy:{eid}", "kind": "mob", "name": n, "zone": zid, "level": z["level"]})
            out.append(e)
    for bid, n, where in BOSSES:
        e = old.get(bid, {"id": bid, "prompt": "", "status": "todo"})
        e.update({"key": f"boss:{bid}", "kind": "boss", "name": n, "zone": where})
        out.append(e)
    save(out)
    from collections import Counter
    print("名簿:", len(out), "件", dict(Counter(e["status"] for e in out)))


def cmd_next(n):
    for e in [e for e in load() if e["status"] == "todo"][:int(n)]:
        print(e["id"], e["kind"], e["name"], e.get("zone"), "| prompt:", e["prompt"] or "（未記入。英語で書く）")


def cmd_draft(ids):
    r = load(); by = {e["id"]: e for e in r}
    os.makedirs(f"{WORK}/raw", exist_ok=True)
    jobs = []
    for i in ids:
        e = by[i]
        assert e["prompt"], f"{i}: 名簿の prompt（英語の指示文）を先に書く"
        kind = "boss" if e["kind"] == "boss" else "monster"
        subprocess.run(["python3", f"{AI}/make_jobs.py", kind, f"{WORK}/j.json", f"{i}:{e['prompt']}, side view facing right, whole body in frame", "--seeds", "3"], check=True, cwd=WORK)
        jobs += json.load(open(f"{WORK}/j.json"))
    json.dump(jobs, open(f"{WORK}/jobs.json", "w"))
    env = dict(os.environ, MODEL="stable-diffusion-v1-5/stable-diffusion-v1-5", VARIANT="fp16", STYLE="painterly")
    subprocess.run(["python3", f"{AI}/generate.py", "jobs.json"], cwd=WORK, env=env, check=True)
    from PIL import Image, ImageDraw
    for i in ids:
        sheet = Image.new("RGB", (3 * 260, 260), "white"); d = ImageDraw.Draw(sheet)
        for k in range(3):
            p = f"{WORK}/raw/{i}_{k}.png"
            if os.path.exists(p):
                sheet.paste(Image.open(p).resize((256, 256)), (k * 260, 0)); d.text((k * 260 + 4, 4), str(k), fill="red")
        sheet.save(f"{WORK}/draft-{i}.png"); by[i]["status"] = "draft"
        print("見比べ:", f"{WORK}/draft-{i}.png")
    save(r)


def cmd_pick(i, k, mirror=False):
    r = load(); by = {e["id"]: e for e in r}; e = by[i]
    size, ncol = (128, 24) if e["kind"] == "boss" else (96, 20)
    d = f"{ART}/{i}"; os.makedirs(d, exist_ok=True)
    subprocess.run(["python3", f"{AI}/sfcize.py", f"{WORK}/raw/{i}_{k}.png", f"{d}/{i}", str(size), str(ncol)], check=True, cwd=WORK)
    if mirror:
        rows = open(f"{d}/{i}.txt").read().split()
        open(f"{d}/{i}.txt", "w").write("\n".join(row[::-1] for row in rows) + "\n")
        from PIL import Image, ImageOps
        ImageOps.mirror(Image.open(f"{d}/{i}.png")).save(f"{d}/{i}.png")
    e["status"] = "picked"; e["draft"] = f"{i}_{k}{' mirror' if mirror else ''}"
    save(r)
    print("ドット絵:", f"{d}/{i}.png", "→ 手直し（edits.py）とエディタの確認のあと final.txt / final.json に")


def cmd_done(i):
    r = load(); by = {e["id"]: e for e in r}; e = by[i]
    rows = open(f"{ART}/{i}/final.txt").read().split()
    pal = json.load(open(f"{ART}/{i}/final.json"))
    size = 128 if e["kind"] == "boss" else 96
    assert len(rows) == size and all(len(x) == size for x in rows), f"{i}: {size}×{size} にする"
    assert len(pal) <= 26, f"{i}: 26色以内にする"
    e["status"] = "done"; save(r); print(i, "done")


def encode(rows, symbols):
    s, prev, n = "", None, 0
    for row in rows:
        for ch in row:
            c = "_" if ch == "." else NAMES[symbols.index(ch)]
            if c == prev:
                n += 1
            else:
                if prev is not None:
                    s += prev + (base36(n) if n > 1 else "")
                prev, n = c, 1
    s += prev + (base36(n) if n > 1 else "")
    return s


def base36(n):
    d = "0123456789abcdefghijklmnopqrstuvwxyz"; s = ""
    while n:
        s = d[n % 36] + s; n //= 36
    return s


def cmd_export():
    out = {}
    for e in load():
        if e["status"] != "done":
            continue
        rows = open(f"{ART}/{e['id']}/final.txt").read().split()
        pal = json.load(open(f"{ART}/{e['id']}/final.json"))
        if e["kind"] == "boss":                                   # 128 → 256（1ドット＝2×2）
            rows = ["".join(ch * 2 for ch in r) for r in rows for _ in range(2)]
        syms = sorted(pal)
        out[e["key"]] = {"size": len(rows), "palette": [pal[s] for s in syms], "rle": encode(rows, syms)}
    json.dump(out, open(f"{ROOT}/tools/pixel-art/enemy-art.json", "w"))
    print("書き出し:", len(out), "体 → node tools/pixel-art/export-game-data.mjs")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit()
    c = a[0]
    if c == "roster": cmd_roster()
    elif c == "next": cmd_next(a[1] if len(a) > 1 else 4)
    elif c == "draft": cmd_draft(a[1:])
    elif c == "pick": cmd_pick(a[1], a[2], "--mirror" in a)
    elif c == "done": cmd_done(a[1])
    elif c == "export": cmd_export()
