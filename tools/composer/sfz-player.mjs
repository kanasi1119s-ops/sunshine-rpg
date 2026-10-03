// SFZ 形式の録音集（ドラム・ベースなど）を読んで、音符を音にする小さな再生プログラム。render-node.mjs が使う。
// sfizz などの外部ソフトは使わない。よく使われる項目だけに対応する:
//   #define・#include（行の途中にあってもよい）、<control>(default_path・set_ccN)・<global>・<master>・<group>・<region> の引き継ぎ、
//   key/lokey/hikey/pitch_keycenter（数字・音名）、lovel/hivel、seq_length/seq_position（録り分けを順に）、lorand/hirand（ばらつき）、
//   locc/hicc（初期値 set_ccN で判定。決まっていない CC は 0）、trigger=attack/release、group/off_by（ハイハットの開閉などで前の音を止める）、
//   volume/amplitude/pan/tune/transpose/pitch_keytrack、amp_veltrack・amp_velcurve_N、ampeg_attack/hold/decay/sustain/release、offset
// 読み方の注意（実際の録音集で確かめたこと）:
//   #include と sample= の場所は、いちばん上のプログラムのフォルダから見た相対の場所。「\」の区切りもある。項目名の大文字・小文字はまちまち。
//   1行に見出しと項目が並ぶことがある。<curve> は使わない（読みとばす）。sample=*silence は音を出さず、off_by で前の音を止めるだけ。
import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";

const SR = 44100;
const PCS = { c: 0, d: 2, e: 4, f: 5, g: 7, a: 9, b: 11 };

export function keyOf(v) {
  if (v === undefined) return undefined;
  const s = String(v).trim();
  if (/^-?\d+$/.test(s)) return Number(s);
  const m = s.toLowerCase().match(/^([a-g])(#|b)?(-?\d+)$/);
  if (!m) return undefined;
  return (Number(m[3]) + 1) * 12 + PCS[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0);
}

/**
 * #include を展開し、#define を置きかえた全文を返す。
 * replace: { "元の#includeの名前": "かわりに読むもの" }（例: ハイハットの割り当て表を差しかえる）
 */
function expand(file, defines, top, replace, depth = 0) {
  if (depth > 12 || !fs.existsSync(file)) return "";
  const text = fs.readFileSync(file, "utf8").replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/[^\n]*/g, "");
  const sub = (x) => x.replace(/\$\w+/g, (v) => (v in defines ? defines[v] : v)); // \w+ は名前の最後まで読むので、長い名前が優先される
  const out = [];
  for (const line of text.split(/\r?\n/)) {
    const def = line.match(/^\s*#define\s+(\$\w+)\s+(.+?)\s*$/);
    if (def) {
      defines[def[1]] = sub(def[2]);
      continue;
    }
    for (const part of line.split(/(#include\s+"[^"]+")/)) {
      const inc = part.match(/^#include\s+"(.+?)"$/);
      if (inc) {
        let name = sub(inc[1]).replace(/\\/g, "/");
        if (replace[name]) name = replace[name];
        out.push("\n" + expand(path.resolve(top, name), defines, top, replace, depth + 1) + "\n");
      } else out.push(sub(part));
    }
    out.push("\n");
  }
  return out.join("");
}

/** SFZ を読み、引き継ぎを済ませた region の一覧と、CC の初期値を返す。 */
export function loadSfz(file, { replace = {}, cc: ccOverride = {} } = {}) {
  const top = path.dirname(file);
  const text = expand(file, {}, top, replace);
  const regions = [];
  const cc = {};
  let control = {}, global = {}, master = {}, group = {}, cur = null, level = "global";
  const flush = () => {
    if (cur) regions.push({ ...global, ...master, ...group, ...cur });
    cur = null;
  };
  for (const part of text.split(/(<[a-z]+>)/)) {
    const h = part.match(/^<([a-z]+)>$/);
    if (h) {
      flush();
      level = h[1];
      if (level === "global") (global = {}), (master = {}), (group = {});
      else if (level === "master") (master = {}), (group = {});
      else if (level === "group") group = {};
      else if (level === "region") cur = {};
      else if (level === "control") control = {};
      continue;
    }
    if (level === "curve" || level === "effect" || level === "midi") continue;
    // 「項目=値」の値には空白が入ることがある（ファイル名）。次の「項目=」の手前までを値にする
    const re = /([A-Za-z0-9_]+)=([\s\S]*?)(?=\s+[A-Za-z0-9_]+=|$)/g;
    let m;
    const body = part.trim();
    while ((m = re.exec(body))) {
      const k = m[1].toLowerCase(), v = m[2].trim();
      const target = level === "region" ? cur : level === "group" ? group : level === "master" ? master : level === "control" ? control : global;
      if (!target) continue;
      target[k] = v;
      if (level === "control" && /^set_cc\d+$/.test(k)) cc[Number(k.slice(6))] = Number(v);
    }
  }
  flush();
  Object.assign(cc, ccOverride);
  const defaultPath = control.default_path ? control.default_path.replace(/\\/g, "/") : "";
  const num = (v, d) => (v === undefined || v === "" || Number.isNaN(Number(v)) ? d : Number(v));
  const list = [];
  for (const r of regions) {
    if (!r.sample) continue;
    const lokey = keyOf(r.lokey ?? r.key), hikey = keyOf(r.hikey ?? r.key);
    if (lokey === undefined || hikey === undefined) continue;
    const curve = {};
    const conds = [];
    for (const [k, v] of Object.entries(r)) {
      if (k.startsWith("amp_velcurve_")) curve[Number(k.slice(13))] = Number(v);
      const lc = k.match(/^locc(\d+)$/), hc = k.match(/^hicc(\d+)$/);
      if (lc) conds.push({ cc: Number(lc[1]), lo: Number(v) });
      if (hc) conds.push({ cc: Number(hc[1]), hi: Number(v) });
    }
    const silent = r.sample.startsWith("*");
    list.push({
      sample: silent ? null : path.resolve(top, defaultPath, r.sample.replace(/\\/g, "/")),
      lokey, hikey,
      center: keyOf(r.pitch_keycenter) ?? keyOf(r.key) ?? lokey,
      keytrack: num(r.pitch_keytrack, 100),
      lovel: num(r.lovel, 0), hivel: num(r.hivel, 127),
      seq: num(r.seq_position, 1), seqLen: num(r.seq_length, 1),
      lorand: num(r.lorand, 0), hirand: num(r.hirand, 1),
      trigger: r.trigger === "release" || r.trigger === "release_key" ? "release" : "attack",
      group: num(r.group, 0), offBy: num(r.off_by, 0),
      volume: num(r.volume, 0), amplitude: num(r.amplitude, 100),
      pan: num(r.pan, 0), tune: num(r.tune, 0), transpose: num(r.transpose, 0),
      veltrack: num(r.amp_veltrack, 100), curve,
      attack: num(r.ampeg_attack, 0), hold: num(r.ampeg_hold, 0), decay: num(r.ampeg_decay, 0),
      sustain: num(r.ampeg_sustain, 100), release: num(r.ampeg_release, 0.001),
      offset: num(r.offset, 0), oneShot: r.loop_mode === "one_shot",
      conds,
    });
  }
  return { regions: list, cc };
}

const audioCache = new Map();
/** 音のファイル（wav・flac・ogg。16/24bit・32bit浮動小数、モノラル・ステレオ、48kHz も）を、44.1kHz のステレオで読む。 */
function readAudio(file) {
  if (audioCache.has(file)) return audioCache.get(file);
  const r = spawnSync("ffmpeg", ["-v", "quiet", "-i", file, "-ac", "2", "-ar", String(SR), "-f", "f32le", "-"], { maxBuffer: 1 << 30 });
  let res = null;
  if (r.status === 0 && r.stdout?.length) {
    const f = new Float32Array(r.stdout.buffer.slice(r.stdout.byteOffset, r.stdout.byteOffset + r.stdout.byteLength));
    const n = f.length >> 1;
    const L = new Float32Array(n), R = new Float32Array(n);
    for (let i = 0; i < n; i++) (L[i] = f[2 * i]), (R[i] = f[2 * i + 1]);
    res = { L, R };
  }
  audioCache.set(file, res);
  return res;
}

/** 強さ → 音量の倍率（amp_velcurve があればそれを、なければ amp_veltrack に沿った2乗のカーブ）。 */
function velGain(r, vel) {
  const pts = Object.keys(r.curve).map(Number).sort((a, b) => a - b);
  if (pts.length) {
    const all = [[0, 0], ...pts.map((p) => [p, r.curve[p]])];
    if (all[all.length - 1][0] < 127) all.push([127, 1]);
    for (let i = 1; i < all.length; i++) {
      if (vel <= all[i][0]) {
        const [x0, y0] = all[i - 1], [x1, y1] = all[i];
        return y0 + ((y1 - y0) * (vel - x0)) / Math.max(1, x1 - x0);
      }
    }
    return 1;
  }
  const v = (vel / 127) ** 2;
  return 1 - (r.veltrack / 100) * (1 - v);
}

/**
 * SFZ を開く。opts.replace: #include の差しかえ、opts.cc: CC の値の上書き（例: マイクの選択）。
 * 戻り値: { render(notes, total, { maxSec }) → { L, R } }
 */
export function openSfz(file, opts = {}) {
  if (!file || !fs.existsSync(file)) return null;
  const { regions, cc } = loadSfz(file, opts);
  const ccOk = (r) => r.conds.every((c) => (c.lo === undefined || (cc[c.cc] ?? 0) >= c.lo) && (c.hi === undefined || (cc[c.cc] ?? 0) <= c.hi));
  const usable = regions.filter(ccOk);
  if (!usable.length) return null;
  const seqCount = new Map();
  let rand = 0x2545f491;
  const rnd = () => {
    rand ^= rand << 13;
    rand ^= rand >>> 17;
    rand ^= rand << 5;
    return ((rand >>> 0) % 100000) / 100000;
  };
  const pitched = usable.filter((r) => r.keytrack > 0 && r.sample);
  const loKey = pitched.length ? Math.min(...pitched.map((r) => r.lokey)) : 0;
  const hiKey = pitched.length ? Math.max(...pitched.map((r) => r.hikey)) : 127;

  function regionsFor(key0, vel, trigger, clampPitch) {
    // 録音のない高さの音（ベースの最低音より低い など）は、いちばん近い録音を高さを変えて使う（7半音まで。それより離れればオクターブを折り返す）
    let key = key0;
    if (clampPitch && (key < loKey || key > hiKey)) {
      while (key < loKey - 7) key += 12;
      while (key > hiKey + 7) key -= 12;
      key = Math.max(loKey, Math.min(hiKey, key));
    }
    const cands = usable.filter((r) => r.trigger === trigger && key >= r.lokey && key <= r.hikey && vel >= r.lovel && vel <= r.hivel);
    if (!cands.length) return [];
    const id = `${trigger}:${key}:${cands[0].lovel}`;
    const n = (seqCount.get(id) ?? 0) + 1;
    seqCount.set(id, n);
    const x = rnd();
    return cands.filter((r) => (r.seqLen <= 1 || r.seq === ((n - 1) % r.seqLen) + 1) && x >= r.lorand && x < r.hirand);
  }

  /**
   * notes: [{ start, end, key, vel }]（秒）。戻り値: { L, R }（total サンプル）。
   * opts.maxSec: 1音の長さの上限。opts.pitched: true なら、録音のない高さは近い録音の高さを変えて使う（ベースなど）
   */
  function render(notes, total, { maxSec = 8, pitched: clampPitch = false } = {}) {
    const L = new Float32Array(total), R = new Float32Array(total);
    const voices = [];
    const sorted = [...notes].sort((a, b) => a.start - b.start);
    for (const n of sorted) {
      for (const trig of ["attack", "release"]) {
        const at = trig === "attack" ? n.start : n.end;
        for (const r of regionsFor(n.key, n.vel, trig, clampPitch)) {
          // 同じ group を止める（off_by）: 例えばハイハットを閉じたら、開いた音を止める
          if (trig === "attack" && r.group) for (const v of voices) if (v.offBy === r.group && v.start < at && v.stop > at) (v.stop = at + 0.006), (v.choke = true);
          if (!r.sample) continue;
          voices.push({ r, start: at, stop: trig === "attack" ? (r.oneShot ? at + maxSec : n.end) : at + maxSec, vel: n.vel, key: n.key, offBy: r.offBy, choke: false });
        }
      }
    }
    for (const v of voices) {
      const a = readAudio(v.r.sample);
      if (!a) continue;
      const r = v.r;
      const ratio = Math.pow(2, ((v.key - r.center) * (r.keytrack / 100) + r.transpose + r.tune / 100) / 12);
      const gain = Math.pow(10, r.volume / 20) * (r.amplitude / 100) * velGain(r, v.vel);
      const p = ((Math.max(-100, Math.min(100, r.pan)) + 100) / 200) * (Math.PI / 2);
      const gl = Math.cos(p) * Math.SQRT2, gr = Math.sin(p) * Math.SQRT2;
      const s0 = Math.round(v.start * SR);
      const relAt = Math.round((v.stop - v.start) * SR);
      const rel = v.choke ? 0.006 : Math.max(0.002, r.release);
      const maxLen = Math.min(Math.round((v.stop - v.start + rel) * SR), Math.round(maxSec * SR), total - s0);
      let pos = r.offset;
      const atk = Math.max(1, r.attack * SR), hold = r.hold * SR, dec = r.decay * SR, sus = r.sustain / 100;
      for (let t = 0; t < maxLen; t++, pos += ratio) {
        const i = Math.floor(pos);
        if (i + 1 >= a.L.length) break;
        const fr = pos - i;
        let env = t < atk ? t / atk : t < atk + hold ? 1 : dec > 0 ? sus + (1 - sus) * Math.exp(-((t - atk - hold) / dec) * 4.6) : 1;
        if (t > relAt) env *= Math.exp(-((t - relAt) / SR) / (rel / 4.6));
        const g = gain * env;
        L[s0 + t] += (a.L[i] * (1 - fr) + a.L[i + 1] * fr) * g * gl;
        R[s0 + t] += (a.R[i] * (1 - fr) + a.R[i + 1] * fr) * g * gr;
      }
    }
    return { L, R };
  }

  return { render, regions: usable, cc };
}
