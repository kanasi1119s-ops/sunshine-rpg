// 使い方: node tools/soundfont/fix-orchestra-heads.mjs [音源.sf3]（省略は assets-src/soundfont/extra/orchestra.sf3）
// オーケストラ音源（VSCO 2 CE）の録音のうち、頭が 0 から始まらないもの（ホルン・コントラバスなど）は、
// 音を出した瞬間に波形が飛んで「プチッ」と鳴る（2026-10-17、人間の指示「雑音とれない？」で調べて分かった）。
// 全部の録音の頭に、ごく短い（4ms）なめらかな立ち上がりを付けて、書き戻す。立ち上がりの音色はほとんど変わらない。
// 元の録音から作り直すときは build-orchestra.mjs が同じ処理をする（applyLoop）。
import fs from "fs";
import path from "path";
import { loadBank, compressBank } from "./lib.mjs";

const file = path.resolve(process.argv[2] ?? "assets-src/soundfont/extra/orchestra.sf3");
await new Promise((r) => setTimeout(r, 3000)); // 圧縮された録音を読む部品（Vorbis）の準備を待つ
const bank = loadBank(file);
const FADE_SEC = 0.004;
let fixed = 0, worst = 0;
for (const s of bank.samples) {
  const d = s.getAudioData();
  const n = Math.min(d.length, Math.max(8, Math.floor(s.sampleRate * FADE_SEC)));
  const head = Math.max(...Array.from(d.subarray(0, 8)).map(Math.abs));
  worst = Math.max(worst, head);
  const out = new Float32Array(d);
  for (let i = 0; i < n; i++) out[i] *= 0.5 - 0.5 * Math.cos((Math.PI * i) / n);
  s.setAudioData(out, s.sampleRate);
  if (head > 0.003) fixed++;
}
await compressBank(bank, 4);
fs.writeFileSync(file, Buffer.from(bank.writeSF2({})));
console.log(`録音 ${bank.samples.length} 本の頭をなめらかにした（頭が 0 から始まらなかったもの ${fixed} 本、いちばん大きい飛び ${worst.toFixed(4)}）→ ${file}`);
