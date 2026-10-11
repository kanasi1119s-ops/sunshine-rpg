// コード進行の「似たり寄ったり」を見つける小さな道具。曲を書き出すとき（song-lib.mjs の build）に警告を出す。
// 見るのは「前のコードからの根音の動き＋長短」の並びだけ（2026-10-11 改良: 調が違っても、回して書いても同じと判定できる）。
// メロディやコードの中身は保存しない・外に出さない。
import fs from "fs";
import path from "path";
import { loadRecipes, realize } from "./chord-recipes.mjs";

const PC = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

/** "F#m7" → { root, minor, plain, bass, quality } 。"Am*2"（小節数つき）・分数コード（G/B）・m7b5・mmaj7 も読む。読めなければ null */
export function parseChord(tok) {
  const m = /^([A-G])([#b♯♭]?)([^/*]*)(?:\/([A-G])([#b♯♭]?))?(?:\*\d+)?$/.exec(tok);
  if (!m) return null;
  const acc = (a) => (a === "#" || a === "♯" ? 1 : a === "b" || a === "♭" ? -1 : 0);
  const root = (PC[m[1]] + acc(m[2]) + 12) % 12;
  const bass = m[4] ? (PC[m[4]] + acc(m[5]) + 12) % 12 : null;
  const q = m[3];
  const minor = /^m(?!aj)/.test(q) || /^dim/.test(q);
  const plain = (q === "" || q === "m") && (bass === null || bass === root);
  return { root, minor, plain, bass, quality: q };
}

/** 連続する同じコードをまとめ、全体が同じ並びのくり返しなら最小の1周にする。 */
function cycle(cs) {
  const merged = [];
  for (const c of cs) {
    const last = merged[merged.length - 1];
    if (!last || last.root !== c.root || last.minor !== c.minor) merged.push(c);
  }
  if (merged.length > 1 && merged[0].root === merged[merged.length - 1].root && merged[0].minor === merged[merged.length - 1].minor) merged.pop(); // 輪の継ぎ目の重複
  const n = merged.length;
  for (let p = 1; p <= n / 2; p++) {
    if (n % p === 0 && merged.every((c, i) => c.root === merged[i % p].root && c.minor === merged[i % p].minor)) return merged.slice(0, p);
  }
  return merged;
}

/**
 * 進行の「形」。各コードを「前のコードからの根音の移動（半音）＋長短」で表した、輪（ループ）の並び。
 * 移調しても、回して（vi–IV–I–V と I–V–vi–IV）書いても、同じ形になる。
 */
export function signature(chordsText) {
  const cs = String(chordsText ?? "").split(/[\s|]+/).map(parseChord).filter(Boolean);
  if (!cs.length) return { seq: [], plainOnly: true, distinct: 0, chords: [] };
  const cyc = cycle(cs);
  const seq = cyc.map((c, i) => `${(c.root - cyc[(i - 1 + cyc.length) % cyc.length].root + 12) % 12}${c.minor ? "m" : ""}`);
  return { seq, plainOnly: cs.every((c) => c.plain), distinct: new Set(cyc.map((c) => `${c.root}${c.minor}`)).size, chords: cyc };
}

/** 輪の n 個組（n=4）の集合。輪なので、どこから数えても同じ。 */
function grams(seq, n) {
  const g = new Set();
  const L = seq.length;
  if (!L) return g;
  for (let i = 0; i < L; i++) {
    const w = [];
    for (let k = 0; k < n; k++) w.push(seq[(i + k) % L]);
    g.add(w.join(" "));
  }
  return g;
}

/** 似ている度合い（0〜1）。輪の4コード（短ければその長さ）の並びが、どれだけ共通か。 */
export function similarity(a, b) {
  const n = Math.min(4, a.length, b.length);
  if (n < 1) return 0;
  const ga = grams(a, n), gb = grams(b, n);
  let both = 0;
  for (const x of ga) if (gb.has(x)) both++;
  return both / Math.min(ga.size, gb.size);
}

let recipeCache;
function recipeSigs() {
  if (!recipeCache) {
    try {
      recipeCache = loadRecipes().recipes.map((r) => ({ ...r, sig: signature(realize(r.roman, 0, { minor: r.mode === "minor" }).join(" ")) }));
    } catch { recipeCache = []; }
  }
  return recipeCache;
}

/** 進行が既知の型（chord-recipes.json）の形を含んでいれば、その型を返す（なければ null）。 */
export function recipeOf(chordsText) {
  const me = signature(chordsText);
  if (!me.seq.length) return null;
  let best = null;
  for (const r of recipeSigs()) {
    const n = Math.min(4, r.sig.seq.length);
    if (r.sig.seq.length < 2 || me.seq.length > r.sig.seq.length * 2) continue;
    const gr = grams(r.sig.seq, n), gm = grams(me.seq, n);
    let hit = 0;
    for (const x of gr) if (gm.has(x)) hit++;
    const score = hit / gr.size;
    if (score >= 0.99 && (!best || r.sig.seq.length > best.sig.seq.length)) best = r;
  }
  return best;
}

/** 警告の文章を返す。others は [{ name, chords }]。 */
export function checkChordVariety(chordsText, others = []) {
  const w = [];
  const me = signature(chordsText);
  if (!me.seq.length) return w;
  if (me.plainOnly) w.push("コード進行が「基本の和音（長3和音・短3和音）」だけです。7th・sus・add9・分数コード・借用和音を1〜2か所入れると響きが変わります（docs/sound/chord-variety-guide.md）。");
  if (me.distinct <= 4) w.push(`コード進行が${me.distinct}種類だけの繰り返しです。曲の後半で転調する・Bメロで別の進行にする・終わりを変えると単調になりません（docs/sound/chord-variety-guide.md）。`);
  const mine = recipeOf(chordsText);
  if (mine?.overused) w.push(`コード進行が「${mine.name}」の形です（使いすぎ注意の型）。別の型に替えるか、借用和音・転調・分数コードで崩してください（docs/sound/chord-variety-guide.md）。`);
  for (const o of others) {
    const s = similarity(me.seq, signature(o.chords).seq);
    if (s >= 0.7) w.push(`コード進行が「${o.name}」とほぼ同じ形です（根音の動きの並びが${Math.round(s * 100)}%一致。調や回し方が違っても同じと数えます）。別のレシピに替えてみてください（docs/sound/chord-variety-guide.md）。`);
    else if (mine && recipeOf(o.chords)?.id === mine.id) w.push(`コード進行が「${o.name}」と同じ型「${mine.name}」です。別の型にしてください（docs/sound/data/chord-recipes.json）。`);
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
