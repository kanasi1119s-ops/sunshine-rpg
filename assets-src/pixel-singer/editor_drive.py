"""ドット絵エディタ（tools/pixel-editor/index.html）をブラウザで開き、マウスのクリックで1ドットずつ打って絵を作る。
使い方: python3 editor_drive.py <絵の設計.py> <出力フォルダ> <名前>
色の一覧だけ入った空の作品を「作品を開く」で読みこみ → パレットの色を選んでキャンバスをクリック → フレームを複製して口と目を描きかえ → 「作品を保存」の文字を受け取る。"""
import json, sys, importlib.util, os
from playwright.sync_api import sync_playwright
spec = importlib.util.spec_from_file_location("art", sys.argv[1]); art = importlib.util.module_from_spec(spec); spec.loader.exec_module(art)
OUT, NAME = sys.argv[2], sys.argv[3]; W, H = art.W, art.H
ED = "file://" + os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools", "pixel-editor", "index.html"))
empty = {"format": "sunshine-pixel", "version": 2, "width": W, "height": H, "symbols": [{"sym": s, "label": l, "color": c} for s, l, c in art.PAL],
         "layers": [{"name": "歌い手", "visible": True, "opacity": 1}], "frames": [{"dur": 400}], "cels": [[["." * W] * H]], "layer": 0, "frame": 0}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1700, "height": 2400}); pg.goto(ED); pg.wait_for_timeout(500)
    pg.keyboard.press("Control+o"); pg.fill("#projText", json.dumps(empty, ensure_ascii=False)); pg.locator("#modalActions").get_by_role("button", name="読み込む").click(); pg.wait_for_timeout(300)
    pg.click('.tool-btn[data-tool="pencil"]')
    pg.uncheck("#symmetry"); pg.uncheck("#showShading")     # 左右対称と陰影プレビューは切る（左右でちがう絵なので）
    print("はじめの設定", pg.evaluate("() => [...document.querySelectorAll('input[type=checkbox]')].filter(e => e.checked).map(e => e.parentElement.textContent.trim().slice(0, 12))"))
    cur = [None]
    def pick(sym):
        if cur[0] != sym:
            i = pg.evaluate("s => [...document.querySelectorAll('#symbolList .sym')].findIndex(e => e.textContent === s)", sym)
            el = pg.locator("#symbolList .sym").nth(i); el.scroll_into_view_if_needed(); el.click(); cur[0] = sym
    def paint(cells):          # cells: {(x, y): 色}。色ごとにまとめて打つ
        by = {}
        for (x, y), s in cells.items(): by.setdefault(s, []).append((x, y))
        for s, pts in by.items():
            pick(s); r = pg.evaluate("() => { const c=document.getElementById('gridCanvas'); c.scrollIntoView({block:'center'}); const r=c.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }")
            for x, y in pts:
                cx, cy = r[0] + (x + .5) * r[2] / W, r[1] + (y + .5) * r[3] / H
                assert pg.evaluate("([x, y]) => document.elementFromPoint(x, y) && document.elementFromPoint(x, y).id === 'gridCanvas'", [cx, cy]), ("キャンバスの外", x, y)
                pg.mouse.click(cx, cy)
    g = art.base(); cells = {(x, y): g[y][x] for y in range(H) for x in range(W) if g[y][x] != "."}; cells.update(art.FRAMES[0][2]); paint(cells)
    for i, (nm, dur, fc) in enumerate(art.FRAMES):
        if i: pg.click("#frameDup"); pg.wait_for_timeout(100); paint(fc)
        pg.fill("#frameDur", str(dur)); pg.dispatch_event("#frameDur", "change")
    pg.screenshot(path=f"{OUT}/{NAME}_エディタの画面.png")
    pg.locator("#menubar").get_by_text("ファイル").click(); pg.locator("#menuPop").get_by_text("作品を保存").click(); pg.wait_for_timeout(200); js = pg.input_value("#projJson"); b.close()
open(f"{OUT}/{NAME}.sunshine-pixel.json", "w", encoding="utf-8").write(js)
d = json.loads(js); print("フレーム", len(d["frames"]), [f["dur"] for f in d["frames"]], "色", len(d["symbols"]))
# エディタが返した作品が設計どおりかを照らし合わせる
bad = 0
for i, (nm, dur, fc) in enumerate(art.FRAMES):
    want = [r[:] for r in g]
    for (x, y), s in {**art.FRAMES[0][2], **fc}.items(): want[y][x] = s
    for y in range(H):
        for x in range(W):
            if d["cels"][0][i][y][x] != want[y][x]: bad += 1
print("設計とちがうマス", bad)
