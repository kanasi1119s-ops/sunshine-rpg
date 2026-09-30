// 使い方: node record-piece.mjs <スプライトのモジュール> <出力名> [出力フォルダ]
// ドット絵エディタ（../editor.html）を、スマホ幅（縦長）で起動して、32×32の絵を1筆ずつ描く様子を録画し、6倍速の縦動画（1080×1920・H.264のMP4）にする。
// 環境変数: PACE=1筆ごとの待ち(ms, 既定850)  SPEED=倍速(既定6)  FFMPEG=ffmpegの場所（H.264対応のもの。npm の ffmpeg-static など）
// スプライトのモジュールは、rows（32行×32文字）と、任意で pal（文字→色）を export する。
import { chromium } from "playwright-core"; import { PAL as BASE_PAL } from "./sprite.mjs"; import { pathToFileURL, fileURLToPath } from "url"; import { execFileSync } from "child_process"; import path from "path"; import fs from "fs";
const [mod, name, outDir = "vid"] = process.argv.slice(2); fs.mkdirSync(outDir, { recursive: true });
const m = await import(pathToFileURL(path.resolve(mod)).href); const rows = m.rows, PAL = { ...BASE_PAL, ...(m.pal ?? {}) }, N = rows.length;
const PACE = +(process.env.PACE ?? 850), SPEED = +(process.env.SPEED ?? 6), FFMPEG = process.env.FFMPEG ?? "ffmpeg";
const used = [...new Set(rows.join("").split("").filter((c) => c !== "." && PAL[c]))];
const count = new Map(); for (const r of rows) for (const c of r) if (PAL[c]) count.set(c, (count.get(c) || 0) + 1);
const order = m.order ?? [...used].sort((a, b) => count.get(b) - count.get(a));
if (order.length > 26) throw new Error("色が26色を超えています: " + order.length);
const editor = fileURLToPath(new URL("../editor.html", import.meta.url));
const b = await chromium.launch({ executablePath: process.env.CHROME_PATH || "/opt/pw-browsers/chromium" });
const t00 = Date.now();
const ctx = await b.newContext({ viewport: { width: 810, height: 1440 }, recordVideo: { dir: path.join(outDir, "_raw"), size: { width: 810, height: 1440 } } });
const p = await ctx.newPage(); await p.route(/fonts\./, (r) => r.abort()); await p.goto(pathToFileURL(editor).href);
// 見えるカーソル（録画にはマウスが映らないため）
await p.evaluate(() => { const d = document.createElement("div"); d.style.cssText = "position:fixed;z-index:99999;width:22px;height:22px;margin:-11px 0 0 -11px;border:3px solid #ffd54a;border-radius:50%;pointer-events:none;box-shadow:0 0 6px #000a;left:-50px;top:-50px"; document.body.appendChild(d); window.addEventListener("mousemove", (e) => { d.style.left = e.clientX + "px"; d.style.top = e.clientY + "px"; }, true); });
await p.selectOption("#templateSelect", "blank"); await p.click("#loadTemplateBtn");
await p.fill("#gridW", String(N)); await p.fill("#gridH", String(N)); await p.click("#resizeBtn");
await p.uncheck("#symmetry"); await p.uncheck("#showShading");
await p.evaluate(() => { const z = document.getElementById("zoom"); z.value = 22; z.dispatchEvent(new Event("input", { bubbles: true })); });
for (let i = 0; i < order.length - 4; i++) await p.click("#addSymbolBtn");
await p.waitForFunction((n) => document.querySelectorAll("#symbolList .sym").length >= n, order.length + 1);
const ci = await p.$$("#symbolList input[type=color]"), li = await p.$$("#symbolList input.label");
for (let i = 0; i < order.length; i++) { await ci[i].evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }, PAL[order[i]]); await li[i].fill(order[i]); }
await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(400);
const tStart = (Date.now() - t00) / 1000;
let box = await p.locator("#gridCanvas").boundingBox(), cw = box.width / N;
const cell = (r, c) => [box.x + c * cw + cw / 2, box.y + r * cw + cw / 2];
const pick = async (k) => { const chips = await p.$$("#qChips .chip"); await chips[k + 1].click(); await p.waitForTimeout(250); await p.locator("#gridCanvas").scrollIntoViewIfNeeded(); box = await p.locator("#gridCanvas").boundingBox(); cw = box.width / N; };
let strokes = 0;
for (let k = 0; k < order.length; k++) { await pick(k);
  for (let r = 0; r < N; r++) { let c = 0; while (c < N) { if (rows[r][c] === order[k]) { let e = c; while (e + 1 < N && rows[r][e + 1] === order[k]) e++; const [x0, y0] = cell(r, c), [x1] = cell(r, e); await p.mouse.move(x0, y0); await p.mouse.down(); if (e > c) await p.mouse.move(x1, y0, { steps: (e - c + 1) * 3 }); await p.mouse.up(); c = e + 1; strokes++; if (PACE) await p.waitForTimeout(PACE); } else c++; } } }
await p.waitForTimeout(2500);
await p.locator("#gridCanvas").screenshot({ path: path.join(outDir, `${name}.png`) });
const tEnd = (Date.now() - t00) / 1000;
const video = p.video(); await ctx.close(); const raw = await video.path(); await b.close();
const mp4 = path.join(outDir, `${name}.mp4`);
execFileSync(FFMPEG, ["-y", "-hide_banner", "-loglevel", "error", "-ss", String(Math.max(0, tStart - 1)), "-t", String(tEnd - tStart + 3), "-i", raw, "-vf", `setpts=PTS/${SPEED},fps=30,scale=1080:1920:flags=neighbor`, "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", mp4]);
const secs = ((tEnd - tStart + 3) / SPEED).toFixed(1);
console.log(`${name}: ${strokes}筆, 撮影${(tEnd - tStart).toFixed(0)}秒 → ${SPEED}倍速で約${secs}秒, ${mp4}`);
