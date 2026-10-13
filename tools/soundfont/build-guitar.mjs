// 使い方: node --experimental-strip-types tools/soundfont/build-guitar.mjs [gretsch|hofner ...]（省略は全部）
// ギター音源の SoundFont を作る（assets-src/soundfont/extra/guitar-*.sf3）。GMのジャズギター（26）とクリーンギター（27）を入れかえる。
//   gretsch: 緑の Gretsch Anniversary（ホロウボディ）の録音。明るくて素直なクリーン。
//   hofner:  黒の Hofner Club の録音。丸みのある太い音。
// 元素材: Black And Green Guitars（Karoryfer Samples。CC0。録音と写真は Brian Wood）
//   環境変数 BGG（置き場。既定 /home/claude/sfzinstruments/bgg。git clone https://github.com/sfzinstruments/karoryfer.black-and-green-guitars）
//   使うのは Samples/{green,black}/ord/ の twang の録音のうち、ラウンドロビンの1番目（rr1）。強さは p・mf・f の3段。
import fs from "fs";
import path from "path";
import { decodeMono, loadBank, monoSample, timecents, compressBank, BasicSoundBank, GeneratorTypes, emptyPresetFrom } from "./lib.mjs";

const BGG = process.env.BGG ?? "/home/claude/sfzinstruments/bgg";
const OUT = path.resolve("assets-src/soundfont/extra");
const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));
const NOTE = { c: 0, db: 1, d: 2, eb: 3, e: 4, f: 5, gb: 6, g: 7, ab: 8, a: 9, bb: 10, b: 11 };
const VEL = { p: [1, 45], mf: [46, 95], f: [96, 127] };
const VARIANTS = {
  gretsch: { label: "Gretsch（クリーン）", dir: "green", programs: [26, 27], q: 5 },
  hofner: { label: "Hofner（丸い音）", dir: "black", programs: [26, 27], q: 5 },
};

const which = process.argv.slice(2).filter((a) => a in VARIANTS);
for (const id of which.length ? which : Object.keys(VARIANTS)) {
  const v = VARIANTS[id];
  const dir = path.join(BGG, "Samples", v.dir, "ord");
  const files = fs.readdirSync(dir).filter((f) => /^twang_[a-g]b?\d_(p|mf|f)_rr1\.wav$/.test(f)).sort();
  if (!files.length) throw new Error(`録音が見つかりません: ${dir}`);
  const out = new BasicSoundBank();
  out.soundBankInfo = { ...base.soundBankInfo, name: `Guitar ${v.label}` };
  const byKey = new Map();
  for (const f of files) {
    const [, n, oct, vel] = /^twang_([a-g]b?)(\d)_(p|mf|f)_rr1\.wav$/.exec(f);
    const key = 12 * (Number(oct) + 1) + NOTE[n];
    const smp = monoSample(`${v.dir} ${n}${oct} ${vel}`, decodeMono(path.join(dir, f), 4.5, "afade=t=out:st=3.9:d=0.6"), key);
    out.addSamples(smp);
    if (!byKey.has(key)) byKey.set(key, []);
    byKey.get(key).push({ smp, vel });
  }
  // 録音の最低音と最高音は、使う範囲（E2〜E6あたり）まで広げる。広げた先は音が細くなるが、鳴らないよりよい
  const keys = [...byKey.keys()].sort((a, b) => a - b);
  const lo = keys[0], hi = keys[keys.length - 1];
  let zones = 0;
  for (const program of v.programs) {
    // ゲーム用の音源は使う楽器だけに削ってあり、26 は無い。27 の入れものを写して番号を付けかえる
    const preset = emptyPresetFrom(base, out, { program: 27 });
    preset.program = program;
    preset.name = `Guitar ${v.label}`;
    const inst = preset.zones[0].instrument;
    while (inst.zones.length) inst.deleteZone(0, true);
    for (const key of keys) {
      for (const { smp, vel } of byKey.get(key)) {
        const z = inst.createZone(smp);
        z.keyRange = { min: key === lo ? 28 : key, max: key === hi ? 96 : key };
        z.velRange = { min: VEL[vel][0], max: VEL[vel][1] };
        // 元の入れものの「音の減り方」は、すぐ消える設定（sustainVolEnv 1000）なので、録音そのままの減り方になるよう打ち消す
        z.setGenerator(GeneratorTypes.attackVolEnv, timecents(0.002));
        z.setGenerator(GeneratorTypes.holdVolEnv, timecents(0.001));
        z.setGenerator(GeneratorTypes.decayVolEnv, timecents(1));
        z.setGenerator(GeneratorTypes.sustainVolEnv, 0);
        // 元の入れものにある「コーラスの送り25%」と「フィルターの共鳴」も打ち消す（電子的に聞こえる原因になる）
        z.setGenerator(GeneratorTypes.chorusEffectsSend, 0);
        z.setGenerator(GeneratorTypes.initialFilterQ, 0);
        z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(0.55));
        z.setGenerator(GeneratorTypes.overridingRootKey, key);
        zones++;
      }
    }
  }
  out.flush();
  await compressBank(out, v.q);
  const buf = out.writeSF2({});
  const file = path.join(OUT, `guitar-${id}.sf3`);
  fs.writeFileSync(file, Buffer.from(buf));
  console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "音:", keys.length, "ゾーン:", zones);
}
