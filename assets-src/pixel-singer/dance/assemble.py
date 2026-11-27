"""エディタで打った形（192種類）を、1000コマの並びにまとめ、エディタで開いて保存しなおす。"""
import json, glob, os
from playwright.sync_api import sync_playwright
U = json.load(open('/tmp/px5/uniq.json')); order = json.load(open('/tmp/px5/order.json'))
painted = []
for f in sorted(glob.glob('/tmp/px5/ed/chunk*.sunshine-pixel.json')):
    d = json.load(open(f)); painted += [["".join(r) for r in g] for g in d['cels'][0]]; base = d
assert len(painted) == len(U) and all(a == b for a, b in zip(painted, U)), "エディタで打った形が設計とちがう"
proj = dict(base); proj['frames'] = [{"dur": 42} for _ in order]; proj['cels'] = [[painted[i] for i in order]]; proj['frame'] = 0
proj['layers'] = [{"name": "ダンス", "visible": True, "opacity": 1}]
ED = "file:///home/claude/wt-mix/tools/pixel-editor/index.html"
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1400, "height": 1400}); ctx.add_init_script("Storage.prototype.setItem = function () {};")
    pg = ctx.new_page(); pg.goto(ED); pg.wait_for_timeout(500)
    pg.keyboard.press("Control+o"); pg.fill("#projText", json.dumps(proj, ensure_ascii=False)); pg.locator("#modalActions").get_by_role("button", name="読み込む").click(); pg.wait_for_timeout(1500)
    pg.screenshot(path="/tmp/px5/ed/assembled_editor.png")
    pg.locator("#menubar").get_by_text("ファイル").click(); pg.locator("#menuPop").get_by_text("作品を保存").click(); pg.wait_for_timeout(1000); js = pg.input_value("#projJson"); b.close()
d = json.loads(js); print("エディタのフレーム", len(d['frames']))
bad = sum(1 for i, k in enumerate(order) for y, r in enumerate(d['cels'][0][i]) for x, ch in enumerate(r) if ch != U[k][y][x])
print("設計とちがうマス", bad)
json.dump(d, open('/tmp/px5/ed/dance1000.sunshine-pixel.json', 'w'), ensure_ascii=False)
