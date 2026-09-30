// エレクトリック・ポリリズム第2作「回転刃（かいてんじん）」（約3分）を書き出す。♩152・4拍子・114小節＝3分0秒。Eマイナー（フリジアン風）。
// 考え方: 16分音符の「ステップ」の上に、周期の違うパターン（3・5・7・9・11・13ステップ）を重ねて、小節の頭とずらす（ポリメトリック）。
// 主題は付点8分（0.75拍）の並びで、4拍子の上に3拍系のノリ（3対4）を作る。最後は全パートがそろう小節でひとつに戻る。
// 使い方: node assets-src/ai-songs/_gen/poly-electro-2.mjs → assets-src/ai-songs/poly-electro-2.json
import fs from "node:fs";
const BARS = 114, SPB = 16, S = BARS * SPB;
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const nm = (m) => NAMES[m % 12] + (Math.floor(m / 12) - 1);
const NP = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const midiOf = (s) => { const m = /^([A-G])(#|b)?(-?\d)$/.exec(s); return NP[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12 * (Number(m[3]) + 1); };
// ---- 区間（小節は1始まり）
const SEC = [
  { n: "序", a: 1, b: 8 }, { n: "ビルドA", a: 9, b: 24 }, { n: "ドロップA", a: 25, b: 40 }, { n: "ブレイク", a: 41, b: 56 },
  { n: "ビルドB(+2)", a: 57, b: 72 }, { n: "ドロップB(+2)", a: 73, b: 88 }, { n: "ポリリズム最高潮", a: 89, b: 104 }, { n: "終曲", a: 105, b: 114 },
];
const secOf = (bar) => SEC.findIndex((s) => bar >= s.a && bar <= s.b);
const shiftOf = (bar) => (bar >= 57 && bar <= 88 ? 2 : 0);                // 57〜88小節は長2度上（Eマイナー → F#マイナー）
// 和音（1小節に1つ、8小節でひとまわり）: Em Em F F C C D B
const CH = [["E", 0, "m"], ["E", 0, "m"], ["F", 1, ""], ["F", 1, ""], ["C", 8, ""], ["C", 8, ""], ["D", 10, ""], ["B", 7, ""]];
const rootSemi = (bar) => [0, 0, 1, 1, 8, 8, 10, 7][(bar - 1) % 8];            // Eからの半音数（根音）
const rootMidi = (bar, oct) => 12 * (oct + 1) + 4 + rootSemi(bar) + shiftOf(bar);
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
  "B4:1.25 E5:1.25 G5:1.5 F#5:1 E5:0.75 D5:0.5 B4:1.75",
  "C5:1.25 F5:1.25 A5:1.5 G5:1 F5:0.75 E5:0.5 C5:1.75",
  "G4:1.25 C5:1.25 E5:1.5 D5:1 C5:0.75 B4:0.5 G4:1.75",
  "A4:1.25 D5:1.25 F#5:1.5 E5:1 D5:0.75 C#5:0.5 D#5:1.75",
];
const themeEvents = (a, b, shift = 0, octave = 0, partName = "lead") => {
  for (let bar = a; bar <= b; bar += 2) {
    const idx = ((bar - a) / 2) % 4; let cur = st(bar, 0);
    for (const tok of fit(THEME[idx], 8)) { const [p, d] = tok.split(":"); const len = Math.round(Number(d) * 4); if (p !== "R") put(partName, cur, nm(midiOf(p) + shift + 12 * octave), len); cur += len; }
  }
};
const lowRoot = (o) => (bar) => rootMidi(bar, o);
// ============ 区間ごとの組み立て ============
const SS = SEC;
const arpMinor = (a, b, part, cycLen, octave, len = 1) => sectionSteps(a, b, (bar, k, i, j) => { const seq = [0, 3, 7, 12, 7, 3, 10, 15, 12, 7, 3, 0, 5]; const v = seq[(j % cycLen) % seq.length]; const third = CH[(bar - 1) % 8][2] === "m" ? 3 : 4; put(part, i, nm(rootMidi(bar, octave) + (v === 3 ? third : v === 15 ? 12 + third : v)), len); });
const four = (a, b, hatEighth = true) => sectionSteps(a, b, (bar, k, i) => { if (k % 4 === 0) put("kick", i, "x"); if (k === 4 || k === 12) put("snare", i, "x"); if (hatEighth && k % 2 === 0) put("hihat", i, "x"); });
const padAt = (a, b, choir = false) => sectionSteps(a, b, (bar, k, i) => { if (k === 0) { put("pad", i, nm(rootMidi(bar, 3) + 7), 16); if (choir) put("choir", i, nm(rootMidi(bar, 4) + (CH[(bar - 1) % 8][2] === "m" ? 3 : 4)), 16); } });
const fillTom = (bar, from = 8) => { for (let k = from; k < 16; k++) put("tom", st(bar, k), "x"); };
// 序
padAt(1, 8); arpMinor(1, 8, "bell", 5, 5, 2); cyc(3, 8, "hihat", ["x", null, null], () => 0, 1); cyc(5, 8, "kick", ["x", null, null, null, null], () => 0, 1); put("crash", st(1, 0), "x");
// ビルドA
four(9, 24, false); padAt(9, 24); cyc(9, 24, "hihat", ["x", null, null], () => 0, 1); cyc(9, 24, "snare", ["x", null, null, null, null, null, null], () => 0, 1);
cyc(9, 24, "bass", [0, null, null, 12, null, 7, null], lowRoot(2), 1); arpMinor(9, 24, "keys", 5, 4, 1); arpMinor(9, 24, "bell", 3, 5, 1);
themeEvents(17, 24, 0, 0, "lead"); put("crash", st(9, 0), "x"); put("crash", st(17, 0), "x"); fillTom(24); fillTom(16, 12);
// ドロップA
four(25, 40); padAt(25, 40); cyc(25, 40, "bass", [0, 0, null, 12, 0, 7, null, 0, 10, null], lowRoot(2), 1);   // 10ステップ周期
arpMinor(25, 40, "keys", 5, 4, 1); arpMinor(25, 40, "lead2", 13, 5, 1); arpMinor(25, 40, "bell", 3, 6, 1);
themeEvents(25, 40, 0, 0, "lead"); put("crash", st(25, 0), "x"); put("crash", st(33, 0), "x"); fillTom(32); fillTom(40, 4);
// ブレイク
padAt(41, 56, true); cyc(41, 56, "tom", ["x", null, null, null, null], () => 0, 1); arpMinor(41, 56, "bell", 6, 5, 2); arpMinor(41, 56, "keys", 7, 4, 2);
cyc(49, 56, "bass", [0, null, null, null, null, null, null, null, null], lowRoot(2), 4); cyc(53, 56, "kick", ["x", null, null, null], () => 0, 1);
sectionSteps(56, 56, (b, k, i) => { if (k >= 8) put("snare", i, "x"); }); put("crash", st(41, 0), "x");
// ビルドB（+2）
four(57, 72, true); padAt(57, 72); cyc(57, 72, "snare", ["x", null, null, null, null, null, null], () => 0, 1); L.snare.fill(null, st(57, 0), st(57, 0));
sectionSteps(57, 72, (bar, k, i) => { if (k === 4 || k === 12) L.snare[i] = null; });
cyc(57, 72, "bass", [0, null, 12, null, 7, null, null, 0, null], lowRoot(2), 1); arpMinor(57, 72, "keys", 5, 4, 1); themeEvents(57, 72, 2, 0, "lead");
put("crash", st(57, 0), "x"); put("crash", st(65, 0), "x"); fillTom(72);
// ドロップB（+2）
four(73, 88); padAt(73, 88); cyc(73, 88, "bass", [0, 0, null, 12, 0, 7, 0], lowRoot(2), 1); arpMinor(73, 88, "keys", 5, 4, 1); arpMinor(73, 88, "lead2", 11, 5, 1);
themeEvents(73, 88, 2, 0, "lead"); themeEvents(81, 88, 2, 1, "bell"); put("crash", st(73, 0), "x"); put("crash", st(81, 0), "x"); fillTom(80); fillTom(88, 4);
// ポリリズム最高潮（Eに戻る）: 周期を全部ずらし、104小節でそろえる
padAt(89, 103);
cyc(89, 103, "kick", ["x", null, null, null, null], () => 0, 1); cyc(89, 103, "snare", ["x", null, null, null, null, null, null], () => 0, 1); cyc(89, 103, "hihat", ["x", null, null], () => 0, 1);
cyc(89, 103, "bass", [0, null, 0, 7, null, null, 12, null, null], lowRoot(2), 1); arpMinor(89, 103, "keys", 11, 4, 1); arpMinor(89, 103, "lead2", 13, 5, 1); arpMinor(89, 103, "bell", 7, 6, 1);
themeEvents(89, 103, 0, 0, "lead"); themeEvents(97, 103, 0, 1, "choir"); cyc(97, 103, "tom", ["x", null, null, null, null, null, null, null, null, null, null], () => 0, 1);
put("crash", st(89, 0), "x"); put("crash", st(97, 0), "x");
sectionSteps(104, 104, (bar, k, i) => { for (const p of ["kick", "snare", "hihat", "tom", "bass", "keys", "lead2", "bell", "choir", "lead"]) L[p][i] = null; if (k % 4 === 0) put("kick", i, "x"); if (k === 4 || k === 12) put("snare", i, "x"); if (k >= 8) put("tom", i, "x"); if (k === 0) put("bass", i, nm(rootMidi(bar, 2)), 8); }); put("crash", st(104, 0), "x");
// 終曲
four(105, 110); padAt(105, 110); sectionSteps(105, 110, (bar, k, i) => { if (k === 0) put("bass", i, nm(rootMidi(bar, 2)), 16); }); themeEvents(105, 110, 0, 0, "lead"); arpMinor(105, 110, "keys", 5, 4, 1); put("crash", st(105, 0), "x");
padAt(111, 114, true); arpMinor(111, 114, "bell", 5, 5, 3); sectionSteps(113, 114, (b, k, i) => { L.bell[i] = null; });
put("bell", st(113, 0), nm(midiOf("E5")), 16); put("bell", st(114, 0), nm(midiOf("B5")), 16); put("pad", st(114, 0), nm(midiOf("E3")), 16); put("choir", st(114, 0), nm(midiOf("G4")), 16); put("crash", st(111, 0), "x");
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
  title: "回転刃", description: "【仮】エレクトリック・ポリリズム（約4分）。第2作。やや速い♩152・4拍子・114小節（3分）。5・7・9・10・11・13ステップの周期のパターンを4拍子の上に重ねてずらし、主題は5＋5＋6の3つ組（1.25拍・1.25拍・1.5拍）の並びで、拍の頭をはぐらかす。Eマイナー（フリジアン風の半音上のF）で始まり、ブレイクをはさんでF#マイナーへ上げ、ポリリズム最高潮でEに戻り、104小節目で全パートがそろって4つ打ちに戻って終わる。",
  bpm: 152, beats: 4, chords, barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "pop", tone: "prs",
  parts: parts.map(([instrument, role, key, volume, pan]) => ({ instrument, role, volume, pan, amp: "auto", notes: toNotes(L[key]) })),
};
fs.writeFileSync(new URL("../poly-electro-2.json", import.meta.url), JSON.stringify(song, null, 2) + "\n", "utf8");
console.log("小節", BARS, "秒", (BARS * 4 / 128 * 60));
