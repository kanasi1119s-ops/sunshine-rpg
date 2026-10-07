// 使い方: node tools/soundfont/build-bass.mjs
// FreePats の Clean Electric Bass YR（CC0）の SFZ を、GMのエレキベース（プログラム33・34）を入れかえる小さなSoundFontにする。
//   assets-src/soundfont/extra/bass-finger.sf3 / bass-pick.sf3
// 元素材の置き場: assets-src/soundfont/extra/src/electric-bass-yr/（git clone https://github.com/freepats/electric-bass-yr）
import fs from "fs";
import path from "path";
import { decodeMono, loadBank, monoSample, timecents, compressBank, BasicSoundBank, GeneratorTypes, emptyPresetFrom } from "./lib.mjs";

const SRC = path.resolve("assets-src/soundfont/extra/src/electric-bass-yr");
const OUT = path.resolve("assets-src/soundfont/extra");
const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));

function parseSfz(file) {
  const regions = [];
  let cur = null;
  for (const raw of fs.readFileSync(file, "utf8").split("\n")) {
    const line = raw.replace(/\/\/.*$/, "").trim();
    if (!line) continue;
    if (line.startsWith("<region>")) { cur = {}; regions.push(cur); }
    else if (line.startsWith("<")) cur = null;
    if (!cur) continue;
    for (const m of line.matchAll(/(\w+)=(.*?)(?=\s+\w+=|$)/g)) cur[m[1]] = m[2].trim();
  }
  return regions;
}

for (const [label, sfz] of [["finger", "FingerBassYR 20190930.sfz"], ["pick", "PickedBassYR 20190930.sfz"]]) {
  const out = new BasicSoundBank();
  out.soundBankInfo = { ...base.soundBankInfo, name: `Bass ${label} (FreePats YR, CC0)` };
  // リアル版は曲調で 33（指弾き）か 34（ピック）を選ぶので、どちらも同じ音（この音源）に入れかえる。木製のベース（32）はそのまま
  const samples = [];
  for (const r of parseSfz(path.join(SRC, sfz))) {
    const root = Number(r.pitch_keycenter ?? r.key);
    const smp = monoSample(path.basename(r.sample, ".flac") + " " + label, decodeMono(path.join(SRC, r.sample)), root);
    out.addSamples(smp);
    samples.push({ smp, lo: Number(r.lokey ?? r.key), hi: Number(r.hikey ?? r.key), root });
  }
  let zones = 0;
  for (const program of [33, 34]) {
    const preset = emptyPresetFrom(base, out, { program });
    preset.name = `Electric Bass (${label})`;
    const inst = preset.zones[0].instrument;
    while (inst.zones.length) inst.deleteZone(0, true);
    for (const { smp, lo, hi, root } of samples) {
      const z = inst.createZone(smp);
      z.keyRange = { min: lo, max: hi };
      z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(0.4));
      z.setGenerator(GeneratorTypes.overridingRootKey, root);
      zones++;
    }
  }
  out.flush();
  await compressBank(out, 5);
  const buf = out.writeSF2({});
  const file = path.join(OUT, `bass-${label}.sf3`);
  fs.writeFileSync(file, Buffer.from(buf));
  console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "ゾーン:", zones);
}
