// サンシャイン作曲ソフト: 自動作曲＋ピアノロールでの手直し＋実楽器の音での試聴＋MIDI・プロジェクトの書き出し。
// 再生エンジン（録音音源・ギターアンプ・ドラムの仕上げ）と作曲エンジンは、ゲーム本体のものをそのまま使う。
import soundfontUrl from "../../src/audio/soundfont/game.sf3?url";
import processorUrl from "spessasynth_lib/dist/spessasynth_processor.min.js?url";
import { AudioEngine } from "../../src/audio/audio-engine";
import { allEntries, getTrack, STYLE_LABEL } from "../../src/audio/catalog";
import "../../src/audio/user-songs";
import { BLANK_TEMPLATES, createBlankScore, type BlankTemplate } from "../../src/audio/blank-song";
import { midiToScore } from "../../src/audio/midi-import";
import { scoreToCsv, scoreToMusicXml } from "../../src/audio/musicxml";
import { encodeFlac } from "../../src/audio/flac";
import { muxOggOpus, type OpusPacket } from "../../src/audio/ogg-opus";
import { barBeats, DENOMINATORS, timeSignatureOf, unitBeats } from "../../src/audio/time-signature";
import { hasCode, validateAmpPlugin, type AmpPluginDef } from "../../src/audio/amp-plugins";
import { midiToName } from "../../src/audio/compose";
import { CHORD_SHAPES, chordIntervals } from "../../src/audio/chord-input";
import { addNotes, copyNotes, moveNotes, notesInRange, notesToEvents, noteStartAt, pasteNotes, removeNotes, resizeNote, setNotesLength, trackToNotes, trackTotalBeats, type RollNote } from "../../src/audio/edit";
import { composeFinale, FINALES } from "../../src/audio/finale";
import { GM_PROGRAM } from "../../src/audio/gm-map";
import { scoreToMidi } from "../../src/audio/midi-export";
import { AMP_PRESETS, AMP_PRESET_NAMES, type AmpPresetName } from "../../src/audio/amp";
import { NamHost } from "../../src/audio/nam/nam-host";
import { AI_SONG_GUIDE, AI_SONG_SCHEMA, aiSongToScore } from "../../src/audio/ai-song";
import { buildNewSong } from "../../src/audio/newsong";
import { noteNameToMidi } from "../../src/audio/note";
import { ps2Edition } from "../../src/audio/ps2-edition";
import { realEdition } from "../../src/audio/real-edition";
import { getScoreDurationSec, REST, type AmpSetting, type Instrument, type Score, type Track } from "../../src/audio/score";
import { composeSong, type Style } from "../../src/audio/songwriter";
import { encodeWav, type WavBits } from "../../src/audio/wav";
import { bytesToBase64, type AudioTrack } from "../../src/audio/audio-clips";
import { ClipPlayer, listInputs, openInput, startRecording, type InputMode, type LiveInput, type Recording } from "./audio-rec";
import { normalizePeak, renderScoreOffline } from "../../src/audio/offline-render";

// 1ファイルのHTMLでは外部ファイルを読み込めないので、埋め込んだ素材（データURL）を録音音源の再生に渡す
function bytesOf(dataUrl: string): Uint8Array {
  const bin = atob(dataUrl.slice(dataUrl.indexOf(",") + 1));
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
let soundfontCopy: ArrayBuffer | null = null;
try {
  // 再生エンジンは読み込み時にデータを使い切るので、WAVの書き出し用に控えを別に持つ
  soundfontCopy = bytesOf(soundfontUrl).buffer as ArrayBuffer;
  globalThis.__sampledAssets = { soundfont: soundfontCopy.slice(0), processorUrl };
} catch (error) {
  console.warn("録音音源の埋め込みを読めませんでした:", error);
}
// 無料のアンプシミュレーター（NAM）: ビルドのときに埋め込んだワークレットとWASMを渡す
declare const __NAM_PROCESSOR__: string;
declare const __NAM_WASM__: string;
declare const __NAM_MODELS__: Record<string, { label: string; json: string }>;
const engine = new AudioEngine();
let namHost: NamHost | null = null;
/** 同梱のNAMモデル（NAM作者のリポジトリにMITライセンスで入っている見本。docs/assets-credits.md）。キーは "builtin:〇〇"。 */
const BUILTIN_NAM: Record<string, { label: string; json: string }> = typeof __NAM_MODELS__ === "object" ? __NAM_MODELS__ : {};
try {
  if (typeof __NAM_PROCESSOR__ === "string" && typeof __NAM_WASM__ === "string") {
    const bin = atob(__NAM_WASM__);
    const wasm = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) wasm[i] = bin.charCodeAt(i);
    globalThis.__namAssets = { processorUrl: __NAM_PROCESSOR__, wasm: wasm.buffer as ArrayBuffer };
    namHost = new NamHost();
    engine.setNamHost(namHost);
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
  tool: "pen" | "select";
  chord: string;
  /** 選んでいる音（始まりの位置）。 */
  picked: number[];
  /** 最後にクリックした位置（貼り付け先）。 */
  cursor: number;
}
const state: State = { score: composeSong({ id: "new", title: "新しい曲", scene: "", style: "rock", tonic: "E", minor: true, bpm: 132, seed: 1 }), name: "新しい曲", edition: "real", selected: 0, grid: 0.25, noteLen: 0.5, muted: new Set(), solo: new Set(), playing: false, paused: false, pausedAt: 0, repeatOff: false, tool: "pen", chord: "none", picked: [], cursor: 0 };

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
/**
 * ファイルに保存する。デスクトップ版は「名前を付けて保存」の画面、Chrome・Edge は保存先を選ぶ画面、
 * それ以外のブラウザは、ふつうのダウンロード（日本語のファイル名が使えないことがあるので、そのときは英数字の名前にする）。
 */
function download(name: string, data: BlobPart, type: string): void {
  void saveFile(name, new Blob([data], { type })).then((where) => {
    if (where) ui.status.textContent = `保存しました: ${where}`;
  }).catch((e: unknown) => {
    if ((e as Error).name !== "AbortError") ui.status.textContent = `保存できませんでした: ${(e as Error).message}`;
  });
}
async function saveFile(name: string, blob: Blob): Promise<string | null> {
  const desktopSave = (window as unknown as { sunshineDesktop?: { saveFile?(name: string, data: Uint8Array): Promise<string | null> } }).sunshineDesktop?.saveFile;
  if (desktopSave) return desktopSave(name, new Uint8Array(await blob.arrayBuffer()));
  const picker = (window as unknown as { showSaveFilePicker?: (o: unknown) => Promise<{ name: string; createWritable(): Promise<{ write(b: Blob): Promise<void>; close(): Promise<void> }> }> }).showSaveFilePicker;
  if (picker) {
    try {
      const ext = name.slice(name.lastIndexOf("."));
      const handle = await picker({ suggestedName: name, types: [{ description: ext, accept: { [blob.type || "application/octet-stream"]: [ext] } }] });
      const w = await handle.createWritable();
      await w.write(blob);
      await w.close();
      return handle.name;
    } catch (e) {
      if ((e as Error).name === "AbortError") throw e;
      // 保存先を選ぶ画面が使えないとき（操作から時間がたった・対応していない形式など）は、ふつうのダウンロードにする
    }
  }
  // eslint-disable-next-line no-control-regex
  const ascii = /^[\x20-\x7e]+$/.test(name) ? name : `sunshine-song-${new Date().toISOString().slice(0, 19).replace(/[-:T]/g, "")}${name.slice(name.lastIndexOf("."))}`;
  const url = URL.createObjectURL(blob);
  const a = h("a", { href: url, download: ascii });
  document.body.append(a);
  a.click();
  a.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 2000);
  return ascii;
}

// ── 再生 ──
function effectiveScore(): Score {
  const soloOn = state.solo.size > 0;
  const tracks = state.score.tracks.map((t, i) => ({ t, i })).filter(({ i }) => !state.muted.has(i) && (!soloOn || state.solo.has(i))).map(({ t }) => t);
  const base: Score = { ...state.score, tracks: tracks.length > 0 ? tracks : [{ waveform: "sine", volume: 0, notes: [{ note: REST, durationBeats: trackTotalBeats(state.score.tracks[0]) }] }] };
  // 同梱のNAMモデルは、プロジェクトには入れず、鳴らすときにだけ渡す
  const used = new Set(base.tracks.map((t) => t.amp?.model).filter((m): m is string => !!m && m in BUILTIN_NAM));
  if (used.size) base.namModels = { ...(base.namModels ?? {}), ...Object.fromEntries([...used].map((k) => [k, BUILTIN_NAM[k].json])) };
  return state.edition === "ps2" ? ps2Edition(base) : state.edition === "real" ? realEdition(base) : base;
}
const clipPlayer = new ClipPlayer(() => engine.audioContext(), () => engine.clipDestination(), () => engine.getBgmPositionSec(), () => namHost);
function play(offset = 0): void {
  const score = effectiveScore();
  engine.playBgm(score, offset);
  clipPlayer.start(score);
  state.playing = true;
  state.paused = false;
  setPauseLook(false);
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

/** 一時停止ボタンの見た目（記号だけにして、枠からはみ出さないようにする。意味は、ふきだしと読み上げで伝える）。 */
function setPauseLook(paused: boolean): void {
  ui.pauseBtn.textContent = paused ? "▶" : "❚❚";
  ui.pauseBtn.title = paused ? "再開" : "一時停止";
  ui.pauseBtn.setAttribute("aria-label", paused ? "再開" : "一時停止");
  ui.pauseBtn.classList.toggle("on", paused);
}
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
  state.picked = [];
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

ui.playBtn.onclick = () => play(0);
ui.stopBtn.onclick = () => {
  engine.stopBgm();
  state.playing = false;
  state.paused = false;
  setPauseLook(false);
};
ui.pauseBtn.onclick = () => {
  if (!state.playing) return;
  if (!state.paused) {
    state.pausedAt = engine.getBgmPositionSec();
    engine.stopBgm();
    state.paused = true;
    setPauseLook(true);
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

function exportProject(): void {
  download(`${state.name || "song"}.sunshine-song.json`, JSON.stringify({ format: "sunshine-song", version: 1, name: state.name, edition: state.edition, score: state.score }), "application/json");
}
/** ファイルを開く: プロジェクト・ゲームの曲・AIソング・MIDI・アンプ定義。 */
function openFile(file: File): void {
  void file.arrayBuffer().then((buf) => {
    const head = new Uint8Array(buf.slice(0, 4));
    // MIDIかどうかは、ファイルの先頭（MThd）で見分ける
    if (String.fromCharCode(...head) === "MThd") openMidi(file.name, buf);
    else openJson(new TextDecoder().decode(buf));
  });
}
function openMidi(fileName: string, buf: ArrayBuffer): void {
  try {
    const r = midiToScore(new Uint8Array(buf));
    loadScore(r.score, fileName.replace(/\.midi?$/i, ""));
    ui.status.textContent = `MIDIを読み込みました（${r.notes}音・${r.score.tracks.length}トラック）${r.warnings.length ? "。注意: " + r.warnings.join(" / ") : ""}`;
  } catch (e) {
    ui.status.textContent = `読み込めませんでした: ${(e as Error).message}`;
  }
}
function openJson(text: string): void {
  try {
    const data = JSON.parse(text) as { format?: string; name?: string; title?: string; edition?: State["edition"]; score?: Score; parts?: unknown; chords?: unknown };
    if (data.format === "sunshine-amp") {
      addAmpPlugin(data, true);
      return;
    }
    if ((data.format === "sunshine-song" || data.format === "sunshine-game-song") && data.score) {
      if (data.edition) {
        state.edition = data.edition;
        editionSel.value = data.edition;
      }
      loadScore(data.score, data.name ?? data.title ?? "読み込んだ曲");
      return;
    }
    if (Array.isArray(data.parts) && typeof data.chords === "string") {
      const r = aiSongToScore(data);
      loadScore(r.score, r.song.title || "読み込んだ曲");
      return;
    }
    throw new Error("知らない形式です（作曲ソフトのプロジェクト・ゲームの曲・AIソング・MIDI・アンプ定義が開けます）");
  } catch (e) {
    ui.status.textContent = `読み込めませんでした: ${(e as Error).message}`;
  }
}
const fileIn = h("input", { type: "file", accept: ".json,.mid,.midi,application/json,audio/midi", hidden: "" });
fileIn.onchange = () => {
  const f = fileIn.files?.[0];
  if (f) openFile(f);
  fileIn.value = "";
};

// ── トラック一覧 ──
function renderTracks(): void {
  ui.trackBox.replaceChildren();
  state.score.tracks.forEach((t, i) => {
    const row = h("div", { class: `trk${i === state.selected ? " sel" : ""}` });
    const nm = h("div", { class: "nm", title: "クリックでピアノロールに表示" }, `${i + 1}. ${instLabel(t.instrument)}`);
    nm.onclick = () => {
      state.selected = i;
      state.picked = [];
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
/** 和音の相手のトラック: 選んだトラックのすぐ後ろに続く、同じ楽器のトラック。 */
function companions(index: number): number[] {
  const tracks = state.score.tracks;
  const inst = tracks[index]?.instrument;
  const out: number[] = [];
  for (let k = index + 1; k < tracks.length && tracks[k].instrument === inst; k++) out.push(k);
  return out;
}
const isDrum = (t: Track): boolean => t.instrument !== undefined && DRUMS.has(t.instrument);
const transpose = (note: string, semi: number): string => midiToName(Math.max(12, Math.min(108, noteNameToMidi(note) + semi)));

function drawRoll(): void {
  const t = state.score.tracks[state.selected];
  const total = trackTotalBeats(t);
  const ghosts = isDrum(t) ? [] : companions(state.selected).map((k) => state.score.tracks[k]);
  const { lo, hi } = rollRange({ ...t, notes: [...t.notes, ...ghosts.flatMap((g) => g.notes)] });
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
  // 拍子に合わせて、小節線（明るい線）と拍の線を引く
  const sig = timeSignatureOf(state.score);
  const bar = barBeats(sig);
  const unit = unitBeats(sig);
  for (let k = 0; k * unit <= total + 1e-9; k++) {
    const b = k * unit;
    const isBar = Math.abs(b / bar - Math.round(b / bar)) < 1e-6;
    ctx.fillStyle = isBar ? css("--roll-bar") : css("--roll-beat");
    ctx.fillRect(Math.round(b * PX), 0, isBar ? 2 : 1, canvas.height);
    if (isBar) {
      ctx.fillStyle = css("--muted");
      ctx.font = "9px monospace";
      ctx.fillText(String(Math.round(b / bar) + 1), Math.round(b * PX) + 3, 9);
    }
  }
  // 和音の相手のトラックの音は、うすく描く
  ctx.globalAlpha = 0.35;
  ctx.fillStyle = css("--note");
  for (const g of ghosts) {
    for (const n of trackToNotes(g)) ctx.fillRect(n.start * PX, (hi - noteNameToMidi(n.note)) * ROW + 1, Math.max(3, n.dur * PX - 1), ROW - 2);
  }
  ctx.globalAlpha = 1;
  const sel = new Set(state.picked);
  // 音は、ほのかに光らせる
  ctx.shadowBlur = 6;
  for (const n of trackToNotes(t)) {
    const y = isDrum(t) ? 0 : (hi - noteNameToMidi(n.note)) * ROW;
    const chosen = sel.has(n.start);
    ctx.fillStyle = chosen ? css("--note-sel") : css("--note");
    ctx.shadowColor = ctx.fillStyle;
    ctx.strokeStyle = chosen ? css("--note-sel-edge") : css("--note-edge");
    ctx.fillRect(n.start * PX, y + 1, Math.max(3, n.dur * PX - 1), ROW - 2);
    ctx.strokeRect(n.start * PX + 0.5, y + 1.5, Math.max(3, n.dur * PX - 1) - 1, ROW - 3);
  }
  ctx.shadowBlur = 0;
  if (box) {
    ctx.strokeStyle = css("--note-sel-edge");
    ctx.setLineDash([4, 3]);
    ctx.strokeRect(Math.min(box.x0, box.x1) + 0.5, Math.min(box.y0, box.y1) + 0.5, Math.abs(box.x1 - box.x0), Math.abs(box.y1 - box.y0));
    ctx.setLineDash([]);
  }
  const help = state.tool === "select"
    ? "ドラッグで囲んで選ぶ／音をクリックで選ぶ（Shiftで追加）／選んだ音をドラッグで移動／Delete・矢印・Ctrl+C・Ctrl+V・Ctrl+D"
    : "クリックで音を足す／音の上をクリックで消す／音の右はしをドラッグで長さを変える";
  const chordInfo = ghosts.length > 0 ? `｜和音の相手: ${companions(state.selected).map((k) => k + 1).join("・")}番` : "";
  ui.info.textContent = `${instLabel(t.instrument)}（${trackToNotes(t).length}音・${Math.round(total)}拍${state.picked.length ? `・${state.picked.length}音を選択中` : ""}）${chordInfo}｜${help}`;
  (canvas as HTMLCanvasElement & { __hi?: number }).__hi = hi;
}
const EDGE_PX = 6;
let resizing: { start: number } | null = null;
let downAt: { x: number; y: number; shift: boolean } | null = null;
let box: { x0: number; y0: number; x1: number; y1: number } | null = null;
let dragging2: { x0: number; y0: number; orig: Track; starts: number[] } | null = null;
function rollPoint(ev: MouseEvent): { x: number; y: number; hi: number } {
  const rect = ui.canvas.getBoundingClientRect();
  const hi = (ui.canvas as HTMLCanvasElement & { __hi?: number }).__hi ?? 84;
  return { x: ev.clientX - rect.left, y: ev.clientY - rect.top, hi };
}
/** 音の右のはしの近くなら、その音の始まりの位置を返す（長さの変更用）。 */
function edgeHit(t: Track, x: number, y: number, hi: number): number | null {
  for (const n of trackToNotes(t)) {
    const yTop = isDrum(t) ? 0 : (hi - noteNameToMidi(n.note)) * ROW;
    const end = (n.start + n.dur) * PX;
    if (Math.abs(x - end) <= EDGE_PX && x >= n.start * PX && (isDrum(t) || (y >= yTop && y < yTop + ROW))) return n.start;
  }
  return null;
}
/** その点にある音（始まりの位置）。 */
function noteHit(t: Track, x: number, y: number, hi: number): number | null {
  const beat = x / PX;
  for (const n of trackToNotes(t)) {
    const yTop = isDrum(t) ? 0 : (hi - noteNameToMidi(n.note)) * ROW;
    if (beat >= n.start && beat < n.start + n.dur && (isDrum(t) || (y >= yTop && y < yTop + ROW))) return n.start;
  }
  return null;
}
function commitTrack(next: Track): void {
  state.score.tracks[state.selected] = next;
  drawRoll();
  renderTracks();
}
function edited(): void {
  drawRoll();
  renderTracks();
  restartSoon();
  save();
}
ui.canvas.onmousemove = (ev) => {
  const t = state.score.tracks[state.selected];
  const { x, y, hi } = rollPoint(ev);
  if (resizing) {
    const dur = Math.max(state.grid, Math.round((x / PX - resizing.start) / state.grid) * state.grid);
    commitTrack(resizeNote(t, resizing.start, dur, trackTotalBeats(t)));
    return;
  }
  if (dragging2) {
    const dBeat = Math.round((x - dragging2.x0) / PX / state.grid) * state.grid;
    const dSemi = isDrum(t) ? 0 : -Math.round((y - dragging2.y0) / ROW);
    const r = moveNotes(dragging2.orig, dragging2.starts, dBeat, dSemi, transpose);
    state.picked = r.starts;
    commitTrack(r.track);
    return;
  }
  if (box) {
    box.x1 = x;
    box.y1 = y;
    drawRoll();
    return;
  }
  ui.canvas.style.cursor = edgeHit(t, x, y, hi) !== null ? "ew-resize" : state.tool === "select" ? (noteHit(t, x, y, hi) !== null ? "move" : "default") : "crosshair";
};
ui.canvas.onmousedown = (ev) => {
  ui.rollBox.focus();
  const t = state.score.tracks[state.selected];
  const { x, y, hi } = rollPoint(ev);
  downAt = { x, y, shift: ev.shiftKey };
  const edge = edgeHit(t, x, y, hi);
  if (edge !== null) {
    resizing = { start: edge };
    return;
  }
  if (state.tool !== "select") return;
  const hit = noteHit(t, x, y, hi);
  if (hit !== null) {
    if (ev.shiftKey) {
      state.picked = state.picked.includes(hit) ? state.picked.filter((s) => s !== hit) : [...state.picked, hit];
    } else if (!state.picked.includes(hit)) {
      state.picked = [hit];
    }
    dragging2 = { x0: x, y0: y, orig: t, starts: [...state.picked] };
    drawRoll();
  } else {
    box = { x0: x, y0: y, x1: x, y1: y };
  }
};
window.addEventListener("mouseup", (ev) => {
  const down = downAt;
  downAt = null;
  if (resizing || dragging2) {
    resizing = null;
    dragging2 = null;
    edited();
    return;
  }
  if (box) {
    const t = state.score.tracks[state.selected];
    const hi = (ui.canvas as HTMLCanvasElement & { __hi?: number }).__hi ?? 84;
    const b = box;
    box = null;
    const found = notesInRange(t, b.x0 / PX, b.x1 / PX, hi - b.y0 / ROW + 1, hi - b.y1 / ROW, isDrum(t) ? () => 0 : noteNameToMidi);
    const inRange = isDrum(t) ? notesInRange(t, b.x0 / PX, b.x1 / PX) : found;
    state.picked = down?.shift ? [...new Set([...state.picked, ...inRange])] : inRange;
    state.cursor = Math.floor(Math.min(b.x0, b.x1) / PX / state.grid) * state.grid;
    drawRoll();
    return;
  }
  if (!down || ev.target !== ui.canvas || state.tool !== "pen") return;
  const t = state.score.tracks[state.selected];
  const { x, y, hi } = rollPoint(ev);
  const beat = Math.floor(x / PX / state.grid) * state.grid;
  const midi = isDrum(t) ? hi : hi - Math.floor(y / ROW);
  state.cursor = beat;
  penClick(beat, midi);
});

/** 和音の相手のトラックを、count 本になるまで足す（同じ楽器・同じアンプで、少し小さい音）。 */
function ensureCompanions(index: number, count: number): number[] {
  let partners = companions(index);
  const t = state.score.tracks[index];
  const total = trackTotalBeats(t);
  while (partners.length < count) {
    state.score.tracks.splice(index + partners.length + 1, 0, { ...t, amp: t.amp ? { ...t.amp } : undefined, volume: Math.max(0.06, t.volume * 0.8), notes: [{ note: REST, durationBeats: total }] });
    state.muted.clear();
    state.solo.clear();
    partners = companions(index);
  }
  return partners;
}

/** ペンの1クリック: 単音なら足す／消す。和音なら、根音をこのトラックに、ほかの音を和音の相手のトラックに入れる（なければ作る）。 */
function penClick(beat: number, midi: number): void {
  const index = state.selected;
  const t = state.score.tracks[index];
  const total = trackTotalBeats(t);
  const at = noteStartAt(t, beat);
  const shape = isDrum(t) ? [0] : chordIntervals(state.chord);
  if (at !== null) {
    // 消す（和音のときは、相手のトラックの、同じ位置から始まる音も消す）
    state.score.tracks[index] = removeNotes(t, [at]);
    if (shape.length > 1) for (const k of companions(index)) state.score.tracks[k] = removeNotes(state.score.tracks[k], [at]);
    state.picked = [];
    edited();
    return;
  }
  const names = shape.map((iv) => midiToName(Math.min(108, midi + iv)));
  state.score.tracks[index] = addNotes(t, [{ start: beat, dur: state.noteLen, note: names[0] }], total);
  if (names.length > 1) {
    const partners = ensureCompanions(index, names.length - 1);
    names.slice(1).forEach((name, k) => {
      const idx = partners[k];
      state.score.tracks[idx] = addNotes(state.score.tracks[idx], [{ start: beat, dur: state.noteLen, note: name }], total);
    });
  }
  edited();
  auditionChord(state.score.tracks[index], names);
}
function auditionChord(track: Track, names: string[]): void {
  for (const n of names) auditionNote(track, n);
}

// 選んだ音の操作
function withPicked(fn: (t: Track, starts: number[]) => { track: Track; starts: number[] } | Track): void {
  if (state.picked.length === 0) return;
  const r = fn(state.score.tracks[state.selected], state.picked);
  if ("track" in r) {
    state.score.tracks[state.selected] = r.track;
    state.picked = r.starts;
  } else {
    state.score.tracks[state.selected] = r;
  }
  edited();
}
let clipboard: RollNote[] = [];
const ops = {
  del: (): void => withPicked((t, s) => {
    const next = removeNotes(t, s);
    state.picked = [];
    return next;
  }),
  move: (dBeat: number, dSemi: number): void => withPicked((t, s) => moveNotes(t, s, dBeat, isDrum(t) ? 0 : dSemi, transpose)),
  copy: (): void => {
    clipboard = copyNotes(state.score.tracks[state.selected], state.picked);
    if (clipboard.length) ui.status.textContent = `${clipboard.length}音をコピーしました。`;
  },
  paste: (at: number): void => {
    if (clipboard.length === 0) return;
    const r = pasteNotes(state.score.tracks[state.selected], clipboard, at);
    state.score.tracks[state.selected] = r.track;
    state.picked = r.starts;
    edited();
  },
  pickedEnd: (): number => {
    const notes = trackToNotes(state.score.tracks[state.selected]).filter((n) => state.picked.includes(n.start));
    return notes.length ? Math.max(...notes.map((n) => n.start + n.dur)) : state.cursor;
  },
  duplicate: (): void => {
    ops.copy();
    ops.paste(ops.pickedEnd());
  },
  length: (dur: number): void => withPicked((t, s) => setNotesLength(t, s, dur)),
  all: (): void => {
    state.picked = trackToNotes(state.score.tracks[state.selected]).map((n) => n.start);
    drawRoll();
  },
};
ui.rollBox.addEventListener("keydown", (ev) => {
  const ctrl = ev.ctrlKey || ev.metaKey;
  const key = ev.key.toLowerCase();
  let handled = true;
  if (key === "delete" || key === "backspace") ops.del();
  else if (key === "arrowleft") ops.move(-state.grid, 0);
  else if (key === "arrowright") ops.move(state.grid, 0);
  else if (key === "arrowup") ops.move(0, ev.shiftKey ? 12 : 1);
  else if (key === "arrowdown") ops.move(0, ev.shiftKey ? -12 : -1);
  else if (ctrl && key === "c") ops.copy();
  else if (ctrl && key === "v") ops.paste(state.picked.length ? ops.pickedEnd() : state.cursor);
  else if (ctrl && key === "d") ops.duplicate();
  else if (ctrl && key === "a") ops.all();
  else if (key === "escape") {
    state.picked = [];
    drawRoll();
  } else handled = false;
  if (handled) ev.preventDefault();
});
const toolSel = select([["pen", "ペン（足す・消す）"], ["select", "選択（囲む・動かす）"]], "pen");
toolSel.onchange = () => {
  state.tool = toolSel.value as State["tool"];
  drawRoll();
};
const chordSel = select(CHORD_SHAPES.map(([k, l]) => [k, l] as [string, string]), "none");
chordSel.onchange = () => (state.chord = chordSel.value);
function opBtn(label: string, title: string, fn: () => void): HTMLButtonElement {
  const b = h("button", { type: "button", title }, label);
  b.onclick = () => {
    fn();
    ui.rollBox.focus();
  };
  return b;
}
const selTools = h("div", { class: "row", style: "margin-bottom:8px" },
  h("span", { class: "muted" }, "選んだ音:"),
  opBtn("すべて選ぶ", "Ctrl+A", ops.all),
  opBtn("消す", "Delete", ops.del),
  opBtn("←", "左へ（←）", () => ops.move(-state.grid, 0)),
  opBtn("→", "右へ（→）", () => ops.move(state.grid, 0)),
  opBtn("半音↑", "↑", () => ops.move(0, 1)),
  opBtn("半音↓", "↓", () => ops.move(0, -1)),
  opBtn("1オクターブ↑", "Shift+↑", () => ops.move(0, 12)),
  opBtn("1オクターブ↓", "Shift+↓", () => ops.move(0, -12)),
  opBtn("コピー", "Ctrl+C", ops.copy),
  opBtn("貼り付け", "Ctrl+V（選んだ音のすぐ後ろ、または最後にクリックした位置）", () => ops.paste(state.picked.length ? ops.pickedEnd() : state.cursor)),
  opBtn("複製", "Ctrl+D（すぐ後ろにくり返す）", ops.duplicate),
  opBtn("長さをそろえる", "「足す音の長さ」にそろえる", () => ops.length(state.noteLen)),
);
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
let warnedBig = false;
function save(): void {
  try {
    window.localStorage.setItem("sunshine-composer", JSON.stringify({ name: state.name, edition: state.edition, score: state.score }));
  } catch {
    // 録音した音は大きいので、ブラウザの自動保存に入りきらないことがある。そのときは録音をのぞいて保存する
    try {
      window.localStorage.setItem("sunshine-composer", JSON.stringify({ name: state.name, edition: state.edition, score: { ...state.score, audioTracks: undefined } }));
      if (!warnedBig) ui.status.textContent = "録音した音は大きいため、自動保存には入りません。「プロジェクトを保存」で残してください。";
      warnedBig = true;
    } catch {
      // 保存できなくても、操作は続けられる
    }
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

// ── 書き出し（音声: WAV・FLAC・Ogg Opus／データ: MIDI・MusicXML・CSV・プロジェクト） ──
const EXPORTS: [string, string][] = [
  ["wav16", "音声: WAV（16ビット・CDと同じ）"], ["wav24", "音声: WAV（24ビット・高音質）"], ["wav32", "音声: WAV（32ビット小数・編集向け）"],
  ["flac", "音声: FLAC（音質そのまま・小さい）"], ["opus", "音声: Ogg Opus（とても小さい・配信向け）"],
  ["mid", "データ: MIDI（ほかの作曲ソフトへ）"], ["musicxml", "データ: MusicXML（楽譜ソフトへ）"], ["csv", "データ: CSV（音の一覧・表計算ソフトへ）"],
  ["project", "データ: プロジェクト（この作曲ソフトで続きを編集）"],
];
const desktopMp3 = (window as unknown as { sunshineDesktop?: { encodeMp3?(c: Float32Array[], sr: number, kbps: number): Promise<Uint8Array> } }).sunshineDesktop?.encodeMp3;
// MP3 は、デスクトップ版だけ（LAME の部品を別のファイルとして入れているため）
if (desktopMp3) EXPORTS.splice(3, 0, ["mp3", "音声: MP3（256kbps・どこでも再生できる）"]);
const exportSel = select(EXPORTS, "wav16");
const exportBtn = h("button", { class: "primary", type: "button" }, "書き出す");
const safeName = (): string => (state.name || "song").replace(/[\\/:*?"<>|]+/g, "_");
async function renderAudio(sampleRate: number): Promise<AudioBuffer> {
  if (!soundfontCopy) throw new Error("録音音源を読み込めていません");
  return renderScoreOffline({ ...effectiveScore(), loop: false }, { soundfont: soundfontCopy, processorUrl, edition: state.edition, nam: namHost, sampleRate });
}
async function encodeOpus(buffer: AudioBuffer): Promise<Uint8Array> {
  const Encoder = (globalThis as unknown as { AudioEncoder?: typeof AudioEncoder }).AudioEncoder;
  if (!Encoder) throw new Error("このブラウザでは Opus を作れません（Chrome・Edge・デスクトップ版で使えます）");
  const packets: OpusPacket[] = [];
  let failure: Error | null = null;
  const encoder = new Encoder({
    output: (chunk) => {
      const data = new Uint8Array(chunk.byteLength);
      chunk.copyTo(data);
      packets.push({ data, samples: Math.round(((chunk.duration ?? 20000) * 48000) / 1e6) });
    },
    error: (e) => (failure = e as Error),
  });
  encoder.configure({ codec: "opus", sampleRate: 48000, numberOfChannels: 2, bitrate: 192000 });
  const frames = buffer.length;
  const step = 48000;
  for (let at = 0; at < frames; at += step) {
    const n = Math.min(step, frames - at);
    const planar = new Float32Array(n * 2);
    planar.set(buffer.getChannelData(0).subarray(at, at + n), 0);
    planar.set(buffer.getChannelData(1).subarray(at, at + n), n);
    const data = new AudioData({ format: "f32-planar", sampleRate: 48000, numberOfFrames: n, numberOfChannels: 2, timestamp: Math.round((at * 1e6) / 48000), data: planar });
    encoder.encode(data);
    data.close();
  }
  await encoder.flush();
  encoder.close();
  if (failure) throw failure;
  return muxOggOpus(packets, { channels: 2, preSkip: 312, inputSampleRate: 48000, totalSamples: frames, title: state.name });
}
async function doExport(kind: string): Promise<void> {
  const started = performance.now();
  const name = safeName();
  if (kind === "mid") return download(`${name}.mid`, scoreToMidi(effectiveScore()) as BlobPart, "audio/midi");
  if (kind === "musicxml") return download(`${name}.musicxml`, scoreToMusicXml(state.score, state.name), "application/vnd.recordare.musicxml+xml");
  if (kind === "csv") return download(`${name}.csv`, "﻿" + scoreToCsv(state.score), "text/csv");
  if (kind === "project") return exportProject();
  ui.status.textContent = "音を作っています…";
  const buffer = await renderAudio(kind === "opus" ? 48000 : 44100);
  const channels = [buffer.getChannelData(0), buffer.getChannelData(1)];
  normalizePeak(channels);
  if (kind.startsWith("wav")) download(`${name}.wav`, encodeWav(channels, buffer.sampleRate, 0, undefined, Number(kind.slice(3)) as WavBits) as BlobPart, "audio/wav");
  else if (kind === "flac") download(`${name}.flac`, encodeFlac(channels, buffer.sampleRate) as BlobPart, "audio/flac");
  else if (kind === "opus") download(`${name}.opus`, (await encodeOpus(buffer)) as BlobPart, "audio/ogg");
  else if (kind === "mp3" && desktopMp3) download(`${name}.mp3`, (await desktopMp3(channels.map((c) => new Float32Array(c)), buffer.sampleRate, 256)) as BlobPart, "audio/mpeg");
  ui.status.textContent = `書き出しました（${mmss(buffer.duration)}の曲を${((performance.now() - started) / 1000).toFixed(1)}秒で作成）。`;
}
exportBtn.onclick = () => {
  if (exportBtn.disabled) return;
  exportBtn.disabled = true;
  void doExport(exportSel.value)
    .catch((e: unknown) => (ui.status.textContent = `書き出せませんでした: ${(e as Error).message}`))
    .finally(() => (exportBtn.disabled = false));
};

// ── 曲を開く・1から作る ──
const openSongSel = h("select", { style: "max-width:320px" });
{
  const groups = new Map<string, HTMLOptGroupElement>();
  for (const e of allEntries()) {
    let g = groups.get(e.group);
    if (!g) {
      g = h("optgroup", { label: e.group });
      groups.set(e.group, g);
      openSongSel.append(g);
    }
    g.append(h("option", { value: e.id }, `${e.title}（${e.scene}）`));
  }
}
const openEditionSel = select([["modern", "現代的"], ["ps2", "PS2世代"], ["real", "実楽器"]], "real");
const openSongBtn = h("button", { type: "button" }, "この曲を開く");
openSongBtn.onclick = () => {
  const e = allEntries().find((x) => x.id === openSongSel.value);
  if (!e) return;
  // 元の曲を開き、サウンドの版は「サウンド」の切り替えで鳴らす（手直しは元の曲に対して行う）
  state.edition = openEditionSel.value as State["edition"];
  editionSel.value = state.edition;
  loadScore(structuredClone(getTrack(e.id)), e.title);
  ui.status.textContent = `ゲームの曲「${e.title}」を開きました。自由に手直しして、保存・書き出しできます（ゲームの元の曲は変わりません）。`;
};
const sigNum = h("input", { type: "number", min: "1", max: "32", value: "4", style: "width:64px" });
const sigDen = select(DENOMINATORS.map((d) => [String(d), String(d)] as [string, string]), "4");
const blankBpm = h("input", { type: "number", min: "20", max: "300", value: "120" });
const blankBars = h("input", { type: "number", min: "1", max: "512", value: "16" });
const blankTpl = select(BLANK_TEMPLATES.map(([k, l]) => [k, l] as [string, string]), "band");
const blankBtn = h("button", { class: "primary", type: "button" }, "1から作る（空の曲）");
const sigOf = (): { num: number; den: number } => ({ num: Math.max(1, Math.min(32, Math.round(Number(sigNum.value) || 4))), den: Number(sigDen.value) });
blankBtn.onclick = () => {
  const score = createBlankScore({ bpm: Number(blankBpm.value) || 120, sig: sigOf(), bars: Number(blankBars.value) || 16, template: blankTpl.value as BlankTemplate });
  loadScore(score, nameIn.value || "新しい曲");
  ui.status.textContent = `空の曲を作りました（${sigOf().num}/${sigOf().den}拍子・${blankBars.value}小節）。ペンでクリックするか、MIDIキーボードで弾いて入れてください。`;
};
const applySigBtn = h("button", { type: "button" }, "今の曲の拍子・テンポにする");
applySigBtn.onclick = () => {
  state.score.timeSig = sigOf();
  state.score.tempoBpm = Math.max(20, Math.min(300, Number(blankBpm.value) || state.score.tempoBpm));
  renderAll();
  restartSoon();
  save();
};
const openFileBtn = h("button", { type: "button" }, "ファイルを開く（プロジェクト・MIDI・AIソング・アンプ定義）");
openFileBtn.onclick = () => fileIn.click();

// ── MIDIキーボード（ステップ入力・リアルタイム録音） ──
const midiDevSel = h("select", {}, h("option", { value: "" }, "（つないでください）"));
const midiConnectBtn = h("button", { type: "button" }, "MIDIキーボードをつなぐ");
const midiModeSel = select([["off", "入力しない（音だけ鳴らす）"], ["step", "ステップ入力（止めたまま1音ずつ）"], ["rec", "リアルタイム録音（再生しながら弾く）"]], "step");
const midiInfo = h("div", { class: "muted", style: "margin-top:6px" }, "USBのMIDIキーボードをつないで「つなぐ」を押してください。和音で弾くと、すぐ下の同じ楽器のトラックに分けて入ります。");
let midiAccess: MIDIAccess | null = null;
let midiInput: MIDIInput | null = null;
const held = new Map<number, { start: number; track: number; vel: number }>();
let stepPlaced = 0;
function beatNow(): number {
  const total = trackTotalBeats(state.score.tracks[0]);
  const b = (engine.getBgmPositionSec() * state.score.tempoBpm) / 60;
  return ((b % total) + total) % total;
}
const quant = (b: number): number => Math.round(b / state.grid) * state.grid;
function voiceTrack(voice: number): number {
  if (voice === 0) return state.selected;
  return ensureCompanions(state.selected, voice)[voice - 1];
}
function onMidiNote(on: boolean, pitch: number, vel: number): void {
  const t = state.score.tracks[state.selected];
  const noteName = midiToName(Math.max(12, Math.min(108, pitch)));
  if (on) auditionNote(t, noteName);
  const mode = midiModeSel.value;
  if (mode === "off") return;
  const total = trackTotalBeats(t);
  if (on) {
    const voice = held.size;
    if (mode === "rec") {
      if (!state.playing || state.paused) {
        midiInfo.textContent = "リアルタイム録音は、▶ で再生しながら弾いてください。";
        return;
      }
      held.set(pitch, { start: quant(beatNow()), track: voiceTrack(voice), vel });
    } else {
      const track = voiceTrack(voice);
      const target = state.score.tracks[track];
      state.score.tracks[track] = addNotes(target, [{ start: state.cursor, dur: Math.min(state.noteLen, total - state.cursor), note: noteName, velocity: Math.round((vel / 100) * 100) / 100 }], total);
      held.set(pitch, { start: state.cursor, track, vel });
      stepPlaced++;
      drawRoll();
    }
    return;
  }
  const h0 = held.get(pitch);
  held.delete(pitch);
  if (!h0) return;
  if (mode === "rec") {
    let end = quant(beatNow());
    if (end <= h0.start) end = end + total <= h0.start + total ? h0.start + state.grid : end + total;
    const dur = Math.max(state.grid, Math.min(end - h0.start, total - h0.start));
    const target = state.score.tracks[h0.track];
    state.score.tracks[h0.track] = addNotes(target, [{ start: h0.start, dur, note: noteName, velocity: Math.round((h0.vel / 100) * 100) / 100 }], trackTotalBeats(target));
    drawRoll();
    renderTracks();
    save();
  } else if (held.size === 0 && stepPlaced > 0) {
    // 和音の鍵盤がすべて離れたら、次の位置へ進む
    state.cursor = Math.min(total - state.grid, state.cursor + state.noteLen);
    stepPlaced = 0;
    drawRoll();
    renderTracks();
    save();
    midiInfo.textContent = `次の入力位置: ${Math.floor(state.cursor / barBeats(timeSignatureOf(state.score))) + 1}小節目（${state.cursor}拍）。ピアノロールをクリックすると、そこから入れられます。`;
  }
}
function attachMidi(id: string): void {
  if (midiInput) midiInput.onmidimessage = null;
  midiInput = midiAccess ? ([...midiAccess.inputs.values()].find((x) => x.id === id) ?? null) : null;
  if (!midiInput) return;
  midiInput.onmidimessage = (ev) => {
    const d = ev.data;
    if (!d || d.length < 3) return;
    const kind = d[0] & 0xf0;
    if (kind === 0x90 && d[2] > 0) onMidiNote(true, d[1], d[2]);
    else if (kind === 0x80 || (kind === 0x90 && d[2] === 0)) onMidiNote(false, d[1], 0);
  };
  midiInfo.textContent = `「${midiInput.name ?? "MIDIキーボード"}」につなぎました。`;
}
function listMidi(): void {
  if (!midiAccess) return;
  const inputs = [...midiAccess.inputs.values()];
  midiDevSel.replaceChildren(...(inputs.length ? inputs.map((x) => h("option", { value: x.id }, x.name ?? x.id)) : [h("option", { value: "" }, "（見つかりません）")]));
  if (inputs.length) attachMidi(inputs[0].id);
}
midiConnectBtn.onclick = () => {
  if (!("requestMIDIAccess" in navigator)) {
    midiInfo.textContent = "このブラウザでは MIDIキーボードを使えません（Chrome・Edge・デスクトップ版で使えます）。";
    return;
  }
  void navigator.requestMIDIAccess({ sysex: false }).then((access) => {
    midiAccess = access;
    access.onstatechange = listMidi;
    listMidi();
  }).catch(() => (midiInfo.textContent = "MIDIキーボードを使う許可がもらえませんでした。"));
};
midiDevSel.onchange = () => attachMidi(midiDevSel.value);
// 画面のテストや、Claude Code から確かめるための入口
(window as unknown as { __midiTest: unknown }).__midiTest = { note: onMidiNote, setMode: (m: string) => (midiModeSel.value = m) };

// ── 追加したアンプ（アンプ定義ファイル） ──
/** 使えるアンプ定義の一覧（見本・デスクトップ版の追加フォルダ・読み込んだもの）。 */
const ampLibrary = new Map<string, AmpPluginDef>();
declare const __AMP_SAMPLES__: AmpPluginDef[];
for (const d of typeof __AMP_SAMPLES__ === "object" ? __AMP_SAMPLES__ : []) ampLibrary.set(d.id, d);
function addAmpPlugin(data: unknown, announce: boolean): AmpPluginDef | null {
  try {
    const def = validateAmpPlugin(data);
    if (hasCode(def) && announce && !window.confirm(`アンプ「${def.label}」は、プログラム（音の処理）を含みます。信頼できる配布元のものだけ使ってください。読み込みますか？`)) return null;
    ampLibrary.set(def.id, def);
    if (announce) ui.status.textContent = `アンプ「${def.label}」を追加しました。「音づくり」で「追加したアンプ」を選ぶと使えます。`;
    renderAmp();
    return def;
  } catch (e) {
    ui.status.textContent = `アンプ定義を読み込めませんでした:\n${(e as Error).message}`;
    return null;
  }
}

// Claude Code の song.mjs（--wav）から、曲をWAVにするための入口
(window as unknown as { __composer: unknown }).__composer = {
  async renderWav(score: Score, edition: State["edition"]): Promise<string> {
    if (!soundfontCopy) throw new Error("録音音源を読み込めていません");
    const edited = edition === "ps2" ? ps2Edition(score) : edition === "real" ? realEdition(score) : score;
    const buffer = await renderScoreOffline({ ...edited, loop: false }, { soundfont: soundfontCopy, processorUrl, edition, nam: namHost });
    const channels = [buffer.getChannelData(0), buffer.getChannelData(1)];
    normalizePeak(channels);
    const bytes = encodeWav(channels, buffer.sampleRate);
    let bin = "";
    for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
    return btoa(bin);
  },
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
  ["auto", "おまかせ（曲の設定どおり）"], ["clean", "クリーン"], ["overdrive", "オーバードライブ"], ["distortion", "ディストーション"], ["metal", "メタルゾーン"], ["prs", "なめらかなリード（PRS風）"], ["plugin", "追加したアンプ（アンプ定義ファイル）"], ["nam", "NAMのアンプモデル（実機を学習したもの）"],
  ["jazz", "ジャズ（太く柔らかい）"], ["blues", "ブルース（浅く温かい歪み）"], ["funk", "ファンク（明るく歯切れよい）"], ["crunch", "クランチ（ざらっと浅い歪み）"], ["hardrock", "ハードロック（深い歪み）"], ["punk", "パンク（勢いのある歪み）"], ["fuzz", "ファズ（荒々しく不穏）"], ["shoegaze", "シューゲイザー（霞んだ音の壁）"], ["lofi", "ローファイ（古い録音）"], ["retro8bit", "レトロ8bit（粗い階段の音）"], ["radio", "ラジオ・電話（遠くの音）"],
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
    const type = typeSel.value as AmpSetting["type"];
    change({ ...amp, type, ...(type === "genre" && !amp.preset ? { preset: "rock" as AmpPresetName } : {}) });
    renderAmp();
  };
  const row = h("div", { class: "row" }, field(`「${instLabel(t.instrument)}」のアンプ`, typeSel),
    slider("歪みの深さ", 0.5, 2, 0.05, amp.drive ?? 1, (v) => change({ ...(t.amp ?? amp), drive: v })),
    slider("高音の明るさ(dB)", -6, 6, 0.5, amp.tone ?? 0, (v) => change({ ...(t.amp ?? amp), tone: v })),
    slider("出力の大きさ", 0.5, 1.5, 0.05, amp.level ?? 1, (v) => change({ ...(t.amp ?? amp), level: v })));
  ampBox.append(row);
  if (amp.type === "genre") {
    const presetSel = select(AMP_PRESET_NAMES.map((k) => [k, `${AMP_PRESETS[k].label}（${AMP_PRESETS[k].genre}）`] as [string, string]), amp.preset ?? "rock");
    presetSel.onchange = () => change({ ...(t.amp ?? amp), type: "genre", preset: presetSel.value as AmpPresetName });
    ampBox.append(h("div", { class: "row", style: "margin-top:8px" }, field("ジャンル", presetSel)),
      h("div", { class: "muted", style: "margin-top:4px" }, "ジャンルごとに、歪み・低音／中音／高音・キャビネットを組み合わせたアンプです（ブラウザの音の部品だけで作った無料のもの。実在の機材の再現ではありません）。ギター以外（ピアノ・シンセ・声など）にもかけられます。"));
  }
  if (amp.type === "plugin") {
    const list: [string, string][] = [["", "（アンプを選ぶ）"], ...[...ampLibrary.values(), ...Object.values(state.score.ampPlugins ?? {}).filter((d) => !ampLibrary.has(d.id))].map((d) => [d.id, `${d.label}${d.license ? `［${d.license}］` : ""}`] as [string, string])];
    const pluginSel = select(list, amp.plugin ?? "");
    pluginSel.onchange = () => {
      const def = ampLibrary.get(pluginSel.value) ?? state.score.ampPlugins?.[pluginSel.value];
      // 選んだアンプの定義は、曲（プロジェクト）の中にも入れておく（ほかのパソコンでも同じ音になるように）
      if (def) state.score.ampPlugins = { ...(state.score.ampPlugins ?? {}), [def.id]: def };
      change({ ...(t.amp ?? amp), type: "plugin", plugin: pluginSel.value || undefined });
      renderAmp();
    };
    const pick = h("input", { type: "file", accept: ".json,application/json", hidden: "" });
    pick.onchange = () => {
      const f = pick.files?.[0];
      if (f) void f.text().then((text) => addAmpPlugin(JSON.parse(text), true));
      pick.value = "";
    };
    const load = h("button", { type: "button" }, "アンプ定義（.sunshine-amp.json）を読み込む");
    load.onclick = () => pick.click();
    const irPick = h("input", { type: "file", accept: ".wav,audio/wav", hidden: "" });
    irPick.onchange = () => {
      const f = irPick.files?.[0];
      if (!f) return;
      void f.arrayBuffer().then((buf) => {
        const bytes = new Uint8Array(buf);
        let bin = "";
        for (let k = 0; k < bytes.length; k += 0x8000) bin += String.fromCharCode(...bytes.subarray(k, k + 0x8000));
        const id = `ir-${f.name.toLowerCase().replace(/\.wav$/, "").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "cab"}`;
        const def = addAmpPlugin({ format: "sunshine-amp", version: 1, id, label: `キャビネットIR: ${f.name}`, license: "利用者が用意したIR（規約は各自で確認）", stages: [{ type: "gain", value: 4 }, { type: "drive", shape: "soft", hardness: 3 }, { type: "ir", wav: btoa(bin), mix: 1 }, { type: "gain", value: 0.6 }] }, true);
        if (def) pluginSel.value = def.id;
      });
      irPick.value = "";
    };
    const ir = h("button", { type: "button" }, "キャビネットIR（.wav）からアンプを作る");
    ir.onclick = () => irPick.click();
    const folderBtn = h("button", { type: "button" }, "アンプの追加フォルダを開く");
    folderBtn.onclick = () => void desktop?.openAmpFolder();
    ampBox.append(h("div", { class: "row", style: "margin-top:8px" }, field("追加したアンプ", pluginSel), load, pick, ir, irPick, ...(desktop ? [folderBtn] : [])),
      h("div", { class: "muted", style: "margin-top:4px" }, "ほかのアンプシミュレーターを、アンプ定義ファイル（歪み・イコライザー・キャビネットIR・自作の処理・NAMモデルの組み合わせ）として追加できます。書き方は docs/design/amp-plugins.md。デスクトップ版では、「アンプの追加フォルダ」に置くと起動時に読み込みます。"));
  }
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
    const load = h("button", { type: "button" }, "ほかのモデル（.nam）を読み込む");
    load.onclick = () => file.click();
    const models: [string, string][] = [["", "（モデルを選ぶ）"], ...Object.entries(BUILTIN_NAM).map(([k, v]) => [k, `同梱: ${v.label}`] as [string, string]), ...Object.keys(state.score.namModels ?? {}).map((k) => [k, `読み込んだモデル: ${k}`] as [string, string])];
    const modelSel = select(models, amp.model ?? "");
    modelSel.onchange = () => {
      change({ ...(t.amp ?? amp), type: "nam", model: modelSel.value || undefined });
      renderAmp();
    };
    ampBox.append(h("div", { class: "row", style: "margin-top:8px" }, field("NAMのモデル", modelSel), load, file, h("span", { class: "muted" }, amp.model ? "" : "モデルを選ぶまでは、元の音のまま")),
      h("div", { class: "muted", style: "margin-top:4px" }, "NAMは、実際のアンプを学習した無料のアンプシミュレーターです。同梱のモデルは、NAMの作者がMITライセンスで公開している見本です。ほかのモデル（.nam）は、配布元の利用規約（商用利用・再配布）を確認してから使ってください。「歪みの深さ」はモデルへ入る音の大きさになります。ゲームには、NAMモデルは入れません（ふつうのアンプの音になります）。"));
  }
}

// ── AIに作曲してもらう（デスクトップ版だけ。APIキーはアプリ本体の側で暗号化して保存し、画面には渡さない） ──
interface DesktopKeyStatus {
  hasKey: boolean;
  last4: string;
  canSave: boolean;
}
interface DesktopApi {
  keyStatus(): Promise<DesktopKeyStatus>;
  setKey(key: string): Promise<DesktopKeyStatus>;
  clearKey(): Promise<DesktopKeyStatus>;
  compose(req: { model: string; effort: string; request: string; system: string; schema: unknown; continue: boolean }): Promise<{ text: string; usage: { input: number; output: number } }>;
  listAmpPlugins(): Promise<{ file: string; text: string }[]>;
  encodeMp3?(channels: Float32Array[], sampleRate: number, kbps: number): Promise<Uint8Array>;
  openAmpFolder(): Promise<void>;
}
const desktop = (window as unknown as { sunshineDesktop?: DesktopApi }).sunshineDesktop;
const aiBox = h("div", {});
function buildAiPanel(api: DesktopApi): void {
  const keyIn = h("input", { type: "password", placeholder: "sk-ant-…", autocomplete: "off", style: "min-width:240px" });
  const keySave = h("button", { type: "button" }, "キーを保存");
  const keyClear = h("button", { type: "button" }, "キーを消す");
  const keyInfo = h("span", { class: "muted" });
  const modelSel = select([["claude-opus-5-5", "Claude Opus 5.5（いちばん上手）"], ["claude-sonnet-5-5", "Claude Sonnet 5.5（速い・安い）"]], "claude-opus-5-5");
  const effortSel = select([["low", "さっと"], ["medium", "ふつう"], ["high", "じっくり"]], "medium");
  const req = h("textarea", { rows: "3", style: "width:100%", placeholder: "例: 雪の降る港町の夜。やさしいピアノとストリングス、少しさみしいけれどあたたかい。70秒くらい。" });
  const newBtn = h("button", { class: "primary", type: "button" }, "AIに新しい曲を作ってもらう");
  const fixBtn = h("button", { type: "button", disabled: "" }, "この曲をAIに直してもらう");
  const msg = h("div", { class: "muted", style: "margin-top:6px;white-space:pre-wrap" });
  const show = (st: DesktopKeyStatus): void => {
    keyInfo.textContent = st.hasKey ? `保存済み（末尾 …${st.last4}）${st.canSave ? "・OSの機能で暗号化" : "・このパソコンでは暗号化できないため、終了すると消えます"}` : "まだ入っていません";
    keyClear.disabled = !st.hasKey;
  };
  void api.keyStatus().then(show);
  keySave.onclick = () => {
    const key = keyIn.value.trim();
    keyIn.value = "";
    void api.setKey(key).then(show).catch((e: unknown) => (msg.textContent = (e as Error).message.replace(/^Error invoking remote method '[^']+': (Error: )?/, "")));
  };
  keyClear.onclick = () => void api.clearKey().then(show);
  let hasHistory = false;
  const run = async (fix: boolean): Promise<void> => {
    const request = req.value.trim();
    if (!request) {
      msg.textContent = fix ? "どう直したいかを書いてください（例: サビをもっと盛り上げて、テンポを少し速く）。" : "どんな曲がほしいかを書いてください。";
      return;
    }
    newBtn.disabled = true;
    fixBtn.disabled = true;
    msg.textContent = "AIが作曲しています…（30秒〜数分かかります）";
    const clean = (e: unknown): string => (e as Error).message.replace(/^Error invoking remote method '[^']+': (Error: )?/, "");
    try {
      let answer = await api.compose({ model: modelSel.value, effort: effortSel.value, request, system: AI_SONG_GUIDE, schema: AI_SONG_SCHEMA, continue: fix });
      let used = { ...answer.usage };
      let built;
      try {
        built = aiSongToScore(JSON.parse(answer.text));
      } catch (first) {
        // 形式のまちがいは、1回だけ理由を伝えて直してもらう
        answer = await api.compose({ model: modelSel.value, effort: effortSel.value, request: `次のまちがいがありました。直した曲を、同じ形式でもう一度書いてください。\n${(first as Error).message}`, system: AI_SONG_GUIDE, schema: AI_SONG_SCHEMA, continue: true });
        used = { input: used.input + answer.usage.input, output: used.output + answer.usage.output };
        built = aiSongToScore(JSON.parse(answer.text));
      }
      hasHistory = true;
      loadScore(built.score, built.song.title || "AIの曲");
      msg.textContent = `できました: 「${built.song.title}」— ${built.song.description}\n使ったトークン: 入力 ${used.input}・出力 ${used.output}${built.warnings.length ? `\n注意: ${built.warnings.join(" / ")}` : ""}\n▶ で聴けます。ピアノロールで手直しもできます。`;
    } catch (e) {
      msg.textContent = clean(e);
    } finally {
      newBtn.disabled = false;
      fixBtn.disabled = !hasHistory;
    }
  };
  newBtn.onclick = () => void run(false);
  fixBtn.onclick = () => void run(true);
  aiBox.append(
    h("div", { class: "row" }, field("Anthropic APIキー", keyIn), keySave, keyClear, keyInfo),
    h("div", { class: "row", style: "margin-top:8px" }, field("モデル", modelSel), field("考える深さ", effortSel)),
    h("div", { style: "margin-top:8px" }, req),
    h("div", { class: "row", style: "margin-top:8px" }, newBtn, fixBtn),
    msg,
    h("div", { class: "muted", style: "margin-top:6px" }, "APIキーは、このパソコンの中だけに暗号化して保存し、Anthropic（api.anthropic.com）との通信にだけ使います。使った分の料金は、キーの持ち主にかかります（https://console.anthropic.com）。AIには、既存の曲をまねしないよう指示しています。"),
  );
}
if (desktop) {
  buildAiPanel(desktop);
  // アンプの追加フォルダのアンプを読み込む
  void desktop.listAmpPlugins().then((files) => {
    const bad: string[] = [];
    for (const f of files) {
      try {
        const def = validateAmpPlugin(JSON.parse(f.text));
        ampLibrary.set(def.id, def);
      } catch (e) {
        bad.push(`${f.file}: ${(e as Error).message.split("\n")[0]}`);
      }
    }
    if (files.length) ui.status.textContent = `アンプの追加フォルダから ${files.length - bad.length} 個のアンプを読み込みました${bad.length ? `（読めなかったもの: ${bad.join(" / ")}）` : ""}。`;
    renderAmp();
  });
}
else aiBox.append(h("div", { class: "muted" }, "AI作曲（Anthropic APIキーを使う）は、デスクトップ版で使えます。Claude Code から作るときは、コネクタ（tools/mcp/server.mjs）か /compose-song を使ってください。"));

// ── 実際の楽器を録る（オーディオインターフェース） ──
const recDevSel = h("select", { style: "max-width:260px" }, h("option", { value: "" }, "（「使う」を押してください）"));
const recUseBtn = h("button", { type: "button" }, "オーディオインターフェースを使う");
const recModeSel = select([["in1", "入力1（左）だけ・モノラル"], ["in2", "入力2（右）だけ・モノラル"], ["stereo", "ステレオ（入力1・2）"]], "in1");
const recTargetSel = h("select", {});
const recMonitor = h("input", { type: "checkbox" });
const recLatency = h("input", { type: "number", min: "-500", max: "1000", value: "", placeholder: "自動", style: "width:80px" });
const recBtn = h("button", { class: "primary", type: "button", disabled: "" }, "● 録音");
const recStopBtn = h("button", { type: "button", disabled: "" }, "■ 録音を止める");
const recInfo = h("div", { class: "muted", style: "margin-top:6px;white-space:pre-wrap" }, "ギター・ベースはライン（楽器の端子）で入力1へ、声やアコースティック楽器はマイクで。録音は、ピアノロールで最後にクリックした位置から始まります。");
const audioBox = h("div", { class: "tracks", style: "margin-top:8px;max-height:280px" });
let liveInput: LiveInput | null = null;
let recording: { rec: Recording; startCtx: number; songStartAt: number | null; startBeat: number; target: number } | null = null;

function audioTracks(): AudioTrack[] {
  state.score.audioTracks ??= [];
  return state.score.audioTracks;
}
function renderRecTargets(): void {
  const keep = recTargetSel.value;
  recTargetSel.replaceChildren(h("option", { value: "new" }, "新しい録音トラック"), ...audioTracks().map((t, i) => h("option", { value: String(i) }, `${i + 1}. ${t.name}`)));
  recTargetSel.value = [...recTargetSel.options].some((o) => o.value === keep) ? keep : "new";
}
const AUDIO_AMPS = (): [string, string][] => [
  ["auto", "アンプなし（そのまま）"], ["clean", "クリーン"], ["overdrive", "オーバードライブ"], ["distortion", "ディストーション"], ["metal", "メタルゾーン"], ["prs", "なめらかなリード"],
  ...AMP_TYPES.filter(([k]) => !["auto", "clean", "overdrive", "distortion", "metal", "prs", "plugin", "nam"].includes(k)).map(([k, l]) => [k, `ジャンル: ${l}`] as [string, string]),
  ...[...ampLibrary.values()].map((d) => [`plugin:${d.id}`, `追加: ${d.label}`] as [string, string]),
  ...Object.keys(BUILTIN_NAM).map((k) => [`nam:${k}`, `NAM: ${BUILTIN_NAM[k].label}`] as [string, string]),
];
function ampToKey(a?: AmpSetting): string {
  if (!a || a.type === "auto") return "auto";
  if (a.type === "genre") return `genre:${a.preset ?? "rock"}`;
  if (a.type === "plugin") return `plugin:${a.plugin}`;
  if (a.type === "nam") return `nam:${a.model}`;
  return a.type;
}
function keyToAmp(k: string): AmpSetting | undefined {
  if (k === "auto") return undefined;
  const [type, rest] = k.split(":");
  if (type === "genre") return { type: "genre", preset: rest as AmpPresetName };
  if (type === "plugin") {
    const def = ampLibrary.get(rest);
    if (def) state.score.ampPlugins = { ...(state.score.ampPlugins ?? {}), [def.id]: def };
    return { type: "plugin", plugin: rest };
  }
  if (type === "nam") return { type: "nam", model: rest };
  return { type: type as AmpSetting["type"] };
}
function renderAudioTracks(): void {
  audioBox.replaceChildren();
  audioTracks().forEach((t, i) => {
    const name = h("input", { type: "text", value: t.name, style: "width:120px" });
    name.onchange = () => {
      t.name = name.value || `録音 ${i + 1}`;
      renderRecTargets();
      save();
    };
    const vol = h("input", { type: "range", min: "0", max: "150", value: String(Math.round(t.volume * 100)), title: "音量" });
    vol.oninput = () => {
      t.volume = Number(vol.value) / 100;
      restartSoon();
      save();
    };
    const pan = h("input", { type: "range", min: "-100", max: "100", value: String(Math.round(t.pan * 100)), title: "左右の位置" });
    pan.oninput = () => {
      t.pan = Number(pan.value) / 100;
      restartSoon();
      save();
    };
    const amp = select(AUDIO_AMPS(), ampToKey(t.amp));
    amp.onchange = () => {
      t.amp = keyToAmp(amp.value);
      if (liveInput && recMonitor.checked && recTargetSel.value === String(i)) liveInput.setMonitor(true, t.amp, effectiveScore());
      restartSoon();
      save();
    };
    const mute = h("button", { type: "button", class: t.muted ? "on" : "", title: "ミュート" }, "M");
    mute.onclick = () => {
      t.muted = !t.muted;
      renderAudioTracks();
      restartSoon();
      save();
    };
    const undo = h("button", { type: "button", title: "最後の録音を消す" }, "↶");
    undo.onclick = () => {
      t.clips.pop();
      renderAudioTracks();
      restartSoon();
      save();
    };
    const del = h("button", { type: "button", title: "この録音トラックを消す" }, "✕");
    del.onclick = () => {
      if (!window.confirm(`録音トラック「${t.name}」を消しますか？（元に戻せません）`)) return;
      audioTracks().splice(i, 1);
      renderAudioTracks();
      renderRecTargets();
      restartSoon();
      save();
    };
    const secs = t.clips.reduce((sum, c) => sum + c.seconds, 0);
    audioBox.append(h("div", { class: "trk", title: `${t.clips.length}回の録音・合計${secs.toFixed(1)}秒` }, h("div", { class: "nm" }, name, h("span", { class: "muted" }, ` ${t.clips.length}回・${secs.toFixed(1)}秒`)), amp, h("div", { class: "bt" }, mute, undo, del), vol, pan));
  });
  if (audioTracks().length === 0) audioBox.append(h("div", { class: "muted" }, "録音トラックはまだありません。"));
}
recUseBtn.onclick = () => {
  void listInputs().then((list) => {
    recDevSel.replaceChildren(...list.map((d) => h("option", { value: d.id }, d.label)));
    recBtn.disabled = list.length === 0;
    recInfo.textContent = list.length ? `${list.length}個の入力が見つかりました。入力を選んで「● 録音」を押してください。ヘッドホンで聞いてください（スピーカーだと、音がマイクに回りこみます）。` : "入力が見つかりません。オーディオインターフェースをつないでから、もう一度押してください。";
  }).catch((e: unknown) => (recInfo.textContent = `使えませんでした: ${(e as Error).message}`));
};
async function ensureInput(): Promise<LiveInput> {
  const ctx = engine.audioContext();
  const key = `${recDevSel.value}|${recModeSel.value}`;
  if (liveInput && (liveInput as LiveInput & { key?: string }).key === key) return liveInput;
  liveInput?.close();
  liveInput = await openInput(ctx, recDevSel.value, recModeSel.value as InputMode, engine.clipDestination(), namHost);
  (liveInput as LiveInput & { key?: string }).key = key;
  return liveInput;
}
const targetAmp = (): AmpSetting | undefined => (recTargetSel.value === "new" ? undefined : audioTracks()[Number(recTargetSel.value)]?.amp);
recMonitor.onchange = () => {
  void ensureInput().then((inp) => inp.setMonitor(recMonitor.checked, targetAmp(), effectiveScore())).catch((e: unknown) => (recInfo.textContent = (e as Error).message));
};
recDevSel.onchange = recModeSel.onchange = () => {
  liveInput?.close();
  liveInput = null;
  if (recMonitor.checked) recMonitor.onchange?.(new Event("change"));
};
recTargetSel.onchange = () => {
  if (recMonitor.checked && liveInput) liveInput.setMonitor(true, targetAmp(), effectiveScore());
};
recBtn.onclick = () => {
  void (async () => {
    const ctx = engine.audioContext();
    const input = await ensureInput();
    if (recMonitor.checked) input.setMonitor(true, targetAmp(), effectiveScore());
    let target = recTargetSel.value === "new" ? -1 : Number(recTargetSel.value);
    if (target < 0) {
      audioTracks().push({ name: `録音 ${audioTracks().length + 1}`, volume: 1, pan: 0, clips: [] });
      target = audioTracks().length - 1;
      renderRecTargets();
      recTargetSel.value = String(target);
    }
    const rec = await startRecording(ctx, input);
    const startBeat = state.cursor;
    recording = { rec, startCtx: ctx.currentTime, songStartAt: null, startBeat, target };
    play((startBeat * 60) / state.score.tempoBpm);
    recBtn.disabled = true;
    recStopBtn.disabled = false;
    recInfo.textContent = "● 録音中… 弾き終わったら「■ 録音を止める」。";
  })().catch((e: unknown) => (recInfo.textContent = `録音を始められませんでした: ${(e as Error).message}`));
};
recStopBtn.onclick = () => {
  const r = recording;
  if (!r) return;
  recording = null;
  recStopBtn.disabled = true;
  void (async () => {
    const { channels, sampleRate } = await r.rec.stop();
    engine.stopBgm();
    state.playing = false;
    const ctx = engine.audioContext();
    // 録音の頭が、曲のどこにあたるか: （録音を始めた時刻 − 曲の頭の時刻 − 入出力の遅れ）
    const auto = (ctx.baseLatency ?? 0) + ((ctx as AudioContext & { outputLatency?: number }).outputLatency ?? 0);
    const latency = recLatency.value === "" ? auto : Number(recLatency.value) / 1000;
    const songStartAt = r.songStartAt ?? r.startCtx;
    let startSec = r.startCtx - songStartAt - latency;
    let skip = 0;
    if (startSec < 0) {
      skip = Math.round(-startSec * sampleRate);
      startSec = 0;
    }
    const songSec = getScoreDurationSec(state.score);
    const keepFrames = Math.max(0, Math.min(channels[0].length - skip, Math.round((songSec - startSec) * sampleRate)));
    if (keepFrames < sampleRate * 0.05) {
      recInfo.textContent = `録音が短すぎるので、捨てました（録れた長さ ${(channels[0].length / sampleRate).toFixed(2)}秒）。`;
      recBtn.disabled = false;
      return;
    }
    const trimmed = channels.map((c) => c.subarray(skip, skip + keepFrames));
    const flac = encodeFlac(trimmed, sampleRate);
    const track = audioTracks()[r.target];
    track.clips.push({ id: `c${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`, startBeat: (startSec * state.score.tempoBpm) / 60, flac: bytesToBase64(flac), seconds: keepFrames / sampleRate });
    renderAudioTracks();
    save();
    recInfo.textContent = `録音しました（${(keepFrames / sampleRate).toFixed(1)}秒・${channels.length === 2 ? "ステレオ" : "モノラル"}・ずれの補正 ${Math.round(latency * 1000)}ミリ秒）。▶ で聴けます。ずれて聞こえるときは「ずれの補正」を変えて録り直してください。`;
    recBtn.disabled = false;
  })().catch((e: unknown) => {
    recInfo.textContent = `録音を止められませんでした: ${(e as Error).message}`;
    recBtn.disabled = false;
  });
};
// 曲の頭の時刻（録音のずれの計算用）を、再生が始まった瞬間に記録する
function watchRecordingStart(): void {
  if (recording && recording.songStartAt === null && state.playing) {
    const pos = engine.getBgmPositionSec();
    if (pos > 0.02) recording.songStartAt = engine.audioContext().currentTime - pos;
  }
  requestAnimationFrame(watchRecordingStart);
}
watchRecordingStart();

// ── 画面を組み立てる ──
function renderAll(): void {
  renderTracks();
  renderAudioTracks();
  renderRecTargets();
  renderAmp();
  drawRoll();
  ui.status.textContent = `${state.name}｜${state.score.tracks.length}トラック｜${mmss(getScoreDurationSec(state.score))}｜テンポ ${state.score.tempoBpm}`;
  lcdTempo.textContent = String(state.score.tempoBpm);
  lcdTracks.textContent = String(state.score.tracks.length).padStart(2, "0");
  lcdLen.textContent = mmss(getScoreDurationSec(state.score));
}
const composeBtn = h("button", { class: "primary", type: "button" }, "自動作曲");
composeBtn.onclick = composeAuto;
const specialBtn = h("button", { type: "button" }, "特別曲（3〜4分）を作る");
specialBtn.onclick = composeSpecial;


const saveBtn = h("button", { type: "button" }, "プロジェクトを保存");
saveBtn.onclick = exportProject;
const loadBtn = h("button", { type: "button" }, "プロジェクトを読み込む");
loadBtn.onclick = () => fileIn.click();

const lcdTempo = h("span", { class: "lcd-v" }, "120");
const lcdTracks = h("span", { class: "lcd-v" }, "0");
const lcdLen = h("span", { class: "lcd-v" }, "0:00");
const lcd = (label: string, value: HTMLElement): HTMLElement => h("div", { class: "lcd-cell" }, h("span", { class: "lcd-k" }, label), value);
ui.playBtn.textContent = "▶";
ui.playBtn.title = "再生（はじめから）";
ui.playBtn.setAttribute("aria-label", "再生（はじめから）");
setPauseLook(false);
ui.stopBtn.textContent = "■";
ui.stopBtn.title = "停止";
ui.stopBtn.setAttribute("aria-label", "停止");
for (const b of [ui.playBtn, ui.pauseBtn, ui.stopBtn]) b.classList.add("tp");
const panel = (code: string, title: string, ...kids: (Node | string)[]): HTMLElement =>
  h("section", { class: "panel" }, h("h2", {}, h("span", { class: "code" }, code), title), ...kids);

app.append(
  h("header", { class: "topbar" },
    h("div", { class: "brand" }, h("div", { class: "logo", "aria-hidden": "true" }), h("div", {}, h("h1", {}, "SUNSHINE", h("b", {}, " COMPOSER")), h("div", { class: "sub" }, "サンシャイン作曲ソフト ・ 実楽器エンジン"))),
    h("div", { class: "transport" }, ui.playBtn, ui.pauseBtn, ui.stopBtn),
    h("div", { class: "lcd" }, h("div", { class: "lcd-time" }, ui.time), lcd("BPM", lcdTempo), lcd("TRK", lcdTracks), lcd("LEN", lcdLen)),
    h("div", { class: "seekwrap" }, ui.seek),
    h("div", { class: "row topopts" }, field("サウンド", editionSel), field("マスター音量", volIn)),
  ),
  h("div", { class: "daw" },
    panel("TRK", "トラック", ui.trackBox, h("div", { class: "row", style: "margin-top:8px" }, addTrackBtn),
      h("div", { class: "muted", style: "margin-top:4px" }, "1つのトラックは1度に1音だけ鳴ります（和音は、トラックを重ねて作ります）。")),
    panel("ROLL", "ピアノロール",
      h("div", { class: "row", style: "margin-bottom:8px" }, field("道具", toolSel), field("和音で足す", chordSel), field("クリックの間隔", gridSel), field("足す音の長さ", lenSel), clearBtn), selTools, h("div", { class: "info" }, ui.info), ui.rollBox,
      h("div", { class: "muted", style: "margin-top:4px" }, "和音: 根音をいま選んでいるトラックに、ほかの音をすぐ下の同じ楽器のトラック（うすく表示。足りなければ自動で作る）に入れます。")),
  ),
  h("div", { class: "grid" },
    panel("AI", "AIに作曲してもらう（Claude）", aiBox),
    panel("PRJ", "曲を開く・1から作る",
      h("div", { class: "row" }, field("ゲームの曲（全曲）", openSongSel), field("サウンド", openEditionSel), openSongBtn),
      h("div", { class: "row", style: "margin-top:10px" }, field("拍子（上）", sigNum), h("span", { style: "align-self:end;padding-bottom:8px" }, "/"), field("拍子（下）", sigDen), field("テンポ", blankBpm), field("小節の数", blankBars), field("はじめの編成", blankTpl)),
      h("div", { class: "row", style: "margin-top:8px" }, blankBtn, applySigBtn),
      h("div", { class: "row", style: "margin-top:10px" }, openFileBtn),
      h("div", { class: "muted", style: "margin-top:6px" }, "拍子は自由に選べます（例: 4/4・3/4・6/8・7/8・5/4・13/16）。ゲームの曲は、開いて手直ししても、ゲームの元の曲は変わりません（保存・書き出し・ゲームへの登録で使えます）。")),
    panel("REC", "実際の楽器を録る（オーディオインターフェース）",
      h("div", { class: "row" }, recUseBtn, field("入力", recDevSel), field("入力のチャンネル", recModeSel)),
      h("div", { class: "row", style: "margin-top:8px" }, field("録音先", recTargetSel), h("label", { class: "row muted" }, recMonitor, "モニター（アンプを通した音を聞きながら録る）"), field("ずれの補正（ミリ秒）", recLatency)),
      h("div", { class: "row", style: "margin-top:8px" }, recBtn, recStopBtn),
      recInfo,
      audioBox),
    panel("KEY", "MIDIキーボード",
      h("div", { class: "row" }, midiConnectBtn, field("キーボード", midiDevSel), field("入力のしかた", midiModeSel)),
      midiInfo,
      h("div", { class: "muted", style: "margin-top:4px" }, "ステップ入力: 「足す音の長さ」ずつ進みます（ピアノロールをクリックした位置から）。リアルタイム録音: 再生しながら弾くと、「クリックの間隔」にそろえて入ります。録った音は、止めて再生し直すと聞こえます。")),
    panel("GEN", "自動作曲",
      h("div", { class: "row" }, field("曲名", nameIn), field("曲調", styleSel), field("調", tonicSel), field("長調・短調", modeSel)),
      h("div", { class: "row", style: "margin-top:8px" }, field("テンポ", bpmIn), field("乱数の種", h("div", { class: "row" }, seedIn, randomBtn)), field("長さ", secIn), field("拍子", beatsSel), field("疾走感（ボス戦向け）", driveChk)),
      h("div", { class: "row", style: "margin-top:10px" }, composeBtn),
      h("div", { class: "row", style: "margin-top:10px" }, field("特別曲の型", finaleSel), specialBtn, h("label", { class: "row muted" }, useFieldsChk, "上の調・テンポ・種を使う")),
      h("div", { class: "muted", style: "margin-top:6px" }, "同じ設定（乱数の種）からは、いつも同じ曲ができます。気に入らなければ🎲で種を変えてください。特別曲は、型ごとの調・テンポ・種で作ります（「上の調・テンポ・種を使う」で変えられます）。")),
    panel("CHD", "新しい曲（コード進行から）",
      h("div", { class: "row" }, field("コード進行（空白でくぎる）", nsChords), field("テンポ", nsBpm), field("拍子", nsBeats), field("1コードの長さ", nsBars), field("くり返し", nsRepeat), field("伴奏の雰囲気", nsFeel), field("メロディの楽器", nsLead)),
      h("div", { class: "row", style: "margin-top:8px" }, nsBtn),
      h("div", { class: "muted", style: "margin-top:4px" }, "ドラム・ベース・ギター・ピアノ・弦の伴奏を作り、最後に空のメロディのトラックを足します。ピアノロールでメロディを書き込んでください。読めるコード: C・Am・F#m7・Bbmaj7・Csus4・Gdim・Eaug など。")),
    panel("AMP", "音づくり（アンプ）", ampBox),
    panel("OUT", "書き出し",
      h("div", { class: "row" }, field("形式", exportSel), exportBtn, saveBtn, loadBtn, fileIn),
      h("div", { class: "row", style: "margin-top:10px" }, field("ゲーム用の曲ID", gameIdIn), field("使う場面", gameSceneIn), gameBtn),
      h("div", { class: "muted", style: "margin-top:6px" }, "音声とMIDIは、いま選んでいるサウンドの編成で書き出します。MusicXML・CSVは元の音符で書き出します。プロジェクトは、あとで続きから編集できます（このブラウザにも自動保存します）。")),
  ),
  h("footer", { class: "statusbar" }, h("span", { class: "led", "aria-hidden": "true" }), ui.status),
);
ui.rollBox.append(ui.canvas);
restore();
renderAll();

// 再生位置の表示と、ピアノロールの再生位置の線（描き直さず、スクロールだけ追う）
const playhead = h("div", { class: "playhead", style: "display:none" });
ui.rollBox.style.position = "relative";
ui.rollBox.append(playhead);
function tick(): void {
  clipPlayer.tick(state.playing && !state.paused);
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
