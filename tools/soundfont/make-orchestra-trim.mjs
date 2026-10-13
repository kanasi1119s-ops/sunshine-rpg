// 使い方: node tools/soundfont/make-orchestra-trim.mjs <audit.json> [出力]
// audit-orchestra.mjs の結果（AUDIT_OUT）から、半音ごとの音量の補正表（assets-src/soundfont/extra/src/orchestra-trim.json）を作る。
// 楽器ごとに、全音の rms の中央値に合わせるための dB（-12〜+12）。±1dB 以内は書かない。build-orchestra.mjs が、あれば半音ごとのゾーンに分けて当てはめる。
import fs from "fs";
const [src, out = "assets-src/soundfont/extra/src/orchestra-trim.json"] = process.argv.slice(2);
const report = JSON.parse(fs.readFileSync(src, "utf8"));
const table = {};
for (const r of report) {
  if (!r.per) continue;
  const lv = r.per.map(([, v]) => v).filter((v) => v > 0.002).sort((a, b) => a - b);
  if (lv.length < 6) continue; // 減衰する短い音（ハープ・ティンパニなど）は、頭の rms の測り方が不安定なので触らない
  const med = lv[Math.floor(lv.length / 2)];
  const t = {};
  for (const [m, v] of r.per) {
    if (v <= 0.002) continue;
    const db = Math.max(-12, Math.min(12, 20 * Math.log10(med / v)));
    if (Math.abs(db) >= 1) t[m] = +db.toFixed(1);
  }
  if (Object.keys(t).length) table[r.p] = t;
}
fs.mkdirSync("assets-src/soundfont/extra/src", { recursive: true });
fs.writeFileSync(out, JSON.stringify(table));
console.log("補正表:", out, Object.entries(table).map(([p, t]) => `${p}:${Object.keys(t).length}`).join(" "));
