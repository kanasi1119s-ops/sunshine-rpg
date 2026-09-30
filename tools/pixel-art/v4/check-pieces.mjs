// 使い方: node check-pieces.mjs <フォルダ...> — 絵の決まりを確かめる（32×32・26色以内・色の定義・人物の両目のハイライト・ファイル名・文字コード）
import fs from "fs"; import path from "path"; import { pathToFileURL } from "url"; import { DEFAULT_PAL } from "./lib4.mjs";
const files = process.argv.slice(2).flatMap((a) => (fs.statSync(a).isDirectory() ? fs.readdirSync(a).filter((f) => f.endsWith(".mjs")).sort().map((f) => path.join(a, f)) : [a])); let bad = 0, n = 0;
for (const f of files) { n++; const errs = []; const base = path.basename(f);
  if (!/^[a-z0-9][a-z0-9-]*\.mjs$/.test(base)) errs.push("ファイル名は半角の英小文字・数字・ハイフンだけ");
  const text = fs.readFileSync(f); if (text.includes(0xef) && text.includes(Buffer.from([0xef, 0xbf, 0xbd]))) errs.push("文字化け（U+FFFD）が含まれる");
  let m; try { m = await import(pathToFileURL(path.resolve(f)).href + "?t=" + Date.now()); } catch (e) { errs.push("読み込めない: " + String(e).split("\n")[0]); }
  if (m) { const rows = m.rows; const PAL = { ...DEFAULT_PAL, ...(m.pal ?? {}) };
    if (!m.name) errs.push("name（日本語の名前）が無い"); if (!m.category) errs.push("category が無い");
    if (!Array.isArray(rows) || rows.length !== 32 || rows.some((r) => r.length !== 32)) errs.push("rows が32行×32文字ではない"); else { const cols = new Set(rows.join("").split("").filter((c) => c !== ".")); if (cols.size > 26) errs.push(`色が${cols.size}色（26色まで）`); const miss = [...cols].filter((c) => !PAL[c]); if (miss.length) errs.push("色が未定義の文字: " + miss.join(""));
      if (m.category === "character") { const eye = (x0, x1) => rows.slice(5, 13).some((r) => r.slice(x0, x1).includes("w")); if (!eye(6, 16) || !eye(16, 26)) errs.push("人物の両目に白いハイライト(w)が無い"); }
      let isolated = 0; for (let y = 1; y < 31; y++) for (let x = 1; x < 31; x++) { const c = rows[y][x]; if (c !== "." && rows[y - 1][x] !== c && rows[y + 1][x] !== c && rows[y][x - 1] !== c && rows[y][x + 1] !== c) isolated++; } if (isolated > 40) errs.push(`孤立した点が${isolated}個（ざらつき。減らす）`); } }
  if (errs.length) { bad++; console.log("NG ", base, errs.join(" / ")); } }
console.log(`${n - bad}/${n} 合格`); process.exit(bad ? 1 : 0);
