// 使い方: BNB=<Black And Blue Basses のフォルダ> node tools/soundfont/build-bass-bnb.mjs [bnb bnb-loud]（省略は両方）
// Black And Blue Basses（Karoryfer Samples、2023。CC0）の「darkblack」＝5弦ベース（BEADG。Washburn AB-95）の指弾き・ネック側ピックアップのライン録音から、
// 作曲ソフトのベース音源（GM 33・34 を入れかえ）と、「ミュート系の短い音」（GM 37）を1つの SF3 にする。
//   assets-src/soundfont/extra/bass-bnb-finger.sf3（--bass bnb）: 録音そのまま（ジャズ・バラードの「一音一音はっきり」にも）
//   assets-src/soundfont/extra/bass-bnb-loud.sf3（--bass bnb-loud）: 同じ録音を、ラウド向けに明るくゴリッと（こもる 250Hz を引き、900Hz・2.5kHz を持ち上げ、軽く圧縮）。歪ませるのはアンプ側
// 中身:
//   GM 33・34（ふつうの bass パート）: 強さ4層（p 1〜31・mp 32〜63・mf 64〜95・f 96〜127）× 録音2つ（強さの値の偶奇で交互＝同じ音のくり返しが機械的にならない）
//   GM 37（パートの patch "bassMute"）: 強さ 1〜70＝ゴーストノート（弱）、71〜100＝ゴーストノート（強）、101〜127＝スタッカート（指で短く止めた音）×録音2つ
//     作曲ソフトの強さの換算（34＋音量×430×比）で、volume 0.18〜0.22 のパートなら ふつう＝スタッカート、「,」＝ゴースト（強）、「,,」＝ゴースト（弱）になる
// 元の SFZ は「1オクターブ上の記譜」（低い B が b1＝35）なので、12 下げて B0＝23 から置く（Growlybass と同じ）。
// 元素材は大きい（961MB）ので git に入れない。必要な録音（reg の rr1・rr2、ghost の rr1、stac の rr1・rr2）だけを sparse checkout で取って使う:
//   git clone --filter=blob:none --no-checkout https://github.com/sfzinstruments/karoryfer.black-and-blue-basses
// 耳での確かめは別（作曲ソフトで鳴らして聞く）。
import fs from "fs";
import path from "path";
import { execFileSync } from "child_process";
import { loadBank, compressBank, timecents, BasicSoundBank, GeneratorTypes, emptyPresetFrom, SR } from "./lib.mjs";
import { BasicSample, SampleTypes } from "spessasynth_core";

const BNB = process.env.BNB ?? "/tmp/bnb";
const OUT = path.resolve("assets-src/soundfont/extra");
const SECONDS = 3.5, FADE = 0.6, Q = 5;
const LOUD = "highpass=f=32,equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=900:t=q:w=1:g=3,equalizer=f=2500:t=q:w=1:g=4,acompressor=threshold=-20dB:ratio=3:attack=6:release=80:makeup=1.5";
const VARIANTS = { bnb: { out: "bass-bnb-finger", label: "BnB Finger", filter: "" }, "bnb-loud": { out: "bass-bnb-loud", label: "BnB Finger Loud", filter: LOUD } };

/** マップの SFZ（<region> sample= lokey= hikey= pitch_keycenter= seq_position=）を読む */
function readMap(file) {
  const text = fs.readFileSync(path.join(BNB, "Programs/maps", file), "utf8");
  return text.split("<region>").slice(1).map((blk) => {
    const g = (k) => (new RegExp(`^${k}=(.*)$`, "m").exec(blk) ?? [])[1]?.trim();
    return { sample: path.join(BNB, g("sample").replace(/\\/g, "/").replace(/^\.\.\//, "")), lo: Number(g("lokey")) - 12, hi: Number(g("hikey")) - 12, center: Number(g("pitch_keycenter") ?? g("lokey")) - 12, rr: Number(g("seq_position") ?? 1) };
  });
}
const decode = (file, filter) => {
  const buf = execFileSync("ffmpeg", ["-v", "error", "-i", file, "-t", String(SECONDS), "-ac", "1", "-ar", String(SR), ...(filter ? ["-af", filter] : []), "-f", "f32le", "-"], { maxBuffer: 1 << 30 });
  const d = new Float32Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
  const f = Math.min(d.length, Math.round(FADE * SR));
  for (let i = 0; i < f; i++) d[d.length - f + i] *= 1 - i / f;
  return d;
};

for (const id of (process.argv.slice(2).filter((a) => a in VARIANTS).length ? process.argv.slice(2).filter((a) => a in VARIANTS) : Object.keys(VARIANTS))) {
  const v = VARIANTS[id];
  const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));
  const out = new BasicSoundBank();
  out.soundBankInfo = { ...base.soundBankInfo, name: `Bass ${v.label} (Karoryfer Black And Blue Basses, CC0)` };
  const cache = new Map();
  let peak = 0;
  const smpOf = (file, key) => {
    if (cache.has(file)) return cache.get(file);
    const data = decode(file, v.filter);
    for (const x of data) peak = Math.max(peak, Math.abs(x));
    const s = new BasicSample(path.basename(file, ".wav").replace("darkblack_", "bb_").slice(0, 19), SR, key, 0, SampleTypes.monoSample, 0, 0);
    s.setAudioData(data, SR);
    out.addSamples(s);
    cache.set(file, s);
    return s;
  };
  // 層: [マップ, 強さの範囲, 使う録音の数]
  const MAIN = [["darkblack_reg_p_map.sfz", 1, 31, 2], ["darkblack_reg_mp_map.sfz", 32, 63, 2], ["darkblack_reg_mf_map.sfz", 64, 95, 2], ["darkblack_reg_f_map.sfz", 96, 127, 2]];
  const MUTE = [["darkblack_ghost_p_map.sfz", 1, 70, 1], ["darkblack_ghost_f_map.sfz", 71, 100, 1], ["darkblack_stac_map.sfz", 101, 127, 2]];
  const fill = (inst, layers) => {
    let zones = 0;
    for (const [map, lv, hv, rr] of layers) {
      const regs = readMap(map).filter((r) => r.rr <= rr && fs.existsSync(r.sample));
      const keys = [...new Set(regs.map((r) => r.center))].sort((a, b) => a - b);
      const lowest = keys[0], highest = keys[keys.length - 1];
      for (const key of keys) {
        const alts = regs.filter((r) => r.center === key).sort((a, b) => a.rr - b.rr);
        const r0 = alts[0];
        const keyRange = { min: key === lowest ? Math.min(21, r0.lo) : r0.lo, max: key === highest ? 84 : r0.hi };
        for (let vel = lv; vel <= hv; vel++) {
          // 強さの値ごとに録音を交互に（人間味づけで強さが少しずれると、弾くたびに別の録音が鳴る）
          const a = alts[vel % alts.length];
          const z = inst.createZone(smpOf(a.sample, key));
          z.keyRange = keyRange;
          z.velRange = { min: vel, max: vel };
          z.setGenerator(GeneratorTypes.overridingRootKey, key);
          z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(0.25));
          z.setGenerator(GeneratorTypes.reverbEffectsSend, 0);
          z.setGenerator(GeneratorTypes.chorusEffectsSend, 0);
          zones++;
        }
      }
    }
    return zones;
  };
  let zones = 0;
  for (const program of [33, 34]) {
    const p = emptyPresetFrom(base, out, { program });
    p.name = `Bass ${v.label}`;
    const inst = p.zones[0].instrument;
    while (inst.zones.length) inst.deleteZone(0, true);
    zones += fill(inst, MAIN);
  }
  // GM 37 は元の音源（game.sf3）に無いので、36（スラップ）の入れものを写して番号を 37 にする（33 を写すと楽器の中身を 33 と共有してしまう）
  const pm = emptyPresetFrom(base, out, { program: 36 });
  pm.program = 37;
  pm.name = `Bass ${v.label} mute`;
  const im = pm.zones[0].instrument;
  while (im.zones.length) im.deleteZone(0, true);
  zones += fill(im, MUTE);
  // 山を -1dB にそろえる（ラウド版は EQ で山が変わるため）
  const g = 0.89 / peak;
  for (const s of cache.values()) { const d = s.getAudioData(); for (let i = 0; i < d.length; i++) d[i] *= g; s.setAudioData(d, SR); }
  out.flush();
  await compressBank(out, Q);
  const buf = out.writeSF2({});
  const file = path.join(OUT, `${v.out}.sf3`);
  fs.writeFileSync(file, Buffer.from(buf));
  console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "録音:", cache.size, "ゾーン:", zones, "倍率:", g.toFixed(2));
}
