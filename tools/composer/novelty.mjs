// 新しい曲が、直前の曲と「同じ選択」をしていないかを調べる（docs/sound/ai-composition-workflow.md の提案 2・10）。
//   node tools/composer/song.mjs novelty <曲.json> [--n 3] [--vs 曲名,曲名]
// 見るもの: 調（主音と長短）・テンポ・進行の形（回して書いても同じ）・入り方（1〜8）・終わり方・主役の楽器・旋律の輪郭（Parsons code。曲どうしの差の点数）。
// 入り方・終わり方は description か plan.json に「入り方: 5」「終わり方: 余韻を残して消える」のように書くと、そのとおりに数える。書いてなければ、最初の小節の鳴り方から推測する。
import fs from "fs";
import path from "path";
import { signature, similarity, recipeOf } from "./chord-variety.mjs";
import { checkIntervalSimilarity } from "./interval-sim.mjs";
import { DRUMS, expand, barChords, estimateKey, melodyParts } from "../audio-check/score-lib.mjs";

export const INTRO_LABEL = {
  1: "いきなり全員", 2: "1つの楽器だけ", 3: "サビを頭に", 4: "無音と一撃", 5: "ドローン", 6: "リズムの型だけ", 7: "途中から入る", 8: "静かに重ねる",
};

const totalBeatsOf = (song) => barChords(song).length * Number(song.beats);

/** 入り方の分類。{ id(1〜8 か 0＝その他), label, declared } */
export function introOf(song, plan) {
  const decl = plan?.card?.intro ?? /入り方[:：\s]*([1-8])/.exec(song.description ?? "")?.[1];
  if (decl !== undefined && INTRO_LABEL[Number(decl)]) return { id: Number(decl), label: INTRO_LABEL[Number(decl)], declared: true };
  const beats = Number(song.beats) || 4;
  const total = totalBeatsOf(song);
  if (!total) return { id: 0, label: "不明", declared: false };
  const parts = song.parts.map((p) => ({ p, seq: expand(p, total) })).filter((x) => x.seq.length);
  if (!parts.length) return { id: 0, label: "不明", declared: false };
  const first = (x, from, to) => x.seq.filter((n) => n.t >= from && n.t < to);
  const act1 = parts.filter((x) => first(x, 0, beats).length);
  const act2 = parts.filter((x) => first(x, 0, beats * 2).length);
  const n = parts.length;
  if (!act1.length && act2.length / n >= 0.6) return { id: 4, label: INTRO_LABEL[4], declared: false };
  if (act1.length / n >= 0.8 && n >= 3) return { id: 1, label: INTRO_LABEL[1], declared: false };
  if (act2.length && act2.every((x) => DRUMS.has(x.p.instrument))) return { id: 6, label: INTRO_LABEL[6], declared: false };
  if (act2.length === 1) {
    const x = act2[0];
    const mean = first(x, 0, beats * 2).reduce((s, q) => s + q.dur, 0) / first(x, 0, beats * 2).length;
    return mean >= beats * 0.75 ? { id: 5, label: INTRO_LABEL[5], declared: false } : { id: 2, label: INTRO_LABEL[2], declared: false };
  }
  if (act2.length / n <= 0.45) return { id: 8, label: INTRO_LABEL[8], declared: false };
  return { id: 0, label: "その他", declared: false };
}

export function outroOf(song, plan) {
  return plan?.card?.outro ?? /終わり方[:：]\s*([^。\n;；]+)/.exec(song.description ?? "")?.[1]?.trim() ?? null;
}

/** 旋律の輪郭（Parsons code。*URDの並び） */
export function contourOf(song) {
  const total = totalBeatsOf(song);
  const mel = melodyParts(song, (p) => expand(p, total))[0];
  if (!mel) return "";
  let code = "";
  for (let i = 1; i < mel.seq.length; i++) code += mel.seq[i].pitch > mel.seq[i - 1].pitch ? "U" : mel.seq[i].pitch < mel.seq[i - 1].pitch ? "D" : "R";
  return code;
}
/** 輪郭の似ている度合い（0〜1）。8音ぶんの並びがどれだけ共通か（R のみの並びは数えない）。 */
export function contourSimilarity(a, b, n = 8) {
  const g = (s) => { const out = new Set(); for (let i = 0; i + n <= s.length; i++) { const w = s.slice(i, i + n); if (/[UD]/.test(w) && new Set(w).size > 1) out.add(w); } return out; };
  const ga = g(a), gb = g(b);
  if (!ga.size || !gb.size) return 0;
  let both = 0;
  for (const x of ga) if (gb.has(x)) both++;
  return both / Math.min(ga.size, gb.size);
}

/** 曲の「選択」の要約 */
export function describeSong(song, name = "", plan) {
  const bars = barChords(song);
  const key = estimateKey(bars);
  const mel = melodyParts(song, (p) => expand(p, totalBeatsOf(song)))[0];
  return {
    name,
    key,
    bpm: Number(song.bpm),
    sig: signature(song.chords),
    recipe: recipeOf(bars.join(" ")),
    intro: introOf(song, plan),
    outro: outroOf(song, plan),
    lead: mel?.instrument ?? null,
    contour: contourOf(song),
  };
}

/** 2曲の選択を比べて、同じものを返す。[{ kind, text }] */
export function compareChoices(me, other) {
  const out = [];
  if (me.key && other.key && me.key.tonic === other.key.tonic && me.key.minor === other.key.minor) out.push({ kind: "調", text: `調が同じ（${me.key.label}）` });
  if (Number.isFinite(me.bpm) && Math.abs(me.bpm - other.bpm) <= 4) out.push({ kind: "テンポ", text: `テンポがほぼ同じ（${me.bpm}と${other.bpm}）` });
  const s = similarity(me.sig.seq, other.sig.seq);
  if (s >= 0.7) out.push({ kind: "進行", text: `進行の形が${Math.round(s * 100)}%一致` });
  else if (me.recipe && other.recipe && me.recipe.id === other.recipe.id) out.push({ kind: "進行", text: `進行の型が同じ（${me.recipe.name}）` });
  if (me.intro.id && me.intro.id === other.intro.id) out.push({ kind: "入り方", text: `入り方が同じ（${me.intro.id}：${me.intro.label}${me.intro.declared && other.intro.declared ? "" : "。推測を含む"}）` });
  if (me.outro && other.outro && me.outro === other.outro) out.push({ kind: "終わり方", text: `終わり方が同じ（${me.outro}）` });
  if (me.lead && me.lead === other.lead) out.push({ kind: "主役の楽器", text: `旋律の楽器が同じ（${me.lead}）` });
  return out;
}

/** assets-src/ai-songs の中の、更新が新しい順の曲（JSON全体つき）。selfName は除く。 */
export function loadRecentFull(dir, n, selfName, names) {
  if (!fs.existsSync(dir)) return [];
  const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json")).map((f) => ({ name: f.replace(/\.json$/, ""), t: fs.statSync(path.join(dir, f)).mtimeMs })).filter((f) => f.name !== selfName);
  const pick = names?.length ? files.filter((f) => names.includes(f.name)) : files.sort((a, b) => b.t - a.t).slice(0, n);
  const out = [];
  for (const f of pick) {
    try {
      const song = JSON.parse(fs.readFileSync(path.join(dir, `${f.name}.json`), "utf8"));
      if (typeof song.chords === "string" && Array.isArray(song.parts)) out.push({ name: f.name, song });
    } catch { /* 読めない曲は飛ばす */ }
  }
  return out;
}

/** 検査。戻り値: { lines(表示用の文), warnings(注意の文), rows([{name, same:[{kind,text}], contour, progression, score}]) } */
export function checkNovelty(song, name, others, plan) {
  const me = describeSong(song, name, plan);
  const rows = others.map((o) => {
    const d = describeSong(o.song, o.name);
    const same = compareChoices(me, d);
    const contour = contourSimilarity(me.contour, d.contour);
    const prog = similarity(me.sig.seq, d.sig.seq);
    return { name: o.name, same, contour, progression: prog, score: Math.round((1 - Math.max(contour, prog)) * 100) };
  });
  const warnings = [];
  rows.forEach((r, i) => {
    if (r.same.length >= 2 || r.same.some((x) => ["進行", "入り方", "終わり方"].includes(x.kind))) {
      warnings.push(`${i === 0 ? "直前の曲" : "最近の曲"}「${r.name}」と同じ選択があります: ${r.same.map((x) => x.text).join("、")}。曲の個性が薄くなるので、調・入り方・進行の型のどれかを変えてください（docs/sound/ai-composition-workflow.md）。`);
    }
    if (r.contour >= 0.35) warnings.push(`旋律の輪郭が「${r.name}」と${Math.round(r.contour * 100)}%重なっています（8音の上下の並び）。旋律を使い回していないか確かめてください。`);
  });
  warnings.push(...checkIntervalSimilarity(song, others).warnings); // 音程列の細かい類似（melody-craft-guide P10）
  const keyCount = rows.filter((r) => r.same.some((x) => x.kind === "調")).length;
  if (rows.length >= 3 && keyCount === rows.length) warnings.push(`直近${rows.length}曲すべてと同じ調（${me.key?.label}）です。主音を変えてください。`);
  const lines = [
    `■ ${name || song.title}: 調 ${me.key?.label ?? "不明"}・bpm ${me.bpm}・進行の型 ${me.recipe?.name ?? "（既知の型なし）"}・入り方 ${me.intro.id ? `${me.intro.id}：${me.intro.label}${me.intro.declared ? "" : "（推測）"}` : me.intro.label}・終わり方 ${me.outro ?? "（未記入）"}・旋律の楽器 ${me.lead ?? "不明"}`,
    ...rows.map((r) => `  vs ${r.name}: 差の点数 ${r.score}（100に近いほど違う。旋律の輪郭の重なり ${Math.round(r.contour * 100)}%・進行の一致 ${Math.round(r.progression * 100)}%）　${r.same.length ? "同じ: " + r.same.map((x) => x.kind).join("・") : "同じ選択なし"}`),
  ];
  return { lines, warnings, rows, me };
}

