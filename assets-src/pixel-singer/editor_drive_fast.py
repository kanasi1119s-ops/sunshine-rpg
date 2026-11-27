"""ドット絵エディタ（tools/pixel-editor/index.html）を開いて、エディタのえんぴつで絵を打つ（コマ数の多い絵のため、速い版）。
editor_drive.py との違い: マウスの操作を1回ずつ送るのではなく、エディタのキャンバスに「マウスを押す → 横に動かす → はなす」の操作をページの中でまとめて送る（エディタのえんぴつの処理がそのまま動く）。
同じ色が横に続く所は、ひと筆で引く。コマは「複製」ボタンで増やし、前のコマとちがう所だけ打つ。localStorage への自動保存は止める（コマが多いと1筆ごとに全部を保存して遅くなるため）。
使い方: python3 editor_drive_fast.py <フレームの JSON（[[行,...],...]）> <パレット JSON（{記号: "#rrggbb"}）> <コマの長さ ms> <出力フォルダ> <名前>"""
import json, sys, os, time
from playwright.sync_api import sync_playwright
FR = json.load(open(sys.argv[1])); PALD = json.load(open(sys.argv[2])); DUR = int(sys.argv[3]); OUT, NAME = sys.argv[4], sys.argv[5]
W, H = len(FR[0][0]), len(FR[0])
ED = "file://" + os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools", "pixel-editor", "index.html"))
syms = [{"sym": k, "label": "色%02d" % (i + 1), "color": v} for i, (k, v) in enumerate(PALD.items())]
empty = {"format": "sunshine-pixel", "version": 2, "width": W, "height": H, "symbols": syms,
         "layers": [{"name": "ダンス", "visible": True, "opacity": 1}], "frames": [{"dur": DUR}], "cels": [[["." * W] * H]], "layer": 0, "frame": 0}
def runs(prev, cur):
    out = []
    for y, (ra, rb) in enumerate(zip(prev, cur)):
        x = 0
        while x < W:
            if ra[x] != rb[x]:
                s = x; c = rb[x]
                while x < W and ra[x] != rb[x] and rb[x] == c: x += 1
                out.append((c, y, s, x - 1))
            else: x += 1
    out.sort(key=lambda r: r[0]); return out
JS = """([runs]) => {
  const cv = document.getElementById('gridCanvas'); const R = cv.getBoundingClientRect();
  const W = %d, H = %d; const cw = R.width / W, ch = R.height / H;
  const symEls = [...document.querySelectorAll('#symbolList .sym')];
  let cur = null;
  const fire = (el, type, x, y) => el.dispatchEvent(new MouseEvent(type, {bubbles: true, cancelable: true, clientX: x, clientY: y, button: 0}));
  for (const [c, y, x0, x1] of runs) {
    if (c !== cur) { const el = c === '.' ? symEls[0] : symEls.find(e => e.textContent === c); el.click(); cur = c; }
    const cy = R.top + (y + 0.5) * ch;
    fire(cv, 'mousedown', R.left + (x0 + 0.5) * cw, cy);
    if (x1 > x0) fire(window, 'mousemove', R.left + (x1 + 0.5) * cw, cy);
    fire(window, 'mouseup', R.left + (x1 + 0.5) * cw, cy);
  }
  return runs.length;
}""" % (W, H)
t0 = time.time()
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1400, "height": 1400})
    ctx.add_init_script("Storage.prototype.setItem = function () {};")          # 自動保存を止める
    pg = ctx.new_page(); pg.goto(ED); pg.wait_for_timeout(500)
    pg.keyboard.press("Control+o"); pg.fill("#projText", json.dumps(empty, ensure_ascii=False)); pg.locator("#modalActions").get_by_role("button", name="読み込む").click(); pg.wait_for_timeout(300)
    pg.click('.tool-btn[data-tool="pencil"]'); pg.uncheck("#symmetry"); pg.uncheck("#showShading")
    pg.evaluate("() => { const e = document.getElementById('zoom'); e.value = 3; e.dispatchEvent(new Event('input', { bubbles: true })); }")
    for name in ("#pixelPerfect",):
        if pg.locator(name).count(): pg.uncheck(name)
    prev = ["." * W] * H; n = 0
    for i, g in enumerate(FR):
        if i: pg.click("#frameDup")
        rs = runs(prev, g); n += len(rs)
        for k in range(0, len(rs), 4000): pg.evaluate(JS, [rs[k:k + 4000]])
        prev = g
        if i % 10 == 0: print(f"  {i + 1}/{len(FR)} コマ  {n} 筆  {time.time() - t0:.0f}秒", flush=True)
    pg.evaluate("d => { document.querySelectorAll('#frameDur').forEach(e => { e.value = d; e.dispatchEvent(new Event('change', {bubbles: true})); }); }", DUR)
    pg.screenshot(path=f"{OUT}/{NAME}_エディタの画面.png")
    pg.locator("#menubar").get_by_text("ファイル").click(); pg.locator("#menuPop").get_by_text("作品を保存").click(); pg.wait_for_timeout(300); js = pg.input_value("#projJson"); b.close()
open(f"{OUT}/{NAME}.sunshine-pixel.json", "w", encoding="utf-8").write(js)
d = json.loads(js); print("フレーム", len(d["frames"]), "色", len(d["symbols"]), f"{time.time() - t0:.0f}秒")
bad = sum(1 for i, g in enumerate(FR) for y in range(H) for x in range(W) if d["cels"][0][i][y][x] != g[y][x])
print("設計とちがうマス", bad)
