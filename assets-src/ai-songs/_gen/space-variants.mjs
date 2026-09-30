// 「クリーン→空間版」を、ボス系の速い曲から自動で作る（元の旋律・コード・ドラムはそのまま）。
//   前半: ギターをすべてクリーントーンにする（歪みの刻みも、歪ませずに鳴らす）
//   中盤(T1〜): ギターがエコーの空間系(shoegazeアンプのエコーギター)に移り、パッドと鐘が重なる
//   後半(T2〜): ドラムが薄れ（キックの鼓動だけ）、最後はベースとパッド・鐘・エコーだけが残る
// 実行: node assets-src/ai-songs/_gen/space-variants.mjs
import fs from "fs";
const IDS = "boss-touri boss-mugikano boss-garasuko boss-tetsu boss-sanone boss-kiri boss-shimo boss-ukishima boss-toushin elite poly-1 prog-1 boss-final secret-boss-2 eight-gods fate".split(" ");
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"], FLAT = { Db: "C#", Eb: "D#", Gb: "F#", Ab: "G#", Bb: "A#" };
const toMidi = (n) => { const m = /^([A-G][#b]?)(-?\d)$/.exec(n); if (!m) return null; const nm = FLAT[m[1]] ?? m[1]; return NAMES.indexOf(nm) + 12 * (+m[2] + 1); };
const fromMidi = (v) => NAMES[((v % 12) + 12) % 12] + (Math.floor(v / 12) - 1);
const parse = (s) => s.trim().split(/\s+/).filter(Boolean).map((t) => { const [n, d] = t.split(":"); return { n, d: +d }; });
// 作曲ソフトは1つの音・休みを長くしすぎると読めないので、休みは16拍ずつに分ける
const fmt = (a) => a.filter((t) => t.d > 1e-9).flatMap((t) => { if (t.n !== "R" || t.d <= 16) return [`${t.n}:${+t.d.toFixed(4)}`]; const o = []; let r = t.d; while (r > 1e-9) { const x = Math.min(16, r); o.push(`R:${+x.toFixed(4)}`); r -= x; } return o; }).join(" ");
/** [from, to) 拍の区間だけ音を残し、外は休みにする（区間をまたぐ音は切る）。 */
function window(tokens, from, to) {
  const out = []; let pos = 0;
  for (const t of tokens) { const a = pos, b = pos + t.d; pos = b; const lo = Math.max(a, from), hi = Math.min(b, to);
    const before = Math.max(0, Math.min(b, from) - a), inside = Math.max(0, hi - lo), after = Math.max(0, b - Math.max(a, to));
    if (before > 0) out.push({ n: "R", d: before }); if (inside > 0) out.push({ n: t.n, d: inside }); if (after > 0) out.push({ n: "R", d: after }); }
  // 隣り合う休みをまとめる
  const m = []; for (const t of out) { const l = m[m.length - 1]; if (l && l.n === "R" && t.n === "R") l.d += t.d; else m.push({ ...t }); } return m;
}
const total = (tokens) => tokens.reduce((s, t) => s + t.d, 0);
/** 音を、指定の範囲(midi)に入るまで1オクターブずつ動かす。 */
function fit(tokens, lo, hi) { return tokens.map((t) => { const v = toMidi(t.n); if (v === null) return t; let x = v; while (x < lo) x += 12; while (x > hi) x -= 12; return { ...t, n: fromMidi(x) }; }); }
function chordFifth(c) { const m = /^([A-G][#b]?)(.*)$/.exec(c); if (!m) return null; const r = NAMES.indexOf(FLAT[m[1]] ?? m[1]); const q = m[2]; const up = /dim/.test(q) ? 6 : /aug/.test(q) ? 8 : 7; return { root: r, fifth: (r + up) % 12, third: (r + (/^m(?!aj)/.test(q) || /dim/.test(q) ? 3 : 4)) % 12 }; }
const note = (pc, oct) => NAMES[pc] + oct;

for (const id of IDS) {
  const p = new URL(`../${id}.json`, import.meta.url); if (!fs.existsSync(p)) { console.log("なし", id); continue; }
  const d = JSON.parse(fs.readFileSync(p, "utf8"));
  const chords = d.chords.split(/\s+/).filter(Boolean), bars = chords.length * d.barsPerChord * d.repeats, bb = d.beats;
  const T1 = Math.round((bars * 0.42) / 4) * 4 * bb, T2 = Math.round((bars * 0.62) / 4) * 4 * bb, T3 = Math.round((bars * 0.88) / 4) * 4 * bb, END = bars * bb;
  const parts = [];
  for (const part of d.parts) {
    const tk = parse(part.notes); const inst = part.instrument; const len = total(tk);
    // 曲の長さに満たないときは、くり返して埋める（元のソフトの規則と同じ）
    const full = []; let acc = 0; while (acc < END - 1e-6) { for (const t of tk) { if (acc >= END - 1e-6) break; const d2 = Math.min(t.d, END - acc); full.push({ ...t, d: d2 }); acc += d2; } if (len === 0) break; }
    const isGuitar = ["guitar", "crunch", "distGuitar", "leadGuitar", "echoGuitar"].includes(inst);
    if (isGuitar) {
      // 前半: クリーン
      const cleanInst = inst === "distGuitar" || inst === "crunch" ? "guitar" : inst;
      parts.push({ ...part, instrument: cleanInst, role: `${part.role}（クリーン）`, amp: "clean", notes: fmt(window(full, 0, T1)) });
      // 中盤から: 空間系（エコーギター。音域 E3〜E6 に収める）
      const dense = inst === "distGuitar" || inst === "crunch"; const from = dense ? T1 : T1; const to = dense ? T3 : END;
      const sp = fit(window(full, from, to), toMidi("E3"), toMidi("E6"));
      parts.push({ ...part, instrument: "echoGuitar", role: `${part.role}（空間）`, amp: "shoegaze", volume: Math.min(0.26, (part.volume ?? 0.2) * (dense ? 0.7 : 1)), notes: fmt(sp) });
    } else if (["hihat", "snare", "crash", "tom"].includes(inst)) {
      parts.push({ ...part, notes: fmt(window(full, 0, T2)) });                   // T2でドラムが薄れる
    } else if (inst === "kick") {
      parts.push({ ...part, notes: fmt(window(full, 0, T2)) });
      const heart = []; for (let b = T2; b < T3; b += bb) heart.push({ n: "x", d: 0.25 }, { n: "R", d: bb - 0.25 });  // 鼓動（1小節に1つ）
      parts.push({ instrument: "kick", role: "キック（鼓動）", volume: (part.volume ?? 0.28) * 0.75, pan: 0, amp: "auto", notes: fmt([{ n: "R", d: T2 }, ...heart, { n: "R", d: END - T3 }]) });
    } else {
      parts.push({ ...part, notes: fmt(full) });                                  // ベース・鍵盤・弦などは、そのまま
    }
  }
  // 空間の層: パッド（コードの3度の長い音）と鐘（コードの5度、1小節に1つ）を T1 から重ねる
  const pad = [], bell = []; const perChord = d.barsPerChord * bb; let c = 0;
  for (let rep = 0; rep < d.repeats; rep++) for (const ch of chords) { const f = chordFifth(ch); const start = c * perChord; c++; if (!f || start < T1) { pad.push({ n: "R", d: perChord }); bell.push({ n: "R", d: perChord }); continue; }
    pad.push({ n: note(f.third, 4), d: perChord }); bell.push({ n: note(f.fifth, 6), d: Math.min(2, perChord) }, ...(perChord > 2 ? [{ n: "R", d: perChord - 2 }] : [])); }
  parts.push({ instrument: "pad", role: "パッド（空間）", volume: 0.16, pan: 0, amp: "auto", notes: fmt(pad) });
  parts.push({ instrument: "bell", role: "鐘（遠い光）", volume: 0.12, pan: -0.3, amp: "auto", notes: fmt(bell) });
  const out = { ...d, title: `${d.title}（クリーン→空間版）`, description: `「${d.title}」と同じ旋律・コード・ドラムを使い、ギターを前半はクリーントーンで鳴らし、中盤からエコーの空間系（エコーギター・パッド・鐘）へ溶けていく版（仮）。ドラムは終盤で薄れ、鼓動のようなキックだけになる。`, parts };
  fs.writeFileSync(new URL(`../${id}-space.json`, import.meta.url), JSON.stringify(out, null, 1));
  console.log(id, "bars", bars, "T1/T2/T3", T1 / bb, T2 / bb, T3 / bb, "parts", parts.length);
}
