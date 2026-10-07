// 使い方: node --experimental-strip-types tools/soundfont/build-drums-jazz.mjs
// Virtuosity Drums（Versilian Studios と Karoryfer Samples。CC0）の元素材を、ジャズ用のドラムのSoundFontにする。
//   assets-src/soundfont/extra/drums-jazz.sf3
// 元素材（約1.4GB）はgitに入れない: git clone https://github.com/sfzinstruments/virtuosity_drums し、環境変数 VIRTUOSITY に、そのフォルダのパスを渡す。
// 録音は、マイクごと（oh＝オーバーヘッド、room＝部屋、mid、kickmic、snaremic）に同じ名前で入っている。
// ここでは「オーバーヘッド＋部屋＋mid＋近接マイク（キックとスネア）」をまぜたステレオ1組にし、強さの層を4つに絞って、必要な長さだけ切り出す。
import fs from "fs";
import path from "path";
import { decodeMono, decodeStereo, stereoPair, timecents, compressBank, loadBank, SR, BasicSoundBank, GeneratorTypes } from "./lib.mjs";

const SRC = process.env.VIRTUOSITY ?? "/home/claude/sfzinstruments/virtuosity_drums";
const OUT = path.resolve("assets-src/soundfont/extra");
const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));

// 鳴らすキー（GM）。art はサンプルの名前（<マイク>_<art>_vlN[_rrM].flac）、dir はフォルダ、root は音程の基準のキー（タムだけ、キーごとに音程が変わる）
const KIT = [
  { art: "kick_snoff", dir: "kick", keys: [36], close: "kickmic", sec: 1.0 },
  { art: "kick_snon", dir: "kick", keys: [35], close: "kickmic", sec: 1.0 },
  { art: "snare_center", dir: "snare", keys: [38], close: "snaremic", sec: 0.9 },
  { art: "snare_offcenter", dir: "snare", keys: [39], close: "snaremic", sec: 0.9 },
  { art: "snare_crossstick", dir: "snare", keys: [37], close: "snaremic", sec: 0.5 },
  { art: "snare_rimshot", dir: "snare", keys: [40], close: "snaremic", sec: 0.9 },
  { art: "hh_closed", dir: "hh", keys: [42], sec: 0.5, exclusive: 1 },
  { art: "hh_pedal", dir: "hh", keys: [44], sec: 0.4, exclusive: 1 },
  { art: "hh_open", dir: "hh", keys: [46], sec: 2.0, exclusive: 1 },
  { art: "ltom_center", dir: "ltom", keys: [41, 45], root: 43, sec: 1.8 },
  { art: "htom_center", dir: "htom", keys: [47, 50], root: 48, sec: 1.6 },
  { art: "crash_crash", dir: "crash", keys: [49], sec: 3.0 },
  { art: "crash_sizzle", dir: "crash", keys: [57], sec: 3.0 },
  { art: "ride_ride", dir: "ride", keys: [51], sec: 3.0 },
  { art: "ride_bell", dir: "ride", keys: [53], sec: 2.2 },
  { art: "flatride_ride", dir: "flatride", keys: [59], sec: 2.6 },
  { art: "flatride_crash", dir: "flatride", keys: [55], sec: 2.4 },
];
const MIX = { oh: 1.0, room: 0.55, mid: 0.4, close: 0.8 };

function files(mic, dir, art) {
  const out = [];
  for (const f of fs.readdirSync(path.join(SRC, "Samples", mic, dir))) {
    const m = new RegExp(`^${mic}_${art}(?:_vl(\\d+))?(?:_rr(\\d+))?\\.flac$`).exec(f);
    if (m) out.push({ f, vl: Number(m[1] ?? 1), rr: Number(m[2] ?? 1) });
  }
  return out;
}

function build() {
  const made = [];
  let peak = 0;
  for (const k of KIT) {
    const all = files("oh", k.dir, k.art);
    const vlMax = Math.max(...all.map((x) => x.vl));
    const n = Math.min(4, vlMax);
    const edges = Array.from({ length: n + 1 }, (_, i) => (i === 0 ? 1 : Math.round((127 * i) / n)));
    for (let i = 0; i < n; i++) {
      const vl = Math.max(1, Math.min(vlMax, Math.ceil(((i + 0.5) * vlMax) / n)));
      const pick = (mic) => {
        const c = files(mic, k.dir, k.art).filter((x) => x.vl === vl).sort((a, b) => a.rr - b.rr)[0];
        return c ? path.join(SRC, "Samples", mic, k.dir, c.f) : null;
      };
      const len = Math.round(k.sec * SR);
      const L = new Float32Array(len), R = new Float32Array(len);
      const addSt = (file, g) => { if (!file) return; const [l, r] = decodeStereo(file, k.sec); for (let j = 0; j < Math.min(len, l.length); j++) { L[j] += l[j] * g; R[j] += r[j] * g; } };
      addSt(pick("oh"), MIX.oh); addSt(pick("room"), MIX.room); addSt(pick("mid"), MIX.mid);
      if (k.close) { const f = pick(k.close); if (f) { const m = decodeMono(f, k.sec); for (let j = 0; j < Math.min(len, m.length); j++) { L[j] += m[j] * MIX.close; R[j] += m[j] * MIX.close; } } }
      const fade = Math.round(0.15 * SR);
      for (let j = 0; j < fade; j++) { const g = j / fade; L[len - 1 - j] *= g; R[len - 1 - j] *= g; }
      for (const b of [L, R]) for (const v of b) peak = Math.max(peak, Math.abs(v));
      made.push({ ...k, lo: edges[i] === 1 ? 1 : edges[i] + 1, hi: edges[i + 1], L, R });
    }
    console.log(k.art, "層:", n);
  }
  const gain = 0.95 / peak;
  for (const m of made) for (const b of [m.L, m.R]) for (let i = 0; i < b.length; i++) b[i] *= gain;
  return made;
}

const made = build();
const out = new BasicSoundBank();
out.soundBankInfo = { ...base.soundBankInfo, name: "Drums Virtuosity Jazz Kit (CC0)" };
const mine = new Set(KIT.flatMap((k) => k.keys));
for (const m of made) {
  [m.l, m.r] = stereoPair(`${m.art} ${m.lo}`, m.L, m.R, m.root ?? m.keys[0]);
  out.addSamples(m.l, m.r);
}
const done = new Set();
for (const program of [0, 8, 16, 32]) {
  const src = base.presets.find((p) => p.isGMGSDrum && p.program === program);
  if (!src) continue;
  const preset = out.clonePreset(src);
  for (const pz of preset.zones) {
    const inst = pz.instrument;
    if (done.has(inst)) continue;
    done.add(inst);
    for (let i = inst.zones.length - 1; i >= 0; i--) {
      const r = inst.zones[i].keyRange;
      if ([...mine].some((k) => k >= r.min && k <= r.max)) inst.deleteZone(i, true);
    }
    for (const m of made) {
      const keys = m.root ? [[m.keys[0], m.keys[m.keys.length - 1]]] : m.keys.map((k) => [k, k]);
      for (const [lo, hi] of keys) {
        for (const smp of [m.l, m.r]) {
          const z = inst.createZone(smp);
          z.keyRange = { min: lo, max: hi };
          z.velRange = { min: m.lo, max: m.hi };
          if (m.root) z.setGenerator(GeneratorTypes.overridingRootKey, m.root); else z.setGenerator(GeneratorTypes.scaleTuning, 0);
          z.setGenerator(GeneratorTypes.pan, smp === m.l ? -500 : 500);
          z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(0.3));
          if (m.exclusive) z.setGenerator(GeneratorTypes.exclusiveClass, m.exclusive);
        }
      }
    }
  }
}
out.flush();
await compressBank(out, 4);
const buf = out.writeSF2({});
const file = path.join(OUT, "drums-jazz.sf3");
fs.writeFileSync(file, Buffer.from(buf));
console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB");
