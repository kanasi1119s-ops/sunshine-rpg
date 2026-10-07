// 使い方: node --experimental-strip-types tools/soundfont/build-bass.mjs [finger|pick|rock|metal|jpop|jazz ...]（省略は全部）
// ベース音源の SoundFont を作る（assets-src/soundfont/extra/bass-*.sf3）。GMのエレキベース（プログラム33・34）を入れかえる。
//   finger／pick: FreePats の Clean Electric Bass YR（CC0）の指弾き／ピック弾き、そのまま
//   rock／metal／jpop: 同じ録音に、ジャンルに合わせたイコライザーとコンプレッサーをかけたもの（rock＝ピック弾き、metal＝ピック弾きを硬く明るく、jpop＝指弾きを粒立ちよく）
//   jazz: Sneakybass（Karoryfer Samples。CC0）のウッドベース（指弾き）。33・34 に加えて、木製のベース（32）も入れかえる
// 元素材（置き場）:
//   assets-src/soundfont/extra/src/electric-bass-yr/（FreePats。git clone https://github.com/freepats/electric-bass-yr）
//   環境変数 SNEAKYBASS（Sneakybass のフォルダ。約190MBなのでgitには入れない。git clone https://github.com/sfzinstruments/karoryfer.sneakybass）
import fs from "fs";
import path from "path";
import { decodeMono, loadBank, monoSample, timecents, compressBank, BasicSoundBank, GeneratorTypes, emptyPresetFrom } from "./lib.mjs";

const SRC = path.resolve("assets-src/soundfont/extra/src/electric-bass-yr");
const SNEAKY = process.env.SNEAKYBASS ?? "/home/claude/sfzinstruments/karoryfer.sneakybass";
const OUT = path.resolve("assets-src/soundfont/extra");
const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));

const FILTERS = {
  rock: "equalizer=f=100:t=q:w=1:g=2,equalizer=f=1800:t=q:w=1:g=2,acompressor=threshold=-18dB:ratio=3:attack=10:release=100:makeup=1.5",
  metal: "highpass=f=40,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=900:t=q:w=1:g=3,equalizer=f=2500:t=q:w=1:g=4,acompressor=threshold=-22dB:ratio=5:attack=3:release=60:makeup=2.5",
  jpop: "equalizer=f=80:t=q:w=1:g=2,equalizer=f=2200:t=q:w=1:g=3.5,equalizer=f=5000:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3:attack=6:release=90:makeup=1.5",
};
const VARIANTS = {
  finger: { label: "指弾き", sfz: "FingerBassYR 20190930.sfz", programs: [33, 34], q: 5 },
  pick: { label: "ピック", sfz: "PickedBassYR 20190930.sfz", programs: [33, 34], q: 5 },
  rock: { label: "ロック", sfz: "PickedBassYR 20190930.sfz", filter: FILTERS.rock, programs: [33, 34], q: 5 },
  metal: { label: "メタル", sfz: "PickedBassYR 20190930.sfz", filter: FILTERS.metal, programs: [33, 34], q: 5 },
  jpop: { label: "J-POP", sfz: "FingerBassYR 20190930.sfz", filter: FILTERS.jpop, programs: [33, 34], q: 5 },
  jazz: { label: "ジャズ（ウッドベース）", sneaky: true, programs: [32, 33, 34], q: 6 },
};

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

const which = process.argv.slice(2).filter((a) => a in VARIANTS);
for (const id of which.length ? which : Object.keys(VARIANTS)) {
  const v = VARIANTS[id];
  const out = new BasicSoundBank();
  out.soundBankInfo = { ...base.soundBankInfo, name: `Bass ${v.label}` };
  const samples = [];
  if (v.sneaky) {
    // Sneakybass: 指弾きの録音。1つのキーに4つの録音（ラウンドロビン）があるので、1番目だけ使う
    for (const r of parseSfz(path.join(SNEAKY, "Programs/modules/maps/sneakybass_finger_map.sfz"))) {
      if (r.seq_position && r.seq_position !== "1") continue;
      const file = path.join(SNEAKY, r.sample.replace(/\\/g, "/").replace(/^\.\.\//, ""));
      const root = Number(r.pitch_keycenter);
      const smp = monoSample(path.basename(file, ".wav"), decodeMono(file, 3.2), root);
      out.addSamples(smp);
      samples.push({ smp, lo: Number(r.lokey), hi: Number(r.hikey), root, tune: Number(r.tune ?? 0) });
    }
  } else {
    for (const r of parseSfz(path.join(SRC, v.sfz))) {
      const root = Number(r.pitch_keycenter ?? r.key);
      const smp = monoSample(path.basename(r.sample, ".flac") + " " + id, decodeMono(path.join(SRC, r.sample), undefined, v.filter), root);
      out.addSamples(smp);
      samples.push({ smp, lo: Number(r.lokey ?? r.key), hi: Number(r.hikey ?? r.key), root, tune: 0 });
    }
  }
  let zones = 0;
  for (const program of v.programs) {
    const preset = emptyPresetFrom(base, out, { program });
    preset.name = `Bass ${v.label}`;
    const inst = preset.zones[0].instrument;
    while (inst.zones.length) inst.deleteZone(0, true);
    for (const { smp, lo, hi, root, tune } of samples) {
      const z = inst.createZone(smp);
      z.keyRange = { min: lo, max: hi };
      z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(0.4));
      z.setGenerator(GeneratorTypes.overridingRootKey, root);
      if (tune) z.setGenerator(GeneratorTypes.fineTune, -tune);
      zones++;
    }
  }
  out.flush();
  await compressBank(out, v.q);
  const buf = out.writeSF2({});
  const file = path.join(OUT, `bass-${id}.sf3`);
  fs.writeFileSync(file, Buffer.from(buf));
  console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "ゾーン:", zones);
}
