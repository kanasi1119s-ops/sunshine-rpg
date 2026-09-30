// 使い方: node pack5.mjs <出力フォルダ> [エディタ出力フォルダ] — pieces/ の大きな敵・ボスの絵を、1つのフォルダにまとめる。
//   <出力>/README.txt・index.csv（UTF-8・BOMつき＝WindowsやExcelでも文字化けしない）
//   <出力>/png_1x/<ID>.png（実寸・透明）  png_4x/<ID>.png（4倍・透明）  png_preview/<ID>.png（暗い背景つき・名前入り）  editor/<ID>.png  rows/<ID>.txt（UTF-8）  _sheet.png（一覧）
// ファイル名は半角の英小文字・数字・ハイフンだけ（日本語の名前は index.csv と README.txt に書く）。
import fs from "fs"; import path from "path"; import { pathToFileURL } from "url"; import { chromium } from "playwright-core";
const [out, editorDir] = process.argv.slice(2); const root = path.dirname(new URL(import.meta.url).pathname); const piecesDir = path.join(root, "pieces");
const items = []; for (const f of fs.readdirSync(piecesDir).filter((x) => x.endsWith(".mjs")).sort()) { const m = await import(pathToFileURL(path.join(piecesDir, f)).href + "?t=" + Date.now()); items.push({ id: f.replace(/\.mjs$/, ""), name: m.name, category: m.category, rows: m.rows, pal: m.pal, n: m.rows.length }); }
fs.rmSync(out, { recursive: true, force: true }); const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }); const page = await b.newPage();
const png = (it, Z, bg) => page.evaluate(({ it, Z, bg }) => { const pad = bg ? 12 : 0, c = document.createElement("canvas"); c.width = it.n * Z + pad * 2; c.height = it.n * Z + pad * 2 + (bg ? 26 : 0); const x = c.getContext("2d"); if (bg) { x.fillStyle = "#3d3160"; x.fillRect(0, 0, c.width, c.height); } it.rows.forEach((r, y) => [...r].forEach((k, xx) => { if (it.pal[k]) { x.fillStyle = it.pal[k]; x.fillRect(pad + xx * Z, pad + y * Z, Z, Z); } })); if (bg) { x.fillStyle = "#fff"; x.font = "14px sans-serif"; x.fillText(it.id + "  " + it.n + "×" + it.n, pad, c.height - 8); } return c.toDataURL("image/png"); }, { it, Z, bg });
const save = (p, d) => { fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, Buffer.from(d.split(",")[1], "base64")); };
const bom = "﻿"; const csv = ["ID,種類,名前,大きさ(縦×横),色数,ファイル"]; const KIND = { monster: "敵", boss: "ボス" };
const kindOf = (it) => (it.category === "boss" ? "ボス（256×256）" : it.n >= 128 ? "大型（128〜192）" : it.n >= 96 ? "中型（96〜128）" : "小型（64）");
for (const it of items) { const cols = new Set(it.rows.join("").replace(/\./g, "")).size;
  save(path.join(out, "png_1x", it.id + ".png"), await png(it, 1, false)); save(path.join(out, "png_4x", it.id + ".png"), await png(it, 4, false)); save(path.join(out, "png_preview", it.id + ".png"), await png(it, Math.max(2, Math.floor(700 / it.n)), true));
  fs.mkdirSync(path.join(out, "rows"), { recursive: true }); fs.writeFileSync(path.join(out, "rows", it.id + ".txt"), `# ${it.name}\n${it.rows.join("\n")}\n`, "utf8");
  if (editorDir && fs.existsSync(path.join(editorDir, it.id + ".png"))) { fs.mkdirSync(path.join(out, "editor"), { recursive: true }); fs.copyFileSync(path.join(editorDir, it.id + ".png"), path.join(out, "editor", it.id + ".png")); }
  csv.push([it.id, kindOf(it), `"${it.name}"`, `${it.n}×${it.n}`, cols, `png_4x/${it.id}.png`].join(",")); }
const maxN = Math.max(...items.map((i) => i.n)), Z = 3, cw = maxN * Z + 12, cols = 4, rowsN = Math.ceil(items.length / cols);
save(path.join(out, "_sheet.png"), await page.evaluate(({ items, Z, cw, cols, rowsN }) => { const c = document.createElement("canvas"); c.width = cols * cw; c.height = rowsN * (cw + 22); const x = c.getContext("2d"); x.fillStyle = "#3d3160"; x.fillRect(0, 0, c.width, c.height); x.font = "13px sans-serif"; items.forEach((it, k) => { const ox = (k % cols) * cw + 6, oy = Math.floor(k / cols) * (cw + 22) + 4; it.rows.forEach((r, yy) => [...r].forEach((kk, xx) => { if (it.pal[kk]) { x.fillStyle = it.pal[kk]; x.fillRect(ox + xx * Z, oy + yy * Z, Z, Z); } })); x.fillStyle = "#fff"; x.fillText(it.id + " " + it.n + "×" + it.n, ox, oy + it.n * Z + 14); }); return c.toDataURL("image/png"); }, { items, Z, cw, cols, rowsN }));
await b.close(); fs.writeFileSync(path.join(out, "index.csv"), bom + csv.join("\r\n") + "\r\n", "utf8");
const readme = `sunshine-rpg 大型の敵・ボスのドット絵 ${items.length}点
作成: サンシャインソフトウェア（Claude Code）  作成日: ${new Date().toISOString().slice(0, 10)}

【大きさの基準（人間の指示 2026-09-30）】
  小型（スライム級・虫・鳥）64×64 ／ 中型（獣・人型）96×96〜128×128 ／ 大型（巨体・中ボス）128×128〜192×192 ／ ボス（画面いっぱい）256×256

【フォルダの中身】
  png_1x/       実寸の透明PNG
  png_4x/       4倍の透明PNG（見やすい拡大）
  png_preview/  暗い背景つき・名前入り（確認用）
  editor/       ドット絵エディタで描いた画面の画像
  rows/         ドットの並び（UTF-8のテキスト。色は文字で表す）
  _sheet.png    一覧（3倍）
  index.csv     一覧表（ID・種類・日本語の名前・大きさ・色数）。UTF-8（BOMつき）なので、Excelでも文字化けしません

【決まり】
  ・完全オリジナルのデザインです（既存作品の敵・ボスは写していません）。技法（陰影・輪郭・光の縁）だけを参考にしました
  ・色は1点あたり26色まで（ゲームに入れる形式の上限）
  ・ファイル名は、文字化けを防ぐため、半角の英小文字・数字・ハイフンだけです
  ・ゲームには、まだ入れていません（人間の判断待ち）。仮の絵です
`;
fs.writeFileSync(path.join(out, "README.txt"), bom + readme.replace(/\n/g, "\r\n"), "utf8"); console.log(items.length, "点 →", out);
