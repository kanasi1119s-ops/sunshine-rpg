// 使い方: node batch-editor.mjs <フォルダ or モジュール...> <出力フォルダ> [並列数(既定3)]
// 絵のモジュールを、ドット絵エディタ（../editor.html）に1つずつマウスで描き込み、エディタの書き出しが元の絵と一致するかを確かめて、
// エディタで描いたキャンバスの画像（<名前>.png）と、書き出し（<名前>.txt。UTF-8）を出力する。
import fs from "fs"; import path from "path"; import { pathToFileURL, fileURLToPath } from "url"; import { chromium } from "playwright-core"; 
const [dataPath, out, fromArg, toArg, concArg] = process.argv.slice(2); const CONC = Number(concArg ?? 3); const DATA = JSON.parse(fs.readFileSync(dataPath, "utf8")).slice(Number(fromArg ?? 0), Number(toArg ?? 1e9));
const files = DATA.filter((d) => true);
const RES = path.join(out, "results.jsonl");
fs.mkdirSync(out, { recursive: true }); const doneIds = new Set(fs.existsSync(RES) ? fs.readFileSync(RES, "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l)).filter((r) => r.ok).map((r) => r.base) : []);
const editor = fileURLToPath(new URL("../editor.html", import.meta.url));
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || "/opt/pw-browsers/chromium" });
const report = []; let next = 0;
async function paint(file) {
  const base = file.id; const m = { rows: file.rows, pal: file.pal, name: file.file };
  const t0 = Date.now(); const rows = m.rows, NH = rows.length, NW = rows[0].length, N = NH, PAL = { ...(m.pal ?? {}) };
  const count = new Map(); for (const r of rows) for (const c of r) if (c !== ".") count.set(c, (count.get(c) || 0) + 1);
  const used = [...count.keys()].sort((a, b) => count.get(b) - count.get(a));
  const miss = used.filter((c) => !PAL[c]); if (miss.length) return { base, ok: false, why: "色が未定義の文字: " + miss.join("") };
  if (used.length > 26) return { base, ok: false, why: "色が26色を超えています: " + used.length };
  if (NW > 256 || NH > 256 || rows.some((r) => r.length !== NW)) return { base, ok: false, why: "大きさが不正" };
  const ctx = await browser.newContext({ viewport: { width: 900, height: 1400 } }); const p = await ctx.newPage();
  try {
    await p.route(/fonts\./, (r) => r.abort()); await p.goto(pathToFileURL(editor).href);
    await p.selectOption("#templateSelect", "blank"); await p.click("#loadTemplateBtn");
    await p.fill("#gridW", String(NW)); await p.fill("#gridH", String(NH)); await p.click("#resizeBtn");
    await p.uncheck("#symmetry"); await p.uncheck("#showShading");
    await p.evaluate((ZOOM) => { const z = document.getElementById("zoom"); z.value = ZOOM; z.dispatchEvent(new Event("input", { bubbles: true })); }, Math.max(3, Math.min(16, Math.floor(860 / Math.max(NW, NH)))));
    for (let i = 0; i < used.length - 4; i++) await p.click("#addSymbolBtn");
    await p.waitForFunction((n) => document.querySelectorAll("#symbolList .sym").length >= n, used.length + 1);
    const syms = await p.$$eval("#symbolList .sym", (els) => els.map((e) => e.textContent.trim())).then((a) => a.slice(1));
    const ci = await p.$$("#symbolList input[type=color]"), li = await p.$$("#symbolList input.label");
    for (let i = 0; i < used.length; i++) { await ci[i].evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }, PAL[used[i]]); await li[i].fill(used[i]); }
    let box = await p.locator("#gridCanvas").boundingBox(), cw = box.width / NW; const cell = (r, c) => [box.x + c * cw + cw / 2, box.y + r * cw + cw / 2];
    const pick = async (k) => { const s = await p.$$("#symbolList .sym"); await s[k + 1].click(); await p.evaluate(() => document.getElementById("gridCanvas").scrollIntoView({ block: "center" })); box = await p.locator("#gridCanvas").boundingBox(); cw = box.width / NW; };
    for (let k = 0; k < used.length; k++) { await pick(k); for (let r = 0; r < NH; r++) { let c = 0; while (c < NW) { if (rows[r][c] === used[k]) { let e = c; while (e + 1 < NW && rows[r][e + 1] === used[k]) e++; const [x0, y0] = cell(r, c), [x1] = cell(r, e); await p.mouse.move(x0, y0); await p.mouse.down(); if (e > c) await p.mouse.move(x1, y0, { steps: Math.ceil((e - c + 1) * 1.3) + 1 }); await p.mouse.up(); c = e + 1; } else c++; } } }
    await p.waitForTimeout(150);
    const exp = JSON.parse((await p.inputValue("#exportRows")).replace(/,\s*\]/, "]")); const back = { ".": "." }; used.forEach((c, i) => (back[syms[i]] = c));
    const got = exp.map((r) => [...r].map((s) => back[s] ?? "?").join("")); const diff = got.reduce((s, r, y) => s + [...r].filter((ch, x) => ch !== rows[y][x]).length, 0);
    if (diff && process.env.DBG) { const l = []; got.forEach((r, y) => [...r].forEach((ch, x) => { if (ch !== rows[y][x] && l.length < 40) l.push(`(${x},${y}) 期待${rows[y][x]} 実際${ch}`); })); console.log(l.join(" ")); }
    if (process.env.SHOT) { await p.evaluate(() => window.scrollTo(0, 0)); await p.screenshot({ path: path.join(out, base + "-page.png") }); }
    await p.locator("#gridCanvas").screenshot({ path: path.join(out, base + ".png") });
    fs.writeFileSync(path.join(out, base + ".txt"), (m.name ? `# ${m.name}\n` : "") + exp.join("\n") + "\n", "utf8");
    return { base, ok: diff === 0, diff, why: diff ? `エディタの書き出しと ${diff} マス違う` : "", colors: used.length, ms: Date.now() - t0, w: NW, h: NH };
  } catch (e) { return { base, ok: false, why: String(e).split("\n")[0] }; } finally { await ctx.close(); }
}
await Promise.all(Array.from({ length: CONC }, async () => { while (next < files.length) { const f = files[next++]; if (doneIds.has(f.id)) continue; const r = await paint(f); report.push(r); fs.appendFileSync(RES, JSON.stringify(r) + "\n"); console.log(r.ok ? "OK " : "NG ", r.base, r.why ?? ""); } }));
await browser.close(); const ng = report.filter((r) => !r.ok); console.log(`\nエディタで描いた: ${report.length - ng.length}/${report.length}` + (ng.length ? `  失敗: ${ng.map((r) => r.base).join(", ")}` : "")); process.exit(ng.length ? 1 : 0);
