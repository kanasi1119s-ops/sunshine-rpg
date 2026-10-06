"""ゲームの敵ぜんぶ（ボス24体・雑魚200種）の絵を、少しずつ作るための道具（2026-10-04、人間の指示「すべての敵キャラを生成」）。

手順は make-art の monster.md と同じ「AIの下絵 → ドット絵化 → 手直し → エディタで描く」。顔は右向き（戦闘画面では敵が左、味方が右）、全身が入る構図。
名簿: tools/pixel-art/ai-gen/monster-roster.json（id・名前・種類・地方・英語の指示文 prompt・状態 status）。
  全身が入るように、名簿に shape（形: ground / float / tall / long / winged / big。layouts.py）と tone（体のおおまかな色 [r,g,b]）も書く。
  下絵は、白い背景のまん中に置いた影絵から描く（img2img）ので、体が端で切れにくい。描いたあと fullbody.py で全身が入っているかを調べる。
  status: todo（未着手）→ draft（下絵あり）→ picked（ドット絵化した）→ done（手直しとエディタの確認まで済み）

使い方（リポジトリの最上位で）:
  python3 tools/pixel-art/ai-gen/monster_batch.py roster            名簿を作る・ゲームの敵の増減を反映する（状態は残す）
  python3 tools/pixel-art/ai-gen/monster_batch.py next 4            次に作る4体（prompt が空なら、先に英語の指示文を名簿に書く）
  python3 tools/pixel-art/ai-gen/monster_batch.py draft ID... [--seeds 4]   下絵を4枚ずつ描き、全身が入っているかを調べる（fullbody.py）
       → 作業フォルダ/draft-<ID>.png（見比べ用。各下絵の上に「全身OK」か「切れ:上下」などが出る）
  python3 tools/pixel-art/ai-gen/monster_batch.py extend ID 番号      端で切れた下絵の外側を描き足す → 番号 x<番号>（例: x2）として選べる
  python3 tools/pixel-art/ai-gen/monster_batch.py pick ID 番号 [--mirror] [--force]   選んだ下絵をドット絵に（左向きなら --mirror で右向きに）
       全身が入っていない下絵は選べない（人間の指示「全身が入るように」。どうしても使うときだけ --force）
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
# ボスは 256×256 で直接作る（人間の指示「リアルなドット絵のボス256×256にしてみよう」2026-10-04）。
# 以前は 128×128・24色で作って2倍に拡大していた。256 では細かさを活かすため40色（ゲームの絵は27色以上も扱える）
BOSS_SIZE, BOSS_COLORS = 256, 40

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


def font(size=18):
    from PIL import ImageFont
    for f in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc", "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
              "/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf", "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def make_sheet(i):
    """見比べ用の1枚。下絵ごとに番号と、全身チェックの結果（緑＝全身OK、赤＝切れ など）を書く"""
    from PIL import Image, ImageDraw
    sys.path.insert(0, AI)
    from fullbody import label
    names = sorted(f[len(i) + 1:-4] for f in os.listdir(f"{WORK}/raw") if f.startswith(i + "_") and f.endswith(".png") and not f.endswith(".layout.png"))
    sheet = Image.new("RGB", (max(1, len(names)) * 260, 290), "white"); d = ImageDraw.Draw(sheet); fnt = font()
    for n, k in enumerate(names):
        p = f"{WORK}/raw/{i}_{k}.png"
        sheet.paste(Image.open(p).convert("RGB").resize((256, 256)), (n * 260, 0))
        res = json.load(open(p + ".check.json")) if os.path.exists(p + ".check.json") else None
        txt = f"{k}  " + (label(res) if res else "未チェック")
        d.text((n * 260 + 4, 262), txt, fill=(0, 130, 0) if res and res["ok"] else (200, 0, 0), font=fnt)
    sheet.save(f"{WORK}/draft-{i}.png")
    return f"{WORK}/draft-{i}.png"


def run_check(paths):
    # 生成（generate.py）が終わってから、別のプロセスで調べる（同時に動かすとメモリが足りない）
    subprocess.run(["python3", f"{AI}/fullbody.py", "check", *paths], cwd=AI, check=True)


def cmd_draft(ids, seeds=4):
    r = load(); by = {e["id"]: e for e in r}
    os.makedirs(f"{WORK}/raw", exist_ok=True)
    jobs = []
    for i in ids:
        e = by[i]
        assert e["prompt"], f"{i}: 名簿の prompt（英語の指示文）を先に書く"
        kind = "boss" if e["kind"] == "boss" else "monster"
        desc = e["prompt"] if "facing right" in e["prompt"] else e["prompt"] + ", facing right"
        extra = ["--seed-base", os.environ["SEED_BASE"]] if os.environ.get("SEED_BASE") else []   # 描き直すときは別の種で
        subprocess.run(["python3", f"{AI}/make_jobs.py", kind, f"{WORK}/j.json", f"{i}:{desc}", "--seeds", str(seeds)] + extra, check=True, cwd=WORK)
        js = json.load(open(f"{WORK}/j.json"))
        # 置き場所の下書き（layouts.py）から描く: 名簿の shape（形）と tone（体のおおまかな色）を使う
        for j in js:
            for w in e.get("neg_drop", []):   # その敵だけ避けなくてよい言葉（天使・悪魔は人の形でよい）
                j["neg"] = j["neg"].replace(", " + w, "").replace(w + ", ", "")
            if e.get("neg_extra"):   # その敵だけ避けたいもの（例: 全環は「指輪」になりやすい）
                j["neg"] = e["neg_extra"] + ", " + j["neg"]
            j["layout"] = {"shape": e.get("shape") or ("big" if e["kind"] == "boss" else "ground"),
                           "tone": e.get("tone") or [110, 100, 95], "strength": e.get("strength", 0.9)}
            if e.get("bg") == "dark":   # 光る・白い敵: 暗い背景で描く（rembg で切り抜くので背景の色は問わない。2026-10-05）
                j["prompt"] = j["prompt"].replace("plain white background", "plain dark charcoal background")
                j["layout"]["bg"] = [34, 32, 38]
        jobs += js
    json.dump(jobs, open(f"{WORK}/jobs.json", "w"))
    env = dict(os.environ, MODEL="stable-diffusion-v1-5/stable-diffusion-v1-5", VARIANT="fp16", STYLE="painterly", QUALITY=os.environ.get("QUALITY", "real"))  # リアルな下絵（1枚 約5分）
    subprocess.run(["python3", f"{AI}/generate.py", "jobs.json"], cwd=WORK, env=env, check=True)
    run_check([f"{WORK}/raw/{j['name']}.png" for j in jobs])
    for i in ids:
        by[i]["status"] = "draft"
        print("見比べ:", make_sheet(i))
    save(r)


def cmd_extend(i, k):
    """端で切れた下絵の外側を描き足して、x<番号> として足す"""
    e = {x["id"]: x for x in load()}[i]
    src, dst = f"{WORK}/raw/{i}_{k}.png", f"{WORK}/raw/{i}_x{k}.png"
    subprocess.run(["python3", f"{AI}/fullbody.py", "extend", src, dst, e["prompt"]], cwd=AI, check=True)
    run_check([dst])
    print("見比べ:", make_sheet(i))


def cmd_pick(i, k, mirror=False, force=False):
    r = load(); by = {e["id"]: e for e in r}; e = by[i]
    chk = f"{WORK}/raw/{i}_{k}.png.check.json"
    if not force:
        if not os.path.exists(chk):
            run_check([f"{WORK}/raw/{i}_{k}.png"])
        res = json.load(open(chk))
        if not res["ok"]:
            sys.exit(f"{i}_{k}: 全身が入っていません（{res.get('cut')}・かたまり{res.get('parts')}）。ほかの下絵を選ぶか、extend で描き足す（どうしても使うときは --force）")
    size, ncol = (BOSS_SIZE, BOSS_COLORS) if e["kind"] == "boss" else (e.get("size", 96), e.get("ncol", 20))
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
    sizes = (BOSS_SIZE, 128) if e["kind"] == "boss" else (e.get("size", 96),)
    assert len(rows) in sizes and all(len(x) == len(rows) for x in rows), f"{i}: {sizes[0]}×{sizes[0]} にする"
    limit = 62 if e["kind"] == "boss" or e.get("size", 96) >= 256 else 26
    assert len(pal) <= limit, f"{i}: {limit}色以内にする"
    e["status"] = "done"; save(r); print(i, "done")


def encode(rows, symbols):
    if len(symbols) > 26:
        # 27色以上: 「色番号:続く数」をカンマでつなぎ、先頭に「~」（export-game-data.mjs と同じ形。透明は -1）
        toks, prev, n = [], None, 0
        for row in rows:
            for ch in row:
                v = -1 if ch == "." else symbols.index(ch)
                if v == prev:
                    n += 1
                else:
                    if prev is not None:
                        toks.append(f"{prev}:{n}")
                    prev, n = v, 1
        toks.append(f"{prev}:{n}")
        return "~" + ",".join(toks)
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
        if e["status"] != "done" or e["kind"] == "extra":   # extra: ゲームにまだ組み込まない絵（天使・悪魔など）
            continue
        rows = open(f"{ART}/{e['id']}/final.txt").read().split()
        pal = json.load(open(f"{ART}/{e['id']}/final.json"))
        if e["kind"] == "boss" and len(rows) == 128:              # 以前の 128 で作ったボスは 256 に拡大（1ドット＝2×2）
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
    elif c == "draft":
        n = int(a[a.index("--seeds") + 1]) if "--seeds" in a else 4
        cmd_draft([x for j, x in enumerate(a[1:], 1) if not x.startswith("--") and (j < 2 or a[j - 1] != "--seeds")], n)
    elif c == "extend": cmd_extend(a[1], a[2])
    elif c == "pick": cmd_pick(a[1], a[2], "--mirror" in a, "--force" in a)
    elif c == "done": cmd_done(a[1])
    elif c == "export": cmd_export()
