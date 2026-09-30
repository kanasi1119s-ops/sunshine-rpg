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

// ---------- 版ごとの組み立て ----------
const idxOfBar = []; { let n = 0; for (const [ix, k] of ORDER.entries()) for (let j = 0; j < S[k][0].split(" ").length; j++) idxOfBar.push(ix); }
const leadBySec = ORDER.map((k) => lead[k]);                // セクション順のメロディ
/** セクション番号 → その拍数ぶんの休み */
const secBeats = ORDER.map((k) => S[k][0].split(" ").length * 4);
const rest = (ix) => `R:${secBeats[ix]}`;
/** バーごとの配列(bass, dist ...)を、セクション単位で切り出す */
function bySec(arr) { const out = ORDER.map(() => []); arr.forEach((v, b) => out[idxOfBar[b]].push(v)); return out.map((a) => a.join(" ")); }
const bassS = bySec(bass), distS = bySec(dist), strS = bySec(strings), keyS = bySec(keys), kickS = bySec(kick), snS = bySec(snare), hatS = bySec(hat), crS = bySec(crash), tomS = bySec(tom);
const join = (f) => ORDER.map((_, ix) => f(ix)).join(" ");
const P = (instrument, role, volume, pan, amp, notes) => ({ instrument, role, volume, pan, amp, notes });

// 歪みのジャリつき対策（曲ごとの drive・tone）は tools/composer/band-amp.mjs の SONG_TWEAKS にある。

function variantMain() {
  return {
    title: "緋色の断章",
    description: "嬰ハ短調の疾走するハード系バンド曲（仮）。日本のPCゲーム音楽に通じる「劇的な短調・速いバンド・弦と鍵盤の厚み」の雰囲気だけを参考にした完全オリジナル。歪みは浅めに抑え、高音のジャリつきを減らした。鍵盤の16分アルペジオで幕を開け、リードギターが「ソ#・ミ・ソ#・シ」の動機で攻め、サビで高く駆け上がる。16分の速弾きソロ、ブリッジの静けさを経て、最後のサビへ。",
    parts: [
      P("leadGuitar", "リードギター", 0.25, 0.2, "prs", leadTxt),
      P("distGuitar", "刻みリフ", 0.15, -0.35, "metal", dist.join(" ")),
      P("bass", "ベース", 0.22, 0, "overdrive", bass.join(" ")),
      P("strings", "弦の厚み", 0.13, 0, "auto", strings.join(" ")),
      P("keys", "鍵盤アルペジオ", 0.13, 0.35, "auto", keys.join(" ")),
      P("kick", "キック", 0.3, 0, "auto", kick.join(" ")), P("snare", "スネア", 0.26, 0, "auto", snare.join(" ")), P("hihat", "ハイハット", 0.11, 0, "auto", hat.join(" ")),
      P("crash", "クラッシュ", 0.17, 0, "auto", crash.join(" ")), P("tom", "タム（フィル）", 0.2, 0, "auto", tom.join(" ")),
    ],
  };
}

/** クリーントーン版: 同じ旋律・コードを、ギターはすべてクリーンで。刻みは、歪ませずに爪弾く8分のアルペジオにする。ドラムは軽く。 */
function variantClean() {
  const pick = [0, 1, 2, 1, 3, 2, 1, 2]; // 8分のアルペジオ（1小節8音）
  const arp = chords.map((c, b) => (secOfBar[b].k === "intro" ? "R:4" : pick.map((i) => `${TONES[c][i]}:0.5`).join(" "))).join(" ");
  const echo = chords.map((c, b) => (["chorus", "solo"].includes(secOfBar[b].k) ? `${TONES[c][3].replace(/(\d)$/, (d) => String(+d + 1))}:2 ${TONES[c][2].replace(/(\d)$/, (d) => String(+d + 1))}:2` : "R:4")).join(" ");
  // ドラム: 二連打をやめ、8分のキックと控えめなフィルにする
  const kk = [], sn = [], hh = [], cc = [], tt = [];
  chords.forEach((c, b) => { const sc = secOfBar[b]; const fill = sc.i % 4 === 3 && sc.k !== "intro" && sc.k !== "outro"; const k = Array(16).fill(0), n = Array(16).fill(0), h = Array(16).fill(0), r = Array(16).fill(0), t = Array(16).fill(0);
    if (sc.k !== "intro") { [0, 8].forEach((i) => (k[i] = 1)); if (["chorus", "solo"].includes(sc.k)) [6, 10].forEach((i) => (k[i] = 1)); [4, 12].forEach((i) => (n[i] = 1)); for (let i = 0; i < 16; i += 2) h[i] = 1; } else { [0, 8].forEach((i) => (k[i] = 1)); [0, 4, 8, 12].forEach((i) => (h[i] = 1)); }
    if (sc.k === "outro" && sc.i >= 2) { k.fill(0); k[0] = 1; n.fill(0); h.fill(0); h[0] = 1; }
    if (fill) { [12, 13, 14, 15].forEach((i) => { n[i] = 1; }); t[8] = 1; t[10] = 1; }
    if (sc.i === 0) r[0] = 1; const tk = (m) => m.map((v) => (v ? "x:0.25" : "R:0.25")).join(" "); kk.push(tk(k)); sn.push(tk(n)); hh.push(tk(h)); cc.push(tk(r)); tt.push(tk(t)); });
  return {
    title: "緋色の断章（クリーン版）",
    description: "「緋色の断章」と同じ旋律・コード・構成を、ギターをすべてクリーントーンで鳴らした版（仮）。刻みは歪ませず、爪弾く8分のアルペジオにして、ジャリつきをなくした。リードはクリーンで歌わせ、サビに高いエコーギターの長い音が重なる。ドラムは二連打をやめ、軽く。",
    parts: [
      P("leadGuitar", "リード（クリーン）", 0.27, 0.2, "clean", leadTxt),
      P("guitar", "爪弾くアルペジオ", 0.17, -0.35, "clean", arp),
      P("echoGuitar", "エコーの長い音", 0.12, 0.45, "clean", echo),
      P("bass", "ベース（指弾き）", 0.22, 0, "clean", bass.join(" ")),
      P("strings", "弦の厚み", 0.14, 0, "auto", strings.join(" ")),
      P("keys", "鍵盤アルペジオ", 0.13, 0.35, "auto", keys.join(" ")),
      P("kick", "キック", 0.26, 0, "auto", kk.join(" ")), P("snare", "スネア", 0.22, 0, "auto", sn.join(" ")), P("hihat", "ハイハット", 0.1, 0, "auto", hh.join(" ")),
      P("crash", "クラッシュ", 0.14, 0, "auto", cc.join(" ")), P("tom", "タム", 0.18, 0, "auto", tt.join(" ")),
    ],
  };
}

/** 空間版: 前半は歪んだバンドで駆け、ソロから歪みが薄れて、エコーの壁・パッド・鐘の空間へ溶けていく。 */
function variantSpace() {
  // セクション番号: 0 導入 1 A 2 B 3 サビ 4 ソロ 5 A' 6 ブリッジ 7 サビ 8 終結
  const distOn = new Set([0, 1, 2, 3, 4]);           // 歪みのバンドは、ソロまで
  const drumsOn = new Set([0, 1, 2, 3, 4]);          // ドラムも、ソロまで（そのあと静かな鼓動だけ）
  const leadOn = new Set([1, 2, 3, 4]);              // 歪みのリード
  const echoLead = new Set([4, 5, 7]);               // エコーのリード（ソロから、空間へ）
  const distNotes = join((ix) => (distOn.has(ix) ? distS[ix] : rest(ix)));
  const leadNotes = join((ix) => (leadOn.has(ix) ? leadBySec[ix] : rest(ix)));
  const echoNotes = join((ix) => (echoLead.has(ix) ? leadBySec[ix === 4 ? 3 : ix] : rest(ix)));
  // 空間の層: パッド（コードの5度の長い音、4小節ぶんずつ）と鐘（コードの高い音を1小節に1つ）
  const padS = ORDER.map((k, ix) => bySec(chords.map((c) => `${TONES[c][1].replace(/(\d)$/, (d) => String(+d - 1))}:4`))[ix]);
  const padNotes = join((ix) => (ix >= 3 ? padS[ix] : rest(ix)));
  const bellS = bySec(chords.map((c) => `${TONES[c][3].replace(/(\d)$/, (d) => String(+d + 1))}:2 R:2`));
  const bellNotes = join((ix) => (ix >= 4 ? bellS[ix] : rest(ix)));
  const bassNotes = join((ix) => (ix <= 4 ? bassS[ix] : ix === 8 ? rest(ix) : bySec(chords.map((c) => `${ROOT[c][1]}:4`))[ix]));
  const strNotes = join((ix) => (ix === 0 ? rest(ix) : strS[ix] || rest(ix)));
  const keyNotes = join((ix) => (ix <= 2 || ix >= 5 ? keyS[ix] : rest(ix)));
  const heart = (ix) => bySec(chords.map(() => "x:0.25 R:3.75"))[ix];  // 静かな鼓動（キック）
  const kickNotes = join((ix) => (drumsOn.has(ix) ? kickS[ix] : ix === 8 ? rest(ix) : heart(ix)));
  const sn = join((ix) => (drumsOn.has(ix) ? snS[ix] : rest(ix))), ht = join((ix) => (drumsOn.has(ix) ? hatS[ix] : rest(ix))), cr = join((ix) => (drumsOn.has(ix) ? crS[ix] : rest(ix))), tm = join((ix) => (drumsOn.has(ix) ? tomS[ix] : rest(ix)));
  return {
    title: "緋色の断章（空間版）",
    description: "「緋色の断章」と同じ旋律・コードを使い、歪んだバンドで駆けたあと、ソロから歪みが薄れ、エコーの壁・パッド・鐘の空間へ溶けていく版（仮）。最後はドラムも消え、遠い鐘と長く残るエコーギターだけが残る。",
    parts: [
      P("leadGuitar", "リード（歪み）", 0.24, 0.2, "prs", leadNotes),
      P("distGuitar", "刻みリフ", 0.14, -0.35, "metal", distNotes),
      P("echoGuitar", "エコーのリード（空間）", 0.22, 0.3, "shoegaze", echoNotes),
      P("bass", "ベース", 0.22, 0, "overdrive", bassNotes),
      P("strings", "弦の厚み", 0.14, 0, "auto", strNotes),
      P("keys", "鍵盤アルペジオ", 0.12, 0.35, "auto", keyNotes),
      P("pad", "パッド（空間）", 0.16, 0, "auto", padNotes),
      P("bell", "鐘（遠い光）", 0.13, -0.3, "auto", bellNotes),
      P("kick", "キック／鼓動", 0.28, 0, "auto", kickNotes), P("snare", "スネア", 0.24, 0, "auto", sn), P("hihat", "ハイハット", 0.1, 0, "auto", ht),
      P("crash", "クラッシュ", 0.16, 0, "auto", cr), P("tom", "タム", 0.18, 0, "auto", tm),
    ],
  };
}

const common = { bpm: BPM, beats: 4, chords: chords.join(" "), barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "rock", tone: "rock" };
const out = { "scarlet-chapter": variantMain(), "scarlet-chapter-clean": variantClean(), "scarlet-chapter-space": variantSpace() };
for (const [id, v] of Object.entries(out)) fs.writeFileSync(new URL(`../${id}.json`, import.meta.url), JSON.stringify({ title: v.title, description: v.description, ...common, parts: v.parts }, null, 1));
console.log("bars", chords.length, "sec", (chords.length * 4 * 60 / BPM).toFixed(1), Object.keys(out).join(" "));
