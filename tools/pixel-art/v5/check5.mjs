// 使い方: node check5.mjs — pieces/ の絵の決まりを確かめる（正方形・64〜256・26色以内・色の定義・ファイル名・文字コード）
import fs from "fs"; import path from "path"; import { pathToFileURL } from "url";
const dir = path.join(path.dirname(new URL(import.meta.url).pathname), "pieces"); let bad = 0, n = 0;
for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".mjs")).sort()) { n++; const errs = [];
  if (!/^[a-z0-9][a-z0-9-]*\.mjs$/.test(f)) errs.push("ファイル名は半角の英小文字・数字・ハイフンだけ");
  if (fs.readFileSync(path.join(dir, f), "utf8").includes("�")) errs.push("文字化け(U+FFFD)");
  const m = await import(pathToFileURL(path.join(dir, f)).href + "?t=" + Date.now()); const rows = m.rows, N = rows.length;
  if (!m.name || !["monster", "boss"].includes(m.category)) errs.push("name / category が不正");
  if (![64, 96, 128, 160, 176, 192, 256].includes(N) && (N < 64 || N > 256)) errs.push("大きさが64〜256ではない: " + N);
  if (m.size !== N || rows.some((r) => r.length !== N)) errs.push("size と rows が合わない");
  const cols = new Set(rows.join("").replace(/\./g, "")); if (cols.size > 26) errs.push(`色が${cols.size}色`); const miss = [...cols].filter((c) => !m.pal[c]); if (miss.length) errs.push("色が未定義: " + miss.join(""));
  let iso = 0; for (let y = 1; y < N - 1; y++) for (let x = 1; x < N - 1; x++) { const c = rows[y][x]; if (c !== "." && rows[y - 1][x] !== c && rows[y + 1][x] !== c && rows[y][x - 1] !== c && rows[y][x + 1] !== c) iso++; }
  console.log(errs.length ? "NG " : "OK ", f.padEnd(28), `${N}×${N} ${cols.size}色 孤立点${iso}`, errs.join(" / ")); if (errs.length) bad++; }
console.log(`${n - bad}/${n} 合格`); process.exit(bad ? 1 : 0);
