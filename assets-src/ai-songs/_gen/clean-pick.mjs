// 「クリーン連打版」: ボス系の速い曲の、ギターの刻みを「クリーントーンの16分の連打」で作り直した別バージョン（既存の曲は変えない）。
// 旋律（リード・ハモリ）・ベース・鍵盤・弦・ドラムは元の曲のまま。歪みの刻み・パワーコードを外し、次の3パートに置きかえる。
//   1. 連打刻み（クリーン）: 1拍を4つの16分に分け、拍ごとの「型」を小節・8小節のまとまりごとに切りかえる（Aメロ風→展開→サビ風）
//   2. アクセント（クリーン・右）: 連打のうち、1オクターブ上の強拍だけを右に重ねて、リズムの輪郭を立てる
//   3. 持続音（クリーン・エコー）: サビの区間に、コードの5度の長い音を薄く重ねる
// 実行: node assets-src/ai-songs/_gen/clean-pick.mjs
import fs from "fs";
const IDS = "boss-touri boss-mugikano boss-garasuko boss-tetsu boss-sanone boss-kiri boss-shimo boss-ukishima boss-toushin elite poly-1 prog-1 boss-final secret-boss-2 eight-gods fate".split(" ");
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"], FLAT = { Db: "C#", Eb: "D#", Gb: "F#", Ab: "G#", Bb: "A#" };
const fromMidi = (v) => NAMES[((v % 12) + 12) % 12] + (Math.floor(v / 12) - 1);
function chordInfo(c) { const m = /^([A-G][#b]?)(.*)$/.exec(c); const pc = NAMES.indexOf(FLAT[m[1]] ?? m[1]); const q = m[2];
  let root = 36 + pc; while (root < 40) root += 12; while (root > 51) root -= 12;               // 低い根音: E2〜D#3（ギターの音域 E2〜E5 に収める）
  const third = /dim/.test(q) || (/^m/.test(q) && !/^maj/.test(q)) ? 3 : /sus2/.test(q) ? 2 : /sus4|sus/.test(q) ? 5 : 4;
  const fifth = /dim/.test(q) ? 6 : /aug/.test(q) ? 8 : 7; return { root, third, fifth }; }
// 拍ごとの型（4つの16分。数字は根音からの半音数、null は休み。T=3度, F=5度）
const cell = (i) => ({
  A: [0, 0, 12, 0],        // 根音・根音・オクターブ(強)・根音
  B: [0, "F", 12, "F"],    // 根音・5度・オクターブ・5度（アルペジオ風）
  C: [0, 0, "F", 0],       // 5度でアクセント
  D: [0, null, 0, 0],      // 軽い（導入・終結）
  E: [0, "T", "F", 12],    // 上がるフィル
  G: [12, 0, 12, 0],       // 強く（サビ）
  H: [12, "F", "T", 0],    // 下がるフィル
  Z: [0, null, null, null],
}[i]);
function barCells(b, N, beats) {
  const intro = Math.min(4, Math.round(N * 0.05 / 1) || 4), outro = N - 4;
  let base;
  if (b < intro) base = ["D", "D", "D", "D"];
  else if (b >= N - 1) base = ["Z", "Z", "Z", "Z"];
  else if (b >= outro) base = ["D", "D", "D", "E"];
  else { const k = Math.floor((b - intro) / 8) % 4, j = (b - intro) % 8;
    base = [["A", "A", "A", "A"], ["A", "A", "C", "A"], ["B", "B", "B", "B"], ["G", "A", "G", "A"]][k];
    if (j === 7) base = { 0: ["A", "A", "A", "E"], 1: ["A", "A", "E", "H"], 2: ["B", "B", "E", "E"], 3: ["G", "G", "E", "H"] }[k];
    else if (k === 3 && j % 4 === 3) base = ["G", "A", "G", "E"]; }
  return Array.from({ length: beats }, (_, i) => base[i % 4]);
}
const parse = (s) => s.trim().split(/\s+/).filter(Boolean).map((t) => { const [n, d] = t.split(":"); return { n, d: +d }; });
const fmt = (a) => a.map((t) => `${t.n}:${+t.d.toFixed(4)}`).join(" ");
const merge = (a) => { const o = []; for (const t of a) { const l = o[o.length - 1]; if (l && l.n === "R" && t.n === "R" && l.d + t.d <= 16) l.d += t.d; else o.push({ ...t }); } return o; };
for (const id of IDS) {
  const p = new URL(`../${id}.json`, import.meta.url); if (!fs.existsSync(p)) { console.log("なし", id); continue; }
  const d = JSON.parse(fs.readFileSync(p, "utf8"));
  const chords = d.chords.split(/\s+/).filter(Boolean), N = chords.length * d.barsPerChord * d.repeats, bb = d.beats;
  const pick = [], acc = [], sus = [];
  let k3 = (b) => { const intro = Math.min(4, Math.round(N * 0.05) || 4); return b >= intro && b < N - 4 && Math.floor((b - intro) / 8) % 4 === 3; };
  for (let b = 0; b < N; b++) {
    const ci = chordInfo(chords[Math.floor(b / d.barsPerChord) % chords.length]); const cells = barCells(b, N, bb);
    for (const c of cells) for (const step of cell(c)) {
      const off = step === "T" ? ci.third : step === "F" ? ci.fifth : step;
      if (off === null) { pick.push({ n: "R", d: 0.25 }); acc.push({ n: "R", d: 0.25 }); continue; }
      const midi = ci.root + off; pick.push({ n: fromMidi(midi), d: 0.25 });
      // アクセント（右）: オクターブ上の強拍だけ
      acc.push(off === 12 ? { n: fromMidi(midi), d: 0.25 } : { n: "R", d: 0.25 });
    }
    // 持続音: サビの小節に、コードの5度（1オクターブ上）を長く
    if (k3(b)) { const n = fromMidi(ci.root + ci.fifth + 12); if (bb === 4) sus.push({ n, d: 4 }); else { sus.push({ n, d: 4 }); sus.push({ n, d: bb - 4 }); } } else sus.push({ n: "R", d: bb });
  }
  const keepRole = /リード|メロディ|ハモリ|ソロ|主題/;
  const parts = [];
  for (const part of d.parts) {
    const g = ["guitar", "crunch", "distGuitar", "leadGuitar", "echoGuitar"].includes(part.instrument);
    if (g) { if ((part.instrument === "leadGuitar" || part.instrument === "echoGuitar") && keepRole.test(part.role)) parts.push({ ...part, role: `${part.role}（クリーン）`, amp: "clean" }); continue; }
    if (part.instrument === "bass") parts.push({ ...part, amp: "clean", role: `${part.role}（指弾き）` }); else parts.push(part);
  }
  parts.push({ instrument: "guitar", role: "連打刻み（クリーン）", volume: 0.19, pan: -0.3, amp: "clean", notes: fmt(merge(pick)) });
  parts.push({ instrument: "guitar", role: "アクセント（クリーン・右）", volume: 0.1, pan: 0.4, amp: "clean", notes: fmt(merge(acc)) });
  parts.push({ instrument: "echoGuitar", role: "持続音（クリーン・エコー）", volume: 0.08, pan: 0.2, amp: "clean", notes: fmt(merge(sus)) });
  const out = { ...d, title: `${d.title}（クリーン連打版）`, description: `「${d.title}」の旋律・ドラム・ベース・鍵盤・弦はそのまま、ギターの刻みを、クリーントーンの16分の連打に作り直した別バージョン（仮）。拍ごとに型を切りかえ（Aメロ風→展開→サビ風）、右に強拍のアクセント、サビには5度の長い音を重ねて、速い刻みを1音ずつ粒立てて聞かせる。`, parts };
  fs.writeFileSync(new URL(`../${id}-cleanpick.json`, import.meta.url), JSON.stringify(out, null, 1));
  console.log(id, "bars", N, "beats", bb, "parts", parts.length);
}
