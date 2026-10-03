// メタル系の曲のギターを、METAL-GTX（Unreal Instruments、DI録音のメタル用ギター音源）で鳴らす。render-node.mjs が使う。
//   https://unreal-instruments.wixsite.com/unreal-instruments/metal-gtx
//   ライセンス: 同梱の「説明および注意事項.txt」に「ライセンスフリーです・クレジット表記は不要です」とある。
//   リポジトリには入れない（約1.4GB）。置き場所は、環境変数 SUNSHINE_METAL_GTX、
//   なければ「ユーザーのフォルダ/Music/sample-libraries/METAL-GTX/UI_METAL-GTX」。見つからなければ null を返す。
//
// 鳴らし方（METAL-GTX の作りに合わせる）:
// - ふつうの音は「サステイン」、短い刻みは「パームミュート」（すぐに10%まで減衰する）の録音
// - 拍の頭と8分の表はダウンピッキング、16分の裏はアップピッキングの録音（オルタネイトピッキング）
// - 強弱は、強く弾くほど明るくなるフィルター（音源と同じ: 30Hz × 2^(8 × 強さ/127)）で表す
// - 同じ音は、録り分け（最大9種類）を順に使う。次の和音を弾いたら前の音は止める
import fs from "fs";
import os from "os";
import path from "path";
import { spawnSync } from "child_process";

const SR = 44100;
const PCS = { c: 0, d: 2, e: 4, f: 5, g: 7, a: 9, b: 11 };

export function metalGtxDir() {
  const cands = [process.env.SUNSHINE_METAL_GTX, path.join(os.homedir(), "Music", "sample-libraries", "METAL-GTX", "UI_METAL-GTX")].filter(Boolean);
  return cands.find((d) => fs.existsSync(path.join(d, "Programs", "Individual Patchs", "METAL-GTX_Full", "Sus_Down.sfz"))) ?? null;
}

/** SFZ の音名（c4=60）を MIDI の番号に。数字ならそのまま。 */
function keyOf(v) {
  if (/^-?\d+$/.test(v)) return Number(v);
  const m = v.trim().toLowerCase().match(/^([a-g])(#|b)?(-?\d+)$/);
  if (!m) return NaN;
  return (Number(m[3]) + 1) * 12 + PCS[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0);
}

/** <global>・<group> の設定を引き継ぎながら、region を読む。CC23（強いサステインの層）が必要な region は除く。 */
function parseSfz(file, baseDir) {
  // 音のファイルの場所は、本体のパッチ（Programs/*.sfz）から見た相対の場所で書かれている
  const dir = baseDir;
  const text = fs.readFileSync(file, "utf8").replace(/\/\/[^\n]*/g, "");
  const regions = [];
  let level = null;
  let global = {}, group = {}, cur = null;
  const flush = () => {
    if (!cur) return;
    const r = { ...global, ...group, ...cur };
    if (r.sample && !(Number(r.locc23 ?? 0) >= 65)) regions.push(r);
    cur = null;
  };
  for (const tok of text.split(/(<[a-z]+>)|\s+/).filter(Boolean)) {
    if (tok.startsWith("<")) {
      flush();
      level = tok;
      if (level === "<global>") (global = {}), (group = {});
      if (level === "<group>") group = {};
      if (level === "<region>") cur = {};
      continue;
    }
    const eq = tok.indexOf("=");
    if (eq < 0) continue;
    const k = tok.slice(0, eq), v = tok.slice(eq + 1);
    const target = level === "<region>" ? cur : level === "<group>" ? group : global;
    if (target) target[k] = v;
  }
  flush();
  return regions.map((r) => ({
    sample: path.resolve(dir, r.sample.replace(/\\/g, "/")),
    lokey: keyOf(r.lokey ?? r.key),
    hikey: keyOf(r.hikey ?? r.key),
    center: keyOf(r.pitch_keycenter ?? r.lokey ?? r.key),
    seq: Number(r.seq_position ?? 1),
    seqLen: Number(r.seq_length ?? 1),
    tune: Number(r.tune ?? 0),
    volume: Number(r.volume ?? 0),
  })).filter((r) => Number.isFinite(r.lokey) && Number.isFinite(r.hikey) && Number.isFinite(r.center));
}

function readAudio(file) {
  const r = spawnSync("ffmpeg", ["-v", "quiet", "-i", file, "-ac", "1", "-ar", String(SR), "-f", "f32le", "-"], { maxBuffer: 1 << 28 });
  if (r.status !== 0 || !r.stdout?.length) throw new Error("音のファイルを読めません: " + file);
  const b = r.stdout;
  return new Float32Array(b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength));
}

export function openMetalSampler(dir = metalGtxDir()) {
  if (!dir) return null;
  const patch = (n) => parseSfz(path.join(dir, "Programs", "Individual Patchs", "METAL-GTX_Full", `${n}.sfz`), path.join(dir, "Programs"));
  const sets = { susD: patch("Sus_Down"), susU: patch("Sus_Up"), muteD: patch("Mute_Down"), muteU: patch("Mute_Up") };
  if (!sets.susD.length || !sets.muteD.length) return null;
  const cache = new Map();
  const load = (f) => {
    if (!cache.has(f)) cache.set(f, readAudio(f));
    return cache.get(f);
  };
  const rr = new Map();
  const pick = (set, key) => {
    let k = key;
    const lo = Math.min(...set.map((r) => r.lokey)), hi = Math.max(...set.map((r) => r.hikey));
    while (k < lo) k += 12;
    while (k > hi) k -= 12;
    const cands = set.filter((r) => k >= r.lokey && k <= r.hikey);
    if (!cands.length) return null;
    const id = `${cands[0].sample.split(/[\\/]/).slice(-2, -1)}:${k}`;
    const n = (rr.get(id) ?? 0) + 1;
    rr.set(id, n);
    const len = Math.max(1, ...cands.map((c) => c.seqLen));
    const r = cands.find((c) => c.seq === ((n - 1) % len) + 1) ?? cands[(n - 1) % cands.length];
    return { r, semis: k - r.center + r.tune / 100 + (key - k) };
  };

  /** 2次のローパス（強く弾くほど明るく）。 */
  function lowpass(buf, cutoff) {
    const w = (2 * Math.PI * Math.min(cutoff, SR * 0.45)) / SR;
    const q = 0.707, alpha = Math.sin(w) / (2 * q), cw = Math.cos(w);
    const a0 = 1 + alpha;
    const b0 = (1 - cw) / 2 / a0, b1 = (1 - cw) / a0, b2 = b0, a1 = (-2 * cw) / a0, a2 = (1 - alpha) / a0;
    let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
    for (let i = 0; i < buf.length; i++) {
      const x = buf[i];
      const y = b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2;
      x2 = x1; x1 = x; y2 = y1; y1 = y;
      buf[i] = y;
    }
  }

  /**
   * notes: [{ start, end, key, vel }]（秒）。beatSec: 1拍の長さ（秒）。戻り値: モノラルの Float32Array（total サンプル）
   */
  function render(notes, total, { beatSec = 0.5 } = {}) {
    const out = new Float32Array(total);
    const sorted = [...notes].sort((a, b) => a.start - b.start);
    for (let i = 0; i < sorted.length; i++) {
      const n = sorted[i];
      const next = sorted.find((m, j) => j > i && m.start > n.start + 0.03);
      n.stop = Math.min(n.end, next ? next.start + 0.004 : n.end);
    }
    for (const n of sorted) {
      const dur = n.stop - n.start;
      // 楽譜でミュートにした刻み（16分）は、拍の 0.2 くらいの長さで来る（midi-export.ts）。0.35拍より短ければパームミュート。8分は鳴らしたまま
      const muted = dur < beatSec * 0.35;
      // 16分の裏（拍の 1/4・3/4 の位置）はアップピッキング
      const frac = ((n.start / beatSec) % 1 + 1) % 1;
      const up = Math.abs(frac - 0.25) < 0.08 || Math.abs(frac - 0.75) < 0.08;
      const set = muted ? (up ? sets.muteU : sets.muteD) : up ? sets.susU : sets.susD;
      const pk = pick(set.length ? set : sets.susD, n.key);
      if (!pk) continue;
      const smp = load(pk.r.sample);
      const ratio = Math.pow(2, pk.semis / 12);
      const start = Math.round(n.start * SR);
      const relS = Math.round(n.stop * SR);
      const endS = relS + Math.round(0.1 * SR); // ampeg_release=0.1
      const len = Math.min(endS - start, Math.floor((smp.length - 2) / ratio));
      if (len <= 0) continue;
      const note = new Float32Array(len);
      let pos = 0;
      for (let t = 0; t < len; t++, pos += ratio) {
        const i = Math.floor(pos), fr = pos - i;
        note[t] = smp[i] * (1 - fr) + smp[i + 1] * fr;
      }
      lowpass(note, 30 * Math.pow(2, (8 * n.vel) / 127));
      const vol = Math.pow(10, pk.r.volume / 20);
      for (let t = 0; t < len; t++) {
        const sec = t / SR;
        let env = Math.min(1, sec / 0.001);
        if (muted) env *= sec < 0.4 ? 1 - 0.9 * (sec / 0.4) : 0.1; // decay 0.4秒で 10% に
        if (start + t > relS) env *= Math.max(0, 1 - (start + t - relS) / (endS - relS));
        if (start + t < total) out[start + t] += note[t] * env * vol;
      }
    }
    return out;
  }

  return { render, dir };
}
