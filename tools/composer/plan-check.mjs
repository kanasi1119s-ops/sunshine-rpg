// 曲の設計図（<曲>.plan.json）の雛形と検査（docs/sound/ai-composition-workflow.md の提案 1）。
//   node tools/composer/song.mjs plan-template            … 雛形を表示（属性カードとセクション表）
//   node tools/composer/song.mjs plan-check <plan.json> [曲.json]
// 設計図だけの検査: 未記入の項目・強さカーブに山があるか・各セクションの「前との違い」・音域表のすみ分け。
// 曲のJSONも渡すと: 小節の合計が曲の長さと合うか・パートが音域表を守っているか・計画にないパートが鳴っていないか・bpm／拍子／調が合うか。
import { DRUMS, RANGE, midi, expand, barChords, estimateKey, melodyParts } from "../audio-check/score-lib.mjs";
import { describeSong } from "./novelty.mjs";

export const PLAN_TEMPLATE = {
  card: {
    scene: "（例）雪原の夜のフィールド曲。静かな孤独から、遠くに灯りが見える希望へ",
    seconds: 150,
    tonic: "D",
    mode: "dorian",
    bpm: 92,
    beats: 4,
    recipe: "（chord-recipes.json の id か名前。直前の3曲と違うことを確認）",
    intro: 5,
    outro: "余韻を残して消える",
    ranges: { bass: ["E1", "G3"], piano: ["C3", "C5"], lead: ["C4", "G5"] },
    soundSet: "（song.mjs sounds の中から。なければ空）",
    bannedChecked: false,
  },
  motif: { notes: "E4:1 G4:0.5 A4:1.5", growth: ["高さをずらす", "リズムを変える", "後半を切る"] },
  sections: [
    { name: "導入", kind: "intro", bars: 4, parts: ["pad", "bell"], intensity: 2, change: "（最初）旋律なし、ドローンだけ" },
    { name: "Aメロ", kind: "verse", bars: 8, parts: ["pad", "bass", "lead"], intensity: 4, change: "旋律が入る、ドラムなし" },
    { name: "サビ", kind: "chorus", bars: 8, parts: ["pad", "bass", "lead", "kick", "snare"], intensity: 9, change: "動機を高く、長い音で" },
    { name: "終わり", kind: "outro", bars: 4, parts: ["pad"], intensity: 2, change: "全員止めて余韻" },
  ],
};

const INTRO_LABEL = { 1: "いきなり全員", 2: "1つの楽器だけ", 3: "サビを頭に", 4: "無音と一撃", 5: "ドローン", 6: "リズムの型だけ", 7: "途中から入る", 8: "静かに重ねる" };

const rangeOverlap = (a, b) => {
  const lo = Math.max(midi(a[0]), midi(b[0])), hi = Math.min(midi(a[1]), midi(b[1]));
  const span = Math.min(midi(a[1]) - midi(a[0]), midi(b[1]) - midi(b[0]));
  return span > 0 ? Math.max(0, hi - lo) / span : 0;
};

/** 設計図を検査する。song は（前処理ずみの）曲のJSON。戻り値: { errors, warnings, info } */
export function checkPlan(plan, song = null) {
  const errors = [], warnings = [], info = [];
  const card = plan?.card, secs = plan?.sections;
  if (!card || typeof card !== "object") errors.push("card（属性カード）がありません。plan-template を見てください。");
  if (!Array.isArray(secs) || !secs.length) errors.push("sections（セクション表）がありません。");
  if (errors.length) return { errors, warnings, info };

  // 属性カードの未記入
  const need = [["tonic", "調（主音）"], ["mode", "旋法"], ["bpm", "bpm"], ["beats", "拍子"], ["recipe", "進行レシピ"], ["intro", "入り方（1〜8）"], ["outro", "終わり方"], ["ranges", "音域のすみ分け"]];
  const blank = need.filter(([k]) => card[k] === undefined || card[k] === "" || (typeof card[k] === "string" && /^（.*）$/.test(card[k])));
  if (blank.length) warnings.push(`属性カードに未記入の項目があります: ${blank.map((x) => x[1]).join("・")}。書かない項目は「ありがちな値」になります。`);
  if (card.intro !== undefined && !INTRO_LABEL[Number(card.intro)]) warnings.push(`入り方は 1〜8 の番号で書いてください（${card.intro}）。`);
  if (card.bannedChecked !== true) warnings.push("banned-sounds.md の確認（card.bannedChecked: true）がまだです。");

  // セクション表
  let total = 0;
  secs.forEach((s, i) => {
    const where = `sections[${i}]（${s.name ?? "?"}）`;
    if (!(Number.isInteger(s.bars) && s.bars >= 1)) errors.push(`${where}: bars は1以上の整数にしてください`);
    else total += s.bars;
    if (!(s.intensity >= 1 && s.intensity <= 10)) errors.push(`${where}: intensity（強さ）は1〜10にしてください`);
    if (!Array.isArray(s.parts) || !s.parts.length) warnings.push(`${where}: 鳴るパート（parts）が空です。`);
    if (i > 0 && (!s.change || /^（.*）$/.test(s.change))) warnings.push(`${where}: 「前との違い（change）」が空です。前のセクションと何を変えるかを書いてください。`);
  });
  if (errors.length) return { errors, warnings, info };
  info.push(`セクション ${secs.length}個・合計 ${total}小節・強さ ${secs.map((s) => s.intensity).join("→")}`);

  // 強さカーブ
  const ints = secs.map((s) => s.intensity);
  const max = Math.max(...ints), min = Math.min(...ints);
  if (secs.length >= 3) {
    if (max - min < 4) warnings.push(`強さカーブが平らです（最大${max}・最小${min}）。差を4以上にすると起伏が出ます（例 2→4→6→9→3→10）。`);
    if (ints.indexOf(max) === 0 && Number(card.intro) !== 1 && Number(card.intro) !== 3) warnings.push("いちばん強いのが最初のセクションです。入り方を「いきなり全員（1）」にするのでなければ、小さく始めて山を後ろに置いてください。");
    if (max < 7) warnings.push(`山が低いです（最大${max}）。サビの強さを7以上にして対比をつけてください。`);
    let run = 1;
    for (let i = 1; i < ints.length; i++) { run = ints[i] === ints[i - 1] ? run + 1 : 1; if (run >= 3) { warnings.push(`強さが3つのセクションで同じです（sections[${i - 2}]〜[${i}]）。途中で引くか、足してください。`); break; } }
    if (ints[ints.length - 1] === max && ints.length > 3 && ints.lastIndexOf(max) === ints.length - 1 && ints.filter((x) => x === max).length === 1) info.push("最後のセクションが山です（最後のサビ型）。");
  }

  // 音域のすみ分け
  const rk = Object.entries(card.ranges ?? {}).filter(([, v]) => Array.isArray(v) && midi(v[0]) !== null && midi(v[1]) !== null);
  for (let a = 0; a < rk.length; a++) for (let b = a + 1; b < rk.length; b++) {
    const ov = rangeOverlap(rk[a][1], rk[b][1]);
    if (ov > 0.6) warnings.push(`音域表で「${rk[a][0]}」と「${rk[b][0]}」が${Math.round(ov * 100)}%重なっています。3度〜1オクターブずらしてください。`);
  }

  if (!song) return { errors, warnings, info };

  // 曲との照合
  const barList = barChords(song);
  const beats = Number(song.beats);
  if (total !== barList.length) errors.push(`セクションの小節の合計（${total}）が、曲の長さ（${barList.length}小節）と合いません。`);
  if (card.bpm !== undefined && Number(card.bpm) !== Number(song.bpm)) warnings.push(`bpm が計画（${card.bpm}）と曲（${song.bpm}）で違います。`);
  if (card.beats !== undefined && Number(card.beats) !== beats) warnings.push(`拍子が計画（${card.beats}）と曲（${beats}）で違います。`);
  const key = estimateKey(barList);
  if (key && card.tonic) {
    const m = /^([A-G])([#b]?)/.exec(String(card.tonic));
    if (m) {
      const pc = ({ C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 }[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12) % 12;
      if (pc !== key.tonic) warnings.push(`調が計画（${card.tonic}）と、コードからの推定（${key.label}）で違います。転調の曲なら問題ありません。`);
    }
  }
  const total_b = barList.length * beats;
  const d = describeSong(song, "", plan);
  if (card.intro !== undefined && !d.intro.declared && d.intro.id && d.intro.id !== Number(card.intro)) warnings.push(`入り方が計画（${card.intro}：${INTRO_LABEL[Number(card.intro)]}）と違って聞こえます（最初の小節の鳴り方からの推測は ${d.intro.id}：${d.intro.label}）。`);

  // パートが音域表を守っているか（楽器名か役割名がキーに一致するもの）
  song.parts.forEach((p, i) => {
    if (DRUMS.has(p.instrument)) return;
    const r = card.ranges?.[p.instrument] ?? card.ranges?.[p.role];
    if (!r || midi(r[0]) === null) return;
    const lo = midi(r[0]), hi = midi(r[1]);
    const seq = expand(p, total_b).filter((n) => n.pitch !== null);
    const out = seq.filter((n) => n.pitch < lo || n.pitch > hi);
    if (out.length) warnings.push(`parts[${i}]（${p.role ?? p.instrument}）が計画の音域（${r[0]}〜${r[1]}）の外に${out.length}音出ます（最初は${Math.floor(out[0].t / beats) + 1}小節目の ${out[0].name}）。`);
    const hw = RANGE[p.instrument];
    if (hw && (lo < midi(hw[0]) || hi > midi(hw[1]))) warnings.push(`計画の音域（${r[0]}〜${r[1]}）が ${p.instrument} の楽器の音域（${hw[0]}〜${hw[1]}）をはみ出しています。`);
  });

  // セクションごとに、計画のパートと実際に鳴るパートを比べる
  let from = 0;
  secs.forEach((s) => {
    const a = from * beats, b = (from + s.bars) * beats;
    from += s.bars;
    const planned = new Set((s.parts ?? []).map(String));
    const sounding = song.parts.filter((p) => expand(p, total_b).some((n) => n.t >= a - 1e-9 && n.t < b - 1e-9));
    const names = (p) => [p.instrument, p.role].filter(Boolean);
    const extra = sounding.filter((p) => !names(p).some((n) => planned.has(n)));
    if (planned.size && extra.length) warnings.push(`セクション「${s.name}」で、計画にないパートが鳴っています: ${extra.map((p) => p.role || p.instrument).join("・")}。`);
    const missing = [...planned].filter((n) => !sounding.some((p) => names(p).includes(n)));
    if (planned.size && missing.length && !song.autoAccompaniment) warnings.push(`セクション「${s.name}」で、計画にあるのに鳴らないパート: ${missing.join("・")}。`);
  });
  // 旋律の動機
  if (plan.motif?.notes && !melodyParts(song, (p) => expand(p, total_b)).length) warnings.push("動機を書いていますが、旋律のパート（役割に「メロディ」を含む）が見つかりません。");
  return { errors, warnings, info };
}

export function formatPlanCheck(r) {
  return [...r.info.map((x) => `  ・${x}`), ...r.errors.map((x) => `× ${x}`), ...r.warnings.map((x) => `△ ${x}`), r.errors.length || r.warnings.length ? "" : "○ 設計図の検査: 問題なし"].filter((x) => x !== "").join("\n");
}
