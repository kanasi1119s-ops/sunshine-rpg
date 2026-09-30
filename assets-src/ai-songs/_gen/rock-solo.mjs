// ロック「燃え尽きる前に」（約4分・ギターソロ入り）を書き出す。♩156・156小節＝ちょうど4分。Aマイナー（最後のサビだけ長2度上のBマイナー）。
// 作風の参考は「ドラマチックな短調のロック（ピアノ・弦・ギターの重なり、せつないメロディ、ギターソロ）」というジャンルの傾向だけ。特定の曲・作曲家の旋律や進行はなぞっていない（CLAUDE.md 1-1）。
// 奏法の書き方: E5+2:1＝2半音のチョーキング、E5@:0.25＝タッピング（作曲ソフトで対応）。
// 使い方: node assets-src/ai-songs/_gen/rock-solo.mjs → assets-src/ai-songs/rock-solo.json
import fs from "node:fs";
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const NP = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const nm = (m) => NAMES[m % 12] + (Math.floor(m / 12) - 1);
const midiOf = (s) => { const m = /^([A-G])(#|b)?(-?\d)$/.exec(s); return NP[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12 * (Number(m[3]) + 1); };
const RNG = { leadGuitar: [52, 88], distGuitar: [40, 64], crunch: [40, 76], guitar: [40, 76], piano: [21, 108], strings: [36, 96], choir: [48, 84], bass: [28, 55] };
const clamp = (ins, m) => { const [lo, hi] = RNG[ins]; while (m > hi) m -= 12; while (m < lo) m += 12; return m; };
// ---- 構成（16分のステップで数える）
const SEC = [
  ["intro", 8], ["verse", 16], ["pre", 8], ["chorus", 16], ["inter", 8], ["verse2", 16], ["pre", 8], ["chorus", 16], ["bridge", 16], ["solo", 24], ["last", 16], ["outro", 4],
];
const PROG = {
  intro: ["Am", "Fmaj7", "C", "G", "Am", "Fmaj7", "Dm", "E"], verse: ["Am", "F", "G", "C", "Am", "F", "Dm", "E"], pre: ["Dm", "Dm", "E", "E", "F", "G", "E", "E"],
  chorus: ["F", "G", "Em", "Am", "F", "G", "E", "E"], inter: ["Am", "Am", "F", "F", "G", "G", "E", "E"], bridge: ["Fmaj7", "Em7", "Dm7", "Cmaj7", "Fmaj7", "Em7", "Dm", "E"],
  solo: ["Am", "F", "C", "G", "Am", "F", "Dm", "E", "Am", "Am", "F", "F", "G", "G", "E", "E", "F", "G", "Am", "Am", "F", "G", "E", "E"], outro: ["Am", "F", "E", "Am"],
};
PROG.verse2 = PROG.verse; PROG.last = PROG.chorus;
const bars = []; // {sec, i(区間内の小節), chord, shift}
let gb = 0;
for (const [sec, n] of SEC) for (let i = 0; i < n; i++) { const p = PROG[sec]; bars.push({ sec, i, n, chord: p[i % p.length], shift: sec === "last" ? 2 : 0, g: gb++ }); }
const BARS = bars.length, S = BARS * 16;
const chordInfo = (name, shift) => { const m = /^([A-G])(#|b)?(m7|maj7|m|7)?$/.exec(name); const pc = (NP[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + shift + 120) % 12; const minor = m[3] === "m" || m[3] === "m7"; return { pc, minor, name: NAMES[pc] + (minor ? "m" : "") }; };
const rootAt = (pc, oct) => 12 * (oct + 1) + pc;
// ---- ステップ列
const mk = () => Array(S).fill(null);
const L = { kick: mk(), snare: mk(), hihat: mk(), crash: mk(), tom: mk(), bass: mk(), distGuitar: mk(), crunch: mk(), guitar: mk(), piano: mk(), strings: mk(), choir: mk(), lead: mk() };
const put = (part, bar, k, n, len = 1, ins) => { const i = bar * 16 + k; if (i < 0 || i >= S) return; let name = n; if (n !== "x" && ins) name = nm(clamp(ins, typeof n === "number" ? n : midiOf(n))); else if (typeof n === "number") name = nm(n); L[part][i] = { n: name, len }; };
// ---- ドラム
const PAT = {
  verse: { kick: [0, 7, 10], snare: [4, 12], hat: [0, 2, 4, 6, 8, 10, 12, 14] }, pre: { kick: [0, 4, 8, 12], snare: [4, 12], hat: [0, 2, 4, 6, 8, 10, 12, 14] },
  chorus: { kick: [0, 4, 6, 8, 12, 14], snare: [4, 12], hat: [0, 2, 4, 6, 8, 10, 12, 14] }, inter: { kick: [0, 3, 6, 8, 11], snare: [4, 12], hat: [0, 2, 4, 6, 8, 10, 12, 14] },
  bridge: { kick: [0, 10], snare: [8], hat: [0, 4, 8, 12] }, intro: { kick: [], snare: [], hat: [] }, outro: { kick: [0], snare: [], hat: [] },
};
PAT.verse2 = PAT.verse; PAT.last = PAT.chorus; PAT.solo = PAT.chorus;
for (const b of bars) {
  let pat = PAT[b.sec];
  const solo3 = b.sec === "solo" && b.i >= 16, solo2 = b.sec === "solo" && b.i >= 8 && b.i < 16;
  if (b.sec === "intro" && b.i >= 4) pat = { kick: [0], snare: [], hat: [0, 4, 8, 12] };
  if (solo3 || (b.sec === "last")) pat = { ...pat, kick: [0, 2, 4, 6, 8, 10, 12, 14] };
  if (b.sec === "verse" && b.i < 4) pat = { kick: [0, 10], snare: [8], hat: [0, 4, 8, 12] };       // 歌い出しは控えめ
  const lastOf8 = b.i % 8 === 7 && b.sec !== "outro";
  for (const k of pat.kick) put("kick", b.g, k, "x");
  for (const k of pat.snare) put("snare", b.g, k, "x");
  for (const k of pat.hat) put("hihat", b.g, k, "x");
  if (b.i % 8 === 0 && ["chorus", "last", "solo", "inter", "verse2"].includes(b.sec) || (b.sec === "intro" && b.i === 0)) put("crash", b.g, 0, "x");
  if (b.sec === "solo" && b.i === 8) put("crash", b.g, 0, "x");
  if (b.sec === "solo" && b.i === 16) put("crash", b.g, 0, "x");
  if (lastOf8 && b.sec !== "intro") { for (let k = 8; k < 16; k++) { L.snare[b.g * 16 + k] = null; put(k >= 12 ? "tom" : "snare", b.g, k, "x"); } if (b.i === 7) L.kick[b.g * 16 + 8] = null; }
  if (b.sec === "bridge" && b.i === 15) for (let k = 0; k < 16; k += 1) { put("snare", b.g, k, "x"); }
  if (b.sec === "outro" && b.i === 0) put("crash", b.g, 0, "x");
}
// ---- 伴奏
const CH_TONES = (c) => [0, c.minor ? 3 : 4, 7, 12];
for (const b of bars) {
  const c = chordInfo(b.chord, b.shift), sec = b.sec, g = b.g;
  const root = (o) => rootAt(c.pc, o);
  const rockish = ["chorus", "last", "solo", "inter"].includes(sec);
  // ベース
  if (sec !== "intro" && sec !== "bridge") { const step = rockish ? [0, 2, 4, 6, 8, 10, 12, 14] : [0, 2, 4, 6, 8, 10, 12, 14]; step.forEach((k, idx) => put("bass", g, k, rootAt(c.pc, 1) + (rockish && (idx === 3 || idx === 7) ? 12 : 0) + (rockish ? 0 : 0), 2, "bass")); }
  if (sec === "bridge") { put("bass", g, 0, rootAt(c.pc, 1), 8, "bass"); put("bass", g, 8, rootAt(c.pc, 1) + 7, 8, "bass"); }
  if (sec === "intro" && b.i >= 4) put("bass", g, 0, rootAt(c.pc, 1), 16, "bass");
  // ギター（歪み）: 8分のチャグ。プリはミュート風に短く、サビ以降はパワーコード
  if (["pre", "chorus", "last", "solo", "inter"].includes(sec) || (sec === "verse2" && b.i >= 8)) for (let k = 0; k < 16; k += 2) put("distGuitar", g, k, rootAt(c.pc, 2), sec === "pre" ? 1 : 2, "distGuitar");
  if (["chorus", "last", "inter"].includes(sec)) { put("crunch", g, 0, rootAt(c.pc, 3), 8, "crunch"); put("crunch", g, 8, rootAt(c.pc, 3) + (c.minor ? 3 : 4) + 4, 8, "crunch"); }
  if (sec === "solo") { put("crunch", g, 0, rootAt(c.pc, 3), 16, "crunch"); }
  // クリーンギターの分散和音
  if (["intro", "verse", "bridge", "outro"].includes(sec) || (sec === "verse2" && b.i < 8)) { const t = CH_TONES(c); const pat = [0, 2, 3, 2, 1, 2, 3, 2]; pat.forEach((ti, idx) => put("guitar", g, idx * 2, rootAt(c.pc, 3) + (ti === 3 ? 12 : t[ti]), 2, "guitar")); }
  // ピアノ
  if (["intro", "verse", "verse2", "bridge", "outro"].includes(sec)) { const t = CH_TONES(c); const pat = sec === "bridge" ? [0, 2, 1, 2, 3, 2, 1, 2] : [0, 1, 2, 1, 3, 1, 2, 1]; pat.forEach((ti, idx) => put("piano", g, idx * 2, rootAt(c.pc, 3) + t[ti], 2, "piano")); put("piano", g, 0, rootAt(c.pc, 2), 16 > 8 ? 2 : 2, "piano"); }
  if (["chorus", "last", "pre", "inter"].includes(sec)) { for (let k = 0; k < 16; k += 4) put("piano", g, k, rootAt(c.pc, 4) + (c.minor ? 3 : 4), 4, "piano"); }
  // 弦
  if (["pre", "chorus", "last", "bridge", "inter", "outro", "solo"].includes(sec) || (sec === "verse2" && b.i >= 8) || (sec === "intro" && b.i >= 4)) put("strings", g, 0, rootAt(c.pc, 4) + (sec === "bridge" ? 7 : (c.minor ? 3 : 4)), 16, "strings");
  if (sec === "last") put("choir", g, 0, rootAt(c.pc, 4) + 7, 16, "choir");
}
// ---- 旋律（ノート名。2小節ずつ）
const T = (phrases) => phrases;
const TOK = (s, shift = 0) => s.trim().split(/\\s+/);
function lay(part, ins, startBar, phrases, shift = 0) {
  let cur = startBar * 16;
  for (const ph of phrases) for (const t of ph.trim().split(/\s+/)) {
    const [nn, d] = t.split(":"); const len = Math.round(Number(d) * 4);
    if (nn !== "R") { const m = /^([A-G][#b]?-?\d)(?:\+(\d+(?:\.\d+)?))?(@)?$/.exec(nn); const base = clamp(ins, midiOf(m[1]) + shift); L[part][cur] = { n: nm(base) + (m[2] ? "+" + m[2] : "") + (m[3] ? "@" : ""), len, raw: true }; }
    cur += len;
  }
  return cur / 16;
}
const secStart = (name, occ = 0) => { let g = 0, o = 0; for (const [s, n] of SEC) { if (s === name) { if (o === occ) return g; o++; } g += n; } throw new Error(name); };
const VERSE = ["E5:1 E5:0.5 D5:0.5 C5:1 D5:0.5 E5:0.5 F5:1.5 E5:0.5 C5:2", "D5:1 D5:0.5 E5:0.5 G5:1.5 E5:0.5 E5:2 D5:1 C5:1", "A4:1 C5:0.5 E5:0.5 A5:1.5 G5:0.5 F5:1 A5:1 G5:1 F5:1", "D5:1 F5:0.5 A5:0.5 G5:1 F5:1 E5:2 G#5:1 B5:1"];
const VERSE2 = ["E5:1 E5:0.5 D5:0.5 C5:1 D5:0.5 E5:0.5 F5:1.5 E5:0.5 C5:2", "D5:1 D5:0.5 E5:0.5 G5:1.5 E5:0.5 E5:2 D5:1 C5:1", "A5:1 C6:0.5 E6:0.5 A5:1.5 G5:0.5 F5:1 A5:1 G5:1 F5:1", "D5:1 F5:0.5 A5:0.5 G5:1 F5:1 E5+2:2 G#5:1 B5:1"];
const PRE = ["A5:2 G5:1 F5:1 A5:2 D6:2", "B5:2 G#5:1 B5:1 E6:4", "C6:2 A5:1 C6:1 D6:2 B5:2", "G#5:1 B5:1 E6:2 E6:1 R:3"];
const CHO = ["A5:1.5 C6:0.5 C6:1 A5:1 B5:1.5 D6:0.5 D6:2", "B5:1 B5:0.5 A5:0.5 G5:1 E5:1 A5:2 C6:1 E6:1", "A5:1.5 C6:0.5 C6:1 A5:1 B5:1.5 D6:0.5 D6:1 B5:1", "G#5:1 B5:1 D6+2:2 E6:3 R:1"];
const INTER = ["A4:0.5 A4:0.25 C5:0.25 A4:0.5 E5:0.5 A4:0.5 A4:0.25 C5:0.25 A4:0.5 G4:0.5 A4:0.5 A4:0.25 C5:0.25 A4:0.5 E5:0.5 A4:0.5 C5:0.25 D5:0.25 E5:0.5 G5:0.5", "G4:0.5 G4:0.25 B4:0.25 G4:0.5 D5:0.5 G4:0.5 G4:0.25 B4:0.25 G4:0.5 F#4:0.5 E4:0.5 E4:0.25 G#4:0.25 E4:0.5 B4:0.5 E4:0.5 G#4:0.25 B4:0.25 E5:0.5 B5:0.5"];
const BRIDGE = ["C5:2 A4:2 B4:2 G4:2", "A4:2 C5:2 B4:1 A4:1 G#4:2", "C5:2 E5:2 D5:2 B4:2", "A4:2 C5:1 D5:1 E5:4"];
const SOLO1 = ["R:0.5 E5:0.5 A5+1:1 A5:0.5 G5:0.5 E5:1 F5+2:1.5 F5:0.5 E5:0.5 C5:0.5 A4:1", "C5:0.5 E5:0.5 G5:1 G5+2:1.5 R:0.5 B5:1 D6:0.5 B5:0.5 G5:1 D5+2:1", "A5+2:2 G5:0.5 E5:0.5 D5:0.5 E5:0.5 C6:1 A5:0.5 C6:0.5 C6+2:1.5 R:0.5", "D6:0.5 C6:0.5 A5:0.5 F5:0.5 D5:1 F5+2:1 G#5:0.5 B5:0.5 E6:1 D6+2:2"];
const tapBar = (a, b, c, d) => [a, b, c, d, c, b, a, b].map((x) => x + "@:0.25").join(" ");
const tp = (r) => [r[0], r[1], r[2], r[3]];
const SOLO2 = [
  tapBar("E5", "A5", "C6", "E6") + " " + tapBar("E5", "A5", "C6", "E6"), tapBar("E5", "A5", "C6", "E6") + " " + tapBar("A5", "C6", "E6", "C6"),
  tapBar("C5", "F5", "A5", "C6") + " " + tapBar("C5", "F5", "A5", "C6"), tapBar("F5", "A5", "C6", "A5") + " " + tapBar("C5", "F5", "A5", "C6"),
  tapBar("D5", "G5", "B5", "D6") + " " + tapBar("D5", "G5", "B5", "D6"), tapBar("G5", "B5", "D6", "B5") + " " + tapBar("D5", "G5", "B5", "D6"),
  tapBar("E5", "G#5", "B5", "E6") + " " + tapBar("E5", "G#5", "B5", "E6"),
  ["E6", "D6", "C6", "B5", "A5", "G#5", "F5", "E5", "D5", "C5", "B4", "A4", "G#4", "F4", "E4", "E4"].map((x) => x + "@:0.25").join(" "),
];
const SOLO3 = ["A5+2:1 C6:0.5 A5:0.5 F5:0.5 A5:0.5 C6:1 B5+2:1.5 D6:0.5 B5:0.5 G5:0.5 D6:1", "E6+0.5:1 D6:0.5 C6:0.5 A5:1 C6:0.5 E6:0.5 C6+2:2 D6:1 E6:1", "C6:0.25 A5:0.25 F5:0.25 A5:0.25 C6:0.25 A5:0.25 F5:0.25 A5:0.25 C6:0.25 A5:0.25 F5:0.25 A5:0.25 C6:0.25 A5:0.25 F5:0.25 A5:0.25 D6:0.25 B5:0.25 G5:0.25 B5:0.25 D6:0.25 B5:0.25 G5:0.25 B5:0.25 D6:0.25 B5:0.25 G5:0.25 B5:0.25 D6:0.25 B5:0.25 G5:0.25 B5:0.25", "G#5:0.25 B5:0.25 E6:0.25 B5:0.25 G#5:0.25 B5:0.25 E6:0.25 B5:0.25 D6+2:2 E6:4"];
lay("lead", "leadGuitar", secStart("intro") + 4, ["E5:2 D5:1 C5:1 E5:2 G5:2", "A5:3 G5:1 F5:2 E5:2"], 0);       // イントロの後半にだけ、ちいさな歌い出しの動機
lay("lead", "leadGuitar", secStart("verse"), VERSE);
lay("lead", "leadGuitar", secStart("verse") + 8, VERSE2);
lay("lead", "leadGuitar", secStart("pre"), PRE);
lay("lead", "leadGuitar", secStart("chorus"), CHO); lay("lead", "leadGuitar", secStart("chorus") + 8, CHO.slice(0, 3).concat(["G#5:1 B5:1 D6+2:2 E6+0.5:3 R:1"]));
lay("lead", "leadGuitar", secStart("inter"), INTER);
lay("lead", "leadGuitar", secStart("verse2"), VERSE2); lay("lead", "leadGuitar", secStart("verse2") + 8, VERSE2);
lay("lead", "leadGuitar", secStart("pre", 1), PRE);
lay("lead", "leadGuitar", secStart("chorus", 1), CHO); lay("lead", "leadGuitar", secStart("chorus", 1) + 8, CHO);
lay("lead", "leadGuitar", secStart("bridge"), BRIDGE); lay("lead", "leadGuitar", secStart("bridge") + 8, BRIDGE.slice(0, 3).concat(["A4:2 C5:1 D5:1 G#4:4"]));
lay("lead", "leadGuitar", secStart("solo"), SOLO1); lay("lead", "leadGuitar", secStart("solo") + 8, SOLO2); lay("lead", "leadGuitar", secStart("solo") + 16, SOLO3);
lay("lead", "leadGuitar", secStart("last"), CHO, 2); lay("lead", "leadGuitar", secStart("last") + 8, CHO.slice(0, 3).concat(["G#5:1 B5:1 D6+2:2 E6+0.5:3 R:1"]), 2);
lay("lead", "leadGuitar", secStart("outro"), ["E5:2 D5:1 C5:1 E5:2 G5:2", "A5:8"]);
// 最終小節はAの長い和音で締める
const lastBar = BARS - 1;
for (let k = 0; k < 16; k++) for (const p of ["kick", "snare", "hihat", "tom", "bass", "distGuitar", "crunch"]) L[p][lastBar * 16 + k] = null;
L.crash[lastBar * 16] = { n: "x", len: 1 }; L.kick[lastBar * 16] = { n: "x", len: 1 };
L.bass[lastBar * 16] = { n: "A1", len: 16 }; L.piano[lastBar * 16] = { n: "A3", len: 16 }; L.strings[lastBar * 16] = { n: "E5", len: 16 };
// ---- 出力
const rest = (out, beats) => { while (beats > 16) { out.push("R:16"); beats -= 16; } if (beats > 0) out.push(`R:${beats}`); };
const toNotes = (arr) => { const out = []; let i = 0; while (i < S) { const e = arr[i]; if (!e) { let j = i; while (j < S && !arr[j]) j++; rest(out, (j - i) * 0.25); i = j; continue; } let nx = i + 1; while (nx < S && !arr[nx]) nx++; const gap = nx - i, len = Math.min(e.len, gap); out.push(`${e.n}:${len * 0.25}`); if (gap > len) rest(out, (gap - len) * 0.25); i = nx; } return out.join(" "); };
const chords = bars.map((b) => chordInfo(b.chord, b.shift).name).join(" ");
const parts = [
  ["kick", "キック", "kick", 0.3, 0], ["snare", "スネア", "snare", 0.26, 0.05], ["hihat", "ハイハット", "hihat", 0.12, 0.25], ["crash", "クラッシュ", "crash", 0.18, -0.2], ["tom", "タム（フィル）", "tom", 0.22, -0.15],
  ["bass", "ベース（8分の根音）", "bass", 0.26, 0, "overdrive"], ["distGuitar", "リズムギター（8分のチャグ）", "distGuitar", 0.17, -0.5, "auto"], ["crunch", "サイドギター（サビのパワーコード）", "crunch", 0.13, 0.5, "auto"],
  ["guitar", "クリーンギター（分散和音）", "guitar", 0.15, -0.3, "clean"], ["piano", "ピアノ", "piano", 0.2, 0.25], ["strings", "ストリングス", "strings", 0.12, 0.3], ["choir", "合唱（最後のサビ）", "choir", 0.14, -0.2],
  ["leadGuitar", "リードギター（旋律・ソロ：チョーキングとタッピング）", "lead", 0.27, 0.05, "prs"],
];
const song = {
  title: "燃え尽きる前に", description: "【仮】ドラマチックな短調のロック（約4分）。ギターソロにチョーキングとタッピングを入れた。ピアノと歌うようなリードで始まり、プレコーラス→サビ、間奏のユニゾンリフ、2番、ピアノの橋（ブリッジ）を経て、ソロ（歌うチョーキング→タッピングの分散和音とプリングオフの下降→速い刻みと長いチョーキング）、長2度上げた最後のサビと合唱で盛り上がる。♩156・156小節。Aマイナー→Bマイナー。",
  bpm: 156, beats: 4, chords, barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "rock", tone: "rock",
  parts: parts.map(([instrument, role, key, volume, pan, amp]) => ({ instrument, role, volume, pan, amp: amp ?? "auto", notes: toNotes(L[key]) })),
};
fs.writeFileSync(new URL("../rock-solo.json", import.meta.url), JSON.stringify(song, null, 2) + "\n", "utf8");
console.log("小節", BARS, "秒", (BARS * 4 / 156 * 60).toFixed(1));
