// エレクトリック・ポリリズム「歯車は光る」（約4分）を書き出す。♩128・4拍子・128小節＝ちょうど4分。
// 考え方: 16分音符の「ステップ」の上に、周期の違うパターン（3・5・7・9・11・13ステップ）を重ねて、小節の頭とずらす（ポリメトリック）。
// 主題は付点8分（0.75拍）の並びで、4拍子の上に3拍系のノリ（3対4）を作る。最後は全パートがそろう小節でひとつに戻る。
// 使い方: node assets-src/ai-songs/_gen/poly-electro.mjs → assets-src/ai-songs/poly-electro.json
import fs from "node:fs";
const BARS = 128, SPB = 16, S = BARS * SPB;
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const nm = (m) => NAMES[m % 12] + (Math.floor(m / 12) - 1);
const NP = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const midiOf = (s) => { const m = /^([A-G])(#|b)?(-?\d)$/.exec(s); return NP[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12 * (Number(m[3]) + 1); };
// ---- 区間（小節は1始まり）
const SEC = [
  { n: "序", a: 1, b: 16 }, { n: "ビルドA", a: 17, b: 32 }, { n: "ドロップA", a: 33, b: 48 }, { n: "ブレイク", a: 49, b: 64 },
  { n: "ビルドB(+3)", a: 65, b: 80 }, { n: "ドロップB(+3)", a: 81, b: 96 }, { n: "ポリリズム最高潮", a: 97, b: 112 }, { n: "終曲", a: 113, b: 128 },
];
const secOf = (bar) => SEC.findIndex((s) => bar >= s.a && bar <= s.b);
const shiftOf = (bar) => (bar >= 65 && bar <= 96 ? 3 : 0);                // 65〜96小節は短3度上（Aマイナー → Cマイナー）
// 和音（1小節に1つ、8小節でひとまわり）: Am Am Bb Bb F F E E
const CH = [["A", 0, "m"], ["A", 0, "m"], ["A#", 1, ""], ["A#", 1, ""], ["F", 8, ""], ["F", 8, ""], ["E", 7, ""], ["E", 7, ""]];
const rootSemi = (bar) => [0, 0, 1, 1, 8, 8, 7, 7][(bar - 1) % 8];            // Aからの半音数（根音）
const rootMidi = (bar, oct) => 12 * (oct + 1) + 9 + rootSemi(bar) + shiftOf(bar);
const chordName = (bar) => { const [r, , q] = CH[(bar - 1) % 8]; const t = shiftOf(bar); const pc = (NP[r[0]] + (r[1] === "#" ? 1 : 0) + t) % 12; return NAMES[pc] + q; };
// ---- ステップ列（各パートの16分音符ごとの出来事: {n: 音名 or "x", len: ステップ数}）
const mk = () => Array(S).fill(null);
const L = { kick: mk(), snare: mk(), hihat: mk(), crash: mk(), tom: mk(), bass: mk(), lead: mk(), lead2: mk(), keys: mk(), pad: mk(), bell: mk(), choir: mk() };
const st = (bar, k = 0) => (bar - 1) * SPB + k;
const RNG = { bass: [24, 48], lead: [48, 96], lead2: [48, 96], keys: [36, 84], pad: [36, 84], bell: [60, 96], choir: [48, 84] };
const clampN = (part, n) => { if (n === "x" || !RNG[part]) return n; let m = midiOf(n); const [lo, hi] = RNG[part]; while (m > hi) m -= 12; while (m < lo) m += 12; return nm(m); };
const put = (part, i, n, len = 1) => { if (i >= 0 && i < S) L[part][i] = { n: clampN(part, n), len }; };
const sectionSteps = (a, b, fn) => { for (let bar = a; bar <= b; bar++) for (let k = 0; k < SPB; k++) fn(bar, k, st(bar, k), st(bar, k) - st(a, 0)); };
// 周期パターン: 区間の頭から数えて cyc ステップごとに繰り返す
const cyc = (a, b, part, riff, base, len = 1) => sectionSteps(a, b, (bar, k, i, j) => { const v = riff[j % riff.length]; if (v === null || v === undefined) return; put(part, i, v === "x" ? "x" : nm(base(bar) + v), len); });
const at = (bar, part) => sectionSteps(bar, bar, (b, k, i) => {});
// ---- 主題（付点8分の3対4）。2小節=8拍ずつ、和音ごと
const fit = (s, beats) => { let sum = 0; const out = []; for (const t of s.trim().split(/\s+/)) { const d = Number(t.split(":")[1]); if (sum + d > beats + 1e-9) break; out.push(t); sum += d; } if (sum < beats - 1e-9) out.push(`R:${(beats - sum).toFixed(2).replace(/\.?0+$/, "")}`); return out; };
const THEME = [
  "E5:0.75 E5:0.75 A5:0.5 G5:1 E5:0.5 D5:0.5 E5:1 R:0.5 C5:0.5 A4:1",
  "F5:0.75 F5:0.75 A#5:0.5 A5:1 F5:0.5 D#5:0.5 F5:1 R:0.5 D5:0.5 A#4:1",
  "C5:0.75 C5:0.75 F5:0.5 E5:1 C5:0.5 A#4:0.5 C5:1 R:0.5 A4:0.5 F4:1",
  "B4:0.75 B4:0.75 E5:0.5 G#5:1 B5:1.5 A5:0.5 G#5:0.5 E5:2",
];
const themeEvents = (a, b, shift = 0, octave = 0, partName = "lead") => {
  for (let bar = a; bar <= b; bar += 2) {
    const idx = ((bar - a) / 2) % 4; let cur = st(bar, 0);
    for (const tok of fit(THEME[idx], 8)) { const [p, d] = tok.split(":"); const len = Math.round(Number(d) * 4); if (p !== "R") put(partName, cur, nm(midiOf(p) + shift + 12 * octave), len); cur += len; }
  }
};
const lowRoot = (o) => (bar) => rootMidi(bar, o);
// ============ 区間ごとの組み立て ============
const S1 = SEC[0], S2 = SEC[1], S3 = SEC[2], S4 = SEC[3], S5 = SEC[4], S6 = SEC[5], S7 = SEC[6], S8 = SEC[7];
const arpTri = (a, b, part, cycLen, octave, len = 1, up = [0, 7, 12, 7, 15, 12, 19]) => { const riff = Array.from({ length: cycLen }, (_, j) => up[j % up.length] + (bar0 => 0)(0)); cyc(a, b, part, riff, lowRoot(octave), len); };
const minorArp = (a, b, part, cycLen, octave, len = 1) => { // 短調の和音の音（根・短3度・5度・オクターブ）をたどる
  sectionSteps(a, b, (bar, k, i, j) => { if (j % 1 !== 0) return; const seq = [0, 3, 7, 12, 7, 3, 10, 15, 12, 7, 3, 0, 5]; const q = j % cycLen; const v = seq[q % seq.length]; const third = (CH[(bar - 1) % 8][2] === "m" ? 3 : 4); put(part, i, nm(rootMidi(bar, octave) + (v === 3 ? third : v === 15 ? 12 + third : v)), len); }); };
// --- 序（1〜16）: パッド・鐘（5周期）・ハイハット（3周期、5小節から）・キック（9小節からまばら、13小節から5周期）
sectionSteps(S1.a, S1.b, (bar, k, i) => { if (k === 0) put("pad", i, nm(rootMidi(bar, 3) + (CH[(bar - 1) % 8][2] === "m" ? 7 : 7)), 16); });
minorArp(S1.a, S1.b, "bell", 5, 5, 2);
cyc(5, 16, "hihat", [ "x", null, null ], () => 0, 1);
cyc(9, 12, "kick", ["x", null, null, null, null, null, null, null], () => 0, 1);
cyc(13, 16, "kick", ["x", null, null, null, null], () => 0, 1);
sectionSteps(9, 16, (bar, k, i) => { if (k === 0) put("bass", i, nm(rootMidi(bar, 2)), 16); });
put("crash", st(1, 0), "x"); put("crash", st(9, 0), "x");
// --- ビルドA（17〜32）
sectionSteps(S2.a, S2.b, (bar, k, i) => { if (k % 4 === 0) put("kick", i, "x"); if (k === 4 || k === 12) put("snare", i, "x"); if (k === 0) put("pad", i, nm(rootMidi(bar, 3) + 7), 16); });
cyc(S2.a, S2.b, "hihat", ["x", null, null], () => 0, 1);
cyc(S2.a, S2.b, "bass", [0, null, null, 12, null, 7, null], lowRoot(2), 1);           // 7ステップ周期
minorArp(S2.a, S2.b, "keys", 5, 4, 1);                                              // 5ステップ周期
minorArp(S2.a, S2.b, "bell", 3, 5, 1);
themeEvents(25, 32, 0, 0, "lead");
put("crash", st(17, 0), "x"); put("crash", st(25, 0), "x");
for (const bar of [24, 32]) { for (let k = 8; k < 16; k += 1) put("snare", st(bar, k), "x"); }
// --- ドロップA（33〜48）
sectionSteps(S3.a, S3.b, (bar, k, i) => { if (k % 4 === 0) put("kick", i, "x"); if (k === 4 || k === 12) put("snare", i, "x"); if (k % 2 === 0) put("hihat", i, "x"); if (k === 0) put("pad", i, nm(rootMidi(bar, 3) + 7), 16); });
cyc(S3.a, S3.b, "bass", [0, null, 0, 12, null, 7, 0], lowRoot(2), 1);
minorArp(S3.a, S3.b, "keys", 5, 4, 1);
minorArp(S3.a, S3.b, "bell", 3, 6, 1);
themeEvents(S3.a, S3.b, 0, 0, "lead");
themeEvents(41, 48, 0, 1, "lead2");                                                  // 後半は1オクターブ上の重ね
for (const bar of [33, 41]) put("crash", st(bar, 0), "x");
for (const bar of [40, 48]) { for (let k = 0; k < 16; k += 1) if (k >= 8) put("tom", st(bar, k), "x"); }
// --- ブレイク（49〜64）: 拍を薄く、パッド・合唱・鐘、トムは5周期
sectionSteps(S4.a, S4.b, (bar, k, i) => { if (k === 0) { put("pad", i, nm(rootMidi(bar, 3) + 7), 16); put("choir", i, nm(rootMidi(bar, 4) + (CH[(bar - 1) % 8][2] === "m" ? 3 : 4)), 16); } });
cyc(S4.a, S4.b, "tom", ["x", null, null, null, null], () => 0, 1);
minorArp(S4.a, S4.b, "bell", 6, 5, 2);
minorArp(S4.a, S4.b, "keys", 7, 4, 2);
cyc(S4.a + 8, S4.b, "bass", [0, null, null, null, null, null, null, null, null], lowRoot(2), 4);
cyc(61, 64, "kick", ["x", null, null, null], () => 0, 1);
for (let k = 0; k < 16; k += (64 - 64 === 0 ? 1 : 1)) put("snare", st(64, k), k < 8 ? null : "x");
sectionSteps(64, 64, (b, k, i) => { if (k < 8) L.snare[i] = null; });
put("crash", st(49, 0), "x");
// --- ビルドB（65〜80、短3度上）
sectionSteps(S5.a, S5.b, (bar, k, i, j) => { if (k % 4 === 0) put("kick", i, "x"); if (k % 2 === 0) put("hihat", i, "x"); if (k === 0) put("pad", i, nm(rootMidi(bar, 3) + 7), 16); });
cyc(S5.a, S5.b, "snare", ["x", null, null, null, null, null, null], () => 0, 1);          // スネアは7ステップ周期
cyc(S5.a, S5.b, "bass", [0, null, 12, null, 7, null, null, 0, null], lowRoot(2), 1);      // 9ステップ周期
minorArp(S5.a, S5.b, "keys", 5, 4, 1);
themeEvents(S5.a, S5.b, 3, 0, "lead");
put("crash", st(65, 0), "x"); put("crash", st(73, 0), "x");
for (const bar of [80]) for (let k = 8; k < 16; k++) put("tom", st(bar, k), "x");
// --- ドロップB（81〜96）
sectionSteps(S6.a, S6.b, (bar, k, i) => { if (k % 4 === 0) put("kick", i, "x"); if (k === 4 || k === 12) put("snare", i, "x"); if (k % 2 === 0 || k % 4 === 3) put("hihat", i, "x"); if (k === 0) put("pad", i, nm(rootMidi(bar, 3) + 7), 16); });
cyc(S6.a, S6.b, "bass", [0, 0, null, 12, null, 7, 0], lowRoot(2), 1);
minorArp(S6.a, S6.b, "keys", 5, 4, 1);
minorArp(S6.a, S6.b, "lead2", 13, 5, 1);                                              // 13ステップ周期の高い分散和音
themeEvents(S6.a, S6.b, 3, 0, "lead");
themeEvents(89, 96, 3, 1, "bell");
put("crash", st(81, 0), "x"); put("crash", st(89, 0), "x");
for (const bar of [88, 96]) for (let k = 4; k < 16; k++) put("tom", st(bar, k), "x");
// --- ポリリズム最高潮（97〜112、Aに戻る）: 周期を全部ずらす。112小節でそろえる
const P = 111;
sectionSteps(S7.a, P, (bar, k, i, j) => { if (k === 0) put("pad", i, nm(rootMidi(bar, 3) + 7), 16); });
cyc(S7.a, P, "kick", ["x", null, null, null, null], () => 0, 1);                        // 5
cyc(S7.a, P, "snare", ["x", null, null, null, null, null, null], () => 0, 1);          // 7（真ん中を1つずらして 4小節ごとに 2拍3連風の噛み合い）
cyc(S7.a, P, "hihat", ["x", null, null], () => 0, 1);                                   // 3
cyc(S7.a, P, "bass", [0, null, 0, 7, null, null, 12, null, null], lowRoot(2), 1);      // 9
minorArp(S7.a, P, "keys", 11, 4, 1);                                                    // 11
minorArp(S7.a, P, "lead2", 13, 5, 1);                                                   // 13
minorArp(S7.a, P, "bell", 7, 6, 1);                                                     // 7
themeEvents(S7.a, P, 0, 0, "lead");
themeEvents(S7.a + 8, P, 0, 1, "choir");
cyc(S7.a + 8, P, "tom", ["x", null, null, null, null, null, null, null, null, null, null], () => 0, 1); // 11
put("crash", st(97, 0), "x"); put("crash", st(105, 0), "x");
sectionSteps(112, 112, (bar, k, i) => { for (const p of ["kick", "snare", "hihat", "tom", "bass", "keys", "lead2", "bell", "choir", "lead"]) L[p][i] = null; if (k % 4 === 0) put("kick", i, "x"); if (k === 4 || k === 12) put("snare", i, "x"); if (k >= 8) put("tom", i, "x"); if (k === 0) put("bass", i, nm(rootMidi(bar, 2)), 8); });
put("crash", st(112, 0), "x");
// --- 終曲（113〜128）: 4つ打ちでそろい、1つずつ抜けて、鐘とパッドで終わる
sectionSteps(113, 120, (bar, k, i) => { if (k % 4 === 0) put("kick", i, "x"); if (k === 4 || k === 12) put("snare", i, "x"); if (k % 2 === 0) put("hihat", i, "x"); if (k === 0) { put("pad", i, nm(rootMidi(bar, 3) + 7), 16); put("bass", i, nm(rootMidi(bar, 2)), 16); } });
themeEvents(113, 120, 0, 0, "lead");
minorArp(113, 120, "keys", 5, 4, 1);
put("crash", st(113, 0), "x");
sectionSteps(121, 128, (bar, k, i) => { if (k === 0) { put("pad", i, nm(rootMidi(bar, 3) + 7), 16); put("choir", i, nm(rootMidi(bar, 4) + (CH[(bar - 1) % 8][2] === "m" ? 3 : 4)), 16); } });
minorArp(121, 128, "bell", 5, 5, 3);
sectionSteps(127, 128, (bar, k, i) => { L.bell[i] = null; });
put("bell", st(127, 0), nm(midiOf("A5")), 16); put("bell", st(128, 0), nm(midiOf("E6")), 16); put("pad", st(128, 0), nm(midiOf("A3")), 16); put("choir", st(128, 0), nm(midiOf("C5")), 16);
put("crash", st(121, 0), "x");
// ---- 出力
const rest = (out, beats) => { while (beats > 16) { out.push("R:16"); beats -= 16; } if (beats > 0) out.push(`R:${beats}`); };
const toNotes = (arr, drum) => { const out = []; let i = 0; while (i < S) { const e = arr[i]; if (!e) { let j = i; while (j < S && !arr[j]) j++; rest(out, (j - i) * 0.25); i = j; continue; } let nextI = i + 1; while (nextI < S && !arr[nextI]) nextI++; const gap = nextI - i; const len = Math.min(e.len, gap); out.push(`${e.n}:${len * 0.25}`); if (gap > len) rest(out, (gap - len) * 0.25); i = nextI; } return out.join(" "); };
const parts = [
  ["kick", "キック（区間ごとに4つ打ち／5ステップ周期）", "kick", 0.32, 0, true], ["snare", "スネア（2・4拍／7ステップ周期）", "snare", 0.24, 0.05, true], ["hihat", "ハイハット（3ステップ周期）", "hihat", 0.13, 0.25, true],
  ["crash", "クラッシュ", "crash", 0.18, -0.2, true], ["tom", "タム（5・11ステップ周期とフィル）", "tom", 0.22, -0.15, true],
  ["sub808", "808ベース（7・9ステップ周期のリフ）", "bass", 0.3, 0, false], ["lead", "シンセリード（主題・付点の3対4）", "lead", 0.24, -0.1, false],
  ["lead", "シンセリード2（13ステップ周期・1オクターブ上の重ね）", "lead2", 0.14, 0.3, false], ["keys", "エレピ（5・7・11ステップ周期の分散和音）", "keys", 0.15, 0.2, false],
  ["pad", "パッド", "pad", 0.12, 0, false], ["bell", "鐘・きらめき（3・5・7ステップ周期）", "bell", 0.13, 0.35, false], ["choir", "合唱", "choir", 0.14, -0.3, false],
];
const chords = Array.from({ length: BARS }, (_, i) => chordName(i + 1)).join(" ");
const song = {
  title: "歯車は光る", description: "【仮】エレクトリック・ポリリズム（約4分）。♩128・4拍子・128小節。3・5・7・9・11・13ステップの周期のパターン（キック・スネア・ハイハット・ベース・分散和音）を4拍子の上に重ねてずらし、付点8分の主題で3対4のノリを作る。Aマイナーで始まり、ブレイクをはさんで短3度上げ（Cマイナー）、ポリリズム最高潮でAに戻り、112小節目で全パートがそろって4つ打ちに戻って終わる。",
  bpm: 128, beats: 4, chords, barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "pop", tone: "prs",
  parts: parts.map(([instrument, role, key, volume, pan]) => ({ instrument, role, volume, pan, amp: "auto", notes: toNotes(L[key]) })),
};
fs.writeFileSync(new URL("../poly-electro.json", import.meta.url), JSON.stringify(song, null, 2) + "\n", "utf8");
console.log("小節", BARS, "秒", (BARS * 4 / 128 * 60));
