// 使い方: node tools/soundfont/sf2-to-sf3.mjs <入力.sf2> <出力.sf3> [--program N] [--name 名前] [--q 4] [--mono] [--no-effects]
// 小さな SF2（FreePats など。CC0）を、作曲ソフトの overlay に使える SF3 にする。
//   元のゾーン（キー範囲・強さの範囲・ループ・エンベロープ）はそのまま残し、サンプルを Vorbis（--q）に圧縮するだけ。
//   --program N: 入っている最初のプリセットを、GM の N 番（0 始まり）に付けかえる（overlay は GM の番号で元の音と入れかわる）。
//       オルガンは 16〜20、ナイロンギターは 24、ピアノは 0〜2、シンセパッドは 88〜95 など。省略は元のまま。
//   --no-effects: コーラス・リバーブの送り（元の音源に入っている分）を 0 にする。作曲ソフトは自前の残響を持つので、二重にならないように。
//   --mono: 左右のサンプルを 1 本に平均して軽くする（ステレオの広がりは失う）。
// 元素材と規約は docs/assets-credits.md に記録する。ゲーム本体には入れない（作曲ソフト専用）。
import fs from "fs";
import path from "path";
import { SoundBankLoader, BasicSoundBank, SampleTypes, GeneratorTypes } from "spessasynth_core";
import { compressBank } from "./lib.mjs";

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
const flags = new Set(["--mono", "--no-effects"]);
const pos = args.filter((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--") && !flags.has(args[i - 1])));
const [inFile, outFile] = pos;
if (!inFile || !outFile) { console.error("使い方: node tools/soundfont/sf2-to-sf3.mjs <in.sf2> <out.sf3> [--program N] [--name NAME] [--q 4] [--mono] [--no-effects]"); process.exit(1); }
await BasicSoundBank.isSF3DecoderReady;
const bank = SoundBankLoader.fromArrayBuffer(fs.readFileSync(inFile).buffer.slice(0));
const program = opt("--program");
if (program !== undefined) {
  const p = bank.presets[0];
  p.program = Number(program);
  p.bankMSB = 0;
  p.bankLSB = 0;
  if (opt("--name")) p.name = opt("--name");
}
if (args.includes("--no-effects")) {
  for (const inst of bank.instruments) {
    for (const z of inst.zones) {
      z.setGenerator(GeneratorTypes.chorusEffectsSend, 0);
      z.setGenerator(GeneratorTypes.reverbEffectsSend, 0);
    }
  }
}
if (args.includes("--mono")) {
  const done = new Set();
  for (const s of bank.samples) {
    if (done.has(s) || s.sampleType === SampleTypes.monoSample) continue;
    if (s.sampleType === SampleTypes.leftSample && s.linkedSample) {
      const r = s.linkedSample;
      const l = s.getAudioData(), rr = r.getAudioData();
      const n = Math.min(l.length, rr.length);
      const d = new Float32Array(n);
      for (let i = 0; i < n; i++) d[i] = (l[i] + rr[i]) / 2;
      s.setAudioData(d, s.sampleRate);
      s.unlinkSample();
      s.setSampleType(SampleTypes.monoSample);
      done.add(s); done.add(r);
    }
  }
  // 右側の片割れを使っているゾーンを消し、使われなくなったサンプルを捨てる
  for (const inst of bank.instruments) {
    for (let i = inst.zones.length - 1; i >= 0; i--) {
      if (inst.zones[i].sample.sampleType === SampleTypes.rightSample) inst.deleteZone(i, true);
    }
  }
  bank.removeUnusedElements();
}
bank.soundBankInfo = { ...bank.soundBankInfo, name: opt("--name", bank.soundBankInfo.name) };
await compressBank(bank, Number(opt("--q", 4)));
bank.flush();
const buf = bank.writeSF2({});
fs.writeFileSync(outFile, Buffer.from(buf));
const inMB = fs.statSync(inFile).size / 1024 / 1024;
console.log("書き出し:", outFile, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "(元", inMB.toFixed(1) + "MB)", "プリセット:", bank.presets.map((p) => `${p.bankMSB}:${p.program}`).join(","), "サンプル:", bank.samples.length);
