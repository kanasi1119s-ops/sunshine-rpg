"""絵の種類（monster / boss / character / field）と、描くものの短い説明から、generate.py の指示ファイルを作る。

使い方:
  python3 tools/pixel-art/ai-gen/make_jobs.py monster jobs.json \
      "golem:an ancient stone golem covered in moss with glowing blue runes" \
      "crab:a giant armored crab monster with huge orange claws and barnacles" [--seeds 2] [--seed-base 2000]
  → jobs.json（1体につき乱数の種を --seeds 個。名前は <名前>_<番号>）
  続けて: MODEL=$(python3 make_jobs.py --model monster) VARIANT=fp16 STYLE=painterly python3 generate.py jobs.json
説明の書き方: 英語で「生き物・人物の種類＋色＋体の特徴＋持ち物」。作品名・ゲーム名・作者名・既存のキャラやモンスターの名前は書かない。
雛形（後ろにつく共通の文・避けるもの・大きさ）は prompts.json。
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "prompts.json")))
BANNED = ["dragon quest", "final fantasy", "pokemon", "zelda", "toriyama", "amano", "nomura", "slime", "chocobo", "moogle", "mario"]

if len(sys.argv) >= 3 and sys.argv[1] == "--model":
    print(P[sys.argv[2]]["model"]); sys.exit(0)
args = [a for a in sys.argv[1:]]
seeds, base = 2, 2000
if "--seeds" in args:
    i = args.index("--seeds"); seeds = int(args[i + 1]); del args[i:i + 2]
if "--seed-base" in args:
    i = args.index("--seed-base"); base = int(args[i + 1]); del args[i:i + 2]
kind, out, items = args[0], args[1], args[2:]
if kind not in P or kind.startswith("_"):
    sys.exit("種類は monster / boss / character / field のどれか")
t = P[kind]
jobs = []
_TOK = None


def tokens(text):
    """CLIPの数え方でのトークン数（77をこえた分はAIに無視される）。数えられないときは単語数で見積もる"""
    global _TOK
    try:
        if _TOK is None:
            from transformers import CLIPTokenizer
            _TOK = CLIPTokenizer.from_pretrained(t["model"], subfolder="tokenizer")
        return len(_TOK(text)["input_ids"])
    except Exception:
        return int(len(text.replace(",", " , ").split()) * 1.25) + 2


for n, item in enumerate(items):
    name, desc = item.split(":", 1)
    low = desc.lower()
    hit = [b for b in BANNED if b in low]
    if hit:
        sys.exit(f"「{name}」の説明に、既存作品につながる言葉があります: {hit}（CLAUDE.md 1-1）。色や体の特徴で言いかえてください")
    prompt = t.get("prefix", "") + desc.strip() + t["suffix"]
    nt = tokens(prompt)
    if nt > 77:
        sys.exit(f"「{name}」の指示文が長すぎます（{nt}トークン、77まで）。後ろの『全身・白い背景』が無視されて体が切れるので、説明を短くしてください")
    for k in range(seeds):
        jobs.append(dict(name=f"{name}_{k}", seed=base + n * 37 + k * 101, steps=t["steps"], cfg=t["cfg"], w=t["w"], h=t["h"],
                         prompt=prompt, neg=t["neg"]))
json.dump(jobs, open(out, "w"), ensure_ascii=False, indent=1)
print(f"{len(jobs)} 枚分の指示を {out} に書きました（{kind}）。変換: {t['convert']}")
