// コード進行の「似たり寄ったり」を見つける小さな道具。曲を書き出すとき（song-lib.mjs の build）に警告を出す。
// 見るのは「主音からの度数の並び」だけ。メロディやコードの中身は保存しない・外に出さない。
import fs from "fs";
import path from "path";

const PC = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

/** "F#m7" → { root: 6, minor: false/true, plain: true/false } 。読めなければ null */
export function parseChord(tok) {
  const m = /^([A-G])([#b♯♭]?)([^/]*)(?:\/.*)?$/.exec(tok);
  if (!m) return null;
  let root = PC[m[1]] + (m[2] === "#" || m[2] === "♯" ? 1 : m[2] === "b" || m[2] === "♭" ? -1 : 0);
  root = (root + 12) % 12;
  const q = m[3];
  const minor = /^m(?!aj)/.test(q) || /^dim/.test(q);
  const plain = q === "" || q === "m";
  return { root, minor, plain };
}

/** 進行を「主音からの度数＋長短」の並びにして、連続する同じコードをまとめる。主音は最初のコード。 */
export function signature(chordsText) {
  const cs = String(chordsText ?? "").split(/\s+/).map(parseChord).filter(Boolean);
  if (!cs.length) return { seq: [], plainOnly: true, distinct: 0 };
  const tonic = cs[0].root;
  const seq = [];
  for (const c of cs) {
    const s = `${(c.root - tonic + 12) % 12}${c.minor ? "m" : ""}`;
    if (seq[seq.length - 1] !== s) seq.push(s);
  }
  return { seq, plainOnly: cs.every((c) => c.plain), distinct: new Set(seq).size };
}

function grams(seq, n = 4) {
  const g = new Set();
  for (let i = 0; i + n <= seq.length; i++) g.add(seq.slice(i, i + n).join(" "));
  return g;
}

/** 似ている度合い（0〜1）。4コードの並びが、どれだけ共通か。 */
export function similarity(a, b) {
  const ga = grams(a), gb = grams(b);
  if (!ga.size || !gb.size) return 0;
  let both = 0;
  for (const x of ga) if (gb.has(x)) both++;
  return both / Math.min(ga.size, gb.size);
}

/** 警告の文章を返す。others は [{ name, chords }]。 */
export function checkChordVariety(chordsText, others = []) {
  const w = [];
  const me = signature(chordsText);
  if (!me.seq.length) return w;
  if (me.plainOnly) w.push("コード進行が「基本の和音（長3和音・短3和音）」だけです。7th・sus・add9・分数コード・借用和音を1〜2か所入れると響きが変わります（docs/sound/chord-variety-guide.md）。");
  if (me.distinct <= 4) w.push(`コード進行が${me.distinct}種類だけの繰り返しです。曲の後半で転調する・Bメロで別の進行にする・終わりを変えると単調になりません（docs/sound/chord-variety-guide.md）。`);
  for (const o of others) {
    const s = similarity(me.seq, signature(o.chords).seq);
    if (s >= 0.7) w.push(`コード進行が「${o.name}」とほぼ同じ形です（度数の並びが${Math.round(s * 100)}%一致）。別のレシピに替えてみてください（docs/sound/chord-variety-guide.md）。`);
  }
  return w;
}

/** assets-src/ai-songs の他の曲の進行を読む。自分自身（同じ曲名）は除く。 */
export function loadOtherSongs(dir, selfName) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const f of fs.readdirSync(dir)) {
    if (!f.endsWith(".json")) continue;
    const name = f.replace(/\.json$/, "");
    if (name === selfName) continue;
    try {
      const d = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));
      if (typeof d.chords === "string") out.push({ name, chords: d.chords });
    } catch { /* 読めない曲は飛ばす */ }
  }
  return out;
}
