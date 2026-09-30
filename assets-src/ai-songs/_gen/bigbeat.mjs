// ダンスミュージック×ロックの曲を10曲まとめて書き出す（ビッグビート／ブレイクビーツ・ドラムンベース・4つ打ちのビートに、歪んだギターのリフ・アシッドなベース・電子のアルペジオを重ねる）。
// 「ブンブンサテライトのような」は、ダンスとロックを混ぜた作風というジャンルの傾向だけを参考にした。特定の曲・アーティストの旋律・リフ・進行はなぞっていない（CLAUDE.md 1-1）。
// 曲ごとに、テンポ・調・進行・ドラムの型・リフの型・ギターソロ（歌うチョーキング／タッピング）・ポリリズム・壮大な弦と合唱、を切りかえる。乱数の種は曲ごとに固定（同じ設定なら同じ曲）。
// 使い方: node assets-src/ai-songs/_gen/bigbeat.mjs → assets-src/ai-songs/bb-01.json … bb-10.json
import fs from "node:fs";
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const nm = (m) => NAMES[((m % 12) + 12) % 12] + (Math.floor(m / 12) - 1);
const RNG = { leadGuitar: [52, 88], distGuitar: [40, 64], bass: [28, 55], sub808: [24, 48], lead: [48, 96], keys: [36, 84], pad: [36, 84], strings: [36, 96], choir: [48, 84], brass: [40, 84], bell: [60, 96], riser: [48, 96], piano: [21, 108] };
const clampTo = (ins, m) => { const [lo, hi] = RNG[ins]; while (m > hi) m -= 12; while (m < lo) m += 12; return m; };
const rngOf = (seed) => { let a = seed >>> 0; return () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
const MIN = [0, 2, 3, 5, 7, 8, 10], PEN = [0, 3, 5, 7, 10];
// 進行（マイナーの度数）
const PROGS = { A: [1, 6, 3, 7], B: [1, 1, 6, 7], C: [1, 4, 6, 5], D: [1, 2, 7, 1], E: [1, 7, 6, 7], F: [6, 7, 1, 1] };
const RIFF_CELLS = ["x.x.xx..x.x.xx..", "x..x..x.x..x..x.", "xx.xx.x.xx.xx.x.", "x.xxx.xxx.xxx.xx", "x...x.x.x...x.x.", "x.x..x.xx.x..x.x", "xxxx.xx.xxxx.xx."];
const DRUM = {
  bigbeat: { kick: ["x..x..x...x..x..", "x..x..x...x.x..."], snare: ["....x..x....x...", "....x.......x..x"], hat: "x.xxx.xxx.xxx.xx", open: "..x...x...x...x.", clap: "....x.......x..." },
  fourfloor: { kick: ["x...x...x...x..."], snare: ["....x.......x..."], hat: "x.x.x.x.x.x.x.x.", open: "..x...x...x...x.", clap: "....x.......x..." },
  dnb: { kick: ["x.........x....."], snare: ["....x.......x..."], hat: "x.x.x.x.x.x.x.x.", open: "..x.......x.....", clap: "" },
  halftime: { kick: ["x.......x.....x."], snare: ["........x......."], hat: "x.x.x.x.x.x.x.x.", open: "......x.......x.", clap: "........x......." },
};
const BASE = [["intro", 8], ["verse", 16], ["drop", 16], ["break", 8], ["build", 8], ["drop", 16], ["solo", 16], ["final", 16], ["outro", 8]];
const SONGS = [
  { id: "bb-01", title: "電光の環", bpm: 138, key: 4, prog: "A", drum: "bigbeat", riff: 1, seed: 11, solo: "melodic", target: 215, desc: "ビッグビートの定番の疾走感。跳ねるブレイクビーツにアシッドなベースと歪んだギターのリフ。中盤にギターソロ。" },
  { id: "bb-02", title: "白い衝動", bpm: 174, key: 6, prog: "B", drum: "dnb", riff: 3, seed: 22, solo: "tap", tap: true, target: 190, desc: "テンポの速いドラムンベース×ロック。イントロからタッピングのリフ、ソロもタッピング。" },
  { id: "bb-03", title: "螺旋の門", bpm: 128, key: 1, prog: "C", drum: "fourfloor", riff: 5, seed: 33, solo: null, poly: true, target: 220, desc: "ポリリズム。5・7・9・11ステップの周期のパターンが4つ打ちの上でずれながら重なり、最後に1つにそろう。" },
  { id: "bb-04", title: "星屑のライダー", bpm: 150, key: 9, prog: "A", drum: "bigbeat", riff: 2, seed: 44, solo: "melodic", epic: true, target: 240, desc: "壮大。弦・ブラス・合唱が重なるビッグビート。ギターソロは歌うチョーキング。" },
  { id: "bb-05", title: "ネオン・インフェルノ", bpm: 160, key: 2, prog: "D", drum: "bigbeat", riff: 0, seed: 55, solo: "both", tap: true, target: 200, desc: "テンポの速い曲。16分の刻みと電子のアルペジオ、ソロはチョーキングからタッピングへ。" },
  { id: "bb-06", title: "重力のむこう", bpm: 116, key: 11, prog: "E", drum: "halftime", riff: 6, seed: 66, solo: "melodic", epic: true, target: 250, desc: "壮大でゆっくり。ハーフタイムの重いビートに弦と合唱が広がり、最後に転調して盛り上がる。" },
  { id: "bb-07", title: "回路の祈り", bpm: 134, key: 7, prog: "F", drum: "bigbeat", riff: 4, seed: 77, solo: "tap", tap: true, poly: true, target: 215, desc: "ポリリズムとタッピングの組み合わせ。周期のずれたリフの上でタッピングのソロ。" },
  { id: "bb-08", title: "暁のシグナル", bpm: 145, key: 6, prog: "C", drum: "fourfloor", riff: 1, seed: 88, solo: "melodic", epic: true, target: 225, desc: "4つ打ちのダンスチューンに、壮大なコードと歌うギターソロ。夜明けに向かって明るくなる。" },
  { id: "bb-09", title: "零の軌道", bpm: 180, key: 0, prog: "A", drum: "dnb", riff: 3, seed: 99, solo: "both", tap: true, poly: true, target: 185, desc: "いちばん速い曲。ドラムンベースの速さに、ポリリズム、ギターソロ、タッピング。" },
  { id: "bb-10", title: "終わらない夜明け", bpm: 126, key: 4, prog: "B", drum: "bigbeat", riff: 5, seed: 111, solo: "both", tap: true, poly: true, epic: true, target: 270, desc: "集大成。壮大な弦と合唱、ポリリズム、チョーキングとタッピングのソロ、転調のラストサビ。" },
];
function build(sp) {
  const rng = rngOf(sp.seed), pick = (a) => a[Math.floor(rng() * a.length)];
  const kBars = (sp.target * sp.bpm) / 240 / 112;
  const secs = BASE.filter(([k]) => (k !== "solo" || sp.solo)).map(([k, n]) => [k, Math.max(4, Math.round((n * kBars) / 4) * 4)]);
  const bars = []; let g = 0; const P = PROGS[sp.prog];
  for (const [kind, n] of secs) for (let i = 0; i < n; i++) bars.push({ kind, i, n, g: g++, deg: P[Math.floor(i / 2) % 4], shift: kind === "final" && (sp.epic || sp.solo === "both") ? 2 : 0 });
  const BARS = bars.length, S = BARS * 16;
  const mk = () => Array(S).fill(null);
  const L = Object.fromEntries(["kick", "snare", "clap", "hihat", "openhat", "crash", "tom", "riser", "bass", "sub", "gL", "gR", "stab", "arp", "pad", "strings", "brass", "choir", "chop", "bell", "hook", "solo", "piano"].map((k) => [k, mk()]));
  const put = (part, bar, k, n, len = 1, ins) => { const i = bar * 16 + k; if (i < 0 || i >= S) return; if (n === "x") { L[part][i] = { n: "x", len }; return; } const m = ins ? clampTo(ins, n) : n; L[part][i] = { n: nm(m), len }; };
  const putRaw = (part, i, txt, len) => { if (i >= 0 && i < S) L[part][i] = { n: txt, len }; };
  const D = DRUM[sp.drum], kickPat = pick(D.kick), snPat = pick(D.snare);
  const st = (p) => [...p].flatMap((c, i) => (c === "." ? [] : [i]));
  const semi = (deg, shift) => sp.key + shift + MIN[(deg - 1) % 7];
  const tonic = (b) => 12 * 3 + semi(b.deg, b.shift);                         // 根音（オクターブ2〜3の目安。あとで音域に丸める）
  const third = (b) => (MIN[(b.deg + 1) % 7] - MIN[(b.deg - 1) % 7] + 12) % 12;
  const isMinorChord = (b) => third(b) === 3;
  // ---- リフ（2小節の型。歪んだギターと、ベースの一部が同じリズムで動く）
  const riffCell = RIFF_CELLS[(sp.riff + 0) % RIFF_CELLS.length], riffCell2 = RIFF_CELLS[(sp.riff + 3) % RIFF_CELLS.length];
  const riffIv = Array.from({ length: 32 }, () => pick([0, 0, 0, 0, 0, 3, 5, 7, 10, 12, 1]));
  // ---- フック（旋律）2小節×4の型
  const hookRhy = ["x..x..x.x..x....", "x.x...x.x.x.....", "x...x..x..x.x...", "x..x.x..x......."].map((p) => st(p));
  const hookNotes = (deg0) => { const out = []; for (let ph = 0; ph < 4; ph++) { const rh = hookRhy[ph % 4]; let idx = pick([0, 2, 3, 4]); const notes = rh.map((k, n) => { if (n > 0) idx = Math.max(0, Math.min(9, idx + pick([-2, -1, -1, 1, 1, 2]))); if (n === rh.length - 1) idx = pick([0, 2, 4]) + (ph === 3 ? 5 : 0); return { k, idx }; }); out.push(notes); } return out; };
  const HOOK = hookNotes();
  const penMidi = (idx, root, oct) => 12 * (oct + 1) + root + PEN[idx % 5] + 12 * Math.floor(idx / 5);
  for (const b of bars) {
    const g0 = b.g, kind = b.kind, root = semi(b.deg, b.shift), r = (o) => 12 * (o + 1) + root;
    const drop = kind === "drop" || kind === "final" || kind === "solo", verse = kind === "verse" || kind === "build";
    const half = sp.drum === "halftime";
    // ドラム
    if (kind === "intro" && b.i >= b.n / 2) { for (const k of [0, 8]) put("kick", g0, k, "x"); for (let k = 0; k < 16; k += 4) put("hihat", g0, k, "x"); }
    if (verse || drop) {
      for (const k of st(kickPat)) put("kick", g0, k, "x"); for (const k of st(snPat)) put("snare", g0, k, "x"); if (D.clap && drop) for (const k of st(D.clap)) put("clap", g0, k, "x");
      for (const [k, c] of [...D.hat].entries()) if (c === "x" && (drop || k % 4 === 0 || k % 4 === 2)) put("hihat", g0, k, "x");
      if (drop) for (const k of st(D.open)) put("openhat", g0, k, "x");
    }
    if (kind === "break" && sp.epic) { if (b.i % 4 === 0) put("tom", g0, 0, "x"); if (b.i >= b.n - 2) for (let k = 0; k < 16; k += 2) put("snare", g0, k, "x"); }
    if (kind === "break" && !sp.epic && b.i >= b.n - 2) for (let k = 0; k < 16; k += 2) put("snare", g0, k, "x");
    if (kind === "build") { if (b.i >= b.n - 4) for (let k = 0; k < 16; k += b.i >= b.n - 2 ? 1 : 2) put("snare", g0, k, "x"); }
    if (kind === "outro" && b.i < b.n / 2) { for (const k of [0, 8]) put("kick", g0, k, "x"); for (const k of [4, 12]) put("snare", g0, k, "x"); }
    if (drop && b.i === 0) put("crash", g0, 0, "x"); if (kind === "solo" && b.i === 8) put("crash", g0, 0, "x");
    if ((kind === "verse" || drop) && b.i % 8 === 7) { for (let k = 8; k < 16; k++) { L.snare[g0 * 16 + k] = null; put(k >= 12 ? "tom" : "snare", g0, k, "x"); } }
    if ((kind === "build" || kind === "break") && b.i === 0) { L.riser[g0 * 16] = { n: nm(r(5)), len: b.n * 16 }; }
    // ベース: アシッド（16分の動き）。ドロップと展開で
    if (verse || drop) { const cell = half ? "x.......x.......": pick([riffCell, riffCell2]); st(cell).forEach((k, n, all) => { const nx = all[n + 1] ?? 16; put("bass", g0, k, r(1) + (n % 5 === 3 ? 12 : 0) + (n % 7 === 5 ? 3 : 0), Math.max(1, Math.min(3, nx - k)), "bass"); }); }
    if (drop) for (const k of [2, 6, 10, 14]) put("sub", g0, k, r(1), 2, "sub808");
    // リズムギター（左: リフ、右: 開放のパワーコードと16分）
    const cellUse = (b.i % 2 === 0 ? riffCell : riffCell2);
    if (verse || drop) { st(cellUse).forEach((k, n, all) => { const nx = all[n + 1] ?? 16; const iv = riffIv[(b.i % 2) * 16 + n]; put("gL", g0, k, r(2) + (kind === "verse" ? 0 : iv), Math.max(1, Math.min(2, nx - k)), "distGuitar"); }); }
    if (drop && kind !== "solo") { put("gR", g0, 0, r(3), 8, "distGuitar"); put("gR", g0, 8, r(3) + (b.i % 4 === 3 ? 3 : 0), 8, "distGuitar"); }
    if (kind === "solo") { put("gR", g0, 0, r(3), 16, "distGuitar"); }
    // シンセ: コードの刻み・アルペジオ・パッド
    const tri = [0, third(b), 7];
    if (drop) for (const k of [0, 3, 6, 10, 12]) put("stab", g0, k, r(4) + tri[(k / 3 | 0) % 3], 2, "lead");
    if (kind === "intro" || kind === "verse" || kind === "build" || drop) for (let k = 0; k < 16; k++) if (kind === "drop" || kind === "final" || (kind === "intro") || (kind === "build")) put("arp", g0, k, r(5) + [0, third(b), 7, 12, 7, third(b)][k % 6], 1, "lead");
    if (["intro", "break", "outro", "build", "final"].includes(kind) || kind === "verse") put("pad", g0, 0, r(4) + 7, 16, "pad");
    if (kind === "break" || kind === "outro") for (let k = 0; k < 16; k += 2) put("piano", g0, k, r(3) + [0, 7, 12, third(b) + 12, 12, 7][(k / 2) % 6], 2, "piano");
    if (kind === "break" || kind === "outro") for (const k of [0, 8]) put("bell", g0, k, r(6) + (k ? 7 : 0), 8, "bell");
    // 壮大（弦・ブラス・合唱）
    if (sp.epic) { if (["break", "final", "drop", "outro", "intro"].includes(kind)) put("strings", g0, 0, r(4) + (kind === "break" ? 7 : third(b)), 16, "strings"); if (kind === "final" || (kind === "drop" && b.i >= 8)) { put("brass", g0, 0, r(3) + 7, 8, "brass"); put("brass", g0, 8, r(3) + third(b), 8, "brass"); } if (kind === "break" || kind === "final") put("choir", g0, 0, r(4) + 7, 16, "choir"); }
    if ((drop || kind === "break") && b.i % 2 === 1 && !sp.epic) for (const k of [3, 6, 11]) put("chop", g0, k, r(4) + 7, 2, "choir");
    // フック（ドロップ・ファイナルのギター旋律）: 2小節ごとに A A' A B
    if ((kind === "drop" || kind === "final") && b.i % 2 === 0) { const ph = (b.i / 2 | 0) % 4, notes = HOOK[ph]; notes.forEach((nn, n, all) => { const nx = all[n + 1]?.k ?? 32; put("hook", g0, nn.k, penMidi(nn.idx, root, 4), Math.max(1, Math.min(8, nx - nn.k)), "leadGuitar"); }); }
  }
  // ---- ポリリズム（ドロップ2・ソロ手前の区間に重ねる）: 周期の違うパターンを小節の頭とずらす。区間の最後の小節でそろえる
  if (sp.poly) {
    const drop2 = bars.filter((b) => b.kind === "drop"); const seg = drop2[drop2.length - 1] ? bars.filter((b) => b.kind === "drop" && b.g >= drop2[drop2.length - 1].g - drop2[drop2.length - 1].i) : [];
    if (seg.length) { const a = seg[0].g, z = seg[seg.length - 1].g;
      for (let i = a * 16; i < (z) * 16; i++) { const j = i - a * 16, bar = seg[Math.min(seg.length - 1, Math.floor(j / 16))]; const rr = 12 * 4 + sp.key + shiftOf(bar);
        for (const p of ["kick", "snare", "hihat", "bass", "arp", "gL", "gR", "stab"]) L[p][i] = null;
        if (j % 5 === 0) putRaw("kick", i, "x", 1); if (j % 7 === 3) putRaw("snare", i, "x", 1); if (j % 3 === 0) putRaw("hihat", i, "x", 1);
        if (j % 9 === 0) putRaw("bass", i, nm(clampTo("bass", rr - 24)), 2); if (j % 11 === 0) putRaw("arp", i, nm(clampTo("lead", rr + 12 + (j % 33 === 0 ? 7 : 0))), 1); if (j % 13 === 2) putRaw("stab", i, nm(clampTo("lead", rr + 19)), 1); if (j % 7 === 0) putRaw("gL", i, nm(clampTo("distGuitar", rr - 12 + [0, 3, 5, 7, 10][(j / 7 | 0) % 5])), 1);
      }
      for (let k = 0; k < 16; k++) { const i = z * 16 + k; for (const p of ["kick", "snare", "hihat", "bass", "arp", "gL", "gR", "stab"]) L[p][i] = null; if (k % 4 === 0) putRaw("kick", i, "x", 1); if (k === 4 || k === 12) putRaw("snare", i, "x", 1); if (k >= 8) putRaw("tom", i, "x", 1); }
      function shiftOf() { return 0; }
    }
  }
  // ---- ソロ（歌うチョーキング／タッピング）
  const solos = bars.filter((b) => b.kind === "solo");
  if (solos.length) {
    const a = solos[0].g; const bar = (i) => bars[a + i]; const n = solos.length;
    const scale = (root, oct, idx) => 12 * (oct + 1) + root + [0, 2, 3, 5, 7, 8, 10][((idx % 7) + 7) % 7] + 12 * Math.floor(idx / 7);
    const tapBar = (i, style) => { const b = bar(i), root = semi(b.deg, b.shift), t = third(b), tones = style === 0 ? [0, t, 7, 12, 7, t, 0, t] : style === 1 ? [0, 7, 12, t + 12, 12, 7, t, 7] : [12, 7, t, 0, t, 7, 12, 19]; for (let k = 0; k < 16; k++) putRaw("solo", (a + i) * 16 + k, nm(clampTo("leadGuitar", 12 * 6 + root + tones[k % 8])) + "@", 1); };
    const singBar = (i, kindIdx) => { const b = bar(i), root = semi(b.deg, b.shift); const chordTones = [0, third(b), 7, 12]; const pos = (k, iv, len, bend) => { putRaw("solo", (a + i) * 16 + k, nm(clampTo("leadGuitar", 12 * 5 + root + iv)) + (bend ? "+" + bend : ""), len); };
      const patterns = [
        () => { pos(0, chordTones[1], 2); pos(2, chordTones[2], 2); pos(4, chordTones[2] + 12 - 12 + 0, 4, 0); pos(8, chordTones[2] - 2, 8, 2); },       // 長い音を途中から2半音チョーキング（=5度）
        () => { pos(0, 12, 4); pos(4, 10, 2); pos(6, 7, 2); pos(8, 5, 4); pos(12, chordTones[1] - 1, 4, 1); },                                            // 下がって最後に半音チョーキング（=短3度）
        () => { for (let k = 0; k < 8; k++) pos(k * 2, [0, 3, 5, 7, 10, 7, 5, 3][k] + 12, 2); pos(0, 12, 2); },
        () => { pos(0, 15, 8, 0); pos(8, 12 - 2, 8, 2); },                                                                                                  // 15から入り、10→12へチョーキング
      ];
      patterns[kindIdx % patterns.length]();
    };
    for (let i = 0; i < n; i++) {
      const tapPart = (sp.solo === "tap") || (sp.solo === "both" && i >= n / 2);
      if (tapPart && i % 8 < 7) tapBar(i, (i / 2 | 0) % 3);
      else if (tapPart) { for (let k = 0; k < 16; k++) putRaw("solo", (a + i) * 16 + k, nm(clampTo("leadGuitar", 12 * 6 + semi(bar(i).deg, bar(i).shift) + [12, 10, 8, 7, 5, 3, 2, 0, -2, -4, -5, -7, -9, -11, -12, -12][k])) + "@", 1); }
      else singBar(i, (i + (sp.seed % 3)) % 4);
    }
    for (let i = 0; i < n * 16; i++) { L.hook[a * 16 + i] = null; }
  }
  // 最終小節: 根音の長い和音で終わる
  const lastBar = BARS - 1, lb = bars[lastBar];
  for (let k = 0; k < 16; k++) for (const p of ["kick", "snare", "clap", "hihat", "openhat", "tom", "bass", "sub", "gL", "gR", "stab", "arp", "hook", "solo", "chop", "riser"]) L[p][lastBar * 16 + k] = null;
  put("crash", lastBar, 0, "x"); put("kick", lastBar, 0, "x"); put("bass", lastBar, 0, 12 * 2 + sp.key, 16, "bass"); put("pad", lastBar, 0, 12 * 4 + sp.key + 7, 16, "pad"); if (sp.epic) put("strings", lastBar, 0, 12 * 4 + sp.key + 3, 16, "strings");
  void lb;
  // ---- 出力
  const rest = (out, beats) => { while (beats > 16) { out.push("R:16"); beats -= 16; } if (beats > 0) out.push(`R:${beats}`); };
  const toNotes = (arr) => { const out = []; let i = 0; while (i < S) { const e = arr[i]; if (!e) { let j = i; while (j < S && !arr[j]) j++; rest(out, (j - i) * 0.25); i = j; continue; } let nx = i + 1; while (nx < S && !arr[nx]) nx++; const gap = nx - i, len = Math.min(e.len, gap); out.push(`${e.n}:${len * 0.25}`); if (gap > len) rest(out, (gap - len) * 0.25); i = nx; } return out.join(" "); };
  const chordName = (b) => { const pc = (sp.key + b.shift + MIN[(b.deg - 1) % 7]) % 12; return NAMES[pc] + (third(b) === 3 ? "m" : ""); };
  const parts = [
    ["kick", "キック", "kick", 0.33, 0], ["snare", "スネア", "snare", 0.25, 0.05], ["clap", "クラップ", "clap", 0.18, 0.1], ["hihat", "ハイハット", "hihat", 0.11, 0.25], ["openhat", "オープンハット", "openhat", 0.13, -0.25],
    ["crash", "クラッシュ", "crash", 0.18, -0.2], ["tom", "タム（フィル・ポリリズム）", "tom", 0.22, -0.15], ["riser", "ライザー", "riser", 0.2, 0],
    ["bass", "アシッドなベース", "bass", 0.25, 0, "overdrive"], ["sub808", "サブベース", "sub", 0.28, 0],
    ["distGuitar", "リズムギター左（リフ）", "gL", 0.17, -0.55, "auto"], ["distGuitar", "リズムギター右（パワーコード）", "gR", 0.12, 0.55, "auto"],
    ["lead", "シンセのコード刻み", "stab", 0.15, 0.2], ["lead", "電子のアルペジオ", "arp", 0.1, -0.3], ["pad", "パッド", "pad", 0.12, 0], ["piano", "ピアノ", "piano", 0.16, 0.25], ["bell", "きらめき", "bell", 0.12, 0.4],
    ...(sp.epic ? [["strings", "ストリングス", "strings", 0.13, 0.3], ["brass", "ブラス", "brass", 0.16, -0.3], ["choir", "合唱", "choir", 0.13, -0.2]] : [["choir", "ボーカルチョップ風", "chop", 0.14, 0.35]]),
    ["leadGuitar", "リードギター（フック）", "hook", 0.25, 0.05, "prs"], ...(solos.length ? [["leadGuitar", sp.solo === "melodic" ? "ギターソロ（チョーキング）" : sp.solo === "tap" ? "ギターソロ（タッピング）" : "ギターソロ（チョーキング→タッピング）", "solo", 0.27, 0.05, "prs"]] : []),
  ].filter(([, , key]) => L[key].some(Boolean));
  const song = {
    title: sp.title, description: `【仮】ダンス×ロックのハイブリッド（♩${sp.bpm}・${BARS}小節）。${sp.desc}`, bpm: sp.bpm, beats: 4, chords: bars.map(chordName).join(" "), barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "rock", tone: "rock", pump: "all", synth: true, drumKit: sp.drum === "fourfloor" ? 24 : 16,
    fx: { tape: 0.2, chorus: 0.12, delay: { beats: 0.75, feedback: 0.28, mix: 0.14 } },
    parts: parts.map(([instrument, role, key, volume, pan, amp]) => ({ instrument, role, volume, pan, amp: amp ?? "auto", notes: toNotes(L[key]) })),
  };
  fs.writeFileSync(new URL(`../${sp.id}.json`, import.meta.url), JSON.stringify(song, null, 2) + "\n", "utf8");
  return { id: sp.id, title: sp.title, bars: BARS, sec: Math.round((BARS * 4 * 60) / sp.bpm) };
}
for (const sp of SONGS) console.log(JSON.stringify(build(sp)));
