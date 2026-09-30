// v3: 32×32の手描きスプライト。左半分(16列)を1行ずつ文字で描き、左右に鏡写しにしてから、非対称の部分を上書きする。
import fs from "fs";
export const W = 32;
export const PAL = { p:"#3a2222", "1":"#4a2a22", "2":"#7a4632", "3":"#a8683e", "4":"#d49a5a", q:"#7a3f3a", a:"#c87a66", b:"#eaa588", c:"#f8cfae", d:"#fff0dc", e:"#2a1e3a", w:"#ffffff", i:"#5a86d0", r:"#14204a", J:"#1e2c66", j:"#2f4a9a", k:"#4c74c8", K:"#86aef0", C:"#efe3c8", y:"#bfae8e", P:"#4a3a3a", Q:"#6e5646", B:"#7a4a2a", A:"#ffb830", X:"#ffe89a", s:"#221a1a", m:"#a04a4a", n:"#8a4a3a" };
export function mirror(half) { return half.map((r, i) => { if (r.length !== 16) console.log(`左半分の長さが違う行 ${i}: ${r.length}`); const l = r.padEnd(16, ".").slice(0, 16); return l + [...l].reverse().join(""); }); }
export function overrides(rows, list) { const g = rows.map((r) => [...r]); for (const [x, y, ch] of list) g[y][x] = ch; return g.map((r) => r.join("")); }
export function validate(rows) { const bad = rows.map((r, i) => [i, r.length]).filter(([, l]) => l !== W); if (rows.length !== W) console.log("行数:", rows.length); if (bad.length) console.log("幅が違う行:", bad.join(" ")); }
