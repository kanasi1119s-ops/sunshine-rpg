// 「緋色の断章」の生成スクリプト。日本のPCゲーム音楽に通じる「疾走するハード系バンド＋弦・鍵盤の劇的な短調」の雰囲気だけを参考にした、完全オリジナル曲。
// 特定の曲のメロディ・コード進行・曲名は使っていない（CLAUDE.md 1-1）。 実行: node assets-src/ai-songs/_gen/scarlet-chapter.mjs
import fs from "fs";
const BPM = 172, BARS_PER = 1;
// [セクション名, コード8個 or 4個]
const S = {
  intro: ["C#m C#m A B"],
  A: ["C#m C#m A B C#m C#m F#m G#7"],
  B: ["A B G#m E A B G#m G#7"],
  chorus: ["A B G#m F#m A B E G#7"],
  solo: ["C#m A F#m G#7 C#m A B G#7"],
  bridge: ["F#m E G#m A F#m E B B"],
  outro: ["C#m A B C#m"],
};
const ORDER = ["intro", "A", "B", "chorus", "solo", "A", "bridge", "chorus", "outro"];
const chords = ORDER.flatMap((k) => S[k][0].split(" "));
const secOfBar = ORDER.flatMap((k) => S[k][0].split(" ").map((_, i) => ({ k, i, n: S[k][0].split(" ").length })));
const lead = {
  intro: "R:16",
  A: "G#5:1 E5:0.5 G#5:0.5 B5:1.5 A5:0.5 G#5:2 F#5:1 E5:1 E5:1 A5:1 C#6:1.5 B5:0.5 D#6:2 B5:1 F#5:1 G#5:1 E5:0.5 G#5:0.5 B5:1 C#6:1 B5:1.5 G#5:0.5 E5:2 F#5:1 A5:1 C#6:1 A5:1 F#5:1 D#5:1 B4:1 G#4:1",
  B: "C#6:1 B5:0.5 A5:0.5 E5:2 D#6:1 C#6:0.5 B5:0.5 F#5:2 B5:1 G#5:1 D#6:2 E6:1.5 B5:0.5 G#5:2 A5:1 C#6:1 E6:2 D#6:1 B5:1 F#5:2 C#6:2 B5:1 C#6:1 B5:1 D#6:1 B5:1 G#5:1",
  chorus: "E6:2 C#6:1 E6:1 D#6:2 B5:1 F#5:1 B5:1.5 D#6:0.5 B5:1 G#5:1 A5:1 C#6:1 E6:2 E6:1 C#6:1 A5:2 F#5:1 B5:1 D#6:1 B5:1 G#5:1 B5:1 E6:2 D#6:1.5 B5:0.5 G#5:1 F#5:1",
  solo: "G#5:0.25 B5:0.25 C#6:0.25 B5:0.25 G#5:0.25 E5:0.25 G#5:0.25 B5:0.25 C#6:1 E6:0.5 D#6:0.5 C#6:0.25 E6:0.25 C#6:0.25 A5:0.25 E5:0.25 A5:0.25 C#6:0.25 A5:0.25 E6:2 A5:0.5 C#6:0.5 F#5:0.5 A5:0.5 C#6:0.5 E6:0.5 C#6:0.5 A5:0.5 B5:0.5 D#6:0.5 F#5:0.5 B5:0.5 D#6:2 E6:0.5 D#6:0.5 C#6:0.5 B5:0.5 G#5:0.5 B5:0.5 C#6:1 A5:0.5 C#6:0.5 E6:0.5 C#6:0.5 A5:0.5 E5:0.5 A5:1 D#6:0.5 B5:0.5 F#5:0.5 B5:0.5 D#6:0.5 F#5:0.5 B5:1 G#5:0.25 B5:0.25 D#6:0.25 B5:0.25 G#5:0.25 F#5:0.25 D#5:0.25 F#5:0.25 G#5:2",
  bridge: "A5:2 C#6:2 B5:2 G#5:2 B5:2 D#6:2 C#6:1 E6:1 C#6:2 A5:2 F#5:2 G#5:2 E5:2 D#6:2 B5:1 F#5:1 B5:2 R:2",
  outro: "G#5:2 E5:2 E6:2 C#6:2 D#6:2 B5:2 C#5:4",
};
const leadTxt = ORDER.map((k) => lead[k]).join(" ");
// コードごとの音（低い根音の高さ）
const ROOT = { "C#m": ["C#3", "C#2"], A: ["A2", "A1"], B: ["B2", "B1"], "G#m": ["G#2", "G#1"], "F#m": ["F#2", "F#1"], E: ["E2", "E1"], G7: null, "G#7": ["G#2", "G#1"] };
const FIFTH = { "C#m": "G#4", A: "E5", B: "F#5", "G#m": "D#5", "F#m": "C#5", E: "B4", "G#7": "D#5" };
const TONES = { "C#m": ["C#4", "E4", "G#4", "C#5"], A: ["A3", "C#4", "E4", "A4"], B: ["B3", "D#4", "F#4", "B4"], "G#m": ["G#3", "B3", "D#4", "G#4"], "F#m": ["F#3", "A3", "C#4", "F#4"], E: ["E3", "G#3", "B3", "E4"], "G#7": ["G#3", "C4", "D#4", "F#4"] };
const APPROACH = { "C#m": "C#2", A: "A1", B: "B1", "G#m": "G#1", "F#m": "F#1", E: "E1", "G#7": "G#1" };
const semi = (n, d) => { const names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]; const m = /^([A-G]#?)(\d)$/.exec(n); const idx = names.indexOf(m[1]) + 12 * (+m[2]) + d; return names[((idx % 12) + 12) % 12] + Math.floor(idx / 12); };
const bass = [], dist = [], strings = [], keys = [];
chords.forEach((c, b) => {
  const nextC = chords[b + 1] ?? c;
  const [hi, lo] = ROOT[c];
  const sec = secOfBar[b];
  if (sec.k === "intro") { bass.push("R:4"); dist.push("R:4"); }
  else {
    // ベース: 8分の連打（1拍目は低いオクターブ）。コードの変わり目の前は半音手前の経過音
    const r = lo, r2 = hi.replace(/\d$/, (d) => String(+d));
    const app = nextC !== c ? semi(APPROACH[nextC], -1) : semi(lo, 7);
    bass.push(`${lo}:0.5 ${lo}:0.5 ${r2}:0.5 ${lo}:0.5 ${lo}:0.5 ${lo}:0.5 ${r2}:0.5 ${app}:0.5`);
    dist.push(`${hi}:0.25 ${hi}:0.25 ${hi}:0.5 ${hi}:0.25 ${hi}:0.25 ${hi}:0.5 ${hi}:0.25 ${hi}:0.25 ${hi}:0.5 ${hi}:0.25 ${hi}:0.25 ${hi}:0.5`);
  }
  strings.push(sec.k === "intro" || sec.k === "solo" ? "R:4" : `${FIFTH[c]}:4`);
  const t = TONES[c]; const pat = [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3];
  keys.push(sec.k === "chorus" || sec.k === "solo" ? "R:4" : pat.map((i) => `${t[i]}:0.25`).join(" "));
});
// ドラム
const kick = [], snare = [], hat = [], crash = [], tom = [];
const tok = (mask) => mask.map((m) => (m ? "x:0.25" : "R:0.25")).join(" ");
chords.forEach((c, b) => {
  const s = secOfBar[b]; const fillBar = s.i % 4 === 3; const lastOfSection = s.i === s.n - 1;
  const heavy = s.k === "chorus" || s.k === "solo" || s.k === "outro" && false;
  let k = Array(16).fill(0), sn = Array(16).fill(0), h = Array(16).fill(0), cr = Array(16).fill(0), tm = Array(16).fill(0);
  if (s.k === "intro") { [0, 8].forEach((i) => (k[i] = 1)); [0, 4, 8, 12].forEach((i) => (h[i] = 1)); }
  else if (s.k === "bridge") { [0, 10].forEach((i) => (k[i] = 1)); sn[8] = 1; for (let i = 0; i < 16; i += 2) h[i] = 1; }
  else if (heavy) { for (let i = 0; i < 16; i += 2) k[i] = 1; [4, 12].forEach((i) => (sn[i] = 1)); for (let i = 0; i < 16; i += 2) h[i] = 1; [6, 14].forEach((i) => (k[i + 1] = 1)); }
  else { [0, 3, 6, 8, 11, 14].forEach((i) => (k[i] = 1)); [4, 12].forEach((i) => (sn[i] = 1)); for (let i = 0; i < 16; i += 2) h[i] = 1; }
  if (s.k === "outro" && s.i >= 2) { k = Array(16).fill(0); k[0] = 1; sn = Array(16).fill(0); h = Array(16).fill(0); h[0] = 1; }
  if (fillBar && s.k !== "intro" && !(s.k === "outro")) { for (let i = 8; i < 16; i++) { sn[i] = i % 2 === 0 ? 1 : 0; tm[i] = i % 2 === 1 ? 1 : 0; k[i] = 0; h[i] = 0; } sn[4] = 1; }
  const prevFill = b > 0 && secOfBar[b - 1].i % 4 === 3 && secOfBar[b - 1].k !== "intro";
  if (s.i === 0 || prevFill) cr[0] = 1;
  kick.push(tok(k)); snare.push(tok(sn)); hat.push(tok(h)); crash.push(tok(cr)); tom.push(tok(tm));
});
const song = {
  title: "緋色の断章",
  description: "嬰ハ短調の疾走するハード系バンド曲（仮）。日本のPCゲーム音楽に通じる「劇的な短調・速いバンド・弦と鍵盤の厚み」の雰囲気だけを参考にした完全オリジナル。鍵盤の16分アルペジオで幕を開け、ディストーションの駆ける刻みに、リードギターが「ソ#・ミ・ソ#・シ」の動機で攻める。サビで高く駆け上がり、16分の速弾きソロ、ブリッジの静けさを経て、最後のサビへ。",
  bpm: BPM, beats: 4, chords: chords.join(" "), barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "rock", tone: "rock",
  parts: [
    { instrument: "leadGuitar", role: "リードギター", volume: 0.27, pan: 0.2, amp: "prs", notes: leadTxt },
    { instrument: "distGuitar", role: "刻みリフ", volume: 0.17, pan: -0.35, amp: "metal", notes: dist.join(" ") },
    { instrument: "bass", role: "ベース", volume: 0.22, pan: 0, amp: "overdrive", notes: bass.join(" ") },
    { instrument: "strings", role: "弦の厚み", volume: 0.12, pan: 0, amp: "auto", notes: strings.join(" ") },
    { instrument: "keys", role: "鍵盤アルペジオ", volume: 0.13, pan: 0.35, amp: "auto", notes: keys.join(" ") },
    { instrument: "kick", role: "キック", volume: 0.3, pan: 0, amp: "auto", notes: kick.join(" ") },
    { instrument: "snare", role: "スネア", volume: 0.26, pan: 0, amp: "auto", notes: snare.join(" ") },
    { instrument: "hihat", role: "ハイハット", volume: 0.11, pan: 0, amp: "auto", notes: hat.join(" ") },
    { instrument: "crash", role: "クラッシュ", volume: 0.17, pan: 0, amp: "auto", notes: crash.join(" ") },
    { instrument: "tom", role: "タム（フィル）", volume: 0.2, pan: 0, amp: "auto", notes: tom.join(" ") },
  ],
};
fs.writeFileSync(new URL("../scarlet-chapter.json", import.meta.url), JSON.stringify(song, null, 1));
console.log("bars", chords.length, "sec", (chords.length * 4 * 60 / BPM).toFixed(1));
