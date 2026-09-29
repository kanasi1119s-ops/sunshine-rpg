// サンシャイン作曲ソフト: 自動作曲＋ピアノロールでの手直し＋実楽器の音での試聴＋MIDI・プロジェクトの書き出し。
// 再生エンジン（録音音源・ギターアンプ・ドラムの仕上げ）と作曲エンジンは、ゲーム本体のものをそのまま使う。
import soundfontUrl from "../../src/audio/soundfont/game.sf3?url";
import processorUrl from "spessasynth_lib/dist/spessasynth_processor.min.js?url";
import { AudioEngine } from "../../src/audio/audio-engine";
import { STYLE_LABEL } from "../../src/audio/catalog";
import { midiToName } from "../../src/audio/compose";
import { notesToEvents, noteStartAt, resizeNote, toggleNote, trackToNotes, trackTotalBeats } from "../../src/audio/edit";
import { composeFinale, FINALES } from "../../src/audio/finale";
import { GM_PROGRAM } from "../../src/audio/gm-map";
import { scoreToMidi } from "../../src/audio/midi-export";
import { NamHost } from "../../src/audio/nam/nam-host";
import { buildNewSong } from "../../src/audio/newsong";
import { noteNameToMidi } from "../../src/audio/note";
import { ps2Edition } from "../../src/audio/ps2-edition";
import { realEdition } from "../../src/audio/real-edition";
import { getScoreDurationSec, REST, type AmpSetting, type Instrument, type Score, type Track } from "../../src/audio/score";
import { composeSong, type Style } from "../../src/audio/songwriter";
import { encodeWav } from "../../src/audio/wav";

// 1ファイルのHTMLでは外部ファイルを読み込めないので、埋め込んだ素材（データURL）を録音音源の再生に渡す
function bytesOf(dataUrl: string): Uint8Array {
  const bin = atob(dataUrl.slice(dataUrl.indexOf(",") + 1));
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
try {
  globalThis.__sampledAssets = { soundfont: bytesOf(soundfontUrl).buffer as ArrayBuffer, processorUrl };
} catch (error) {
  console.warn("録音音源の埋め込みを読めませんでした:", error);
}
// 無料のアンプシミュレーター（NAM）: ビルドのときに埋め込んだワークレットとWASMを渡す
declare const __NAM_PROCESSOR__: string;
declare const __NAM_WASM__: string;
const engine = new AudioEngine();
try {
  if (typeof __NAM_PROCESSOR__ === "string" && typeof __NAM_WASM__ === "string") {
    const bin = atob(__NAM_WASM__);
    const wasm = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) wasm[i] = bin.charCodeAt(i);
    globalThis.__namAssets = { processorUrl: __NAM_PROCESSOR__, wasm: wasm.buffer as ArrayBuffer };
    engine.setNamHost(new NamHost());
  }
} catch (error) {
  console.warn("アンプシミュレーター（NAM）を読み込めませんでした:", error);
}

const INSTRUMENTS: [Instrument, string][] = [
  ["kick", "バスドラム"], ["snare", "スネア"], ["hihat", "ハイハット"], ["crash", "クラッシュ"], ["tom", "タム"],
  ["bass", "ベース"], ["slap", "スラップベース"], ["guitar", "クリーンギター"], ["crunch", "クランチギター"], ["distGuitar", "ディストーションギター"], ["leadGuitar", "リードギター"], ["echoGuitar", "エコーギター"],
  ["keys", "エレピ"], ["piano", "ピアノ"], ["harpsichord", "チェンバロ"], ["strings", "弦楽"], ["pad", "パッド"], ["choir", "合唱"], ["brass", "ブラス"], ["lead", "リード"], ["bell", "鐘"],
];
const DRUMS = new Set<string>(["kick", "snare", "hihat", "crash", "tom"]);
const instLabel = (i?: Instrument): string => INSTRUMENTS.find(([k]) => k === i)?.[1] ?? "音色なし";
const TONICS = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"];

interface State {
  score: Score;
  name: string;
  edition: "modern" | "ps2" | "real";
  selected: number;
  grid: number;
  noteLen: number;
  muted: Set<number>;
  solo: Set<number>;
  playing: boolean;
  paused: boolean;
  pausedAt: number;
  repeatOff: boolean;
}
const state: State = { score: composeSong({ id: "new", title: "新しい曲", scene: "", style: "rock", tonic: "E", minor: true, bpm: 132, seed: 1 }), name: "新しい曲", edition: "real", selected: 0, grid: 0.25, noteLen: 0.5, muted: new Set(), solo: new Set(), playing: false, paused: false, pausedAt: 0, repeatOff: false };

// ── 小さなDOM道具 ──
function h<K extends keyof HTMLElementTagNameMap>(tag: K, attrs: Record<string, string> = {}, ...kids: (Node | string)[]): HTMLElementTagNameMap[K] {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") el.className = v;
    else el.setAttribute(k, v);
  }
  for (const c of kids) el.append(c);
  return el;
}
const mmss = (s: number): string => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
function download(name: string, data: BlobPart, type: string): void {
  const url = URL.createObjectURL(new Blob([data], { type }));
  const a = h("a", { href: url, download: name });
  document.body.append(a);
  a.click();
  a.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 2000);
}

// ── 再生 ──
function effectiveScore(): Score {
  const soloOn = state.solo.size > 0;
  const tracks = state.score.tracks.map((t, i) => ({ t, i })).filter(({ i }) => !state.muted.has(i) && (!soloOn || state.solo.has(i))).map(({ t }) => t);
  const base: Score = { ...state.score, tracks: tracks.length > 0 ? tracks : [{ waveform: "sine", volume: 0, notes: [{ note: REST, durationBeats: trackTotalBeats(state.score.tracks[0]) }] }] };
  return state.edition === "ps2" ? ps2Edition(base) : state.edition === "real" ? realEdition(base) : base;
}
function play(offset = 0): void {
  engine.playBgm(effectiveScore(), offset);
  state.playing = true;
  state.paused = false;
  ui.pauseBtn.textContent = "一時停止";
}
function restartHere(): void {
  if (state.playing && !state.paused) play(engine.getBgmPositionSec());
}
let restartTimer = 0;
function restartSoon(): void {
  window.clearTimeout(restartTimer);
  restartTimer = window.setTimeout(restartHere, 200);
}
function auditionNote(track: Track, noteName: string): void {
  const program = track.instrument ? GM_PROGRAM[track.instrument] : undefined;
  const drum = track.instrument !== undefined && DRUMS.has(track.instrument);
  engine.playSe({ tempoBpm: 240, loop: false, tracks: [{ waveform: track.waveform, instrument: track.instrument, gm: program ?? (drum ? 0 : undefined), gmDrum: drum || undefined, volume: Math.max(0.12, track.volume), notes: [{ note: noteName, durationBeats: 1 }] }] });
}

// ── 画面の部品 ──
const app = document.getElementById("app")!;
const ui = {
  status: h("div", { class: "muted" }),
  seek: h("input", { id: "seek", type: "range", min: "0", max: "100", step: "0.1", value: "0", "aria-label": "再生位置" }),
  time: h("span", { class: "time" }, "0:00 / 0:00"),
  playBtn: h("button", { class: "primary", type: "button" }, "▶ 再生"),
  pauseBtn: h("button", { type: "button" }, "一時停止"),
  stopBtn: h("button", { type: "button" }, "■ 停止"),
  trackBox: h("div", { class: "tracks" }),
  rollBox: h("div", { class: "rollbox", tabindex: "0", "aria-label": "ピアノロール" }),
  canvas: h("canvas"),
  info: h("div", { class: "muted" }),
};

function field(label: string, control: HTMLElement): HTMLElement {
  return h("label", { class: "f" }, label, control);
}
function select(options: [string, string][], value: string): HTMLSelectElement {
  const s = h("select");
  for (const [v, l] of options) s.append(h("option", { value: v }, l));
  s.value = value;
  return s;
}

// 自動作曲のパネル
const styleSel = select(Object.entries(STYLE_LABEL).map(([k, v]) => [k, v] as [string, string]), "rock");
const tonicSel = select(TONICS.map((t) => [t, t] as [string, string]), "E");
const modeSel = select([["minor", "短調"], ["major", "長調"]], "minor");
const bpmIn = h("input", { type: "number", min: "50", max: "240", value: "132" });
const seedIn = h("input", { type: "number", min: "1", max: "999999", value: "1" });
const secIn = select([["60", "1分"], ["75", "1分15秒"], ["90", "1分半"]], "75");
const beatsSel = select([["4", "4拍子"], ["3", "3拍子"], ["7", "7拍子"]], "4");
const driveChk = h("input", { type: "checkbox" });
const finaleSel = select(FINALES.map((f) => [f.id, `${f.title}（${f.scene}）`] as [string, string]), FINALES[0].id);
const nameIn = h("input", { type: "text", value: state.name });

function loadScore(score: Score, name: string): void {
  engine.stopBgm();
  state.playing = false;
  state.score = score;
  state.name = name;
  state.selected = 0;
  state.muted.clear();
  state.solo.clear();
  nameIn.value = name;
  renderAll();
  save();
}
function composeAuto(): void {
  const spec = { id: "new", title: nameIn.value || "新しい曲", scene: "", style: styleSel.value as Style, tonic: tonicSel.value, minor: modeSel.value === "minor", bpm: Number(bpmIn.value) || 120, seed: Number(seedIn.value) || 1, beats: Number(beatsSel.value) as 3 | 4 | 7, targetSec: Number(secIn.value), drive: driveChk.checked };
  loadScore(composeSong(spec), spec.title);
}
const useFieldsChk = h("input", { type: "checkbox" });
function composeSpecial(): void {
  const f = FINALES.find((x) => x.id === finaleSel.value)!;
  // 既定は、その型の調・テンポ・種のまま（速い曲は速く、遅い曲は遅く）。チェックすると、上の欄の値を使う
  const score = composeFinale(useFieldsChk.checked ? { ...f, tonic: tonicSel.value, bpm: Number(bpmIn.value) || f.bpm, seed: Number(seedIn.value) || f.seed } : f);
  loadScore(score, `${f.title}（特別曲）`);
}
const randomBtn = h("button", { type: "button" }, "🎲");
randomBtn.onclick = () => {
  seedIn.value = String(1 + Math.floor(Math.random() * 99999));
};

// 版・再生・書き出し
const editionSel = select([["modern", "現代的"], ["ps2", "PS2世代"], ["real", "実楽器（バンド・オーケストラ）"]], state.edition);
editionSel.onchange = () => {
  state.edition = editionSel.value as State["edition"];
  restartHere();
  save();
};
const volIn = h("input", { type: "range", min: "0", max: "100", value: "60", "aria-label": "音量" });
volIn.oninput = () => engine.setBgmVolume(Number(volIn.value) / 100);
engine.setBgmVolume(0.6);
const repeatChk = h("input", { type: "checkbox", checked: "" });
ui.playBtn.onclick = () => play(0);
ui.stopBtn.onclick = () => {
  engine.stopBgm();
  state.playing = false;
  state.paused = false;
  ui.pauseBtn.textContent = "一時停止";
};
ui.pauseBtn.onclick = () => {
  if (!state.playing) return;
  if (!state.paused) {
    state.pausedAt = engine.getBgmPositionSec();
    engine.stopBgm();
    state.paused = true;
    ui.pauseBtn.textContent = "再開";
  } else {
    play(state.pausedAt);
  }
};
let dragging = false;
ui.seek.oninput = () => {
  dragging = true;
  ui.time.textContent = `${mmss(Number((ui.seek as HTMLInputElement).value))} / ${mmss(getScoreDurationSec(state.score))}`;
};
ui.seek.onchange = () => {
  dragging = false;
  const pos = Number((ui.seek as HTMLInputElement).value);
  if (state.paused) state.pausedAt = pos;
  else if (state.playing) engine.seekBgm(pos);
  else play(pos);
};

function exportMidi(): void {
  download(`${state.name || "song"}.mid`, scoreToMidi(effectiveScore()) as BlobPart, "audio/midi");
}
function exportProject(): void {
  download(`${state.name || "song"}.sunshine-song.json`, JSON.stringify({ format: "sunshine-song", version: 1, name: state.name, edition: state.edition, score: state.score }), "application/json");
}
function importProject(file: File): void {
  void file.text().then((text) => {
    try {
      const data = JSON.parse(text) as { format?: string; name?: string; edition?: State["edition"]; score?: Score };
      if (data.format !== "sunshine-song" || !data.score) throw new Error("形式が違います");
      if (data.edition) {
        state.edition = data.edition;
        editionSel.value = data.edition;
      }
      loadScore(data.score, data.name ?? "読み込んだ曲");
    } catch (e) {
      ui.status.textContent = `読み込めませんでした: ${(e as Error).message}`;
    }
  });
}
const fileIn = h("input", { type: "file", accept: ".json,application/json", hidden: "" });
fileIn.onchange = () => {
  const f = fileIn.files?.[0];
  if (f) importProject(f);
};

// ── トラック一覧 ──
function renderTracks(): void {
  ui.trackBox.replaceChildren();
  state.score.tracks.forEach((t, i) => {
    const row = h("div", { class: `trk${i === state.selected ? " sel" : ""}` });
    const nm = h("div", { class: "nm", title: "クリックでピアノロールに表示" }, `${i + 1}. ${instLabel(t.instrument)}`);
    nm.onclick = () => {
      state.selected = i;
      renderTracks();
      renderAmp();
      drawRoll();
    };
    const inst = select(INSTRUMENTS.map(([k, l]) => [k, l] as [string, string]), t.instrument ?? "lead");
    inst.onchange = () => {
      t.instrument = inst.value as Instrument;
      delete t.program;
      renderTracks();
      restartSoon();
      save();
    };
    const vol = h("input", { type: "range", min: "0", max: "50", value: String(Math.round(t.volume * 100)), title: "音量" });
    vol.oninput = () => {
      t.volume = Number(vol.value) / 100;
      restartSoon();
      save();
    };
    const pan = h("input", { type: "range", min: "-100", max: "100", value: String(Math.round((t.pan ?? 0) * 100)), title: "左右の位置" });
    pan.oninput = () => {
      t.pan = Number(pan.value) / 100;
      restartSoon();
      save();
    };
    const mute = h("button", { type: "button", class: state.muted.has(i) ? "on" : "", title: "ミュート" }, "M");
    mute.onclick = () => {
      if (state.muted.has(i)) state.muted.delete(i);
      else state.muted.add(i);
      renderTracks();
      restartSoon();
    };
    const solo = h("button", { type: "button", class: state.solo.has(i) ? "on" : "", title: "ソロ" }, "S");
    solo.onclick = () => {
      if (state.solo.has(i)) state.solo.delete(i);
      else state.solo.add(i);
      renderTracks();
      restartSoon();
    };
    const del = h("button", { type: "button", title: "このトラックを消す" }, "✕");
    del.onclick = () => {
      if (state.score.tracks.length <= 1) return;
      state.score.tracks.splice(i, 1);
      state.muted.clear();
      state.solo.clear();
      state.selected = Math.min(state.selected, state.score.tracks.length - 1);
      renderAll();
      restartSoon();
      save();
    };
    row.append(nm, inst, vol, pan, h("div", { class: "bt" }, mute, solo, del));
    ui.trackBox.append(row);
  });
}
const addTrackBtn = h("button", { type: "button" }, "＋ トラックを足す");
addTrackBtn.onclick = () => {
  const total = trackTotalBeats(state.score.tracks[0]);
  state.score.tracks.push({ waveform: "triangle", instrument: "piano", volume: 0.15, notes: [{ note: REST, durationBeats: total }] });
  state.selected = state.score.tracks.length - 1;
  renderAll();
  save();
};

// ── ピアノロール ──
const PX = 16;
const ROW = 12;
function css(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim() || "#888";
}
function rollRange(t: Track): { lo: number; hi: number } {
  const notes = trackToNotes(t).map((n) => noteNameToMidi(n.note));
  if (t.instrument && DRUMS.has(t.instrument)) {
    const m = notes[0] ?? 36;
    return { lo: m, hi: m };
  }
  const lo = Math.min(...notes, 60) - 4;
  const hi = Math.max(...notes, 72) + 4;
  return { lo: Math.max(12, Math.min(lo, hi - 24)), hi: Math.min(108, Math.max(hi, lo + 24)) };
}
function drawRoll(): void {
  const t = state.score.tracks[state.selected];
  const total = trackTotalBeats(t);
  const { lo, hi } = rollRange(t);
  const rows = hi - lo + 1;
  const canvas = ui.canvas;
  canvas.width = Math.ceil(total * PX);
  canvas.height = Math.max(rows * ROW, ROW * 3);
  const ctx = canvas.getContext("2d")!;
  ctx.fillStyle = css("--roll-bg");
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  for (let m = lo; m <= hi; m++) {
    const y = (hi - m) * ROW;
    if ([1, 3, 6, 8, 10].includes(m % 12)) {
      ctx.fillStyle = css("--roll-black");
      ctx.fillRect(0, y, canvas.width, ROW);
    }
    if (m % 12 === 0) {
      ctx.fillStyle = css("--muted");
      ctx.font = "10px sans-serif";
      ctx.fillText(midiToName(m), 3, y + ROW - 2);
    }
  }
  const beatsPerBar = 4;
  for (let b = 0; b <= total; b += 1) {
    ctx.fillStyle = b % beatsPerBar === 0 ? css("--roll-bar") : css("--roll-beat");
    ctx.fillRect(Math.round(b * PX), 0, 1, canvas.height);
  }
  ctx.fillStyle = css("--note");
  ctx.strokeStyle = css("--note-edge");
  for (const n of trackToNotes(t)) {
    const y = (hi - noteNameToMidi(n.note)) * ROW;
    ctx.fillRect(n.start * PX, y + 1, Math.max(3, n.dur * PX - 1), ROW - 2);
    ctx.strokeRect(n.start * PX + 0.5, y + 1.5, Math.max(3, n.dur * PX - 1) - 1, ROW - 3);
  }
  ui.info.textContent = `${instLabel(t.instrument)}（${trackToNotes(t).length}音・${Math.round(total)}拍）｜クリックで音を足す／音の上をクリックで消す／音の右はしをドラッグで長さを変える`;
  (canvas as HTMLCanvasElement & { __hi?: number }).__hi = hi;
}
const EDGE_PX = 6;
let resizing: { start: number } | null = null;
let downAt: { x: number; y: number } | null = null;
function rollPoint(ev: MouseEvent): { x: number; y: number; hi: number } {
  const rect = ui.canvas.getBoundingClientRect();
  const hi = (ui.canvas as HTMLCanvasElement & { __hi?: number }).__hi ?? 84;
  return { x: ev.clientX - rect.left, y: ev.clientY - rect.top, hi };
}
/** 音の右のはしの近くなら、その音の始まりの位置を返す（長さの変更用）。 */
function edgeHit(t: Track, x: number, y: number, hi: number): number | null {
  const drum = t.instrument !== undefined && DRUMS.has(t.instrument);
  for (const n of trackToNotes(t)) {
    const row = drum ? 0 : hi - noteNameToMidi(n.note);
    const yTop = drum ? 0 : row * ROW;
    const end = (n.start + n.dur) * PX;
    if (Math.abs(x - end) <= EDGE_PX && x >= n.start * PX && (drum || (y >= yTop && y < yTop + ROW))) return n.start;
  }
  return null;
}
function commitTrack(next: Track): void {
  state.score.tracks[state.selected] = next;
  drawRoll();
  renderTracks();
}
ui.canvas.onmousemove = (ev) => {
  const t = state.score.tracks[state.selected];
  const { x, y, hi } = rollPoint(ev);
  if (resizing) {
    const dur = Math.max(state.grid, Math.round((x / PX - resizing.start) / state.grid) * state.grid);
    commitTrack(resizeNote(t, resizing.start, dur, trackTotalBeats(t)));
    return;
  }
  ui.canvas.style.cursor = edgeHit(t, x, y, hi) !== null ? "ew-resize" : "crosshair";
};
ui.canvas.onmousedown = (ev) => {
  const t = state.score.tracks[state.selected];
  const { x, y, hi } = rollPoint(ev);
  downAt = { x, y };
  const edge = edgeHit(t, x, y, hi);
  if (edge !== null) resizing = { start: edge };
};
window.addEventListener("mouseup", (ev) => {
  if (resizing) {
    resizing = null;
    downAt = null;
    restartSoon();
    save();
    return;
  }
  if (!downAt || ev.target !== ui.canvas) {
    downAt = null;
    return;
  }
  downAt = null;
  const t = state.score.tracks[state.selected];
  const { x, y, hi } = rollPoint(ev);
  const beat = Math.floor(x / PX / state.grid) * state.grid;
  const midi = t.instrument && DRUMS.has(t.instrument) ? hi : hi - Math.floor(y / ROW);
  const noteName = midiToName(midi);
  const total = trackTotalBeats(t);
  // 長さを変えるドラッグ（音の上でボタンを押して、はしをつかむ）は上で済んでいる。ここは、ふつうのクリック
  const covered = noteStartAt(t, beat) !== null;
  const next = toggleNote(t, beat, noteName, state.noteLen, total);
  commitTrack(next);
  if (!covered) auditionNote(next, noteName);
  restartSoon();
  save();
});
const gridSel = select([["1", "1拍"], ["0.5", "1/2拍"], ["0.25", "1/4拍"]], "0.25");
gridSel.onchange = () => (state.grid = Number(gridSel.value));
const lenSel = select([["0.25", "1/4拍"], ["0.5", "1/2拍"], ["1", "1拍"], ["2", "2拍"], ["4", "4拍"]], "0.5");
lenSel.onchange = () => (state.noteLen = Number(lenSel.value));
const clearBtn = h("button", { type: "button" }, "このトラックを空にする");
clearBtn.onclick = () => {
  const t = state.score.tracks[state.selected];
  state.score.tracks[state.selected] = { ...t, notes: notesToEvents([], trackTotalBeats(t)) };
  drawRoll();
  renderTracks();
  restartSoon();
  save();
};

// ── 保存（このブラウザに自動保存） ──
function save(): void {
  try {
    window.localStorage.setItem("sunshine-composer", JSON.stringify({ name: state.name, edition: state.edition, score: state.score }));
  } catch {
    // 保存できなくても、操作は続けられる
  }
}
function restore(): void {
  try {
    const raw = window.localStorage.getItem("sunshine-composer");
    if (!raw) return;
    const data = JSON.parse(raw) as { name?: string; edition?: State["edition"]; score?: Score };
    if (data.score && data.score.tracks?.length) {
      state.score = data.score;
      state.name = data.name ?? state.name;
      nameIn.value = state.name;
      if (data.edition) {
        state.edition = data.edition;
        editionSel.value = data.edition;
      }
    }
  } catch {
    // 読み込めなければ、初期の曲のまま
  }
}

// ── WAVで書き出す（実際に鳴らしながら録音する。曲の頭から1周ぶん） ──
const wavBtn = h("button", { type: "button" }, "WAVで書き出す");
let exporting = false;
wavBtn.onclick = () => {
  if (exporting) return;
  exporting = true;
  wavBtn.disabled = true;
  const total = getScoreDurationSec(state.score);
  const stop = engine.startCapture();
  play(0);
  const started = performance.now();
  const timer = window.setInterval(() => {
    const left = total - (performance.now() - started) / 1000;
    ui.status.textContent = `WAVを録音中… あと${Math.max(0, Math.ceil(left))}秒（この間は、ほかの操作をしないでください）`;
    if (left > 0) return;
    window.clearInterval(timer);
    const { channels, sampleRate } = stop();
    engine.stopBgm();
    state.playing = false;
    state.paused = false;
    // 再生の立ち上がりの無音をのぞいて、曲の長さぶんを切り出す
    let first = 0;
    while (first < channels[0].length && Math.abs(channels[0][first]) < 1e-4 && Math.abs(channels[1][first]) < 1e-4) first++;
    download(`${state.name || "song"}.wav`, encodeWav(channels, sampleRate, first, first + Math.round(total * sampleRate)) as BlobPart, "audio/wav");
    ui.status.textContent = "WAVを書き出しました。";
    exporting = false;
    wavBtn.disabled = false;
  }, 250);
};

// ── ゲームの曲として登録（書き出したファイルを src/audio/songs/ に置くと、ゲームの曲一覧に入る） ──
const gameIdIn = h("input", { type: "text", value: "my-song", placeholder: "英小文字・数字・-" });
const gameSceneIn = h("input", { type: "text", value: "", placeholder: "どの場面の曲か（例: 新しい町）" });
const gameBtn = h("button", { type: "button" }, "ゲームの曲として登録用ファイルを書き出す");
gameBtn.onclick = () => {
  const id = gameIdIn.value.trim();
  if (!/^[a-z0-9][a-z0-9-]*$/.test(id)) {
    ui.status.textContent = "曲のIDは、英小文字・数字・「-」だけにしてください。";
    return;
  }
  download(`${id}.sunshine-song.json`, JSON.stringify({ format: "sunshine-game-song", version: 1, id, title: state.name, scene: gameSceneIn.value.trim(), score: state.score }), "application/json");
  ui.status.textContent = `${id}.sunshine-song.json を書き出しました。リポジトリの src/audio/songs/ に置くと、ゲームの曲一覧に入ります。`;
};

// ── 新しい曲（コード進行から、バンドの伴奏を作る） ──
const nsChords = h("input", { type: "text", value: "Am F C G", style: "min-width:180px" });
const nsBpm = h("input", { type: "number", min: "50", max: "240", value: "110" });
const nsBeats = select([["4", "4拍子"], ["3", "3拍子"], ["6", "6拍子"], ["7", "7拍子"]], "4");
const nsBars = select([["1", "1小節"], ["2", "2小節"]], "1");
const nsRepeat = select([["2", "2回"], ["4", "4回"], ["6", "6回"], ["8", "8回"]], "4");
const nsFeel = select([["rock", "ロック"], ["pop", "ポップ"], ["ballad", "バラード"]], "rock");
const nsLead = select(INSTRUMENTS.filter(([k]) => !DRUMS.has(k)).map(([k, l]) => [k, l] as [string, string]), "leadGuitar");
const nsBtn = h("button", { class: "primary", type: "button" }, "この進行で新しい曲を作る");
nsBtn.onclick = () => {
  try {
    const score = buildNewSong({ bpm: Number(nsBpm.value) || 110, beats: Number(nsBeats.value), chords: nsChords.value, barsPerChord: Number(nsBars.value), repeats: Number(nsRepeat.value), feel: nsFeel.value as "rock" | "pop" | "ballad", leadInstrument: nsLead.value as Instrument });
    loadScore(score, nameIn.value || "新しい曲");
    state.selected = score.tracks.length - 1;
    renderAll();
  } catch (e) {
    ui.status.textContent = (e as Error).message;
  }
};

// ── 音づくり（トラックごとのアンプ・NAM） ──
const ampBox = h("div", {});
const AMP_TYPES: [AmpSetting["type"], string][] = [
  ["auto", "おまかせ（曲の設定どおり）"], ["clean", "クリーン"], ["overdrive", "オーバードライブ"], ["distortion", "ディストーション"], ["metal", "メタルゾーン"], ["prs", "なめらかなリード（PRS風）"], ["nam", "NAMのアンプモデル（読み込み）"],
];
function slider(label: string, min: number, max: number, step: number, value: number, on: (v: number) => void): HTMLElement {
  const input = h("input", { type: "range", min: String(min), max: String(max), step: String(step), value: String(value) });
  const out = h("span", { class: "muted" }, String(value));
  input.oninput = () => {
    const v = Number(input.value);
    out.textContent = String(v);
    on(v);
  };
  return h("label", { class: "f" }, label, h("div", { class: "row" }, input, out));
}
function renderAmp(): void {
  ampBox.replaceChildren();
  const t = state.score.tracks[state.selected];
  if (!t) return;
  const amp: AmpSetting = t.amp ?? { type: "auto" };
  const change = (next: AmpSetting): void => {
    t.amp = next.type === "auto" && next.drive === undefined && next.tone === undefined && next.level === undefined ? undefined : next;
    restartSoon();
    save();
  };
  const typeSel = select(AMP_TYPES.map(([k, l]) => [k, l] as [string, string]), amp.type);
  typeSel.onchange = () => {
    change({ ...amp, type: typeSel.value as AmpSetting["type"] });
    renderAmp();
  };
  const row = h("div", { class: "row" }, field(`「${instLabel(t.instrument)}」のアンプ`, typeSel),
    slider("歪みの深さ", 0.5, 2, 0.05, amp.drive ?? 1, (v) => change({ ...(t.amp ?? amp), drive: v })),
    slider("高音の明るさ(dB)", -6, 6, 0.5, amp.tone ?? 0, (v) => change({ ...(t.amp ?? amp), tone: v })),
    slider("出力の大きさ", 0.5, 1.5, 0.05, amp.level ?? 1, (v) => change({ ...(t.amp ?? amp), level: v })));
  ampBox.append(row);
  if (amp.type === "nam") {
    const file = h("input", { type: "file", accept: ".nam,application/json", hidden: "" });
    file.onchange = () => {
      const f = file.files?.[0];
      if (!f) return;
      void f.text().then((text) => {
        try {
          JSON.parse(text);
        } catch {
          ui.status.textContent = "NAMモデルとして読めませんでした（.namファイルを選んでください）。";
          return;
        }
        const key = f.name.replace(/\.nam$/i, "");
        state.score.namModels = { ...(state.score.namModels ?? {}), [key]: text };
        change({ ...(t.amp ?? amp), type: "nam", model: key });
        ui.status.textContent = `NAMモデル「${key}」を読み込みました。`;
        renderAmp();
      });
    };
    const load = h("button", { type: "button" }, "NAMモデル（.nam）を読み込む");
    load.onclick = () => file.click();
    ampBox.append(h("div", { class: "row", style: "margin-top:8px" }, load, file, h("span", { class: "muted" }, amp.model ? `使用中: ${amp.model}` : "まだ読み込んでいません（そのあいだは、ふつうのアンプの音）")),
      h("div", { class: "muted", style: "margin-top:4px" }, "NAMは、実際のアンプを学習した無料のアンプシミュレーターです。モデル（.nam）は、配布元の利用規約（商用利用・再配布）を確認してから使ってください。ゲームには、NAMモデルは入れません（ふつうのアンプの音になります）。"));
  }
}

// ── 画面を組み立てる ──
function renderAll(): void {
  renderTracks();
  renderAmp();
  drawRoll();
  ui.status.textContent = `${state.name}｜${state.score.tracks.length}トラック｜${mmss(getScoreDurationSec(state.score))}｜テンポ ${state.score.tempoBpm}`;
}
const composeBtn = h("button", { class: "primary", type: "button" }, "自動作曲");
composeBtn.onclick = composeAuto;
const specialBtn = h("button", { type: "button" }, "特別曲（3〜4分）を作る");
specialBtn.onclick = composeSpecial;
const midiBtn = h("button", { type: "button" }, "MIDIで書き出す");
midiBtn.onclick = exportMidi;
const saveBtn = h("button", { type: "button" }, "プロジェクトを保存");
saveBtn.onclick = exportProject;
const loadBtn = h("button", { type: "button" }, "プロジェクトを読み込む");
loadBtn.onclick = () => fileIn.click();

app.append(
  h("div", {}, h("h1", {}, "サンシャイン作曲ソフト"), h("div", { class: "muted" }, "自動で曲を作り、ピアノロールで直して、実楽器の音（ギターアンプ・ドラムの仕上げつき）で聴けます。")),
  h("div", { class: "grid" },
    h("div", { class: "panel" }, h("h2", {}, "自動作曲"),
      h("div", { class: "row" }, field("曲名", nameIn), field("曲調", styleSel), field("調", tonicSel), field("長調・短調", modeSel)),
      h("div", { class: "row", style: "margin-top:8px" }, field("テンポ", bpmIn), field("乱数の種", h("div", { class: "row" }, seedIn, randomBtn)), field("長さ", secIn), field("拍子", beatsSel), field("疾走感（ボス戦向け）", driveChk)),
      h("div", { class: "row", style: "margin-top:10px" }, composeBtn),
      h("div", { class: "row", style: "margin-top:10px" }, field("特別曲の型", finaleSel), specialBtn, h("label", { class: "row muted" }, useFieldsChk, "上の調・テンポ・種を使う")),
      h("div", { class: "muted", style: "margin-top:6px" }, "同じ設定（乱数の種）からは、いつも同じ曲ができます。気に入らなければ🎲で種を変えてください。特別曲は、型ごとの調・テンポ・種で作ります（「上の調・テンポ・種を使う」で変えられます）。")),
    h("div", { class: "panel" }, h("h2", {}, "再生と書き出し"),
      h("div", { class: "row" }, ui.playBtn, ui.pauseBtn, ui.stopBtn, field("サウンド", editionSel), field("音量", volIn)),
      h("div", { class: "row", style: "margin-top:10px" }, ui.seek, ui.time),
      h("div", { class: "row", style: "margin-top:10px" }, wavBtn, midiBtn, saveBtn, loadBtn, fileIn),
      h("div", { class: "row", style: "margin-top:10px" }, field("ゲーム用の曲ID", gameIdIn), field("使う場面", gameSceneIn), gameBtn),
      h("div", { class: "muted", style: "margin-top:6px" }, "MIDIは、いま選んでいるサウンドの編成で書き出します。プロジェクトは、あとで続きから編集できます（このブラウザにも自動保存します）。"),
      ui.status)),
  h("div", { class: "panel" }, h("h2", {}, "トラック"), ui.trackBox, h("div", { class: "row", style: "margin-top:8px" }, addTrackBtn),
    h("div", { class: "muted", style: "margin-top:4px" }, "1つのトラックは1度に1音だけ鳴ります（和音は、トラックを重ねて作ります）。")),
  h("div", { class: "panel" }, h("h2", {}, "新しい曲（コード進行から）"),
    h("div", { class: "row" }, field("コード進行（空白でくぎる）", nsChords), field("テンポ", nsBpm), field("拍子", nsBeats), field("1コードの長さ", nsBars), field("くり返し", nsRepeat), field("伴奏の雰囲気", nsFeel), field("メロディの楽器", nsLead)),
    h("div", { class: "row", style: "margin-top:8px" }, nsBtn),
    h("div", { class: "muted", style: "margin-top:4px" }, "ドラム・ベース・ギター・ピアノ・弦の伴奏を作り、最後に空のメロディのトラックを足します。ピアノロールでメロディを書き込んでください。読めるコード: C・Am・F#m7・Bbmaj7・Csus4・Gdim・Eaug など。")),
  h("div", { class: "panel" }, h("h2", {}, "音づくり（アンプ）"), ampBox),
  h("div", { class: "panel" }, h("h2", {}, "ピアノロール"),
    h("div", { class: "row", style: "margin-bottom:8px" }, field("クリックの間隔", gridSel), field("足す音の長さ", lenSel), clearBtn, ui.info), ui.rollBox),
);
ui.rollBox.append(ui.canvas);
restore();
renderAll();

// 再生位置の表示と、ピアノロールの再生位置の線（描き直さず、スクロールだけ追う）
const playhead = h("div", { style: "position:absolute;top:0;bottom:0;width:2px;background:var(--playhead);pointer-events:none;display:none" });
ui.rollBox.style.position = "relative";
ui.rollBox.append(playhead);
function tick(): void {
  const total = getScoreDurationSec(state.score);
  ui.seek.setAttribute("max", String(total));
  if (state.playing && !state.paused && !dragging) {
    const pos = engine.getBgmPositionSec();
    (ui.seek as HTMLInputElement).value = String(pos);
    ui.time.textContent = `${mmss(pos)} / ${mmss(total)}`;
    const beat = (pos * state.score.tempoBpm) / 60;
    const px = beat * PX;
    playhead.style.display = "block";
    playhead.style.left = `${px}px`;
    if (px < ui.rollBox.scrollLeft || px > ui.rollBox.scrollLeft + ui.rollBox.clientWidth - 40) ui.rollBox.scrollLeft = Math.max(0, px - 80);
  } else if (!state.playing) {
    playhead.style.display = "none";
  }
  requestAnimationFrame(tick);
}
tick();
