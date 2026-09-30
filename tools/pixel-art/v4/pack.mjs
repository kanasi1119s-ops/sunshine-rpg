// 使い方: node pack.mjs <出力フォルダ> [エディタ出力フォルダ] — pieces/ の全ての絵を、カテゴリ別のフォルダにまとめる。
//   <出力>/README.txt・index.csv（UTF-8・BOMつき＝WindowsやExcelでも文字化けしない）
//   <出力>/<カテゴリ>/png_1x/<ID>.png（32×32・透明）  png_8x/<ID>.png（256×256・透明）  editor/<ID>.png（エディタで描いた画面）  rows/<ID>.txt（UTF-8）  _sheet.png（一覧）
// ファイル名は、文字化けしないよう、半角の英小文字・数字・ハイフンだけ。日本語の名前は index.csv と README.txt に書く。
import fs from "fs"; import path from "path"; import { pathToFileURL } from "url"; import { chromium } from "playwright-core"; import { DEFAULT_PAL, pieceRows } from "./lib4.mjs";
const [out, editorDir] = process.argv.slice(2); const root = path.dirname(new URL(import.meta.url).pathname); const piecesDir = process.env.PIECES ?? path.join(root, "pieces");
const CAT = { character: ["characters", "人物"], monster: ["monsters", "敵"], boss: ["bosses", "ボス"], item: ["items", "アイテム"], object: ["objects", "マップの物"], icon: ["icons", "アイコン"] };
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walk(path.join(d, e.name)) : e.name.endsWith(".mjs") ? [path.join(d, e.name)] : []));
const items = []; for (const f of walk(piecesDir).sort()) { const m = await import(pathToFileURL(f).href + "?t=" + Date.now()); if (!m.rows) continue; const id = path.basename(f, ".mjs"); items.push({ id, name: m.name ?? id, category: m.category ?? "object", rows: pieceRows(m), pal: { ...DEFAULT_PAL, ...(m.pal ?? {}) } }); }
fs.rmSync(out, { recursive: true, force: true }); const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }); const page = await b.newPage();
const draw = (it, Z, sheetCols) => it; // 参照用
const png = (rows, pal, Z) => page.evaluate(({ rows, pal, Z }) => { const c = document.createElement("canvas"); c.width = 32 * Z; c.height = 32 * Z; const x = c.getContext("2d"); rows.forEach((r, y) => [...r].forEach((k, xx) => { if (pal[k]) { x.fillStyle = pal[k]; x.fillRect(xx * Z, y * Z, Z, Z); } })); return c.toDataURL("image/png"); }, { rows, pal, Z });
const sheet = (list, Z, cols) => page.evaluate(({ list, Z, cols }) => { const cw = 32 * Z + 8, rowsN = Math.ceil(list.length / cols), c = document.createElement("canvas"); c.width = cols * cw; c.height = rowsN * cw; const x = c.getContext("2d"); x.fillStyle = "#3d3160"; x.fillRect(0, 0, c.width, c.height); list.forEach((it, n) => { const ox = (n % cols) * cw + 4, oy = Math.floor(n / cols) * cw + 4; it.rows.forEach((r, yy) => [...r].forEach((k, xx) => { if (it.pal[k]) { x.fillStyle = it.pal[k]; x.fillRect(ox + xx * Z, oy + yy * Z, Z, Z); } })); }); return c.toDataURL("image/png"); }, { list, Z, cols });
const save = (p, dataUrl) => { fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, Buffer.from(dataUrl.split(",")[1], "base64")); };
const bom = "﻿"; const csv = ["ID,カテゴリ,名前,色数,ファイル（フォルダ内）"]; const counts = {};
for (const it of items) { const [dir, jp] = CAT[it.category] ?? ["others", "その他"]; const d = path.join(out, dir); const cols = new Set(it.rows.join("").split("").filter((c) => c !== ".")).size;
  save(path.join(d, "png_1x", it.id + ".png"), await png(it.rows, it.pal, 1)); save(path.join(d, "png_8x", it.id + ".png"), await png(it.rows, it.pal, 8));
  fs.mkdirSync(path.join(d, "rows"), { recursive: true }); fs.writeFileSync(path.join(d, "rows", it.id + ".txt"), `# ${it.name}\n${it.rows.join("\n")}\n`, "utf8");
  if (editorDir && fs.existsSync(path.join(editorDir, it.id + ".png"))) { fs.mkdirSync(path.join(d, "editor"), { recursive: true }); fs.copyFileSync(path.join(editorDir, it.id + ".png"), path.join(d, "editor", it.id + ".png")); }
  csv.push([it.id, jp, `"${it.name.replace(/"/g, '""')}"`, cols, `${dir}/png_8x/${it.id}.png`].join(",")); counts[dir] = (counts[dir] ?? 0) + 1; it.dir = dir; }
for (const dir of Object.keys(counts)) save(path.join(out, dir, "_sheet.png"), await sheet(items.filter((i) => i.dir === dir), 4, 10));
await b.close();
fs.writeFileSync(path.join(out, "index.csv"), bom + csv.join("\r\n") + "\r\n", "utf8");
const readme = `sunshine-rpg ドット絵 ${items.length}点（32×32・人物は2頭身）
作成: サンシャインソフトウェア（Claude Code）  作成日: ${new Date().toISOString().slice(0, 10)}

【フォルダの中身】
` + Object.entries(counts).map(([d, n]) => `  ${d}/  ${n}点`).join("\n") + `
  各フォルダの中:
    png_1x/  32×32の透明PNG（ゲームで使う大きさ）
    png_8x/  256×256の透明PNG（見やすい拡大。SNSなどにはこちら）
    editor/  ドット絵エディタで描いた画面の画像
    rows/    ドットの並び（UTF-8のテキスト。色は文字で表す）
    _sheet.png  一覧（4倍）
  index.csv  一覧表（ID・カテゴリ・日本語の名前・色数）。UTF-8（BOMつき）なので、Excelでも文字化けしません

【決まり】
  ・人物は2頭身（胴は細め）。目には必ず白いハイライトを入れています
  ・完全オリジナルのデザインです（既存作品の絵・キャラクターは写していません）
  ・ファイル名は、文字化けを防ぐため、半角の英小文字・数字・ハイフンだけです
  ・ゲームには、まだ入れていません（人間の判断待ち）
`;
fs.writeFileSync(path.join(out, "README.txt"), bom + readme.replace(/\n/g, "\r\n"), "utf8");
console.log(items.length, "点 →", out, JSON.stringify(counts));
