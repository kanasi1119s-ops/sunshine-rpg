// ブラウザ（Playwright・Chromium）なしで、曲（Score）を音にする。録音音源（サウンドフォント）を spessasynth_core で鳴らし、
// パート（ドラム・ベース・ギター・鍵盤・弦…）ごとに別々に音にして、パートごとに音量・EQ・圧縮・残響をととのえてから合わせる。
// FFmpeg が必要（なければ、ととのえずに合わせるだけの簡易版になる）。Node だけで動くので、クラウドでも PC でも同じ結果になる。
import fs from "fs";
import os from "os";
import path from "path";
import { spawnSync } from "child_process";
import { BasicMIDI, SoundBankLoader, SpessaSynthProcessor, SpessaSynthSequencer } from "spessasynth_core";
import { fileURLToPath } from "url";

const ROOT = path.resolve(fileURLToPath(new URL("../../", import.meta.url)));

const SR = 44100;
const BLOCK = 128;
export const DEFAULT_SOUNDFONT = path.join(ROOT, "assets-src", "soundfont", "FluidR3Mono_GM.sf3");

/** 32bit浮動小数のステレオWAVを少しずつ書く（メモリを使わない）。 */
class StemWriter {
  constructor(file) {
    this.file = file;
    this.fd = fs.openSync(file, "w");
    this.bytes = 0;
    fs.writeSync(this.fd, Buffer.alloc(44));
    this.buf = Buffer.alloc(BLOCK * 8);
  }
  write(left, right, n) {
    const b = this.buf.length >= n * 8 ? this.buf : Buffer.alloc(n * 8);
    for (let i = 0; i < n; i++) {
      b.writeFloatLE(left[i], i * 8);
      b.writeFloatLE(right[i], i * 8 + 4);
    }
    fs.writeSync(this.fd, b, 0, n * 8);
    this.bytes += n * 8;
  }
  close() {
    const h = Buffer.alloc(44);
    h.write("RIFF", 0);
    h.writeUInt32LE(36 + this.bytes, 4);
    h.write("WAVEfmt ", 8);
    h.writeUInt32LE(16, 16);
    h.writeUInt16LE(3, 20); // IEEE float
    h.writeUInt16LE(2, 22);
    h.writeUInt32LE(SR, 24);
    h.writeUInt32LE(SR * 8, 28);
    h.writeUInt16LE(8, 32);
    h.writeUInt16LE(32, 34);
    h.write("data", 36);
    h.writeUInt32LE(this.bytes, 40);
    fs.writeSync(this.fd, h, 0, 44, 0);
    fs.closeSync(this.fd);
  }
}

/** 残響のインパルス応答（左右で違う、減衰するノイズ。高い音ほど早く消える）。 */
function writeReverbIr(file, seconds = 2.2) {
  const n = Math.floor(SR * seconds);
  const w = new StemWriter(file);
  let seed = 12345;
  const rnd = () => {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    return seed / 4294967296 * 2 - 1;
  };
  const L = new Float32Array(n);
  const R = new Float32Array(n);
  let lpL = 0;
  let lpR = 0;
  const pre = Math.floor(SR * 0.018);
  for (let i = pre; i < n; i++) {
    const t = (i - pre) / SR;
    const env = Math.exp(-t / 0.55);
    // 時間がたつほど高域が減る（ローパスの係数を、時間とともに強める）
    const a = Math.min(0.97, 0.35 + t * 0.4);
    lpL = a * lpL + (1 - a) * rnd();
    lpR = a * lpR + (1 - a) * rnd();
    L[i] = lpL * env;
    R[i] = lpR * env;
  }
  // 全体の大きさをそろえる（エネルギーが一定になるように）
  let e = 0;
  for (let i = 0; i < n; i++) e += L[i] * L[i] + R[i] * R[i];
  const g = 1 / Math.sqrt(e / 2);
  for (let i = 0; i < n; i++) {
    L[i] *= g;
    R[i] *= g;
  }
  for (let i = 0; i < n; i += BLOCK) w.write(L.subarray(i, i + BLOCK), R.subarray(i, i + BLOCK), Math.min(BLOCK, n - i));
  w.close();
}

function hasFfmpeg() {
  return spawnSync("ffmpeg", ["-version"], { encoding: "utf8" }).status === 0;
}

/**
 * 曲（Score）を、パート別に音にして、ととのえて合わせる。
 * @returns {{wav:string, groups:Record<string,{db:number|null,gain:number|null}>, seconds:number, ffmpeg:boolean, peak:number|null}}
 */
export async function renderMix(kit, score, { edition = "real", outWav, soundfont = DEFAULT_SOUNDFONT, tailSec = 3, keepDir = null, flavors = [] } = {}) {
  const T0 = Date.now();
  const k = await kit.mixKit(score, edition);
  const { mix } = k;
  const sf = fs.readFileSync(soundfont);
  const synth = new SpessaSynthProcessor(SR, { eventsEnabled: false, maxBufferSize: BLOCK });
  synth.soundBankManager.addSoundBank(SoundBankLoader.fromArrayBuffer(sf.buffer.slice(sf.byteOffset, sf.byteOffset + sf.byteLength)), "main");
  await synth.processorInitialized;
  const midi = BasicMIDI.fromArrayBuffer(k.midi.buffer.slice(k.midi.byteOffset, k.midi.byteOffset + k.midi.byteLength));
  const seq = new SpessaSynthSequencer(synth);
  seq.loadNewSongList([midi]);
  seq.loopCount = 0;
  seq.play();

  const work = fs.mkdtempSync(path.join(os.tmpdir(), "mix-"));
  const groupOfChannel = (ch) => (ch === 9 ? "drums" : mix.groupOf(k.instruments[ch]));
  const present = [...new Set(Array.from({ length: 16 }, (_, ch) => groupOfChannel(ch)))].filter((g) => g === "drums" || Object.keys(k.instruments).some((c) => Number(c) !== 9 && groupOfChannel(Number(c)) === g));
  const writers = {};
  const stats = {};
  const WIN = Math.floor((SR * 0.4) / BLOCK) * BLOCK;
  for (const g of present) {
    writers[g] = new StemWriter(path.join(work, `${g}.wav`));
    stats[g] = { acc: 0, n: 0, sum: 0, count: 0 };
  }
  const total = Math.ceil((k.seconds + tailSec) * SR);
  const outs = Array.from({ length: 16 }, () => [new Float32Array(BLOCK), new Float32Array(BLOCK)]);
  const fxL = new Float32Array(BLOCK);
  const fxR = new Float32Array(BLOCK);
  const fxWriter = new StemWriter(path.join(work, "fx.wav"));
  const fxStat = { acc: 0, n: 0, sum: 0, count: 0 };
  const gl = {};
  const gr = {};
  for (const g of present) {
    gl[g] = new Float32Array(BLOCK);
    gr[g] = new Float32Array(BLOCK);
  }
  const tally = (st, l, r, n) => {
    for (let i = 0; i < n; i++) st.acc += l[i] * l[i] + r[i] * r[i];
    st.n += n;
    if (st.n >= WIN) {
      const p = st.acc / (2 * st.n);
      if (Math.sqrt(p) > 0.001) {
        st.sum += p;
        st.count++;
      }
      st.acc = 0;
      st.n = 0;
    }
  };
  for (let done = 0; done < total; done += BLOCK) {
    const n = Math.min(BLOCK, total - done);
    seq.processTick();
    for (const o of outs) {
      o[0].fill(0);
      o[1].fill(0);
    }
    fxL.fill(0);
    fxR.fill(0);
    synth.processSplit(outs, fxL, fxR, 0, n);
    for (const g of present) {
      gl[g].fill(0);
      gr[g].fill(0);
    }
    for (let ch = 0; ch < 16; ch++) {
      const g = groupOfChannel(ch);
      if (!gl[g]) continue;
      for (let i = 0; i < n; i++) {
        gl[g][i] += outs[ch][0][i];
        gr[g][i] += outs[ch][1][i];
      }
    }
    for (const g of present) {
      writers[g].write(gl[g], gr[g], n);
      tally(stats[g], gl[g], gr[g], n);
    }
    fxWriter.write(fxL, fxR, n);
    tally(fxStat, fxL, fxR, n);
  }
  for (const g of present) writers[g].close();
  fxWriter.close();
  const dbOf = (st) => (st.count ? 10 * Math.log10(st.sum / st.count) : null);

  const plan = mix.mixPlan(score.style, flavors);
  const groups = {};
  for (const g of present) {
    const db = dbOf(stats[g]);
    groups[g] = { db, gain: mix.gainForTarget(db, plan[g].target) };
  }
  const active = present.filter((g) => groups[g].gain !== null);
  const fxDb = dbOf(fxStat);

  const tSynth = Date.now() - T0;
  const ffmpeg = hasFfmpeg();
  let peak = null;
  if (ffmpeg && active.length) {
    writeReverbIr(path.join(work, "ir.wav"));
    const inputs = [];
    const flt = [];
    const dry = [];
    const rvSends = [];
    const dlSends = [];
    const beatMs = 60000 / k.tempoBpm;
    active.forEach((g, i) => {
      inputs.push("-i", path.join(work, `${g}.wav`));
      const m = plan[g];
      const chain = mix.dryChain(m);
      flt.push(`[${i}:a]volume=${groups[g].gain.toFixed(2)}dB,${chain}[d_${g}]`);
      const outs2 = [`d1_${g}`];
      if (m.reverb > 0) outs2.push(`r_${g}`);
      if (m.delay > 0) outs2.push(`l_${g}`);
      if (outs2.length === 1) {
        dry.push(`[d_${g}]`);
      } else {
        flt.push(`[d_${g}]asplit=${outs2.length}${outs2.map((o) => `[${o}]`).join("")}`);
        dry.push(`[d1_${g}]`);
        if (m.reverb > 0) {
          flt.push(`[r_${g}]volume=${(m.reverb * 0.5).toFixed(3)}[rs_${g}]`);
          rvSends.push(`[rs_${g}]`);
        }
        if (m.delay > 0) {
          flt.push(`[l_${g}]volume=${m.delay.toFixed(3)}[ls_${g}]`);
          dlSends.push(`[ls_${g}]`);
        }
      }
    });
    const irIndex = active.length;
    inputs.push("-i", path.join(work, "ir.wav"));
    const fxIndex = active.length + 1;
    inputs.push("-i", path.join(work, "fx.wav"));
    flt.push(`[${fxIndex}:a]volume=0.8[fx]`);
    const mixIn = [...dry, "[fx]"];
    flt.push(`${dry.join("")}amix=inputs=${dry.length}:normalize=0:dropout_transition=0[drymix]`);
    const wet = [];
    if (rvSends.length) {
      flt.push(`${rvSends.join("")}amix=inputs=${rvSends.length}:normalize=0[rvin]`);
      flt.push(`[rvin][${irIndex}:a]afir=dry=0:wet=1[rvret]`);
      wet.push("[rvret]");
    }
    if (dlSends.length) {
      flt.push(`${dlSends.join("")}amix=inputs=${dlSends.length}:normalize=0[dlin]`);
      flt.push(`[dlin]aecho=0.9:0.55:${Math.round(beatMs * 0.75)}|${Math.round(beatMs * 1.5)}:0.38|0.2[dlret]`);
      wet.push("[dlret]");
    }
    void mixIn;
    flt.push(`[drymix]${wet.join("")}[fx]amix=inputs=${2 + wet.length}:normalize=0:dropout_transition=0,acompressor=threshold=0.16:ratio=2:attack=30:release=250:makeup=1,alimiter=limit=0.95:level=disabled[out]`);
    const outFile = outWav ?? path.join(work, "mix.wav");
    const r = spawnSync("ffmpeg", ["-y", "-v", "error", ...inputs, "-filter_complex", flt.join(";"), "-map", "[out]", "-ar", String(SR), "-c:a", "pcm_s16le", outFile], { encoding: "utf8" });
    if (r.status !== 0) throw new Error("ffmpeg の合成に失敗しました:\n" + (r.stderr ?? "").slice(-900));
  } else {
    // FFmpeg がない: 音量だけそろえて合わせる簡易版
    throw new Error("FFmpeg が見つかりません。setup_windows.ps1 で FFmpeg を入れてください（パート別ミックスに必要です）。");
  }
  if (keepDir) fs.cpSync(work, keepDir, { recursive: true });
  fs.rmSync(work, { recursive: true, force: true });
  return { wav: outWav, groups, seconds: k.seconds, ffmpeg, fxDb, peak, timing: { synthMs: tSynth, totalMs: Date.now() - T0 } };
}
