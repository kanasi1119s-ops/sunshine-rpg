// DJ・クラブ調「夜明けのフロア」（約2分半）を書き出す。♩128・80小節。新しい楽器（clap・openhat・scratch・riser）とサイドチェーン（pump: "all"）の見本。
// 構成: イントロ（DJツール風のビート＋スクラッチ）→ ビルド（ライザー＋スネアロール）→ ドロップA → ブレイクダウン → ビルド → ドロップB → アウトロ（ミックスアウト）
// 使い方: node assets-src/ai-songs/_gen/dj-floor.mjs → assets-src/ai-songs/dj-floor.json
import fs from "node:fs";
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const nm = (m) => NAMES[m % 12] + (Math.floor(m / 12) - 1);
const SEC = [["intro", 8], ["build", 8], ["dropA", 16], ["break", 8], ["build", 8], ["dropB", 24], ["outro", 8]];
const CH = [["F", 5, true], ["C#", 1, false], ["G#", 8, false], ["D#", 3, false]];   // Fm | Db | Ab | Eb（根音のピッチクラス）
const bars = []; let g = 0;
for (const [sec, n] of SEC) for (let i = 0; i < n; i++) bars.push({ sec, i, n, g: g++, c: CH[g % 4 === 0 ? 0 : (g - 1) % 4] });
bars.forEach((b, k) => { b.c = CH[k % 4]; });
const BARS = bars.length, S = BARS * 16;
const mk = () => Array(S).fill(null);
const L = Object.fromEntries(["kick", "clap", "openhat", "hihat", "snare", "crash", "scratch", "riser", "sub808", "lead", "keys", "pad", "choir", "bell"].map((k) => [k, mk()]));
const put = (p, bar, k, n, len = 1) => { const i = bar * 16 + k; if (i < S) L[p][i] = { n, len }; };
const root = (b, o) => 12 * (o + 1) + b.c[1];
const third = (b) => (b.c[2] ? 3 : 4);
for (const b of bars) {
  const s = b.sec, g = b.g, last = b.i === b.n - 1;
  const drop = s === "dropA" || s === "dropB", bld = s === "build";
  // ドラム
  if (s === "intro" || s === "outro") { for (let k = 0; k < 16; k += 4) put("kick", g, k, "x"); for (let k = 2; k < 16; k += 4) put("openhat", g, k, "x"); if (b.i >= 4 || s === "outro") for (const k of [4, 12]) put("clap", g, k, "x"); }
  if (drop) { for (let k = 0; k < 16; k += 4) put("kick", g, k, "x"); for (const k of [4, 12]) put("clap", g, k, "x"); for (let k = 2; k < 16; k += 4) put("openhat", g, k, "x"); for (let k = 0; k < 16; k += 2) if (k % 4 !== 2) put("hihat", g, k + 1 > 15 ? k : k, "x"); }
  if (bld) { for (let k = 0; k < 16; k += 4) put("kick", g, k, "x"); if (b.i >= 4) for (let k = 0; k < 16; k += 2) put("snare", g, k, "x"); if (b.i >= 6) for (let k = 0; k < 16; k++) put("snare", g, k, "x"); if (b.i < 4) for (const k of [4, 12]) put("clap", g, k, "x"); }
  if (s === "break") { if (b.i >= 6) for (let k = 0; k < 16; k += 2) put("snare", g, k, "x"); if (b.i === 7) for (let k = 8; k < 16; k++) put("snare", g, k, "x"); }
  if ((drop && b.i % 8 === 0) || (s === "intro" && b.i === 0)) put("crash", g, 0, "x");
  // スクラッチ: イントロの合いの手、ドロップ前後のつなぎ
  if (s === "intro" && (b.i === 3 || b.i === 7)) for (const k of [10, 12, 14]) put("scratch", g, k, "x");
  if (s === "break" && b.i === 7) for (const k of [0, 2, 4, 6]) put("scratch", g, k, "x");
  if (s === "outro" && b.i % 2 === 1) for (const k of [12, 14]) put("scratch", g, k, "x");
  if (s === "dropB" && b.i === 23) for (const k of [8, 10, 12, 14]) put("scratch", g, k, "x");
  // ライザー: ビルドの全長（8小節=32拍）を1音で
  if (bld && b.i === 0) L.riser[g * 16] = { n: "C5", len: 128 };
  // ベース（オフビートのロールするサブ）
  if (drop) for (const k of [2, 3, 6, 7, 10, 11, 14, 15]) put("sub808", g, k, nm(root(b, 1)), 1);
  if (s === "intro" && b.i >= 4) for (const k of [2, 6, 10, 14]) put("sub808", g, k, nm(root(b, 1)), 1);
  if (s === "outro") for (const k of [2, 6, 10, 14]) put("sub808", g, k, nm(root(b, 1)), 1);
  // 和音・シンセ
  if (drop || s === "break" || bld || s === "outro") put("pad", g, 0, nm(root(b, 3) + 7), 16);
  if (drop || (bld && b.i >= 4)) { const t = [0, third(b), 7]; for (const k of [0, 3, 6, 10, 12]) put("keys", g, k, nm(root(b, 4) + t[(k % 3)]), 2); }
  // リード（アルペジオ・16分）
  if (drop) { const t = [0, third(b), 7, 12, 7, third(b)]; for (let k = 0; k < 16; k++) if (!(b.sec === "dropA" && b.i < 8)) put("lead", g, k, nm(root(b, 4) + t[k % 6] + (b.i % 8 >= 4 ? 12 : 0)), 1); }
  if (s === "dropB" && b.i >= 8) { const m = [12, 7, 3 + 4 - (b.c[2] ? 0 : 1), 7, 12, 15]; for (const k of [0, 4, 8, 12]) put("bell", g, k, nm(root(b, 5) + m[(k / 4) % 6]), 4); }
  // ボーカルチョップ風の合唱（休符をはさむ短い音）
  if (drop && b.i % 2 === 1) for (const k of [3, 6, 11]) put("choir", g, k, nm(root(b, 4) + 7), 2);
  if (s === "break") put("choir", g, 0, nm(root(b, 4) + third(b)), 16);
  if (s === "break" && b.i >= 2) for (const k of [0, 8]) put("bell", g, k, nm(root(b, 5) + [0, 7][k / 8]), 8);
}
// ---- 出力
const rest = (out, beats) => { while (beats > 16) { out.push("R:16"); beats -= 16; } if (beats > 0) out.push(`R:${beats}`); };
const toNotes = (arr) => { const out = []; let i = 0; while (i < S) { const e = arr[i]; if (!e) { let j = i; while (j < S && !arr[j]) j++; rest(out, (j - i) * 0.25); i = j; continue; } let nx = i + 1; while (nx < S && !arr[nx]) nx++; const gap = nx - i, len = Math.min(e.len, gap); out.push(`${e.n}:${len * 0.25}`); if (gap > len) rest(out, (gap - len) * 0.25); i = nx; } return out.join(" "); };
const chords = bars.map((b) => NAMES[b.c[1] % 12] + (b.c[2] ? "m" : "")).join(" ");
const parts = [
  ["kick", "キック（4つ打ち）", "kick", 0.34, 0], ["clap", "クラップ（2・4拍）", "clap", 0.24, 0.1], ["openhat", "オープンハット（裏拍）", "openhat", 0.15, 0.3], ["hihat", "ハイハット（16分）", "hihat", 0.1, -0.25],
  ["snare", "スネアロール（ビルド）", "snare", 0.2, 0], ["crash", "クラッシュ", "crash", 0.18, -0.2], ["scratch", "スクラッチ（合いの手・つなぎ）", "scratch", 0.22, -0.35], ["riser", "ライザー（ビルド）", "riser", 0.2, 0],
  ["sub808", "サブベース（オフビート）", "sub808", 0.3, 0], ["lead", "シンセリード（16分アルペジオ）", "lead", 0.16, 0.2], ["keys", "コードスタブ", "keys", 0.16, -0.2], ["pad", "パッド", "pad", 0.12, 0],
  ["choir", "ボーカルチョップ風の合唱", "choir", 0.16, 0.35], ["bell", "きらめき", "bell", 0.12, -0.4],
];
const song = {
  title: "夜明けのフロア", description: "【仮】DJ・クラブ調（約2分半・♩128・Fマイナー）。DJツール風のビートとスクラッチで入り、ライザーとスネアロールで盛り上げてドロップ。サイドチェーン（キックに合わせた音量の凹み）、オフビートのサブベース、16分のシンセアルペジオ、ブレイクダウン、2度目のドロップ、スクラッチでつなぐミックスアウト。新しい楽器（clap・openhat・scratch・riser）の見本。",
  bpm: 128, beats: 4, chords, barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "pop", tone: "prs", pump: "all", synth: true, drumKit: 24,
  parts: parts.map(([instrument, role, key, volume, pan]) => ({ instrument, role, volume, pan, amp: "auto", notes: toNotes(L[key]) })),
};
fs.writeFileSync(new URL("../dj-floor.json", import.meta.url), JSON.stringify(song, null, 2) + "\n", "utf8");
console.log("小節", BARS, "秒", (BARS * 4 / 128 * 60).toFixed(1));
