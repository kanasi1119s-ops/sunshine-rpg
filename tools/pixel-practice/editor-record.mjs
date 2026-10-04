// ドット絵エディタ（tools/pixel-editor/index.html）で、1枚の絵を作っていく様子を動画にする（2026-10-04、人間の依頼「エディタでの製作動画」）。
// 使い方: node editor-record.mjs <仕上げ前の絵.txt> <パレット.json> <手直し.json> <出力.mp4> [--ref 下絵.png] [--title "名前"] [--anim 動き.json] [--bgm 曲.mp3]
//   --anim: boss_anim.py が作った歩く・攻撃のコマ。エディタのフレームに1コマずつ入れ、タイムラインで再生して見せる
//   --bgm: 動画に曲を入れる（動画の長さで切り、最後の3秒で小さくしていく）
//   仕上げ前の絵: ドット絵化（sfcize.py）した文字グリッド。色を暗い順に1色ずつ、エディタの「貼り付けて読み込む」で置いていく
//   手直し.json: {"palette": {"y": "#rrggbb"}, "strokes": [[行0, 列0, 行1, 列1, "記号"], ...]}
//     新しいレイヤー「手直し」に、ペン（太さ1）でマウスを動かして実際に描く
//   --ref: AIの下絵を「下絵（トレース用）」として薄く重ねる
// 出力: 動画（MP4）と、<出力>.rows.txt（最後にエディタが書き出した配列。仕上げた絵と同じか確かめる）
// 必要なもの: playwright-core（npm install --no-save playwright-core）、ffmpeg、/opt/pw-browsers/chromium
import { chromium } from "playwright-core";
import { fileURLToPath } from "url";
import fs from "fs";
import path from "path";
import { execFileSync } from "child_process";

const [txt, palPath, editPath, out, ...rest] = process.argv.slice(2);
const opt = (k, d) => (rest.includes(k) ? rest[rest.indexOf(k) + 1] : d);
const ref = opt("--ref", null), title = opt("--title", ""), animPath = opt("--anim", null), bgm = opt("--bgm", null);
const rows = fs.readFileSync(txt, "utf8").split("\n").filter((l) => l.trim());
const pal = JSON.parse(fs.readFileSync(palPath, "utf8"));
const edit = JSON.parse(fs.readFileSync(editPath, "utf8"));
const H = rows.length, W = rows[0].length;
const allPal = { ...pal, ...(edit.palette || {}) };
const syms = Object.keys(allPal);
const lum = (h) => { const v = parseInt(h.slice(1), 16); return 0.299 * (v >> 16) + 0.587 * ((v >> 8) & 255) + 0.114 * (v & 255); };
const baseSyms = Object.keys(pal).sort((a, b) => lum(pal[a]) - lum(pal[b]));   // 暗い色から

const editor = process.env.EDITOR || fileURLToPath(new URL("../pixel-editor/index.html", import.meta.url));
const vdir = fs.mkdtempSync("/tmp/editor-video-");
const VW = 1600, VH = 1000;
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await browser.newContext({ viewport: { width: VW, height: VH }, recordVideo: { dir: vdir, size: { width: VW, height: VH } } });
const p = await ctx.newPage();
await p.route(/fonts\./, (r) => r.abort());
await p.goto("file://" + editor);
await p.evaluate(() => localStorage.clear());
await p.reload();
const wait = (ms) => p.waitForTimeout(ms);
const setRange = (sel, v) => p.evaluate(([s, val]) => { const e = document.querySelector(s); e.value = val; e.dispatchEvent(new Event("input", { bubbles: true })); }, [sel, v]);
// 見出し（画面の上に、いま何をしているかを出す）
await p.addStyleTag({ content: "#recCap{position:fixed;left:50%;top:12px;transform:translateX(-50%);z-index:99;background:rgba(20,14,36,.88);color:#f2c14e;font:700 20px 'Noto Sans JP',sans-serif;padding:8px 18px;border-radius:10px;border:1px solid #f2c14e55;pointer-events:none}" });
const cap = (s) => p.evaluate((t) => { let e = document.getElementById("recCap"); if (!e) { e = document.createElement("div"); e.id = "recCap"; document.body.appendChild(e); } e.textContent = t; }, s);

await cap((title ? title + " — " : "") + "新しいキャンバス " + W + "×" + H);
await p.selectOption("#templateSelect", "blank"); await p.click("#loadTemplateBtn");
await p.fill("#gridW", String(W)); await p.fill("#gridH", String(H)); await p.click("#resizeBtn");
await p.uncheck("#symmetry"); await p.uncheck("#showShading");
await setRange("#zoom", 3);
await p.locator("#gridCanvas").scrollIntoViewIfNeeded();
await wait(800);

// パレット: 必要な数だけ色を足し、色と名前を入れる（エディタの記号に対応づける）
await cap("パレットに色を入れる（" + syms.length + "色）");
for (let i = 4; i < syms.length; i++) await p.click("#addSymbolBtn");
const ci = await p.$$("#symbolList input[type=color]"), li = await p.$$("#symbolList input.label");
const edSyms = await p.$$eval("#symbolList .symbol-row .sym", (els) => els.map((e) => e.textContent).filter((t) => t !== "消"));
const map = {};
for (let i = 0; i < syms.length; i++) {
  map[syms[i]] = edSyms[i];
  await ci[i].evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }, allPal[syms[i]]);
  await li[i].fill(syms[i]);
}
await p.locator("#gridCanvas").scrollIntoViewIfNeeded();
await wait(600);

if (ref) {
  await cap("AIの下絵を、下絵（トレース用）として薄く重ねる");
  await p.setInputFiles("#refFile", ref); await wait(400); await setRange("#refOpacity", 55); await wait(1500);
}

// 1色ずつ置いていく（暗い色 → 明るい色）
const toEd = (r) => [...r].map((ch) => (ch === "." ? "." : map[ch])).join("");
for (let k = 0; k < baseSyms.length; k++) {
  const keep = new Set(baseSyms.slice(0, k + 1));
  const partial = rows.map((r) => toEd([...r].map((ch) => (keep.has(ch) ? ch : ".")).join("")));
  await cap(`ドット絵を置く: 暗い色から ${k + 1} / ${baseSyms.length} 色`);
  await p.fill("#importRows", JSON.stringify(partial));
  await p.click("#importBtn");
  await p.locator("#gridCanvas").scrollIntoViewIfNeeded();
  await wait(k < 6 ? 700 : 420);
}
if (ref) { await setRange("#refOpacity", 0); await wait(500); await p.click("#refClearBtn"); }
await cap("ドット絵化した絵（手直しの前）");
await wait(1500);

// 手直し: 新しいレイヤーに、ペンで描く。描く所を拡大して見せる
await cap("手直し: 新しいレイヤー「手直し」を作る");
await p.click("#layerAdd"); await p.fill("#layerName", "手直し"); await p.dispatchEvent("#layerName", "change"); await wait(700);
await cap("手直し: 直線ツールを選ぶ"); await p.click("#toolGrid [data-tool=line]"); await wait(800);   // 直線ツール（マウスでドラッグして引く）
const Z = 8;
const center = async (r, c) => { await p.evaluate(([r, c, z]) => { const w = document.getElementById("canvasWrap"); w.scrollLeft = c * z - w.clientWidth / 2; w.scrollTop = r * z - w.clientHeight / 2; }, [r, c, Z]); await p.locator("#canvasWrap").scrollIntoViewIfNeeded(); };
// 描く所が枠の中に見えているか（見えていなければ、そこがまん中に来るようにスクロールする）
const visible = async (r, c) => p.evaluate(([r, c, n]) => { const w = document.getElementById("canvasWrap").getBoundingClientRect(), b = document.getElementById("gridCanvas").getBoundingClientRect(); const s = b.width / n; const x = b.left + c * s, y = b.top + r * s; return x > w.left + 30 && x < w.right - 30 && y > w.top + 30 && y < w.bottom - 30 && y > 30 && y < innerHeight - 30; }, [r, c, W]);
await setRange("#zoom", Z); await wait(300);
await center(edit.strokes[0][0], edit.strokes[0][1]);
await wait(900);
const cellXY = async (r, c) => { const b = await p.locator("#gridCanvas").boundingBox(); const s = b.width / W; return [b.x + c * s + s / 2, b.y + r * s + s / 2]; };
let curSym = null;
for (const [r0, c0, r1, c1, ch] of edit.strokes) {
  if (ch !== curSym) {
    await cap("手直し: 直線ツールで描く（" + (ch === "y" ? "青白く光る色" : ch === "z" ? "白い光" : "色 " + ch) + "）");
    const rowsEl = await p.$$("#symbolList .symbol-row .sym");
    await rowsEl[syms.indexOf(ch) + 1].click(); curSym = ch;
    await center(r0, c0); await wait(300);
  }
  if (!(await visible(r0, c0)) || !(await visible(r1, c1))) { await center((r0 + r1) >> 1, (c0 + c1) >> 1); await wait(400); }
  const [x0, y0] = await cellXY(r0, c0), [x1, y1] = await cellXY(r1, c1);
  await p.mouse.move(x0, y0); await p.mouse.down();
  await p.mouse.move(x1, y1, { steps: Math.max(4, Math.abs(r1 - r0) + Math.abs(c1 - c0)) * 2 });
  await p.mouse.up();
  await wait(110);
}
await wait(900);

// できあがり: 全体に戻して見せる
await cap("できあがり（全身）");
// 全身が画面に収まる拡大率に縮めて、キャンバスを画面のまん中に
const fitZ = await p.evaluate((n) => Math.max(1, Math.floor(Math.min(innerHeight - 260, document.getElementById("canvasWrap").clientWidth - 20) / n)), W);
await setRange("#zoom", fitZ); await p.evaluate(() => { const w = document.getElementById("canvasWrap"); w.scrollLeft = 0; w.scrollTop = 0; });
await p.locator("#gridCanvas").evaluate((el) => el.scrollIntoView({ block: "center" })); await wait(2500);
await cap("「手直し」レイヤーを消したり付けたりして、手直しした所を見る");
await p.click("#timeline [data-eye='1']"); await wait(1200); await p.locator("#gridCanvas").evaluate((el) => el.scrollIntoView({ block: "center" })); await p.click("#timeline [data-eye='1']"); await p.locator("#gridCanvas").evaluate((el) => el.scrollIntoView({ block: "center" })); await wait(1500);

const exported = await p.$eval("#exportRows", (t) => t.value);
const back = Object.fromEntries(Object.entries(map).map(([a, b]) => [b, a]));
const got = JSON.parse(exported.replace(/,\s*\]/, "]")).map((r) => [...r].map((s) => (s === "." ? "." : back[s] ?? "?")).join(""));
fs.writeFileSync(out + ".rows.txt", got.join("\n") + "\n");

// 動き（歩く・攻撃）: レイヤーを1枚にまとめ、フレームを足して1コマずつ入れ、タイムラインで再生する
if (animPath) {
  const A = JSON.parse(fs.readFileSync(animPath, "utf8"));
  for (const k of Object.keys(A.palette)) if (!syms.includes(k)) {   // 「当たり」のコマの明るい色をパレットに足す
    await p.click("#addSymbolBtn");
    const all = await p.$$eval("#symbolList .symbol-row .sym", (els) => els.map((e) => e.textContent).filter((t) => t !== "消"));
    map[k] = all[all.length - 1]; syms.push(k);
    const cis = await p.$$("#symbolList input[type=color]");
    await cis[cis.length - 1].evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }, A.palette[k]);
  }
  await cap("動き: 「手直し」を下のレイヤーと結合して1枚に");
  await p.click("#layerMerge"); await wait(900);
  const fitZ2 = await p.evaluate((n) => Math.max(1, Math.floor(Math.min(innerHeight - 330, document.getElementById("canvasWrap").clientWidth - 20) / n)), W);
  await setRange("#zoom", fitZ2); await p.locator("#gridCanvas").evaluate((el) => el.scrollIntoView({ block: "center" }));
  await p.check("#onionSkin");
  const put = async (rowsK, ms, label) => {
    await cap(label);
    await p.click("#frameAdd"); await wait(250);
    await p.fill("#importRows", JSON.stringify(rowsK.map(toEd)));
    await p.click("#importBtn");
    await p.fill("#frameDur", String(ms)); await p.dispatchEvent("#frameDur", "change");
    await p.locator("#gridCanvas").evaluate((el) => el.scrollIntoView({ block: "center" }));
    await wait(650);
  };
  // 1コマ目（いまの絵）は使わず、歩くコマから順に足す
  for (let i = 0; i < A.walk.length; i++) await put(A.walk[i], A.walk_ms[i], `歩く動き: ${i + 1} / ${A.walk.length} コマ目（オニオンスキンで前後のコマを透かして見る）`);
  for (let i = 0; i < A.attack.length; i++) await put(A.attack[i], A.attack_ms[i], `攻撃の動き: ${i + 1} / ${A.attack.length} コマ目`);
  await p.click("#timeline th[data-f='0']"); await p.click("#frameDel"); await wait(500);   // 使わない1コマ目を消す
  await p.uncheck("#onionSkin");
  await p.locator("#gridCanvas").evaluate((el) => el.scrollIntoView({ block: "center" }));
  const show = async (f) => { await p.evaluate((i) => document.querySelector(`#timeline th[data-f='${i}']`).click(), f); };
  const nW = A.walk.length;
  await cap("再生: 歩く");
  for (let loop = 0; loop < 3; loop++) for (let i = 0; i < nW; i++) { await show(i); await wait(A.walk_ms[i]); }
  await cap("再生: 攻撃");
  for (let loop = 0; loop < 3; loop++) {
    for (let i = 0; i < A.attack.length; i++) { await show(nW + i); await wait(A.attack_ms[i]); }
    await wait(450);
  }
  await cap("再生: 歩いてから攻撃");
  for (let loop = 0; loop < 2; loop++) {
    for (let w = 0; w < 2; w++) for (let i = 0; i < nW; i++) { await show(i); await wait(A.walk_ms[i]); }
    for (let i = 0; i < A.attack.length; i++) { await show(nW + i); await wait(A.attack_ms[i]); }
    await wait(350);
  }
  await show(0); await wait(800);
}
await p.close(); await ctx.close(); await browser.close();
const webm = fs.readdirSync(vdir).filter((f) => f.endsWith(".webm")).map((f) => path.join(vdir, f))[0];
const dur = parseFloat(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", webm]).toString()) || 60;
const vargs = ["-vf", "scale=1280:-2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24", "-movflags", "+faststart"];
if (bgm) execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", webm, "-i", bgm, "-map", "0:v", "-map", "1:a", ...vargs, "-af", `afade=t=in:d=1,afade=t=out:st=${Math.max(0, dur - 3).toFixed(2)}:d=3`, "-c:a", "aac", "-b:a", "160k", "-shortest", out]);
else execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", webm, ...vargs, out]);
console.log("動画:", out);
