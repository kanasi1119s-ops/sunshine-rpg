// ハイブリッド・ロック「灯を撃て」（約3分40秒）— 「ドラマチックな短調のロック」というジャンルの傾向だけを参考にした完全オリジナル。特定の曲・作曲家の旋律や進行はなぞっていない（CLAUDE.md 1-1）。
// 2026年ふうの作り: ロックのバンド（歪んだギター2本・ベース）に、電子のキック・クラップ・サブベース・シンセの分厚いコード・ライザー・ボーカルチョップ・サイドチェーンを重ねる。
// 従来の「1コード1小節の型」に縛られず、ドロップ（電子）とバンドを行き来し、テンポ感の切り替え・ディレイ・テープの飽和・コーラスも使う。
// ♩168・152小節＝3分37秒。Eマイナー（最後のサビだけ嬰ヘ短調）。
// 使い方: node assets-src/ai-songs/_gen/modern-rock.mjs → assets-src/ai-songs/modern-rock.json
import fs from "node:fs";
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const NP = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const nm = (m) => NAMES[m % 12] + (Math.floor(m / 12) - 1);
const midiOf = (s) => { const m = /^([A-G])(#|b)?(-?\d)$/.exec(s); return NP[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12 * (Number(m[3]) + 1); };
const RNG = { leadGuitar: [52, 88], distGuitar: [40, 64], guitar: [40, 76], piano: [21, 108], strings: [36, 96], choir: [48, 84], bass: [28, 55], sub808: [24, 48], lead: [48, 96], bell: [60, 96], riser: [48, 96] };
const clamp = (ins, m) => { const [lo, hi] = RNG[ins]; while (m > hi) m -= 12; while (m < lo) m += 12; return m; };
const SEC = [["intro", 8], ["verse", 16], ["pre", 8], ["chorus", 16], ["drop", 8], ["verse2", 16], ["pre", 8], ["chorus", 16], ["bridge", 16], ["solo", 16], ["last", 16], ["outro", 8]];
const PROG = {
  intro: ["Em", "C", "G", "D", "Em", "C", "Am", "B"], verse: ["Em", "C", "G", "D", "Em", "C", "Am", "B"], pre: ["Am", "Am", "B", "B", "C", "D", "B", "B"],
  chorus: ["C", "D", "Em", "Bm", "C", "D", "B", "B"], drop: ["Em", "Em", "C", "C", "D", "D", "B", "B"], bridge: ["Am", "G", "C", "B", "Am", "G", "B", "B"],
  solo: ["Em", "C", "G", "D", "Am", "B", "Em", "Em", "C", "D", "Em", "Bm", "C", "D", "B", "B"], outro: ["Em", "C", "Am", "B", "Em", "C", "Am", "Em"],
};
PROG.verse2 = PROG.verse; PROG.last = PROG.chorus;
const bars = []; let gb = 0;
for (const [sec, n] of SEC) for (let i = 0; i < n; i++) { const p = PROG[sec]; bars.push({ sec, i, n, chord: p[i % p.length], shift: sec === "last" ? 2 : 0, g: gb++ }); }
const BARS = bars.length, S = BARS * 16;
const chordInfo = (name, shift) => { const m = /^([A-G])(#|b)?(m)?(7)?$/.exec(name); const pc = (NP[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + shift + 120) % 12; return { pc, minor: m[3] === "m", name: NAMES[pc] + (m[3] ?? "") + (m[4] ?? "") }; };
const at = (pc, oct) => 12 * (oct + 1) + pc;
const mk = () => Array(S).fill(null);
const L = Object.fromEntries(["kick", "snare", "clap", "hihat", "openhat", "crash", "tom", "riser", "bass", "sub", "gL", "gR", "lead", "stab", "arp", "piano", "strings", "choir", "chop", "bell", "melody"].map((k) => [k, mk()]));
const put = (part, bar, k, n, len = 1, ins) => { const i = bar * 16 + k; if (i < 0 || i >= S) return; L[part][i] = { n: n === "x" ? "x" : nm(ins ? clamp(ins, typeof n === "number" ? n : midiOf(n)) : n), len }; };
const has = (b, ...s) => s.includes(b.sec);
for (const b of bars) {
  const c = chordInfo(b.chord, b.shift), g = b.g, sec = b.sec;
  const big = has(b, "chorus", "last", "solo"), half = has(b, "verse", "verse2"), drop = has(b, "drop");
  const root = (o) => at(c.pc, o), third = c.minor ? 3 : 4;
  // ---- ドラム（バンドの太鼓に、電子のクラップ・キックを重ねる）
  if (has(b, "intro") && b.i >= 4) { for (const k of [0, 8]) put("kick", g, k, "x"); for (let k = 0; k < 16; k += 4) put("hihat", g, k, "x"); }
  if (half) { for (const k of b.i < 4 && sec === "verse" ? [0, 10] : [0, 6, 8, 11]) put("kick", g, k, "x"); for (const k of [4, 12]) put("snare", g, k, "x"); for (let k = 0; k < 16; k += 2) put("hihat", g, k, "x"); }
  if (has(b, "pre")) { for (let k = 0; k < 16; k += 4) put("kick", g, k, "x"); for (const k of [4, 12]) put("snare", g, k, "x"); for (let k = 0; k < 16; k += 2) put("hihat", g, k, "x"); if (b.i >= 4) for (let k = 0; k < 16; k += b.i >= 6 ? 1 : 2) put("snare", g, k, "x"); }
  if (big) { for (let k = 0; k < 16; k += 4) put("kick", g, k, "x"); if (sec !== "solo" || b.i < 8) for (const k of [6, 14]) put("kick", g, k, "x"); for (const k of [4, 12]) { put("snare", g, k, "x"); put("clap", g, k, "x"); } for (let k = 0; k < 16; k += 2) put("hihat", g, k, "x"); for (const k of [2, 6, 10, 14]) put("openhat", g, k, "x"); }
  if (drop) { for (let k = 0; k < 16; k += 4) put("kick", g, k, "x"); for (const k of [4, 12]) put("clap", g, k, "x"); for (const k of [2, 6, 10, 14]) put("openhat", g, k, "x"); for (let k = 1; k < 16; k += 2) put("hihat", g, k, "x"); }
  if (has(b, "bridge")) { if (b.i >= 8) for (const k of [0, 10]) put("kick", g, k, "x"); if (b.i >= 12) for (const k of [8]) put("snare", g, k, "x"); }
  if (has(b, "outro")) { if (b.i < 4) { for (const k of [0, 8]) put("kick", g, k, "x"); for (const k of [4, 12]) put("snare", g, k, "x"); } }
  if (b.i % 8 === 0 && has(b, "chorus", "last", "drop", "verse2") || (sec === "solo" && b.i % 8 === 0)) put("crash", g, 0, "x");
  const lastOf8 = b.i % 8 === 7 && !has(b, "intro", "outro");
  if (lastOf8) { for (let k = 8; k < 16; k++) { L.snare[g * 16 + k] = null; put(k >= 12 ? "tom" : "snare", g, k, "x"); } }
  if (has(b, "pre") && b.i === 0) L.riser[g * 16] = { n: nm(at(4, 5)), len: 8 * 16 };            // ライザー（プレの全長）
  if (has(b, "bridge") && b.i === 8) L.riser[g * 16] = { n: nm(at(4, 5)), len: 8 * 16 };
  // ---- ベース: バンドのベースが8分、ドロップと4つ打ちの区間はサブベースがオフビート
  if (!has(b, "intro", "bridge", "outro") && !drop) for (let k = 0; k < 16; k += 2) put("bass", g, k, at(c.pc, 1) + (big && k % 8 === 6 ? 12 : 0), 2, "bass");
  if (big || drop) for (const k of [2, 3, 6, 7, 10, 11, 14, 15]) put("sub", g, k, at(c.pc, 1), 1, "sub808");
  if (has(b, "pre")) for (let k = 0; k < 16; k += 4) put("sub", g, k, at(c.pc, 1), 3, "sub808");
  // ---- リズムギター2本（左: 8分のチャグ、右: 16分のミュート。サビは開放のパワーコード）
  if (half && b.i >= (sec === "verse" ? 4 : 0) || has(b, "pre")) { for (let k = 0; k < 16; k += 2) put("gL", g, k, at(c.pc, 2), 2, "distGuitar"); }
  if (big) { put("gL", g, 0, at(c.pc, 2), 8, "distGuitar"); put("gL", g, 8, at(c.pc, 2), 8, "distGuitar"); for (let k = 0; k < 16; k++) if (k % 4 !== 0 && !(sec === "solo" && b.i >= 8 && false)) put("gR", g, k, at(c.pc, 3), 1, "distGuitar"); }
  if (drop) { const t = third; const riff = [[12, 2], [12, 1], [12 + t, 1], [12, 2], [19, 2], [12, 2], [10, 2], [12, 2], [12 + t, 2]]; let k = 0; for (const [iv, len] of riff) { put("gL", g, k, at(c.pc, 2) + iv - 12, len, "distGuitar"); put("stab", g, k, at(c.pc, 3) + iv, len, "lead"); k += len; } }
  // ---- シンセのコード（電子の厚み）: サビとドロップは16分の刻み、ブリッジは白玉
  if (big || drop) { const t = [0, third, 7]; for (const k of [0, 3, 6, 10, 12]) put("stab", g, k, at(c.pc, 4) + t[(k / 3 | 0) % 3], 2, "lead"); }
  if (has(b, "pre", "bridge", "intro", "outro")) put("strings", g, 0, at(c.pc, 4) + (has(b, "bridge") ? 7 : third), 16, "strings");
  if (big) put("strings", g, 0, at(c.pc, 4) + 7, 16, "strings");
  // ---- アルペジオ（16分。イントロ・サビ・ドロップ）
  if (has(b, "intro", "chorus", "last", "drop") || (sec === "verse2" && b.i >= 8)) { const t = [0, third, 7, 12, 7, third]; for (let k = 0; k < 16; k++) put("arp", g, k, at(c.pc, 5) + t[k % 6], 1, "lead"); }
  // ---- ボーカルチョップ風の合唱・鐘
  if ((big || drop) && b.i % 2 === 1) for (const k of [3, 6, 11]) put("chop", g, k, at(c.pc, 4) + 7, 2, "choir");
  if (has(b, "bridge")) { put("choir", g, 0, at(c.pc, 4) + third, 16, "choir"); }
  if (has(b, "last")) put("choir", g, 0, at(c.pc, 4) + 7, 16, "choir");
  if (has(b, "bridge", "outro", "intro")) { const t = [0, 7, 12, third + 12, 12, 7]; for (let k = 0; k < 16; k += 2) put("piano", g, k, at(c.pc, 3) + t[(k / 2) % 6], 2, "piano"); }
  if (has(b, "bridge") && b.i >= 8) for (const k of [0, 8]) put("bell", g, k, at(c.pc, 6) + (k ? 7 : 0), 8, "bell");
}
// ---- 旋律
function lay(part, ins, start, phrases, shift = 0) {
  let cur = start * 16;
  for (const ph of phrases) for (const t of ph.trim().split(/\s+/)) {
    const [nn, d] = t.split(":"); const len = Math.round(Number(d) * 4);
    if (nn !== "R") { const m = /^([A-G][#b]?-?\d)(?:\+(\d+(?:\.\d+)?))?(@)?$/.exec(nn); if (!m) throw new Error(t); L[part][cur] = { n: nm(clamp(ins, midiOf(m[1]) + shift)) + (m[2] ? "+" + m[2] : "") + (m[3] ? "@" : ""), len }; }
    cur += len;
  }
}
const start = (name, occ = 0) => { let g = 0, o = 0; for (const [s, n] of SEC) { if (s === name) { if (o === occ) return g; o++; } g += n; } throw new Error(name); };
const VERSE = ["B4:0.5 E5:0.5 G5:1 F#5:0.5 E5:0.5 B4:1 C5:0.5 E5:0.5 G5:1.5 E5:0.5 D5:1", "D5:0.5 G5:0.5 B5:1 A5:0.5 G5:0.5 D5:1 D5:0.5 F#5:0.5 A5:1.5 F#5:0.5 D5:1", "B4:0.5 E5:0.5 G5:1 B5:0.5 A5:0.5 G5:1 C6:1 B5:0.5 G5:0.5 E5:2", "A4:0.5 C5:0.5 E5:1 A5:1.5 G5:0.5 F#5:1 B5:1 D#6:2"];
const VERSE2 = [VERSE[0], VERSE[1], "B4:0.5 E5:0.5 G5:1 B5:0.5 A5:0.5 G5:1 C6:1 B5:0.5 G5:0.5 E6+2:2", VERSE[3]];
const PRE = ["E5:1 A5:1 C6:2 B5:1 A5:1 E5:2", "F#5:1 B5:1 D#6:2 D#6:1 B5:1 F#5:2", "G5:1 C6:1 E6:2 F#5:1 A5:1 D6:2", "D#6:2 B5:1 F#5:1 B5:3 R:1"];
const CHO = ["E5:1 G5:0.5 E5:0.5 C6:2 A5:1 F#5:0.5 A5:0.5 D6:2", "B5:1 G5:0.5 E5:0.5 G5:1.5 B5:0.5 D6:1 B5:0.5 F#5:0.5 D6:2", "E6:1 D6:0.5 C6:0.5 G5:2 A5:1 D6:1 A5:2", "D#6:1 F#5:1 B5:2 D#6+1:3 R:1"];
const DROPMEL = [];
const BRIDGE = ["A4:2 C5:2 B4:2 D5:2", "C5:2 E5:2 D#5:2 F#5:2", "A4:2 C5:2 B4:2 D5:2", "C5:2 E5:2 D#5:1 F#5:1 B5+2:2"];
const SOLO1 = ["R:0.5 B4:0.5 E5+2:1 E5:0.5 D5:0.5 B4:1 C5:0.5 E5:0.5 G5:1 G5+2:1.5 R:0.5 B5:1 D6:0.5 B5:0.5 G5:1 D5+2:1 A5+2:2 F#5:0.5 A5:0.5 D6:1"];
const tap = (a) => a.map((x) => x + "@:0.25").join(" ");
const SOLO2 = [tap(["E5", "A5", "C6", "E6", "C6", "A5", "E5", "A5", "E5", "A5", "C6", "E6", "C6", "A5", "E5", "A5"]), tap(["B4", "D#5", "F#5", "B5", "F#5", "D#5", "B4", "D#5", "F#5", "B5", "D#6", "B5", "F#5", "B5", "D#6", "B5"]), tap(["E5", "G5", "B5", "E6", "B5", "G5", "E5", "G5", "E5", "G5", "B5", "E6", "B5", "G5", "E5", "G5"]), tap(["E6", "D6", "C6", "B5", "A5", "G5", "F#5", "E5", "D5", "C5", "B4", "A4", "G4", "F#4", "E4", "E4"])];
const SOLO3 = ["E6+0.5:1 D6:0.5 C6:0.5 G5:1 E5:0.5 G5:0.5 A5+2:1 D6:0.5 A5:0.5 F#5:0.5 A5:0.5 D6:1 B5+2:2 G5:0.5 B5:0.5 E6:1 D6:0.5 B5:0.5 F#5:0.5 B5:0.5 D6+2:2", "C6:0.25 G5:0.25 E5:0.25 G5:0.25 C6:0.25 G5:0.25 E5:0.25 G5:0.25 C6:0.25 G5:0.25 E5:0.25 G5:0.25 C6:0.25 G5:0.25 E5:0.25 G5:0.25 D6:0.25 A5:0.25 F#5:0.25 A5:0.25 D6:0.25 A5:0.25 F#5:0.25 A5:0.25 D6:0.25 A5:0.25 F#5:0.25 A5:0.25 D6:0.25 A5:0.25 F#5:0.25 A5:0.25 D#6:0.25 B5:0.25 F#5:0.25 B5:0.25 D#6:0.25 B5:0.25 F#5:0.25 B5:0.25 D#6+1:2 D#6:2 F#5:1 B5:1"];
lay("melody", "leadGuitar", start("verse"), VERSE); lay("melody", "leadGuitar", start("verse") + 8, VERSE);
lay("melody", "leadGuitar", start("pre"), PRE); lay("melody", "leadGuitar", start("chorus"), CHO); lay("melody", "leadGuitar", start("chorus") + 8, CHO);
lay("melody", "leadGuitar", start("verse2"), VERSE2); lay("melody", "leadGuitar", start("verse2") + 8, VERSE2);
lay("melody", "leadGuitar", start("pre", 1), PRE); lay("melody", "leadGuitar", start("chorus", 1), CHO); lay("melody", "leadGuitar", start("chorus", 1) + 8, CHO);
lay("melody", "leadGuitar", start("bridge"), BRIDGE); lay("melody", "leadGuitar", start("bridge") + 8, BRIDGE);
lay("melody", "leadGuitar", start("solo"), SOLO1); lay("melody", "leadGuitar", start("solo") + 4, SOLO2); lay("melody", "leadGuitar", start("solo") + 8, [SOLO3[0]]); lay("melody", "leadGuitar", start("solo") + 12, [SOLO3[1]]);
lay("melody", "leadGuitar", start("last"), CHO, 2); lay("melody", "leadGuitar", start("last") + 8, CHO, 2);
lay("melody", "leadGuitar", start("outro"), ["E5:2 D5:1 C5:1 E5:2 G5:2 A5:2 G5:2 E5:4"]);
// イントロのアルペジオの上に、ギターのハーモニクス風の高い音
lay("bell", "bell", start("intro") + 4, ["E6:4 B5:4 E6:4 G6:4"]);
// 最終小節
const lastBar = BARS - 1;
for (let k = 0; k < 16; k++) for (const p of ["kick", "snare", "clap", "hihat", "openhat", "tom", "bass", "sub", "gL", "gR", "arp", "stab", "chop", "melody"]) L[p][lastBar * 16 + k] = null;
L.crash[lastBar * 16] = { n: "x", len: 1 }; L.kick[lastBar * 16] = { n: "x", len: 1 }; L.bass[lastBar * 16] = { n: "E1", len: 16 }; L.piano[lastBar * 16] = { n: "E3", len: 16 }; L.strings[lastBar * 16] = { n: "B4", len: 16 };
// ---- 出力
const rest = (out, beats) => { while (beats > 16) { out.push("R:16"); beats -= 16; } if (beats > 0) out.push(`R:${beats}`); };
const toNotes = (arr) => { const out = []; let i = 0; while (i < S) { const e = arr[i]; if (!e) { let j = i; while (j < S && !arr[j]) j++; rest(out, (j - i) * 0.25); i = j; continue; } let nx = i + 1; while (nx < S && !arr[nx]) nx++; const gap = nx - i, len = Math.min(e.len, gap); out.push(`${e.n}:${len * 0.25}`); if (gap > len) rest(out, (gap - len) * 0.25); i = nx; } return out.join(" "); };
const chords = bars.map((b) => chordInfo(b.chord, b.shift).name).join(" ");
const parts = [
  ["kick", "キック（バンド＋電子）", "kick", 0.32, 0], ["snare", "スネア", "snare", 0.25, 0.05], ["clap", "クラップ（サビ・ドロップで重ねる）", "clap", 0.2, 0.1], ["hihat", "ハイハット", "hihat", 0.11, 0.25], ["openhat", "オープンハット", "openhat", 0.13, -0.25],
  ["crash", "クラッシュ", "crash", 0.18, -0.2], ["tom", "タム（フィル）", "tom", 0.22, -0.15], ["riser", "ライザー（プレ・ブリッジ）", "riser", 0.2, 0],
  ["bass", "ベース（8分）", "bass", 0.24, 0, "overdrive"], ["sub808", "サブベース（オフビート）", "sub", 0.3, 0],
  ["distGuitar", "リズムギター左", "gL", 0.16, -0.55, "auto"], ["distGuitar", "リズムギター右（16分・開放）", "gR", 0.12, 0.55, "auto"],
  ["lead", "シンセのコード刻み", "stab", 0.15, 0.2], ["lead", "シンセのアルペジオ", "arp", 0.1, -0.3], ["strings", "ストリングス", "strings", 0.12, 0.3], ["choir", "合唱", "choir", 0.13, -0.2], ["choir", "ボーカルチョップ風", "chop", 0.14, 0.35],
  ["piano", "ピアノ", "piano", 0.18, 0.25], ["bell", "きらめき", "bell", 0.12, 0.4], ["leadGuitar", "リードギター（旋律・ソロ）", "melody", 0.27, 0.05, "prs"],
];
const song = {
  title: "灯を撃て", description: "【仮】2026年ふうのハイブリッド・ロック（約3分40秒・♩168）。バンド（歪んだギター2本・ベース・生ドラム）に、電子のキック・クラップ・サブベース・シンセの刻み・ライザー・ボーカルチョップ・サイドチェーンを重ねる。ピアノとアルペジオのイントロ→ヴァース→ライザーのプレ→サビ→電子のドロップ（ギターとシンセのユニゾンリフ）→2番→サビ→ピアノと合唱のブリッジ→ギターソロ（チョーキング・タッピング）→嬰ヘ短調へ上げた最後のサビ→アウトロ。ディレイ・テープの飽和・コーラスを曲全体にかけている。",
  bpm: 168, beats: 4, chords, barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "rock", tone: "rock", pump: "all", synth: true, drumKit: 16,
  fx: { tape: 0.25, chorus: 0.15, delay: { beats: 0.75, feedback: 0.3, mix: 0.16 } },
  parts: parts.map(([instrument, role, key, volume, pan, amp]) => ({ instrument, role, volume, pan, amp: amp ?? "auto", notes: toNotes(L[key]) })),
};
fs.writeFileSync(new URL("../modern-rock.json", import.meta.url), JSON.stringify(song, null, 2) + "\n", "utf8");
console.log("小節", BARS, "秒", (BARS * 4 / 168 * 60).toFixed(1));
