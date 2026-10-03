// 鍵盤（ピアノ・エレクトリックピアノ）とシンセ（リード・パッド・シンセベース・808）を、繊細な音で鳴らす。render-node.mjs が使う。
// - ピアノ: 本物の録音 Osiris Piano（Versilian Studios・Karoryfer、CC0）。サステインペダル（CC64）を踏んでいる間は音を伸ばす
// - エレクトリックピアノ・シンセ: synth-engine.mjs（計算で作る。素材は使わない）
// 置き換えるのは、音源で電子的な音色や鍵盤を選んでいるパートだけ（フルート・サックス・合唱などは、そのまま）。
import fs from "fs";
import path from "path";
import { openSfz } from "./sfz-player.mjs";
import { renderSynth } from "./synth-engine.mjs";
import { sampleLibDir, notesOf } from "./real-rhythm.mjs";

/** サステインペダル（CC64）を踏んでいる間に離した音は、ペダルを上げるまで伸ばす。 */
function notesWithPedal(midi, ch) {
  const notes = notesOf(midi, ch);
  const pedal = [];
  for (const tr of midi.tracks) {
    for (const ev of tr.events) {
      if ((ev.statusByte & 0xf0) === 0xb0 && (ev.statusByte & 0x0f) === ch && ev.data[0] === 64) pedal.push({ t: midi.midiTicksToSeconds(ev.ticks), down: ev.data[1] >= 64 });
    }
  }
  if (!pedal.length) return notes;
  pedal.sort((a, b) => a.t - b.t);
  const downAt = (t) => {
    let d = false;
    for (const p of pedal) {
      if (p.t > t) break;
      d = p.down;
    }
    return d;
  };
  return notes.map((n) => {
    if (!downAt(n.end)) return n;
    const up = pedal.find((p) => p.t > n.end && !p.down);
    return { ...n, end: up ? Math.max(n.end, up.t) : n.end + 2 };
  });
}

/** このチャンネルを、どの音で鳴らすか。null なら従来の音源のまま。 */
function voiceFor(inst, program, style) {
  if (inst === "piano" || ((inst === "keys" || inst === "harpsichord") && program <= 3)) return { kind: "piano" };
  if (inst === "keys" && (program === 4 || program === 5)) return { kind: "synth", preset: "epiano" };
  if (inst === "lead" && program >= 80 && program <= 87) return { kind: "synth", preset: "lead" };
  if (inst === "pad" && program >= 88 && program <= 95) return { kind: "synth", preset: "pad" };
  if (inst === "sub808") return { kind: "synth", preset: "bass808" };
  if (inst === "bass" && (program === 38 || program === 39)) return { kind: "synth", preset: "synthBass" };
  return null;
}

/**
 * 戻り値: { parts: { パート名: { L, R } }, muted: Set<チャンネル>, used: [名前] }
 * groupOfChannel: チャンネル → パート名（mix-plan.ts の groupOf と同じ）。skip: ほかで鳴らすことにしたチャンネル
 */
export function renderRealKeys({ midi, instruments, programs, style, total, groupOfChannel, skip = new Set() }) {
  const parts = {};
  const muted = new Set();
  const used = new Set();
  const lib = sampleLibDir();
  const pianoFile = lib && path.join(lib, "Osiris_Piano", "Osiris_Piano-main", "Programs", "01-natural.sfz");
  let piano = null;
  const add = (g, buf, gain = 1) => {
    if (!parts[g]) parts[g] = { L: new Float32Array(total), R: new Float32Array(total) };
    for (let i = 0; i < total; i++) (parts[g].L[i] += buf.L[i] * gain), (parts[g].R[i] += buf.R[i] * gain);
  };
  for (const c of Object.keys(instruments).map(Number)) {
    if (c === 9 || skip.has(c)) continue;
    const v = voiceFor(instruments[c], programs[c] ?? 0, style);
    if (!v) continue;
    const g = groupOfChannel(c);
    if (v.kind === "piano") {
      if (!piano && pianoFile && fs.existsSync(pianoFile)) piano = openSfz(pianoFile);
      if (!piano) continue;
      const notes = notesWithPedal(midi, c);
      if (!notes.length) continue;
      add(g, piano.render(notes, total, { maxSec: 12, pitched: true }));
      used.add("Osiris Piano");
    } else {
      const notes = instruments[c] === "keys" ? notesWithPedal(midi, c) : notesOf(midi, c);
      if (!notes.length) continue;
      add(g, renderSynth(v.preset, notes, total, { seed: c + 1 }));
      used.add(`シンセ（${v.preset}）`);
    }
    muted.add(c);
  }
  return { parts, muted, used: [...used] };
}
