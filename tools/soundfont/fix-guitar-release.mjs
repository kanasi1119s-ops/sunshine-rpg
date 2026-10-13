// 上書き用ギター SF3（gretsch・hofner・pluck-*）の実効リリースを 0.55 秒にそろえる（2026-10-14）。
//   原因: 土台に写した game.sf3 の27番のプリセット全体ゾーンに「リリース ×0.3」が残っていて、楽器側に書いた 0.35／0.25 秒が掛け算で 0.105／0.075 秒になっていた。
//   ストロークの1音ごとがノートオフ後すぐ（約0.1秒）に消え、「ダッダッダッ」と途切れて聞こえた。
//   直し方: プリセット側のリリース係数を消し、楽器側のリリースを 0.55 秒にする（標準の27番の実効 0.60 秒に近い）。サンプルはそのまま（Oggのまま書き戻す）。
// 使い方: node --experimental-strip-types tools/soundfont/fix-guitar-release.mjs [ファイル...]（省略時は assets-src/soundfont/extra/guitar-*.sf3 のうち gretsch・hofner・pluck*）
import fs from "fs";
import path from "path";
import { loadBank, timecents, GeneratorTypes } from "./lib.mjs";

const DIR = path.resolve("assets-src/soundfont/extra");
const files = process.argv.slice(2).length ? process.argv.slice(2) : fs.readdirSync(DIR).filter((f) => /^guitar-(gretsch|hofner|pluck.*)\.sf3$/.test(f)).map((f) => path.join(DIR, f));
const RELEASE = Number(process.env.RELEASE ?? 0.55);
const REL = GeneratorTypes.releaseVolEnv;
for (const file of files) {
  const bank = loadBank(file);
  let preset = 0, inst = 0, before = new Set();
  const strip = (zone) => { const n = zone.generators.length; zone.generators = zone.generators.filter((g) => g.type !== REL); return n !== zone.generators.length; };
  for (const p of bank.presets) {
    if (strip(p.globalZone)) preset++;
    for (const pz of p.zones) {
      if (strip(pz)) preset++;
      const i = pz.instrument;
      for (const z of i.zones) { const g = z.generators.find((x) => x.type === REL); if (g) before.add(Math.round(2 ** (g.value / 1200) * 1000) / 1000); z.setGenerator(REL, timecents(RELEASE)); inst++; }
      const gg = i.globalZone.generators.find((x) => x.type === REL);
      if (gg) i.globalZone.setGenerator(REL, timecents(RELEASE));
    }
  }
  bank.flush();
  const buf = bank.writeSF2({});
  fs.writeFileSync(file, Buffer.from(buf));
  console.log(path.basename(file), "プリセット側の係数を消した:", preset, "楽器側の設定:", inst, "元の楽器側リリース(秒):", [...before].join(","), "→", RELEASE, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB");
}
