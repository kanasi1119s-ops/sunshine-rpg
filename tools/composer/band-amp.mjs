// バンド版の曲の、アンプシミュレーター設定をそろえる。
// ・アンプの指定が空のギター・ベースに、楽器に合うアンプを入れる（作曲ソフトのアンプシミュレーターで鳴らす）
// ・以前付けた曲ごとの歪みの深さ(drive)は外す（歪みの抑えは amp-rack.ts に一本化した）
// 使い方: node tools/composer/band-amp.mjs        → src/audio/songs/*.sunshine-song.json をすべて処理（何度実行しても同じ結果）
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// 歪みの深さの抑えは、再生エンジン側（src/audio/amp-rack.ts の GUITAR_DRIVE_TRIM）で全曲共通にかけている。
// ここで曲ごとの drive は付けない（二重にかからないよう、以前付けた drive は外す）。
const GUITARS = new Set(["guitar", "crunch", "distGuitar", "leadGuitar", "echoGuitar"]);
const BASSES = new Set(["bass", "slap", "sub808"]);
/** 歪ませる種類のアンプ（ここだけ drive を下げる。クリーン・ジャズ・ブルース・ファンク・ローファイ・シューゲイザーは触らない）。 */
const DISTORTING = new Set(["overdrive", "distortion", "metal", "prs", "crunch", "hardrock", "punk", "fuzz"]);
const DEFAULT_GUITAR_AMP = { guitar: "clean", crunch: "crunch", distGuitar: "metal", leadGuitar: "prs", echoGuitar: "clean" };

/**
 * 曲ごとの音づくりの上書き（歪みの深さ drive・高音 tone[dB]）。特定の曲の「ジャリつき」を抑えるときに使う。
 * 全曲共通の抑えは src/audio/amp-rack.ts（GUITAR_DRIVE_TRIM・HARSH_CUT_DB）にある。
 */
export const SONG_TWEAKS = {
  "scarlet-chapter": { leadGuitar: { drive: 0.7, tone: -3 }, distGuitar: { drive: 0.65, tone: -4 } },
  "scarlet-chapter-space": { leadGuitar: { drive: 0.7, tone: -3 }, distGuitar: { drive: 0.65, tone: -4 }, echoGuitar: { drive: 0.8, tone: -3 } },
};

export function applyBandAmp(score, id) {
  for (const t of score.tracks) {
    const inst = t.instrument;
    if (!t.amp || t.amp.type === "auto") {
      if (GUITARS.has(inst)) t.amp = { type: DEFAULT_GUITAR_AMP[inst] };
      else if (inst === "bass") t.amp = { type: "clean" };
      else if (inst === "slap") t.amp = { type: "funk" };
    }
    const tw = SONG_TWEAKS[id]?.[inst];
    if (tw && t.amp) t.amp = { ...t.amp, ...tw };
  }
  return score;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const dir = fileURLToPath(new URL("../../src/audio/songs/", import.meta.url));
  let n = 0;
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".sunshine-song.json"))) {
    const p = path.join(dir, f), d = JSON.parse(fs.readFileSync(p, "utf8"));
    if (!d.score) continue;
    fs.writeFileSync(p, JSON.stringify({ ...d, score: applyBandAmp(d.score, d.id) })); n++;
  }
  console.log("アンプ設定をそろえた曲:", n);
}
