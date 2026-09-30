// 使い方: node check-eyes.mjs — キャラクターの目（y13〜17）に、白いハイライト(w)が両目にあるかを確かめる（人間の指示 2026-09-30「目には必ずハイライトを入れる」）
import { pathToFileURL } from "url"; import path from "path";
const files = ["yuri", "reto", "mina", "guide", "orca", "ayame", "kasen", "edrea", "dorn"].map((n) => `${n}-front.mjs`); let bad = 0;
for (const f of files) { const { rows } = await import(pathToFileURL(path.resolve(f)).href); const eye = (x0, x1) => rows.slice(13, 18).some((r) => r.slice(x0, x1).includes("w")); const l = eye(8, 15), r = eye(17, 24); console.log(f.padEnd(20), l && r ? "OK" : `NG 左${l} 右${r}`); if (!(l && r)) bad++; }
process.exit(bad ? 1 : 0);
