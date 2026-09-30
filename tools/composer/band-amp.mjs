// バンド版の曲の、アンプシミュレーター設定をそろえる。
// ・アンプの指定が空のギター・ベースに、楽器に合うアンプを入れる（作曲ソフトのアンプシミュレーターで鳴らす）
// ・歪み系のギターは、歪みの深さ(drive)を0.9倍にして、ほんの少しだけ抑える（人間の指示 2026-09-30「ほんのほんの少し抑えて」）
// 使い方: node tools/composer/band-amp.mjs        → src/audio/songs/*.sunshine-song.json をすべて処理（何度実行しても同じ結果）
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

export const BAND_DRIVE = 0.9;
const GUITARS = new Set(["guitar", "crunch", "distGuitar", "leadGuitar", "echoGuitar"]);
const BASSES = new Set(["bass", "slap", "sub808"]);
/** 歪ませる種類のアンプ（ここだけ drive を下げる。クリーン・ジャズ・ブルース・ファンク・ローファイ・シューゲイザーは触らない）。 */
const DISTORTING = new Set(["overdrive", "distortion", "metal", "prs", "crunch", "hardrock", "punk", "fuzz"]);
const DEFAULT_GUITAR_AMP = { guitar: "clean", crunch: "crunch", distGuitar: "metal", leadGuitar: "prs", echoGuitar: "clean" };

export function applyBandAmp(score) {
  for (const t of score.tracks) {
    const inst = t.instrument;
    if (!t.amp || t.amp.type === "auto") {
      if (GUITARS.has(inst)) t.amp = { type: DEFAULT_GUITAR_AMP[inst] };
      else if (inst === "bass") t.amp = { type: "clean" };
      else if (inst === "slap") t.amp = { type: "funk" };
    }
    if (GUITARS.has(inst) && t.amp && DISTORTING.has(t.amp.type) && t.amp.drive === undefined) t.amp = { ...t.amp, drive: BAND_DRIVE };
  }
  return score;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const dir = fileURLToPath(new URL("../../src/audio/songs/", import.meta.url));
  let n = 0;
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".sunshine-song.json"))) {
    const p = path.join(dir, f), d = JSON.parse(fs.readFileSync(p, "utf8"));
    if (!d.score) continue;
    fs.writeFileSync(p, JSON.stringify({ ...d, score: applyBandAmp(d.score) })); n++;
  }
  console.log("アンプ設定をそろえた曲:", n);
}
