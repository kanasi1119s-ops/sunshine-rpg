// 本物のギターの録音（SFZ形式のサンプル集）で、ギターのパートを鳴らす。render-node.mjs が使う。
// 使う録音: Karoryfer「Black And Green Guitars」（CC0＝自由に使える。アンプを通す前のギターの音＝DI）。
//   https://github.com/sfzinstruments/karoryfer.black-and-green-guitars
//   リポジトリには入れない（約560MB）。置き場所は、環境変数 SUNSHINE_GUITAR_SFZ、なければ「ユーザーのフォルダ/Music/guitar-samples」。
//   見つからなければ null を返し、これまでどおり音源（サウンドフォント）のギターで鳴らす。
//
// 鳴らし方（生のギターに近づけるための決まりごと）:
// - 音の高さと強さに合う録音を選ぶ。同じ音が続くときは、毎回ちがう録音（4種類）を順に使う（同じ音のくり返しは機械っぽく聞こえる）
// - 短い刻み（brief）は「短く切った弾き方（staccato）」の録音、それ以外は「鳴らしっぱなし（twang）」の録音
// - 次の和音を弾いたら、前の和音の音は止める（同じ弦を弾き直すので、前の音は鳴り続けない）
// - 録音より低い音は、少しなら下げて使い、離れていれば1オクターブ上の録音を使う
import fs from "fs";
import os from "os";
import path from "path";

const SR = 44100;
/** これより短い音（秒）は、短く切った弾き方の録音を使う。 */
const SHORT_SEC = 0.13;

/** 人が弾いたような、ごくわずかなずれ（同じ種からは同じずれ）。2回弾いたギターを左右に置くときに、左右で別のずれにする。 */
export function humanizeNotes(notes, { ms = 0, vel = 0, seed = 1 } = {}) {
  if (!ms && !vel) return notes;
  let a = seed >>> 0;
  const rnd = () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  // 同じ和音（30ms以内に始まる音）は、同じだけずらす（和音の中の順番は崩さない）
  let lastStart = -1, shift = 0;
  return [...notes].sort((x, y) => x.start - y.start).map((n) => {
    if (n.start - lastStart > 0.03) shift = (rnd() * 2 - 1) * ms / 1000;
    lastStart = n.start;
    const v = Math.max(1, Math.min(127, Math.round(n.vel + (rnd() * 2 - 1) * vel)));
    return { ...n, start: Math.max(0, n.start + shift), end: Math.max(n.start + shift + 0.01, n.end + shift), vel: v };
  });
}

export function guitarSampleDir() {
  const cands = [process.env.SUNSHINE_GUITAR_SFZ, path.join(os.homedir(), "Music", "guitar-samples")].filter(Boolean);
  return cands.find((d) => fs.existsSync(path.join(d, "Programs", "modules", "maps_green", "ord.sfz"))) ?? null;
}

/** SFZ の region を読む（このサンプル集で使っている項目だけ）。 */
function parseSfz(file) {
  const base = path.dirname(path.dirname(path.dirname(file))); // Programs/modules/maps_green → Programs
  const text = fs.readFileSync(file, "utf8");
  const regions = [];
  for (const chunk of text.split("<region>").slice(1)) {
    const r = { lovel: 0, hivel: 127, seq: 1, seqLen: 1 };
    for (const line of chunk.split(/\r?\n/)) {
      const m = line.match(/^\s*([a-z_0-9]+)=(.+?)\s*$/);
      if (!m) continue;
      const [, key, val] = m;
      if (key === "sample") r.sample = path.resolve(base, val.replace(/\\/g, "/"));
      else if (key === "lokey") r.lokey = Number(val);
      else if (key === "hikey") r.hikey = Number(val);
      else if (key === "lovel") r.lovel = Number(val);
      else if (key === "hivel") r.hivel = Number(val);
      else if (key === "pitch_keycenter") r.center = Number(val);
      else if (key === "seq_position") r.seq = Number(val);
      else if (key === "seq_length") r.seqLen = Number(val);
    }
    if (r.sample && r.lokey !== undefined) {
      r.hikey ??= r.lokey;
      r.center ??= r.lokey;
      regions.push(r);
    }
  }
  return regions;
}

/** 16・24・32bit の PCM WAV（モノラル・ステレオ）を読んで、モノラルの Float32Array にする。 */
function readWav(file) {
  const b = fs.readFileSync(file);
  let p = 12;
  let fmt = null;
  while (p + 8 <= b.length) {
    const id = b.toString("ascii", p, p + 4);
    const size = b.readUInt32LE(p + 4);
    if (id === "fmt ") fmt = { ch: b.readUInt16LE(p + 10), rate: b.readUInt32LE(p + 12), bits: b.readUInt16LE(p + 22), tag: b.readUInt16LE(p + 8) };
    if (id === "data" && fmt) {
      const bytes = fmt.bits / 8;
      const frames = Math.floor(size / (bytes * fmt.ch));
      const out = new Float32Array(frames);
      const float = fmt.tag === 3 || (fmt.tag === 0xfffe && fmt.bits === 32 && false);
      for (let i = 0; i < frames; i++) {
        let s = 0;
        for (let c = 0; c < fmt.ch; c++) {
          const o = p + 8 + (i * fmt.ch + c) * bytes;
          if (float) s += b.readFloatLE(o);
          else if (bytes === 2) s += b.readInt16LE(o) / 32768;
          else if (bytes === 3) s += b.readIntLE(o, 3) / 8388608;
          else s += b.readInt32LE(o) / 2147483648;
        }
        out[i] = s / fmt.ch;
      }
      return { data: out, rate: fmt.rate };
    }
    p += 8 + size + (size & 1);
  }
  throw new Error("WAV を読めません: " + file);
}

export function openGuitarSampler(dir = guitarSampleDir()) {
  if (!dir) return null;
  const maps = path.join(dir, "Programs", "modules", "maps_green");
  const ord = parseSfz(path.join(maps, "ord.sfz"));
  const stac = parseSfz(path.join(maps, "stac.sfz"));
  if (!ord.length) return null;
  const cache = new Map();
  const load = (f) => {
    if (!cache.has(f)) cache.set(f, readWav(f));
    return cache.get(f);
  };
  const minKey = Math.min(...ord.map((r) => r.lokey));
  const maxKey = Math.max(...ord.map((r) => r.hikey));
  const rr = new Map();

  /** 音の高さ・強さ・弾き方に合う録音を選ぶ。 */
  function pick(key, vel, short) {
    let k = key;
    let shift = 0;
    if (k < minKey) {
      // 低すぎる音: 5半音までは録音を下げて使い、それより低ければ1オクターブ上で弾く
      if (minKey - k <= 5) {
        shift = k - minKey;
        k = minKey;
      } else {
        while (k < minKey) k += 12;
      }
    }
    while (k > maxKey) k -= 12;
    const set = short && stac.length ? stac : ord;
    let cands = set.filter((r) => k >= r.lokey && k <= r.hikey && vel >= r.lovel && vel <= r.hivel);
    if (!cands.length) cands = set.filter((r) => k >= r.lokey && k <= r.hikey);
    if (!cands.length) return null;
    const id = `${short ? "s" : "o"}:${k}:${cands[0].lovel}`;
    const n = (rr.get(id) ?? 0) + 1;
    rr.set(id, n);
    const len = cands[0].seqLen || 1;
    const r = cands.find((c) => c.seq === ((n - 1) % len) + 1) ?? cands[(n - 1) % cands.length];
    return { region: r, semis: key + shift - k + (k - r.center) };
  }

  /**
   * 音符（秒）の並びを、1本のギターの音にする。
   * notes: [{ start, end, key, vel }]（同じ楽器の音を時間順に）。戻り値: モノラルの Float32Array（total サンプル）
   */
  function render(notes, total) {
    const out = new Float32Array(total);
    const sorted = [...notes].sort((a, b) => a.start - b.start);
    // 次の和音（30ms より後に始まる音）が来たら、それまでの音を止める
    for (let i = 0; i < sorted.length; i++) {
      const n = sorted[i];
      const next = sorted.find((m, j) => j > i && m.start > n.start + 0.03);
      n.choked = !!next && next.start + 0.004 < n.end;
      n.stop = Math.min(n.end, next ? next.start + 0.004 : n.end);
    }
    for (const n of sorted) {
      const dur = n.stop - n.start;
      const short = dur < SHORT_SEC;
      const pk = pick(n.key, n.vel, short);
      if (!pk) continue;
      const smp = load(pk.region.sample);
      const ratio = Math.pow(2, pk.semis / 12) * (smp.rate / SR);
      const start = Math.round(n.start * SR);
      // 消え方は指数カーブ（最初は速く、あとはゆっくり）。弾き直しは時定数35ms、手を離したときは50ms（短い音は25ms）
      const tau = short ? 0.025 : n.choked ? 0.035 : 0.05;
      const release = tau * 5;
      const endS = Math.round((n.stop + release) * SR);
      const relS = Math.round(n.stop * SR);
      const gain = 0.35 + 0.65 * Math.pow(n.vel / 127, 1.3);
      let pos = 0;
      for (let t = start; t < endS && t < total; t++, pos += ratio) {
        const i = Math.floor(pos);
        if (i + 1 >= smp.data.length) break;
        const fr = pos - i;
        let v = smp.data[i] * (1 - fr) + smp.data[i + 1] * fr;
        if (t < start + 44) v *= (t - start) / 44; // 1ms で立ち上げる（プチッという音を防ぐ）
        if (t > relS) v *= Math.exp(-(t - relS) / SR / tau);
        out[t] += v * gain;
      }
    }
    return out;
  }

  return { render, dir };
}
